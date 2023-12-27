<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="900px"
    :before-close="closeDialog"
  >
    <el-form
      ref="ruleForm"
      :model="apiForm"
      label-width="120px"
      class="demo-ruleForm"
    >
      <el-form-item label="HttpRunner项目">
        <el-select
          v-model="projectValue"
          placeholder="请选择HttpRunner项目名称"
          style="width: 100%;"
          @change="changeProject"
        >
          <el-option
            v-for="item in projectOption"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <div style="margin-top: 10px">
          <el-card style="width: 28%; height: 300px; float: left">
            <el-tree
              :data="moduleData"
              node-key="id"
              default-expand-all
              :expand-on-click-node="false"
              @node-click="nodeClick"
            >
              <span slot-scope="{ node }" class="custom-tree-node">
                <span style="float: left">{{ node.label }}</span>
              </span>
            </el-tree>
          </el-card>
          <div style="width: 70%; float: right">
            <el-table
              ref="multipleTable"
              :data="apiData"
              border
              style="width: 100%"
              @select="selectionOneApi"
              @select-all="selectionAllApi"
            >
              <el-table-column type="selection" width="55" />
              <el-table-column prop="id" label="接口ID" width="70" />
              <el-table-column prop="name" label="接口名称" width="150" />
              <el-table-column prop="api_path" label="接口地址" />
            </el-table>
            <!--分页-->
            <div style="width: 100%; text-align: right">
              <el-pagination
                background
                layout="prev, pager, next"
                :page-size="req.size"
                :total="total"
                @current-change="handleCurrentChange"
              />
            </div>
          </div>
        </div>
      </el-form-item>
      <el-form-item style="text-align: right">
        <div class="dialog-footer">
          已选择【{{ apiNum }}】接口
          <el-button @click="closeDialog()">取消</el-button>
          <el-button
            type="primary"
            @click="showHttpRunnerApi"
          >创建HttpRunner工程接口</el-button>
        </div>
      </el-form-item>
    </el-form>
    <http-runner-create-api-dialog v-if="createApiDialog" :modal="false" :datas="apiInfoList" :project="apiForm.httprunner_project_id" @visible="dialogClose" @cancel="closeDialog" />
  </el-dialog>
</template>

<script>
import { getModuleTree } from '@/api/modules'
import { httpRunnerProjectList } from '@/api/httprunner'
import { getApisList } from '@/api/apis'
import HttpRunnerCreateApiDialog from './httpRunnerCreateApiDialog'

export default {
  components: { HttpRunnerCreateApiDialog },
  props: {
  },
  data() {
    return {
      showTitle: '选择接口',
      dialogVisible: true,
      apiForm: {
        name: '',
        httprunner_project_id: '',
        base_api_id: ''
      },
      moduleData: [],
      apiData: [],
      apiNum: 0,
      casesData: [],
      currentModuleId: 0,
      apiInfoList: [],
      projectValue: '',
      projectLabel: '',
      projectOption: [],
      projectId: 0,
      req: {
        page: 1,
        size: 10
      },
      // 分页页数
      total: 10,
      createApiDialog: false
    }
  },
  mounted() {
    this.initHttpRunnerProjectList()
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
    },
    dialogClose(value) {
      if (value === false) {
        this.createApiDialog = false
      }
    },
    async initHttpRunnerProjectList() {
      const resp = await httpRunnerProjectList(this.req)
      if (resp.success === true) {
        for (let i = 0; i < resp.items.length; i++) {
          this.projectOption.push({
            value: resp.items[i].id,
            label: resp.items[i].name,
            projectId: resp.items[i].project_id
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
      this.projectId = this.projectOption.find(
        (item) => item.value === value
      ).projectId
      this.apiForm.httprunner_project_id = value
      this.getModuleList(this.projectId)
    },
    // 查询模块列表
    async getModuleList(pid) {
      const resp = await getModuleTree(pid)
      if (resp.success === true) {
        this.moduleData = resp.result
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 点击模块
    nodeClick(data) {
      this.currentModuleId = data.id
      this.getModuleApiList(data.id)
    },
    // 初始化模块下接口数据
    async getModuleApiList(mid) {
      const resp = await getApisList(mid, this.req)
      if (resp.success === true) {
        this.apiData = resp.items
        // this.$message.success('查询成功！')
        // 记录模块下，已选中的接口
        this.$nextTick(() => {
          const rows = []
          for (let i = 0; i < this.apiInfoList.length; i++) {
            for (let j = 0; j < this.apiData.length; j++) {
              if (this.apiInfoList[i].id === this.apiData[j].id) {
                rows.push(this.apiData[j])
              }
            }
          }
          rows.forEach((row) => {
            this.$refs.multipleTable.toggleRowSelection(row)
          })
        })
      } else {
        this.$message.error(resp.error.message)
      }
    },
    // 选择所有用例
    selectionAllApi(val, row) {
      this.selectiveApi(val)
    },
    // 选择一条用例
    selectionOneApi(val, row) {
      this.selectiveApi(val)
    },
    // 公共方法：选择接口
    selectiveApi(multipleSelection) {
      var selective = false
      for (let i = 0; i < this.apiInfoList.length; i++) {
        if (this.apiInfoList[i].module_id === this.currentModuleId) {
          selective = true
          this.apiInfoList = multipleSelection
        }
      }
      if (selective === false) {
        for (let i = 0; i < multipleSelection.length; i++) {
          this.apiInfoList.push(multipleSelection[i])
        }
      }
      this.calculationApi()
    },
    // 公共方法：计算用例数量
    calculationApi() {
      this.apiNum = 0
      this.apiNum += this.apiInfoList.length
    },
    showHttpRunnerApi() {
      this.createApiDialog = true
    },
    // 跳转到第几页
    handleCurrentChange(val) {
      this.req.page = val
      this.getModuleApiList(this.currentModuleId)
    }
  }
}
</script>
<style scoped>
#image {
  text-align: left;
}
</style>
