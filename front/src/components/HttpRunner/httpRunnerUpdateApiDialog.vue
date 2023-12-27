<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="900px"
    :before-close="closeDialog"
  >
    <el-form
      :model="apiDetailInfo"
      label-width="120px"
    >
      <el-form-item label="接口名称：" prop="name">
        <el-input v-model="apiDetailInfo.name" />
      </el-form-item>
      <el-form-item label="基础环境：" prop="base_url">
        <el-input v-model="apiDetailInfo.base_url" :disabled="true" />
      </el-form-item>
      <el-tabs v-model="activeName">
        <el-tab-pane label="请求参数变量" name="first" prop="variables">
          <ace-code-editor-dialog ref="ace" :value="variables" class="ace-editor" :min-lines="18" :mode-path="language" @getCode="getInputVariables" />
        </el-tab-pane>
        <el-tab-pane label="请求接口信息" name="second" :lazy="true">
          <el-form-item label="请求方式：" prop="method">
            <el-select
              v-model="method"
              placeholder="方法"
              style="width: 100%; float: left"
            >
              <el-option
                v-for="item in methodOption"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="接口地址：" prop="url">
            <el-input v-model="url" />
          </el-form-item>
          <el-form-item label="请求头信息：" prop="headers" :lazy="true">
            <ace-code-editor-dialog ref="ace" :value="headers" class="ace-editor" :min-lines="18" :mode-path="language" @getCode="getInputHeaders" />
          </el-form-item>
          <el-form-item label="请求请求参数：" prop="json" :lazy="true">
            <ace-code-editor-dialog ref="ace" :value="json" class="ace-editor" :min-lines="18" :mode-path="language" @getCode="getInputJson" />
          </el-form-item>
        </el-tab-pane>
        <el-tab-pane label="接口提取数据" name="third" :lazy="true">
          <ace-code-editor-dialog ref="ace" :value="extract" class="ace-editor" :min-lines="18" :mode-path="language" @getCode="getInputExtract" />
        </el-tab-pane>
        <el-tab-pane label="接口断言信息" name="fourth" :lazy="true">
          <ace-code-editor-dialog ref="ace" :value="validate" class="ace-editor" :min-lines="18" :mode-path="language" @getCode="getInputValidate" />
        </el-tab-pane>
        <el-tab-pane label="前置处理器(SetUp)" name="fifth" :lazy="true">
          <el-row :gutter="20">
            <el-col :span="12">
              <div align="right">
                <el-button size="small" type="primary" @click="runPreCode()">点击运行</el-button>
              </div>
              <div style="margin-top: 10px;">
                <ace-code-editor-dialog ref="ace" :value="pre_code" class="ace-editor" :min-lines="18" :mode-path="language_python" @getCode="getPreCode" />
              </div>
            </el-col>
            <el-col :span="12">
              <el-button size="small" type="warning" disabled>运行结果</el-button>
              <div style="margin-top: 10px;">
                <ace-code-editor-dialog ref="ace" v-model="result" class="ace-editor" :min-lines="18" :mode-path="language_python" />
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>
        <el-tab-pane label="后置处理器(TearDown)" name="sixth" :lazy="true">
          <el-row :gutter="20">
            <el-col :span="12">
              <div align="right">
                <el-button size="small" type="primary" @click="runPostCode()">点击运行</el-button>
              </div>
              <div style="margin-top: 10px;">
                <ace-code-editor-dialog ref="ace" :value="post_code" class="ace-editor" :min-lines="18" :mode-path="language_python" @getCode="getPostCode" />
              </div>
            </el-col>
            <el-col :span="12">
              <el-button size="small" type="warning" disabled>运行结果</el-button>
              <div style="margin-top: 10px;">
                <ace-code-editor-dialog ref="ace" v-model="result" class="ace-editor" :min-lines="18" :mode-path="language_python" />
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>
      </el-tabs>
      <el-form-item style="text-align: right; margin-top: 20px;">
        <div class="dialog-footer">
          <el-button @click="closeDialog()">取消</el-button>
          <el-button type="primary" @click="updateHttpRunnerApi()">更新</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import { httpRunnerApiDetail, updateHttpRunnerApi, run } from '@/api/httprunner'
