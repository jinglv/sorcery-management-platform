<template>
  <div class="httpRunnerPrject">
    <div style="text-align: left; margin-top: 20px">
      <el-button
        style="float: right;margin-bottom: 10px;"
        type="primary"
        size="medium"
        @click="createProject()"
      >创建HttpRunner项目</el-button>
    </div>

    <div>
      <el-table :data="projectData" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="project_name" label="项目名称" />
        <el-table-column prop="name" label="HttpRunner工程名称" />
        <el-table-column prop="describe" label="描述" />
        <el-table-column prop="env_code" label="环境变量">
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="envs(scope.row)"
            >.env</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="code" label="DebugTalk">
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="debugtalk(scope.row)"
            >debugtalk</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" />
        <el-table-column prop="update_time" label="更新时间" />
      </el-table>
    </div>
    <div style="width: 100%; text-align: right">
      <el-pagination
        background
        layout="prev, pager, next"
        :page-size="req.size"
        :total="total"
        @current-change="handleCurrentChange"
      />
    </div>

    <debugtalk-dialog
      v-if="dialogFlag"
      :title="dialogTitle"
      :hid="httpRunnerProjectId"
      :pid="curruntProjectId"
      :hname="httpRunnerProjectName"
      :desc="httpRunnerDesc"
      :code="code"
      :ecode="env_code"
      @cancel="closeDialog()"
    />
    <env-dialog
      v-if="envDialogFlag"
      :title="dialogTitle"
      :hid="httpRunnerProjectId"
      :pid="curruntProjectId"
      :hname="httpRunnerProjectName"
      :desc="httpRunnerDesc"
      :code="code"
      :ecode="env_code"
      @cancel="closeDialog()"
    />
    <create-project-dialog v-if="createProjectDialogFlag" :title="dialogTitle" @cancel="closeDialog" />
  </div>
</template>

<script>
import { httpRunnerProjectList } from '@/api/httprunner'
import createProjectDialog from '@/components/HttpRunner/createProjectDialog'
import debugtalkDialog from '@/components/HttpRunner/debugtalkDialog'
import envDialog from '@/components/HttpRunner/envDialog'

export default {
  components: {
    debugtalkDialog,
    envDialog,
    createProjectDialog
  },
  data() {
    return {
      projectOption: [],
      projectName: '',
      httpRunnerProjectId: 0,
      curruntProjectId: 0,
      httpRunnerProjectName: '',
      httpRunnerDesc: '',
      code: '',
      env_code: '',
      dialogFlag: false,
      envDialogFlag: false,
      dialogTitle: 'env',
      projectData: [],
      req: {
        page: 1,
        size: 10
      },
      total: 10,
      taskData: [],
      createProjectDialogFlag: false
    }
  },
  mounted() {
    this.initHttpRunnerProjectList()
  },
  methods: {
    // 初始化项目列表
    async initHttpRunnerProjectList() {
      const resp = await httpRunnerProjectList(this.req)
      if (resp.success === true) {
        this.projectData = resp.items
        this.total = resp.total
        for (let i = 0; i < resp.items.length; i++) {
          resp.items[i].create_time = this.$moment(
            resp.items[i].create_time
          ).format('YYYY-MM-DD HH:mm:ss')
        }
        // this.$message.success("查询成功！")
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 创建HttpRunner项目
    createProject() {
      this.dialogTitle = 'createProject'
      this.createProjectDialogFlag = true
    },
    // debugtalk
    debugtalk(row) {
      this.dialogTitle = 'debugtalk'
      this.curruntProjectId = row.project_id
      this.httpRunnerProjectId = row.id
      this.httpRunnerProjectName = row.name
      this.httpRunnerDesc = row.describe
      this.code = row.code
      this.env_code = row.env_code
      this.dialogFlag = true
    },
    // 环境变量
    envs(row) {
      this.dialogTitle = 'env'
      this.curruntProjectId = row.project_id
      this.httpRunnerProjectId = row.id
      this.httpRunnerProjectName = row.name
      this.httpRunnerDesc = row.describe
      this.code = row.code
      this.env_code = row.env_code
      this.envDialogFlag = true
    },
    // 关闭弹窗
    closeDialog() {
      this.dialogFlag = false
      this.envDialogFlag = false
      this.createProjectDialogFlag = false
      this.initHttpRunnerProjectList()
    },
    // 跳转到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.req.page = val
    }
  }
}
</script>
