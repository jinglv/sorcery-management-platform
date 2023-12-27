<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="900px"
    :before-close="closeDialog"
  >
    <el-form
      ref="ruleForm"
      :model="casesRunForm"
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
      <el-form-item label="执行环境">
        <el-select
          v-model="envValue"
          placeholder="请选择执行环境"
          style="width: 100%;"
          @change="changeEnv"
        >
          <el-option
            v-for="item in envOption"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="类型">
        <el-input v-model="casesRunForm.type" :disabled="true" />
      </el-form-item>
      <el-form-item style="text-align: right">
        <div class="dialog-footer">
          <el-button @click="closeDialog()">取消</el-button>
          <el-button
            :loading="loading"
            type="primary"
            @click="httpRunnerApi"
          >执行</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import { httpRunnerProjectList, httpRunnerRunCases } from '@/api/httprunner'
import { envsListByProject } from '@/api/envs'

export default {
  components: {},
  props: {
    ids: {
      type: Array,
      default: null
    }
  },
  data() {
    return {
      showTitle: 'HttpRunner接口执行',
      dialogVisible: true,
      projectValue: '',
      projectLabel: '',
      projectOption: [],
      projectId: 0,
      envValue: '',
      envLabel: '',
      envOption: [],
      casesRunForm: {
        httprunner_project_id: '',
        type: 'TESTCASE',
        cases_ids: [],
        env_url: ''
      },
      req: {
        page: 1,
        size: 10
      },
      // 分页页数
      total: 10,
      loading: false
    }
  },
  mounted() {
    this.initHttpRunnerProjectList()
    // if (this.ids.length === 0) {
    //   this.$message.error('请选择接口')
    // }
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
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
      this.getEnvList()
    },
    // 查看环境列表
    async getEnvList() {
      const resp = await envsListByProject(this.projectId)
      if (resp.success === true) {
        for (let i = 0; i < resp.result.length; i++) {
          this.envOption.push({
            value: resp.result[i].env + '=' + resp.result[i].protocol + resp.result[i].base_url,
            label: resp.result[i].name
          })
        }
        // this.$message.success('查询成功！')
      } else {
        this.$message.error('查询失败！')
      }
    },
    changeEnv(value) {
      this.envValue = value
      this.envLabel = this.envOption.find(
        (item) => item.value === value
      ).label
    },
    async httpRunnerApi() {
      this.casesRunForm.httprunner_project_id = this.projectValue
      this.casesRunForm.env_url = this.envValue
      this.casesRunForm.cases_ids = this.ids
      this.loading = true
      const resp = await httpRunnerRunCases(this.casesRunForm)
      if (resp.success === true) {
        this.$message.success('执行成功！')
        this.loading = false
        this.closeDialog()
      } else {
        this.$message.error(resp.error.message)
      }
    }
  }
}
</script>
<style scoped>
#image {
  text-align: left;
}
</style>
