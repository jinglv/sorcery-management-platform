<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="1000px"
    :before-close="closeDialog"
  >
    <el-form
      ref="ruleForm"
      :rules="rules"
      :model="httpRunnerProjectForm"
      label-width="200px"
      class="demo-ruleForm"
    >
      <el-form-item label="项目名称" prop="project_id">
        <el-select
          v-model="httpRunnerProjectForm.project_id"
          style="width: 760px;"
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
      <el-form-item label="HttpRunner工程名称" prop="name">
        <el-input v-model="httpRunnerProjectForm.name" />
      </el-form-item>
      <el-form-item label="描述" prop="describe">
        <el-input v-model="httpRunnerProjectForm.describe" />
      </el-form-item>
      <el-form-item style="text-align: right">
        <div class="dialog-footer">
          <el-button @click="closeDialog()">取消</el-button>
          <el-button
            type="primary"
            :disabled="saveFlag"
            @click="submitForm('ruleForm')"
          >保存</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import { projectList } from '@/api/projects'
import { createHttpRunnerProject } from '@/api/httprunner'

export default {
  props: {
    title: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      showTitle: '',
      dialogVisible: true,
      httpRunnerProjectForm: {
        project_id: 0,
        name: '',
        describe: '',
        code: '',
        env_code: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入HttpRunner工程名称', trigger: 'blur' }
        ]
      },
      projectForm: {
        name: ''
      },
      req: {
        page: 1,
        size: 10
      },
      // 分页页数
      total: 6,
      projectOption: [],
      saveFlag: false
    }
  },
  mounted() {
    this.projectList()
    if (this.title === 'createProject') {
      this.showTitle = '创建HTTpRunner项目'
    }
  },
  methods: {
    // 初始化项目列表
    async projectList() {
      const resp = await projectList(this.req, JSON.stringify(this.projectForm))
      if (resp.success === true) {
        this.projectValue = resp.items[0].id
        this.projectLabel = resp.items[0].name
        this.httpRunnerProjectForm.project_id = resp.items[0].id
        for (let i = 0; i < resp.items.length; i++) {
          this.projectOption.push({
            value: resp.items[i].id,
            label: resp.items[i].name
          })
        }
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 修改选中项目
    changeProject(value) {
      this.projectValue = value
      this.projectLabel = this.projectOption.find(
        (item) => item.value === value
      ).label
    },
    closeDialog() {
      this.$emit('cancel', {})
    },
    // 创建项目
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          createHttpRunnerProject(this.httpRunnerProjectForm).then((resp) => {
            if (resp.success === true) {
              // 创建成功，关闭弹窗
              this.closeDialog()
              this.$message.success('项目创建成功！')
            } else {
              this.$message.error(resp.error.message)
            }
          })
        } else {
          return false
        }
      })
    }
  }
}
</script>
<style scoped>
#image {
  text-align: left;
}
</style>
