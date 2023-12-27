<template>
  <div :style="{'max-height': timeLineHeight +'px'}" style="margin-left: 10px; margin-right: 10px; overflow-y:scroll;">
    <div v-if="title == '接口详情'" class="div-line">
      <el-form
        :model="apiForm"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="接口名称：" prop="name">{{ apiForm.name }}</el-form-item>
        <el-form-item label="接口地址：" prop="api_path">{{ apiForm.api_path }}</el-form-item>
        <el-form-item label="请求方式：" prop="method">{{ apiForm.method }}</el-form-item>
        <el-form-item label="请求头：" prop="header">
          <el-table
            :data="apiForm.header"
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
        <el-form-item label="请求参数：" prop="params_type">{{ apiForm.params_type }}</el-form-item>
        <el-form-item v-if="apiForm.params_type=='params' || apiForm.params_type=='form-data'" label="请求主体：" prop="params_body">
          <el-table
            :data="params"
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
        <el-form-item v-if="apiForm.params_type=='json'" label="请求主体：" prop="params_body">
          <json-viewer :value="apiForm.params_body" :expand-depth="3" />
        </el-form-item>
        <el-form-item label="响应主体：" prop="response">
          <json-viewer :value="apiForm.response" :expand-depth="3" />
        </el-form-item>
        <el-form-item label="断言：">
          <el-table
            :data="assertList"
            border
            style="width: 80%"
          >
            <el-table-column
              prop="name"
              label="名称"
              width="120"
            />
            <el-table-column
              prop="assert_extract"
              label="断言表达式"
              width="120"
            />
            <el-table-column
              prop="assert_type"
              label="断言类型"
              width="120"
            />
            <el-table-column
              prop="expect_text"
              label="断言预期值"
            />
          </el-table>
        </el-form-item>
        <el-form-item label="提取器：">
          <el-table
            :data="extractList"
            border
            style="width: 80%"
          >
            <el-table-column
              prop="name"
              label="名称"
              width="180"
            />
            <el-table-column
              prop="value"
              label="提取器表达式"
            />
          </el-table>
        </el-form-item>
        <el-form-item style="text-align: right">
          <el-button @click="closeDialog()">返回</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div v-if="title != '接口详情'">
      <div class="div-line" style="height: 50px">
        <el-select
          v-model="apiForm.method"
          placeholder="方法"
          style="width: 10%; float: left"
        >
          <el-option
            v-for="item in methodOption"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        <el-select
          v-model="evnValue"
          placeholder="请选执行择环境"
          style="width: 15%; float: left"
          @change="changeEnvs"
        >
          <el-option
            v-for="item in envsOption"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        <el-input
          v-model="apiForm.api_path"
          placeholder="API Path"
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
      <span class="title-text">Param/Body</span>
      <div class="div-line" style="margin-top: 10px;">
        <el-radio v-model="apiForm.params_type" label="params" @change="changeRadio">Params</el-radio>
        <el-radio v-model="apiForm.params_type" label="form" @change="changeRadio">Form-data</el-radio>
        <el-radio v-model="apiForm.params_type" label="json" @change="changeJsonRadio">JSON</el-radio>
      </div>
      <div v-show="bodyFlag" class="div-line" style="height: 220px; overflow-y: auto;">
        <ace-code-editor-dialog ref="ace" :value="apiForm.params_body" class="ace-editor" :min-lines="18" :mode-path="language" @getCode="getInputJsonBody" />
      </div>
      <div v-show="paramFlag" class="div-line" style="height: 220px; overflow-y: auto;">
        <dict-dialog :dict-data="paramData" />
      </div>
      <div class="div-line" style="height: 220px; overflow-y: auto;">
        <el-tabs>
          <el-tab-pane label="接口响应结果">
            <json-viewer :value="apiForm.response" :expand-depth="3" />
          </el-tab-pane>
        </el-tabs>
      </div>
      <div class="div-line" style="margin-top: 70px">
        <el-collapse>
          <el-collapse-item title="断言" name="1">
            <el-form :inline="true" label-width="60px">
              <div v-for="(item, index) in assertList" :key="index">
                <el-form-item>
                  <el-col :span="4">
                    <el-input
                      v-model="item.name"
                      placeholder="名称"
                      style="width: 200px"
                    />
                  </el-col>
                  <el-col :span="4" style="margin-left: 70px;">
                    <el-input
                      v-model="item.assert_extract"
                      placeholder="断言表达式"
                      style="width: 200px"
                    />
                  </el-col>
                  <el-col class="line" :span="3" style="margin-left: 70px;">
                    <el-select
                      v-model="item.assert_type"
                      placeholder="断言类型"
                      @change="changeAssert"
                    >
                      <el-option
                        v-for="i in assertOption"
                        :key="i.value"
                        :label="i.label"
                        :value="i.value"
                      />
                    </el-select>
                  </el-col>
                  <el-col :span="4" style="margin-left: 10px;">
                    <el-input
                      v-model="item.expect_text"
                      placeholder="断言预期值"
                      style="width: 100%"
                    />
                  </el-col>
                  <el-col class="line" :span="3">
                    <el-button
                      class="debug-button"
                      type="success"
                      plain
                      size="small"
                      @click="assertClick(item)"
                    >断言</el-button>
                  </el-col>
                  <el-button
                    type="text"
                    style="padding-right: 10px"
                    @click="removeAssert(index)"
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
              @click="addAssert()"
            >添加</el-button>
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
                  <el-col :span="8">
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
        <el-button
          v-if="title == '编辑接口'"
          type="primary"
          size="small"
          style="float: left"
          :disabled="saveFlag"
          @click="updateTestCase()"
        >更新</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import jsonViewer from 'vue-json-viewer'
