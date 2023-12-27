<template>
  <div :style="{'max-height': timeLineHeight +'px'}" style="margin-left: 10px; margin-right: 10px; overflow-y:scroll;">
    <div v-if="title == '接口详情'" class="div-line">
      <el-form
        :model="apiInfoForm"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="接口URL:" prop="url">{{ apiInfoForm.url }}</el-form-item>
        <el-form-item label="请求方式:" prop="method">{{ apiInfoForm.method }}</el-form-item>
        <el-form-item label="请求头:" prop="request_headers">
          <el-table
            :data="apiInfoForm.request_headers"
            border
            style="width: 80%"
          >
            <el-table-column
              prop="name"
              label="Name"
              width="180"
            />
            <el-table-column
              prop="value"
              label="Value"
            />
          </el-table>
        </el-form-item>
        <el-form-item label="Params:" prop="request_params">
          <el-table
            :data="apiInfoForm.request_params"
            border
            style="width: 80%"
          >
            <el-table-column
              prop="name"
              label="Name"
              width="180"
            />
            <el-table-column
              prop="value"
              label="Value"
            />
          </el-table>
        </el-form-item>
        <el-form-item label="Body:" prop="request_body">
          <json-viewer :value="apiInfoForm.request_body" :expand-depth="3" />
        </el-form-item>
        <el-form-item label="响应主体:" prop="response_body">
          <json-viewer :value="apiInfoForm.response_body" :expand-depth="3" />
        </el-form-item>
        <el-form-item style="text-align: right">
          <el-button @click="closeDialog()">返回</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div v-if="title != '接口详情'">
      <div class="div-line" style="height: 50px">
        <el-select
          v-model="apiInfoForm.method"
          placeholder="方法"
          style="width: 20%; float: left"
        >
          <el-option
            v-for="item in methodOption"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        <el-input
          v-model="apiInfoForm.url"
          placeholder="接口URL"
          style="width: 65%; float: left"
        />
        <el-button
          type="primary"
          style="float: left"
          @click="sendClick()"
        >发送</el-button>
      </div>
      <div class="div-line" style="height: 260px; overflow-y: auto;">
        <span class="title-text">Headers</span>
        <dict-dialog :dict-data="headerData" />
      </div>
      <span class="title-text">Request Params</span>
      <div class="div-line" style="height: 220px; overflow-y: auto;">
        <dict-dialog :dict-data="paramData" />
      </div>
      <span class="title-text">Request Body</span>
      <div class="div-line" style="height: 220px; overflow-y: auto;">
        <ace-code-editor-dialog ref="ace" :value="apiInfoForm.request_body" class="ace-editor" :min-lines="18" :mode-path="language" @getCode="getInputJsonBody" />
      </div>
      <div class="div-line" style="height: 150px; overflow-y: auto;">
        <el-tabs>
          <el-tab-pane label="接口响应结果">
            <json-viewer :value="apiForm.response" :expand-depth="3" />
          </el-tab-pane>
        </el-tabs>
      </div>
      <div class="div-line" style="margin-top: 70px">
        <el-collapse>
          <el-collapse-item title="断言" name="1">
            <div style="height: 40px">
              <el-radio
                v-model="apiForm.assert_type"
                label="include"
              >Include</el-radio>
              <el-radio
                v-model="apiForm.assert_type"
                label="equal"
              >Equal</el-radio>
              <el-button
                class="debug-button"
                type="success"
                plain
                size="small"
                @click="assertClick()"
              >断言</el-button>
            </div>
            <div style="height: 120px">
              <el-input
                v-model="apiForm.assert_text"
                type="textarea"
                :rows="5"
                placeholder="Assert text"
              />
            </div>
          </el-collapse-item>
        </el-collapse>
        <el-collapse>
          <el-collapse-item title="提取器" name="2">
            <el-form label-width="60px">
              <div v-for="(item, index) in extractList" :key="index">
                <el-form-item label="提取器">
                  <el-col :span="8">
                    <el-input
                      v-model="item.name"
                      placeholder="变量名"
                      style="width: 200px"
                    />
                  </el-col>
                  <el-col class="line" :span="2">-</el-col>
                  <el-col :span="11">
                    <el-input
                      v-model="item.value"
                      placeholder="提取规则"
                      style="width: 100%"
                    />
                  </el-col>
                  <el-button
                    type="text"
                    style="padding-right: 10px"
                    @click="removeExtract(index)"
                  >
                    <i class="el-icon-remove-outline" />
                  </el-button>
                </el-form-item>
              </div>
            </el-form>
            <el-button
              type="primary"
              size="mini"
              icon="el-icon-plus"
              plain
              @click="addExtract()"
            >添加</el-button>
            <el-button
              type="success"
              size="mini"
              icon="el-icon-document-checked"
              plain
              @click="checkExtract()"
            >检查</el-button>
          </el-collapse-item>
        </el-collapse>
      </div>
      <div style="height: 50px">
        <el-input
          v-model="apiForm.name"
          placeholder="请输入用例名称"
          size="small"
          style="width: 60%; float: left"
        />
        <el-button
          v-if="title != '编辑接口'"
          type="primary"
          size="small"
          style="float: left"
          :disabled="saveFlag"
          @click="saveTestCase()"
        >保存</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import jsonViewer from 'vue-json-viewer'
