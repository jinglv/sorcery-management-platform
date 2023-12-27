<template>
  <div class="httprunner-apis">
    <div class="filter-container">
      <el-row :gutter="24">
        <el-col :span="6">
          <div class="demo-input-suffix">
            接口名称:
            <el-input v-model="apiForm.name" placeholder="请输入接口名称" style="width: 54%;margin-right: 5px;" class="filter-item" />
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
        <el-button class="filter-item" type="primary" icon="el-icon-search" @click="initHttpRunnerApiList()">搜索</el-button>
      </div>
    </div>
    <div style="text-align: left; width: 100%; margin-top: 10px;">
      <el-button type="primary" icon="el-icon-circle-plus-outline" @click="showDialog()">创建HttpRunner项目接口</el-button>
      <el-button type="warning" icon="el-icon-bicycle" @click="showRunDialog()">接口执行</el-button>
      <el-button type="success" icon="el-icon-view" @click="showResultDialog()">查看执行结果</el-button>
    </div>
    <div style="margin-top: 10px;">
      <el-table ref="multipleTable" :data="httpRunnerProjectApiData" border style="width: 100%" @selection-change="handleSelectionChange">
        <el-table-column
          type="selection"
          width="55"
        />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="接口名称" />
        <el-table-column prop="httprunner_project_name" label="HttpRunner项目名称" />
        <el-table-column prop="create_time" label="创建时间" />
        <el-table-column fixed="right" label="操作">
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="showRowApiInfo(scope.row)"
            >详情</el-button>
            <el-button
              type="text"
              @click="updateRowApiInfo(scope.row)"
            >编辑</el-button>
            <el-button
              type="text"
              @click="deleteRowApiInfo(scope.row)"
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
    <!--引入子组件-->
    <http-runner-api-dialog v-if="dialogFlag" @cancel="closeDialog" />
    <http-runner-run-api-dialog v-if="dialogRunFlag" :ids="apiIds" @cancel="closeDialog" />
    <http-runner-run-result-dialog v-if="dialogResultFlag" :type="type" @cancel="closeDialog" />
    <http-runner-show-api-detail-dialog v-if="dialogViewApiFlag" :id="currentApiId" @cancel="closeDialog" />
    <http-runner-update-api-dialog v-if="dialogUpdateApiFlag" :id="currentApiId" @cancel="closeDialog" />
  </div>
</template>

<script>
import HttpRunnerApiDialog from '@/components/HttpRunner/httpRunnerApiDialog'
import { httpRunnerProjectList, getHttpRunnerApiList, deleteHttpRunnerApi } from '@/api/httprunner'
import HttpRunnerRunApiDialog from '@/components/HttpRunner/httpRunnerRunApiDialog'
import HttpRunnerRunResultDialog from '@/components/HttpRunner/httpRunnerRunResultDialog'
import HttpRunnerShowApiDetailDialog from '@/components/HttpRunner/httpRunnerShowApiDetailDialog'
import HttpRunnerUpdateApiDialog from '@/components/HttpRunner/httpRunnerUpdateApiDialog'

export default {
  name: 'HttpRunnerApi',
  components: {
    HttpRunnerApiDialog,
    HttpRunnerRunApiDialog,
    HttpRunnerRunResultDialog,
    HttpRunnerShowApiDetailDialog,
    HttpRunnerUpdateApiDialog
  },
  data() {
    return {
      dialogFlag: false,
      dialogRunFlag: false,
      dialogResultFlag: false,
      dialogViewApiFlag: false,
      dialogUpdateApiFlag: false,
      type: 'API',
      apiForm: {
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
      httpRunnerProjectApiData: [],
      apiIds: [],
      currentApiId: 0
    }
  },
  mounted() {
    // 组件加载的时候 进行调用
    this.initHttpRunnerProjectList()
    this.initHttpRunnerApiList()
  },
  methods: {
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
      this.apiForm.httprunner_project_id = value
      console.info('project value:', this.projectValue)
    },
    async initHttpRunnerApiList() {
      this.apiForm.httprunner_project_id = this.projectValue === '' ? 0 : this.projectValue
      const resp = await getHttpRunnerApiList(this.req, this.apiForm)
      if (resp.success === true) {
        this.total = resp.total
        for (let i = 0; i < resp.items.length; i++) {
          resp.items[i].create_time = this.$moment(
            resp.items[i].create_time
          ).format('YYYY-MM-DD HH:mm:ss')
        }
        this.httpRunnerProjectApiData = resp.items
        this.$message.success('查询成功！')
        // this.$message.success("查询成功！")
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 清除搜索
    clearSearch() {
      this.apiForm.name = ''
      this.projectValue = 0
      if (this.projectValue === 0) {
        this.projectValue = ''
      }
      this.initHttpRunnerApiList()
    },
    // 展示子组件
    showDialog() {
      this.dialogFlag = true
    },
    showRunDialog() {
      this.dialogRunFlag = true
    },
    showResultDialog() {
      this.dialogResultFlag = true
    },
    showRowApiInfo(row) {
      this.currentApiId = row.id
      this.dialogViewApiFlag = true
    },
    updateRowApiInfo(row) {
      this.currentApiId = row.id
      this.dialogUpdateApiFlag = true
    },
    async deleteRowApiInfo(row) {
      await deleteHttpRunnerApi(row.id).then((resp) => {
        this.$confirm('删除任务, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          center: true
        }).then(() => {
          if (resp.success === true) {
            this.initHttpRunnerApiList()
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
      this.initHttpRunnerApiList()
    },
    // 跳转到第几页
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`)
      this.req.page = val
      this.initProjectList()
    },
    toggleSelection(rows) {
      if (rows) {
        rows.forEach(row => {
          this.$refs.multipleTable.toggleRowSelection(row)
        })
      } else {
        this.$refs.multipleTable.clearSelection()
      }
    },
    handleSelectionChange(val) {
      this.selectiveApi(val)
    },
    selectiveApi(multipleSelection) {
      // 获取选中的API id
      const apiList = []
      for (let i = 0; i < multipleSelection.length; i++) {
        apiList.push(multipleSelection[i].id)
      }
      this.apiIds = apiList
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
