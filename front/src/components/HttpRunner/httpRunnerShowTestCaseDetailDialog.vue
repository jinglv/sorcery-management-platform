<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="900px"
    :before-close="closeDialog"
  >
    <el-form
      ref="ruleForm"
      :model="testCaseDetailForm"
      label-width="180px"
      class="demo-ruleForm"
    >
      <el-form-item label="测试用例名称：" prop="name">{{ testCaseDetailForm.name }}</el-form-item>
      <el-form-item label="用例配置信息：" prop="config">
        <json-viewer :value="testCaseDetailForm.config" :expand-depth="2" />
      </el-form-item>
      <el-form-item label="测试步骤：" prop="teststeps">
        <json-viewer :value="testCaseDetailForm.teststeps" :expand-depth="2" />
      </el-form-item>
      <el-form-item label="前置处理器：" prop="pre_processor">
        <el-collapse>
          <el-collapse-item title="代码">
            <pre><code class="python line-numbers">{{ testCaseDetailForm.pre_processor }}</code></pre>
          </el-collapse-item>
        </el-collapse>
      </el-form-item>
      <el-form-item label="后置处理器代码：" prop="post_processor">
        <el-collapse>
          <el-collapse-item title="代码">
            <pre><code class="python line-numbers">{{ testCaseDetailForm.post_processor }}</code></pre>
          </el-collapse-item>
        </el-collapse>
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
import Prism from 'prismjs'
import jsonViewer from 'vue-json-viewer'
import { httpRunnerTestCaseDetail } from '@/api/httprunner'

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
      testCaseDetailForm: {
        name: '',
        config: '',
        teststeps: {},
        pre_processor: '',
        post_processor: ''
      }
    }
  },
  mounted() {
    Prism.highlightAll()
    this.httpRunnerTestCaseDetail()
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
    },
    async httpRunnerTestCaseDetail() {
      const resp = await httpRunnerTestCaseDetail(this.id)
      if (resp.success === true) {
        this.testCaseDetailForm = resp.result
        if (Object.keys(this.testCaseDetailForm.config).length !== 0) {
          this.testCaseDetailForm.config = JSON.parse(resp.result.config.replace(/'/g, '"'))
        } else {
          this.testCaseDetailForm.config = {}
        }
        this.testCaseDetailForm.teststeps = JSON.parse(resp.result.teststeps.replace(/'/g, '"'))
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
