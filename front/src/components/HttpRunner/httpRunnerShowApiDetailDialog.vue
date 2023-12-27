<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="900px"
    :before-close="closeDialog"
  >
    <el-form
      ref="ruleForm"
      :model="apiDetailForm"
      label-width="120px"
      class="demo-ruleForm"
    >
      <el-form-item label="接口名称：" prop="name">{{ apiDetailForm.name }}</el-form-item>
      <el-form-item label="基础接口名称：" prop="base_name">{{ apiDetailForm.base_api_name }}</el-form-item>
      <el-form-item label="接口详细信息：" prop="api_info">
        <json-viewer :value="apiDetailForm.api_info" :expand-depth="3" />
      </el-form-item>
      <el-form-item style="text-align: right">
        <div class="dialog-footer">
          <el-button @click="closeDialog()">取消</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import jsonViewer from 'vue-json-viewer'
import { httpRunnerApiDetail } from '@/api/httprunner'

export default {
  components: {
    jsonViewer
  },
  props: {
    id: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      showTitle: '查看接口详情',
      dialogVisible: true,
      apiDetailForm: {
        name: '',
        base_api_name: '',
        api_info: {}
      }
    }
  },
  mounted() {
    this.httpRunnerApiDetail()
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
    },
    async httpRunnerApiDetail() {
      const resp = await httpRunnerApiDetail(this.id)
      if (resp.success === true) {
        this.apiDetailForm = resp.result
        // this.$message.success('查询成功！')
      } else {
        this.$message.error('查询失败！')
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
