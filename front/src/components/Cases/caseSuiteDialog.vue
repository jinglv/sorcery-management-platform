<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="500px"
    :before-close="closeDialog"
  >
    <el-form
      ref="ruleForm"
      :model="caseSuiteForm"
      :rules="rules"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="用例集名称" prop="name">
        <el-input v-model="caseSuiteForm.name" />
      </el-form-item>
      <el-form-item v-if="parentObj.label !== undefined" label="父节点">
        <el-input v-model="parentObj.label" disabled />
      </el-form-item>
      <el-form-item label="描述" prop="describe">
        <el-input v-model="caseSuiteForm.describe" />
      </el-form-item>
      <el-form-item style="text-align: right">
        <el-button @click="closeDialog">取消</el-button>
        <el-button
          type="primary"
          @click="submitForm('ruleForm')"
        >确定</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import { createCaseSuite } from '@/api/cases'

export default {
  name: 'CaseSuiteDialog',
  components: {},
  props: {
    rootId: {
      type: Boolean,
      default: true
    },
    parentObj: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      showTitle: '',
      dialogVisible: true,
      caseSuiteForm: {
        name: '',
        describe: '',
        parent_id: 0
      },
      rules: {
        name: [
          { required: true, message: '请输入用例集名称', trigger: 'blur' }
        ]
      },
      fileList: [],
      imageUrl: '',
      imageVisible: false,
      disabled: false
    }
  },
  mounted() {
    if (this.rootId === true) {
      this.showTitle = '创建根节点'
    } else {
      this.showTitle = '创建子节点'
      this.caseSuiteForm.parent_id = this.parentObj.id
    }
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
    },
    // 创建模块
    submitForm(formName) {
      console.info('请求参数：', this.caseSuiteForm)
      this.$refs[formName].validate((valid) => {
        if (valid) {
          createCaseSuite(this.caseSuiteForm).then((resp) => {
            if (resp.success === true) {
              this.closeDialog()
              this.$message.success('创建成功！')
            } else {
              this.$message.error(resp.error.message)
            }
          })
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
