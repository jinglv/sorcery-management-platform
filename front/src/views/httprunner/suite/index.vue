<template>
  <div class="httprunner-suite">
    <div class="filter-container">
      <el-row :gutter="24">
        <el-col :span="6">
          <div class="demo-input-suffix">
            用例集名称:
            <el-input v-model="suiteForm.name" placeholder="请输入用例集名称" style="width: 54%;margin-right: 5px;" class="filter-item" />
          </div>
        </el-col>
        <el-col :span="7">
          <div class="demo-input-suffix">
            HttpRunner项目名称:
            <el-select
              v-model="projectValue"
              placeholder="请选择HttpRunner项目名称"
              style="width: 58%;"
              @change="changeProject"
            >
              <el-option
                v-for="item in projectOption"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>
        </el-col>
      </el-row>
      <div style="text-align: right;margin-top: 10px;">
        <el-button class="filter-item" icon="el-icon-delete" @click="clearSearch()">重置</el-button>
        <el-button class="filter-item" type="primary" icon="el-icon-search" @click="initHttpRunnerSuiteList()">搜索</el-button>
      </div>
    </div>
    <div style="text-align: left; width: 100%; margin-top: 10px;">
      <el-button type="primary" icon="el-icon-circle-plus-outline" @click="showDialog()">创建HttpRunner测试用例集</el-button>
      <el-button type="warning" icon="el-icon-bicycle" @click="showBatchRunDialog()">批量执行测试用例集</el-button>
      <el-button type="success" icon="el-icon-view" @click="showResultDialog()">查看批量执行结果</el-button>
    </div>
    <div style="margin-top: 10px;">
      <el-table ref="multipleTable" :data="httpRunnerProjectSuiteData" border style="width: 100%" @selection-change="handleSelectionChange">
        <el-table-column
          type="selection"
          width="55"
        />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="测试用例集名称" />
        <el-table-column prop="httprunner_project_name" label="HttpRunner项目名称" />
        <el-table-column prop="status" label="执行结果">
          <template slot-scope="{ row }">
            <el-tag :type="statusType(row.status)" effect="dark">
              {{ row.status | resultStatus }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" />
        <el-table-column fixed="right" label="操作">
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="runSuite(scope.row)"
            >执行</el-button>
            <el-button
              type="text"
              @click="viewSuiteReport(scope.row)"
            >查看报告</el-button>
            <el-button
              type="text"
              @click="showRowTestCaseInfo(scope.row)"
            >详情</el-button>
            <el-button
              type="text"
              @click="updateRowSuiteInfo(scope.row)"
            >编辑</el-button>
            <el-button
              type="text"
              @click="deleteRowSuiteInfo(scope.row)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <!--分页-->
    <div class="pagination-container">
      <el-pagination
        background
        layout="total, prev, pager, next"
        :page-size="req.size"
        :total="total"
        @current-change="handleCurrentChange"
      />
    </div>
    <el-drawer
      :title="suiteTitle"
      :visible.sync="drawer"
      direction="rtl"
      size="60%"
    >
      <http-runner-suite-dialog v-if="drawer" :title="suiteTitle" :sid="currentSuiteId" @cancel="closeDrawer()" @refresh="refreshApiList()" />
    </el-drawer>
    <!--引入子组件-->
    <http-runner-run-suite-dialog v-if="dialogRunFlag" :ids="suiteIds" @cancel="closeDialog" />
    <http-runner-run-result-dialog v-if="dialogResultFlag" :type="type" @cancel="closeDialog" />
    <http-runner-show-test-case-detail-dialog v-if="dialogViewApiFlag" :id="currentTestCaseId" @cancel="closeDialog" />
  </div>
</template>

<script>
import { httpRunnerProjectList, getHttpRunnerSuiteList, httpRunnerRenderReportApi, deleteHttpRunnerSuite } from '@/api/httprunner'
import httpRunnerRunResultDialog from '@/components/HttpRunner/httpRunnerRunResultDialog'
import httpRunnerShowTestCaseDetailDialog from '@/components/HttpRunner/httpRunnerShowTestCaseDetailDialog'
import httpRunnerSuiteDialog from '@/components/HttpRunner/httpRunnerSuiteDialog'
import httpRunnerRunSuiteDialog from '@/components/HttpRunner/httpRunnerRunSuiteDialog'

export default {
  name: 'HttpRunnerApi',
  components: {
    httpRunnerRunResultDialog,
    httpRunnerShowTestCaseDetailDialog,
    httpRunnerSuiteDialog,
    httpRunnerRunSuiteDialog
  },
  filters: {
    resultStatus(value) {
      if (value === 'fail') {
        return '测试失败'
      } else if (value === 'success') {
        return '测试通过'
      } else if (value === 'non') {
        return '未执行'
      } else if (value === 'error') {
        return '执行错误'
      } else {
        return '未知状态'
      }
    }
  },
  data() {
    return {
      dialogFlag: false,
      dialogRunFlag: false,
      dialogResultFlag: false,
      dialogViewApiFlag: false,
      dialogUpdateApiFlag: false,
      type: 'TESTSUITE',
      suiteForm: {
        name: '',
        httprunner_project_id: ''
      },
      projectValue: '',
      projectLabel: '',
      projectOption: [],
      req: {
        page: 1,
        size: 6
      },
      // 分页页数
      total: 10,
      httpRunnerProjectSuiteData: [],
      suiteIds: [],
      currentSuiteId: 0,
      drawer: false,
      suiteTitle: ''
    }
  },
  mounted() {
    // 组件加载的时候 进行调用
    this.initHttpRunnerProjectList()
    this.initHttpRunnerSuiteList()
  },
  methods: {
    statusType(value) {
      if (value === 'fail') {
        return 'danger'
      } else if (value === 'non') {
        return 'info'
      } else if (value === 'error') {
        return 'warning'
      } else if (value === 'success') {
        return 'success'
      } else {
        return '未知状态'
      }
    },
    async initHttpRunnerProjectList() {
      const resp = await httpRunnerProjectList(this.req)
      if (resp.success === true) {
        for (let i = 0; i < resp.items.length; i++) {
          this.projectOption.push({
            value: resp.items[i].id,
            label: resp.items[i].name
          })
        }
        this.total = resp.total
        // this.$message.success('查询成功！')
      } else {
        this.$message.error('查询失败！')
      }
    },
    changeProject(value) {
      this.projectValue = value
      this.projectLabel = this.projectOption.find(
        (item) => item.value === value
      ).label
      this.suiteForm.httprunner_project_id = value
      console.info('project value:', this.projectValue)
    },
    async initHttpRunnerSuiteList() {
      this.suiteForm.httprunner_project_id = this.projectValue === '' ? 0 : this.projectValue
      const resp = await getHttpRunnerSuiteList(this.req, this.suiteForm)
      if (resp.success === true) {
        this.total = resp.total
        for (let i = 0; i < resp.items.length; i++) {
          resp.items[i].create_time = this.$moment(
            resp.items[i].create_time
          ).format('YYYY-MM-DD HH:mm:ss')
        }
        this.httpRunnerProjectSuiteData = resp.items
        this.$message.success('查询成功！')
        // this.$message.success("查询成功！")
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 清除搜索
    clearSearch() {
      this.suiteForm.name = ''
      this.projectValue = 0
      if (this.projectValue === 0) {
        this.projectValue = ''
      }
      this.initHttpRunnerSuiteList()
    },
    // 展示子组件
    showDialog() {
      this.drawer = true
      this.suiteTitle = '创建测试用例集'
    },
    runSuite(row) {
      this.suiteIds = []
      this.suiteIds.push(row.id)
      console.info('suite ids:', this.suiteIds)
      this.dialogRunFlag = true
    },
    async viewSuiteReport(row) {
      console.info('name:', row.report_name)
      const reportContent = await httpRunnerRenderReportApi(row.report_name)
      // 保存进localStorage
      window.localStorage.removeItem('callbackHTML')
      window.localStorage.setItem('callbackHTML', reportContent)
      // 读取本地保存的html数据，使用新窗口打开
      const newWin = window.open('_', '_blank')
      newWin.document.write(localStorage.getItem('callbackHTML'))
      // 关闭输出流
      newWin.document.close()
    },
    showBatchRunDialog() {
      console.info('batch caseIds:', this.casesIds)
      this.dialogRunFlag = true
    },
    showResultDialog() {
      this.dialogResultFlag = true
    },
    showRowCaseTestInfo(row) {
      this.currentSuiteId = row.id
      this.dialogViewApiFlag = true
    },
    updateRowSuiteInfo(row) {
      this.suiteTitle = '编辑测试用例集'
      this.currentSuiteId = row.id
      this.drawer = true
    },
    async deleteRowSuiteInfo(row) {
      await deleteHttpRunnerSuite(row.id).then((resp) => {
        this.$confirm('删除测试用例集, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          center: true
        }).then(() => {
          if (resp.success === true) {
            this.initHttpRunnerSuiteList()
          } else {
            this.$message.error(resp.error.msg)
          }
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
      })
    },
    // 关闭子组件，子组件的closeDialog回调父组件
    closeDialog() {
      this.dialogFlag = false
      this.dialogRunFlag = false
      this.dialogResultFlag = false
      this.dialogViewApiFlag = false
      this.dialogUpdateApiFlag = false
      this.initHttpRunnerSuiteList()
    },
    // 传递子组件，关闭抽屉
    closeDrawer() {
      this.drawer = false
      this.initHttpRunnerSuiteList()
    },
    // 跳转到第几页
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`)
      this.req.page = val
      this.initHttpRunnerSuiteList()
    },
    handleSelectionChange(val) {
      this.selectiveTestCase(val)
    },
    selectiveTestCase(multipleSelection) {
      // 获取选中的API id
      const casesList = []
      for (let i = 0; i < multipleSelection.length; i++) {
        casesList.push(multipleSelection[i].id)
      }
      this.casesIds = casesList
    }
  }
}
</script>

<style scoped>
.pagination-container{
  width: 100px;
  height: 100px;
  position: absolute;
  right: 10%;
  bottom: 0;
}
</style>