import { debugApi, assertApi, createApi, checkExtract, updateApi } from '@/api/apis'
import { apiInfoDetail } from '@/api/infos'
import dictDialog from '@/components/Api/dictDialog.vue'
import aceCodeEditorDialog from '@/components/HttpRunner/aceCodeEditorDialog'

export default {
  name: 'ApiRequest',
  components: {
    jsonViewer,
    dictDialog,
    aceCodeEditorDialog
  },
  props: {
    title: {
      type: String,
      default: null
    },
    aid: {
      type: Number,
      default: 1
    }
  },
  data() {
    return {
      methodOption: [
        {
          value: 'get',
          label: 'GET'
        },
        {
          value: 'post',
          label: 'POST'
        },
        {
          value: 'put',
          label: 'PUT'
        },
        {
          value: 'delete',
          label: 'DELETE'
        }
      ],
      request_path: '',
      activeName: 'first',
      paramsType: 1,
      json: {},
      response: '',
      assertType: 'include',
      apiInfoForm: {
        url: '',
        method: '',
        request_headers: [],
        request_params: [],
        request_body: {},
        response_body: {},
        assert_type: 'include',
        assert_text: ''
      },
      apiForm: {
        name: '',
        module_id: 0,
        api_path: '',
        method: 'get',
        header: [],
        params_type: 'params',
        params_body: '',
        response: '',
        assert_type: 'include',
        assert_text: ''
      },
      params: [],
      saveFlag: false,
      extractList: [],
      timeLineHeight: '',
      headerData: [{
        key: '',
        value: '',
        // 是否显示新增按钮
        show: 'true'
      }],
      paramData: [{
        key: '',
        value: '',
        // 是否显示新增按钮
        show: 'true'
      }],
      bodyFlag: false,
      paramFlag: true,
      json_body: ''
    }
  },
  mounted() {
    // 窗口滑动
    this.timeLineHeight = document.documentElement.clientHeight - 150
    window.onresize = () => { this.timeLineHeight = document.documentElement.clientHeight - 150 }
    // 初始化数据
    this.getApiInfoDetail()
  },
  methods: {
    // 获取一条用例信息
    async getApiInfoDetail() {
      const resp = await apiInfoDetail(this.aid)
      console.info('响应结果：', resp)
      if (resp.success === true) {
        // 接口获取数据
        this.apiInfoForm = resp.result
        // 将获取到的数据赋值给表单数据
        this.headerData = resp.result.request_headers
        // 获取头信息后，添加，是否可展示信息
        this.headerData[this.headerData.length - 1]['show'] = 'true'
        this.paramData = resp.result.request_params
        if (this.paramData.length !== 0) {
          this.paramData[this.paramData.length - 1]['show'] = 'true'
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },
    getInputJsonBody(value) {
      this.json_body = value
    },
    // 发送请求
    async sendClick() {
      // 请求头参数转换
      const req_header = []
      for (var i = 0; i < this.headerData.length; i++) {
        const head = {
          name: this.headerData[i].name,
          value: this.headerData[i].value
        }
        req_header.push(head)
      }
      if (this.apiInfoForm.request_params.length === 0) {
        this.apiForm.params_type = 'json'
      } else {
        this.apiForm.params_type = 'params'
      }
      // 入参进行转换
      const req = {
        method: this.apiInfoForm.method.toLocaleLowerCase(),
        url: this.apiInfoForm.url,
        header: req_header,
        params_type: this.apiForm.params_type,
        params_body: this.apiForm.params_type === 'params' ? JSON.stringify(this.paramData) : JSON.stringify(this.json_body)
      }
      console.info('req:', req)
      const resp = await debugApi(req)
      if (resp.success === true) {
        this.$message.success('请求成功')
        this.apiForm.response = JSON.parse(resp.result.response)
      } else {
        if (resp.error.code === '10044') {
          this.$message.error(resp.error.message)
        }
        console.log(resp)
      }
    },
    // 接口断言
    async assertClick() {
      const req = {
        response: JSON.stringify(this.apiForm.response),
        assert_type: this.apiForm.assert_type,
        assert_text: this.apiForm.assert_text
      }
      const resp = await assertApi(req)
      if (resp.success === true) {
        this.$message.success('断言成功')
      } else {
        this.$message.error('断言失败')
      }
    },
    // 保存用例
    async saveTestCase() {
      // 请求头参数转换
      const req_header = this.dictHeaderData()
      const req_params = this.dictParamsData()
      if (this.apiForm.params_type !== 'json') {
        this.apiForm.params_body = req_params
      } else {
        this.apiForm.params_body = this.json_body
      }
      this.apiForm.extract_list = this.extractList
      this.apiForm.header = req_header
      this.apiForm.response = JSON.stringify(this.apiForm.response)
      const resp = await createApi(this.apiForm)
      if (resp.success === true) {
        this.$message.success('保存成功')
        this.saveFlag = true
        // 延时器
        setTimeout(() => {
          this.$emit('close')
          this.$emit('refresh')
        }, 500)
      } else {
        this.$message.error('保存失败')
      }
    },
    // 更新用例
    async updateTestCase() {
      // 请求头参数转换
      const req_header = this.dictHeaderData()
      const req_params = this.dictParamsData()
      if (this.apiForm.params_type !== 'json') {
        this.apiForm.params_body = req_params
      }
      this.apiForm.extract_list = this.extractList
      this.apiForm.header = req_header
      this.apiForm.response = JSON.stringify(this.apiForm.response)
      const resp = await updateApi(this.cid, this.apiForm)
      if (resp.success === true) {
        this.$message.success('更新成功')
        this.saveFlag = true
        // 延时器
        setTimeout(() => {
          this.$emit('close')
          this.$emit('refresh')
        }, 500)
      } else {
        this.$message.error('更新失败')
      }
    },
    // 添加提取规则
    addExtract() {
      this.extractList.push({ name: '', value: '' })
      console.info(this.extractList)
    },
    // 删除提取规则
    removeExtract(index) {
      this.extractList.splice(index, 1)
    },
    // 校验提取规则
    async checkExtract() {
      if (this.extractList.length === 0) {
        this.$message.error('请添加提取器')
        return
      }
      const req = {
        response: this.apiForm.response,
        extractList: this.extractList
      }
      console.info('断言请求：', req)
      const resp = await checkExtract(req)
      if (resp.success === true) {
        this.$message.success('提取器校验成功')
      } else {
        this.$message.error(resp.error.message)
      }
    },
    // 关闭
    closeDialog() {
      this.$emit('close')
    },
    dictHeaderData() {
      const req_header = []
      for (var i = 0; i < this.headerData.length; i++) {
        const head = {
          key: this.headerData[i].key,
          value: this.headerData[i].value
        }
        req_header.push(head)
      }
      return req_header
    },
    dictParamsData() {
      const req_params = []
      for (var i = 0; i < this.paramData.length; i++) {
        const param = {
          key: this.paramData[i].key,
          value: this.paramData[i].value
        }
        req_params.push(param)
      }
      return req_params
    }
  }
}
</script>

<style>
div.jsoneditor {
  border: thin solid #ced4da;
}
div.jsoneditor-menu {
  display: none;
}
.ace-jsoneditor .ace_gutter {
  background: white;
}
div.jsoneditor-outer.has-main-menu-bar {
  margin-top: 0px;
  padding-top: 0px;
}
.per-label {
  margin-right: 10px;
  margin-bottom: 4px;
  font-size: 1rem;
}
</style>

<style scoped>
.debug-button {
  float: right;
  margin-right: 20px;
}
.div-line {
  height: auto;
  width: 100%;
  text-align: left;
  margin-bottom: 10px;
}
.title-text {
  font-family: "Lucida Calligraphy", cursive, serif, sans-serif;
  font-size: 18px;
  font-weight: bolder;
}
</style>