import AceCodeEditorDialog from '@/components/HttpRunner/aceCodeEditorDialog'

export default {
  components: {
    AceCodeEditorDialog
  },
  props: {
    id: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      showTitle: '编辑接口详情',
      dialogVisible: true,
      apiDetailInfo: {},
      method: '',
      url: '',
      headers: '',
      in_headers: '',
      json: '',
      in_json: '',
      methodOption: [
        {
          value: 'GET',
          label: 'GET'
        },
        {
          value: 'POST',
          label: 'POST'
        },
        {
          value: 'PUT',
          label: 'PUT'
        },
        {
          value: 'DELETE',
          label: 'DELETE'
        }
      ],
      activeName: 'first',
      language: 'json',
      language_python: 'python',
      variables: '',
      in_variables: '',
      extract: '',
      in_extract: '',
      validate: '',
      in_validate: '',
      pre_code: '',
      in_pre_code: '',
      post_code: '',
      in_post_code: '',
      result: ''
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
        const body = resp.result
        this.apiDetailInfo = body.api_info
        this.variables = JSON.stringify(this.apiDetailInfo.variables, null, 2)
        this.method = this.apiDetailInfo.request.method
        this.url = this.apiDetailInfo.request.url
        this.headers = JSON.stringify(this.apiDetailInfo.request.headers, null, 2)
        this.json = JSON.stringify(this.apiDetailInfo.request.json, null, 2)
        this.extract = JSON.stringify(this.apiDetailInfo.extract, null, 2)
        this.validate = JSON.stringify(this.apiDetailInfo.validate, null, 2)
        this.pre_code = body.pre_processor
        this.post_code = body.post_processor
        // this.$message.success('查询成功！')
      } else {
        this.$message.error('查询失败！')
      }
    },
    getInputVariables(value) {
      this.in_variables = value
    },
    getInputHeaders(value) {
      this.in_headers = value
    },
    getInputJson(value) {
      this.in_json = value
    },
    getInputExtract(value) {
      this.in_extract = value
    },
    getInputValidate(value) {
      this.in_validate = value
    },
    getPreCode(code) {
      this.in_pre_code = code
    },
    getPostCode(code) {
      this.in_post_code = code
    },
    async updateHttpRunnerApi() {
      const api_info_req = {
        'name': this.apiDetailInfo.name,
        'base_url': this.apiDetailInfo.base_url,
        'variables': JSON.parse(this.in_variables === '' ? this.variables : this.in_variables),
        'request': {
          'method': this.method,
          'url': this.url,
          'headers': JSON.parse(this.in_headers === '' ? this.headers : this.in_headers),
          'json': JSON.parse(this.in_json === '' ? this.json : this.in_json)
        },
        'extract': JSON.parse(this.in_extract === '' ? this.extract : this.in_extract),
        'validate': JSON.parse(this.in_validate === '' ? this.validate : this.in_validate)
      }
      const req = {
        'name': this.apiDetailInfo.name,
        'api_info': api_info_req,
        'pre_processor': this.in_pre_code === '' ? this.pre_code : this.in_pre_code,
        'post_processor': this.in_post_code === '' ? this.post_code : this.in_post_code
      }
      console.info('update req:', req)
      const resp = await updateHttpRunnerApi(this.id, req)
      if (resp.success === true) {
        this.$message.success('更新成功！')
        this.closeDialog()
      } else {
        this.$message.error('更新失败！')
      }
    },
    // 运行
    async runPreCode() {
      const req = {
        code: this.in_pre_code === '' ? this.pre_code : this.in_pre_code
      }
      const resp = await run(req)
      if (resp.success === true) {
        this.result = resp.result
      } else {
        this.$message.error('执行失败！')
      }
    },
    async runPostCode() {
      const req = {
        code: this.in_post_code === '' ? this.post_code : this.in_post_code
      }
      const resp = await run(req)
      if (resp.success === true) {
        this.result = resp.result
      } else {
        this.$message.error('执行失败！')
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