import { debugApi, getApiDetail, assertApi, createApi, checkExtract, updateApi } from '@/api/apis'
import { envsListByProject, getEnvsInfo } from '@/api/envs'
import dictDialog from '@/components/Api/dictDialog'
import aceCodeEditorDialog from '@/components/HttpRunner/aceCodeEditorDialog'
export default {
  name: 'ApiDialog',
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
    mid: {
      type: Number,
      default: 1
    },
    pid: {
      type: Number,
      default: 1
    },
    cid: {
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
      envLabel: '',
      evnValue: '',
      envsOption: [],
      request_path: '',
      activeName: 'first',
      paramsType: 1,
      json: {},
      response: '',
      assertType: 'include',
      apiForm: {
        name: '',
        module_id: 0,
        api_path: '',
        method: 'get',
        header: [],
        params_type: 'params',
        params_body: '',
        response: '',
        assert_list: [],
        extract_list: [],
        extract_result_list: []
      },
      params: [],
      saveFlag: false,
      extractList: [],
      extractResultList: [],
      assertList: [],
      assertForm: {
        name: '',
        assert_type: '',
        assert_extract: '',
        expect_text: ''
      },
      assertLabel: '',
      assertOption: [
        {
          value: 'contains',
          label: 'CONTAINS'
        },
        {
          value: 'equal',
          label: 'EQUAL'
        }
      ],
      timeLineHeight: '',
      headerData: [{
        name: '',
        value: '',
        // 是否显示新增按钮
        show: 'true'
      }],
      paramData: [{
        name: '',
        value: '',
        // 是否显示新增按钮
        show: 'true'
      }],
      bodyFlag: false,
      paramFlag: true,
      language: 'json',
      json_body: ''
    }
  },
  mounted() {
    console.info('title:', this.title)
    // 窗口滑动
    this.timeLineHeight = document.documentElement.clientHeight - 150
    window.onresize = () => { this.timeLineHeight = document.documentElement.clientHeight - 150 }
    // 初始化数据
    this.apiForm.module_id = this.mid
    if (this.cid !== 0) {
      // 调用接口获取数据
      this.getApiInfo()
    }
    this.getEnvsList(this.pid)
  },
  methods: {
    // 获取一条用例信息
    async getApiInfo() {
      const resp = await getApiDetail(this.cid)
      if (resp.success === true) {
        // 接口获取数据
        this.apiForm = resp.result
        const header = resp.result.header.replace(/'/g, '"')
        const params_body = resp.result.params_body.replace(/'/g, '"')
        const response = resp.result.response.replace(/'/g, '"')
        // 将获取到的数据赋值给表单数据
        this.apiForm.header = JSON.parse(header)
        this.headerData = resp.result.header
        // 获取头信息后，添加，是否可展示信息
        this.headerData[this.headerData.length - 1]['show'] = 'true'
        if (resp.result.params_type === 'json') {
          this.apiForm.params_body = JSON.stringify(JSON.parse(params_body), null, 2)
          this.bodyFlag = true
          this.paramFlag = false
        } else {
          this.params = JSON.parse(params_body)
          this.apiForm.params_body = ''
          this.paramData = JSON.parse(params_body)
          this.paramData[this.paramData.length - 1]['show'] = 'true'
          this.bodyFlag = false
          this.paramFlag = true
        }
        this.apiForm.response = JSON.parse(response)
        this.extractList = resp.result.extract_list
        this.assertList = resp.result.assert_list
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
      // 入参进行转换
      const req = {
        method: this.apiForm.method,
        url: this.request_path + this.apiForm.api_path,
        header: req_header,
        params_type: this.apiForm.params_type,
        params_body: this.apiForm.params_type === 'params' ? JSON.stringify(this.paramData) : this.json_body
      }
      const resp = await debugApi(req)
      if (resp.success === true) {
        if (resp.result.response === 'Method not allowed') {
          this.$message.error('接口请求方法错误！')
        } else {
          this.apiForm.response = JSON.parse(resp.result.response)
        }
      } else {
        if (resp.error.code === '10044') {
          this.$message.error(resp.error.message)
        }
        console.log(resp)
      }
    },
    // 接口断言
    async assertClick(item) {
      const req = {
        response: this.apiForm.response,
        assert_type: item.assert_type,
        assert_extract: item.assert_extract,
        expect_text: item.expect_text
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
      this.apiForm.assert_list = this.assertList
      this.apiForm.extract_list = this.extractList
      this.apiForm.extract_result_list = this.extractResultList
      this.apiForm.header = req_header
      this.apiForm.response = JSON.stringify(this.apiForm.response)
      console.info('req:', this.apiForm)
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
      } else {
        this.apiForm.params_body = this.json_body
      }
      this.apiForm.assert_list = this.assertList
      this.apiForm.extract_list = this.extractList
      this.apiForm.extract_result_list = this.extractResultList
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
    },
    // 删除提取规则
    removeExtract(index) {
      this.extractList.splice(index, 1)
    },
    changeAssert(value) {
      this.assert_type = value
      this.assertLabel = this.assertOption.find(
        (item) => item.value === value
      ).label
    },
    // 添加提取规则
    addAssert() {
      this.assertList.push({ name: '', assert_type: '', assert_extract: '', expect_text: '' })
    },
    // 删除提取规则
    removeAssert(index) {
      this.assertList.splice(index, 1)
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
      const resp = await checkExtract(req)
      if (resp.success === true) {
        this.extractResultList = resp.result
        this.$message.success('提取器校验成功')
      } else {
        this.$message.error(resp.error.message)
      }
    },
    // 关闭
    closeDialog() {
      this.$emit('close')
    },
    // 根据pid获取环境变量
    async getEnvsList() {
      const resp = await envsListByProject(this.pid)
      if (resp.success === true) {
        for (let i = 0; i < resp.result.length; i++) {
          this.envsOption.push({
            value: resp.result[i].id,
            label: resp.result[i].name
          })
        }
        // this.$message.success("查询成功！")
      } else {
        this.$message.error('查询环境失败！')
      }
    },
    // 获取选中的环境的base_url
    async changeEnvs(value) {
      this.evnValue = value
      this.envLabel = this.envsOption.find(
        (item) => item.value === value
      ).label
      const resp = await getEnvsInfo(value)
      if (resp.success === true) {
        const res = resp.result
        this.request_path = res.protocol + res.base_url
        console.info('url:', this.request_path)
      } else {
        this.$message.error('查询环境信息失败！')
      }
    },
    changeJsonRadio() {
      this.bodyFlag = true
      this.paramFlag = false
    },
    changeRadio() {
      this.bodyFlag = false
      this.paramFlag = true
    },
    dictHeaderData() {
      const req_header = []
      for (var i = 0; i < this.headerData.length; i++) {
        const head = {
          name: this.headerData[i].name,
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
          name: this.paramData[i].name,
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
