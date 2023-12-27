<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="1300px"
    :before-close="closeDialog"
  >
    <el-row :gutter="20">
      <el-col :span="12">
        <div align="right">
          <el-button size="small" type="primary" @click="runDebugtalk()">点击运行</el-button>
          <el-button size="small" type="success" :disabled="saveFlag" @click="updateInfo()">提交保存</el-button>
        </div>
        <div style="margin-top: 10px;">
          <ace-code-editor-dialog ref="ace" :value="codes" class="ace-editor" :min-lines="25" :mode-path="language" @getCode="getCode" />
        </div>
      </el-col>
      <el-col :span="12">
        <el-button size="small" type="warning" disabled>运行结果</el-button>
        <div style="margin-top: 10px;">
          <ace-code-editor-dialog ref="ace" v-model="result" class="ace-editor" :min-lines="25" :mode-path="language" />
        </div>
      </el-col>
    </el-row>
    <div class="dialog-footer" align="right">
      <el-button @click="closeDialog()">取消</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { run, updateHttpRunnerProject } from '@/api/httprunner'
import AceCodeEditorDialog from '@/components/HttpRunner/aceCodeEditorDialog.vue'

export default {
  components: {
    AceCodeEditorDialog
  },
  props: {
    title: {
      type: String,
      default: null
    },
    hid: {
      type: Number,
      default: 1
    },
    pid: {
      type: Number,
      default: 1
    },
    hname: {
      type: String,
      default: null
    },
    desc: {
      type: String,
      default: null
    },
    code: {
      type: String,
      default: null
    },
    ecode: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      showTitle: '',
      dialogVisible: true,
      language: 'python',
      codes: '',
      in_code: '',
      result: '',
      saveFlag: false
    }
  },
  mounted() {
    if (this.title === 'debugtalk') {
      this.showTitle = 'DebugTalk'
    }
    this.codes = this.code
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
    },
    getCode(code) {
      this.in_code = code
    },
    // 运行
    async runDebugtalk() {
      // this.getCode()
      const req = {
        code: this.in_code === '' ? this.code : this.in_code
      }
      console.info('code', req)
      console.info('in_code', req)
      const resp = await run(req)
      if (resp.success === true) {
        this.result = resp.result
      } else {
        this.$message.error('执行失败！')
      }
    },
    // 更新
    async updateInfo() {
      const req = {
        'project_id': this.pid,
        'env_code': this.ecode,
        'name': this.hname,
        'describe': this.desc,
        'code': typeof (this.in_code) === 'undefined' ? '' : this.in_code
      }
      console.info('req', req)
      const resp = await updateHttpRunnerProject(this.hid, req)
      if (resp.success === true) {
        this.closeDialog()
        this.$message.success('保存成功')
        this.saveFlag = true
        // 延时器
        setTimeout(() => {
          this.$emit('close')
        }, 500)
      } else {
        this.$message.error('保存失败')
      }
    }
  }
}
</script>
<style scoped>
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
  }
</style>
