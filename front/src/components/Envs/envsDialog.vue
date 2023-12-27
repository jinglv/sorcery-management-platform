<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="1000px"
    :before-close="closeDialog"
  >
    <div v-if="title === 'view'">
      <el-form
        :model="envForm"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="项目名称：" prop="project_name">{{ envForm.project_name }}</el-form-item>
        <el-form-item label="环境名称：" prop="name">{{ envForm.name }}</el-form-item>
        <el-form-item label="环境值：" prop="env">{{ envForm.env }}</el-form-item>
        <el-form-item label="浏览器：" prop="browser">{{ envForm.browser }}</el-form-item>
        <el-form-item label="请求协议：" prop="protocol">{{ envForm.protocol }}</el-form-item>
        <el-form-item label="基础URL:" prop="base_url">{{ envForm.base_url }}</el-form-item>
        <el-form-item style="text-align: right">
          <el-button @click="closeDialog()">返回</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-if="title !== 'view'">
      <el-form
        ref="ruleForm"
        :model="envForm"
        :rules="rules"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item v-if="pid===0" label="请选择项目" prop="name">
          <el-select
            v-model="projectValue"
            placeholder="请选择项目"
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
        <el-form-item label="环境名称" prop="name">
          <el-input v-model="envForm.name" />
        </el-form-item>
        <el-form-item label="环境值" prop="env">
          <el-input v-model="envForm.env" />
        </el-form-item>
        <el-form-item label="浏览器">
          <el-input v-model="envForm.browser" />
        </el-form-item>
        <el-form-item label="基础URL" prop="base_url" :inline="true">
          <el-select
            v-model="httpValue"
            style="width: 15%; float: left"
            @change="changeProtocol"
          >
            <el-option
              v-for="item in httpOption"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
          <el-input v-model="envForm.base_url" style="width:85%" />
        </el-form-item>
        <el-form-item>
          <div class="dialog-footer" style="text-align: right">
            <el-button v-if="pid!==0" type="primary" @click="jumpEnvs()">查看环境列表</el-button>
            <el-button @click="closeDialog()">取消</el-button>
            <el-button
              type="primary"
              :disabled="saveFlag"
              @click="submitForm('ruleForm')"
            >保存</el-button>
          </div>
        </el-form-item>
      </el-form>
    </div>
  </el-dialog>
</template>

<script>
import { projectList } from '@/api/projects'
import { createEnvs, updateEnvs, getEnvsInfo } from '@/api/envs'

export default {
  props: {
    title: {
      type: String,
      default: null
    },
    pid: {
      type: Number,
      default: 0
    },
    eid: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      showTitle: '',
      dialogVisible: true,
      envForm: {
        project_id: 0,
        name: '',
        env: '',
        browser: '',
        protocol: '',
        base_url: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入环境的名称', trigger: 'blur' }
        ],
        env: [
          { required: true, message: '请输入环境的值,如:dev、test、prod', trigger: 'blur' }
        ],
        base_url: [
          { required: true, message: '请输入环境的基础URL', trigger: 'blur' }
        ]
      },
      httpValue: 1,
      httpLabel: 'http://',
      httpOption: [
        {
          value: 1,
          label: 'http://'
        },
        {
          value: 2,
          label: 'https://'
        }
      ],
      saveFlag: false,
      projectValue: '',
      projectLabel: '',
      projectOption: []
    }
  },
  mounted() {
    this.initProjectList()
    if (this.title === 'create') {
      this.showTitle = '创建环境详情'
    } else if (this.title === 'edit') {
      this.showTitle = '编辑环境详情'
      this.getEnvsInfo()
    } else if (this.title === 'view') {
      this.showTitle = '查看环境详情'
      this.getEnvsInfo()
    }
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.title === 'create') {
            if (this.pid !== 0) {
              this.envForm.project_id = this.pid
            } else {
              this.envForm.project_id = this.projectValue
            }
            this.envForm.protocol = this.httpLabel
            createEnvs(this.envForm).then((resp) => {
              if (resp.success === true) {
                // 延时器
                setTimeout(() => {
                  this.saveFlag = true
                }, 500)
                this.closeDialog()
                this.$message.success('创建成功！')
              } else {
                this.$message.error(resp.error.message)
              }
            })
          } else if (this.title === 'edit') {
            this.envForm.project_id = this.projectValue
            this.envForm.protocol = this.httpLabel
            updateEnvs(this.eid, this.envForm).then((resp) => {
              if (resp.success === true) {
                // 延时器
                setTimeout(() => {
                  this.saveFlag = true
                }, 500)
                this.closeDialog()
                this.$message.success('更新成功！')
              } else {
                this.$message.error(resp.error.message)
              }
            })
          }
        } else {
          return false
        }
      })
    },
    // 获取选中的协议值
    changeProtocol(value) {
      this.httpValue = value
      this.httpLabel = this.httpOption.find(
        (item) => item.value === value
      ).label
      console.log('选中名称', this.httpLabel)
    },
    // 初始化项目列表
    async initProjectList() {
      const req_body = {
        'name': ''
      }
      const resp = await projectList(this.req, req_body)
      if (resp.success === true) {
        for (let i = 0; i < resp.items.length; i++) {
          this.projectOption.push({
            value: resp.items[i].id,
            label: resp.items[i].name
          })
        }
        // this.$message.success("查询成功！")
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
    async getEnvsInfo() {
      const resp = await getEnvsInfo(this.eid)
      if (resp.success === true) {
        this.envForm = resp.result
        this.projectValue = resp.result.project_id
      } else {
        this.$message.error(resp.error.message)
      }
    },
    jumpEnvs() {
      this.$router.push('/envs/index')
    }
  }
}
</script>
<style scoped>
#image {
  text-align: left;
}
</style>
