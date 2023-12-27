<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="750px"
    :before-close="closeDialog"
  >
    <div style="margin-top: 10px;">
      <ace-code-editor-dialog ref="ace" :value="env_codes" class="ace-editor" :min-lines="25" :mode-path="language" @getCode="getCode" />
    </div>
    <div class="dialog-footer" align="right">
      <el-button @click="closeDialog()">取消</el-button>
      <el-button
        type="primary"
        :disabled="saveFlag"
        @click="updateInfo()"
      >保存</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { updateHttpRunnerProject } from '@/api/httprunner'
import AceCodeEditorDialog from '@/components/HttpRunner/aceCodeEditorDialog.vue'

export default {
  name: 'EnvDialog',
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
      env_codes: '',
      env_code: '',
      saveFlag: false
    }
  },
  mounted() {
    if (this.title === 'env') {
      this.showTitle = '环境变量'
    }
    this.env_codes = this.ecode
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
    },
    getCode(code) {
      this.env_code = code
    },
    // 更新
    async updateInfo() {
      const req = {
        'project_id': this.pid,
        'env_code': typeof (this.env_code) === 'undefined' ? '' : this.env_code,
        'name': this.hname,
        'describe': this.desc,
        'code': this.code
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
