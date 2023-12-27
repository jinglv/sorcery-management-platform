<template>
  <div :style="{'max-height': timeLineHeight +'px'}" style="margin-left: 10px; margin-right: 10px; overflow-y:scroll;">
    <el-form
      ref="ruleForm"
      :model="casesFrom"
      label-width="180px"
      class="demo-ruleForm"
    >
      <el-form-item label="HttpRunner项目：">
        <el-select
          v-model="casesFrom.httprunner_project_id"
          placeholder="请选择HttpRunner项目名称"
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
      <el-form-item label="测试用例名称：" prop="name">
        <el-input v-model="casesFrom.name" placeholder="请输入测试用例名称" />
      </el-form-item>
      <el-tabs v-model="activeName">
        <el-tab-pane label="测试步骤" name="first" prop="testSteps">
          <div style="height: 400px; overflow-y: auto;">
            <el-table :data="testStepList">
              <el-table-column>
                <template slot-scope="scope">
                  <el-form label-width="120px">
                    <div class="container">
                      <span class="label-text">Setp: {{ scope.$index + 1 }}</span>
                      <el-button
                        v-if="scope.row.show === 'true'"
                        type="success"
                        class="btn"
                        icon="el-icon-circle-plus-outline"
                        size="mini"
                        style="margin-right: 50px;"
                        plain
                        @click="addTestStep(scope.$index)"
                      />
                      <el-button
                        class="btn"
                        type="danger"
                        size="mini"
                        icon="el-icon-delete"
                        plain
                        @click="removeTestStep(scope.$index)"
                      />
                    </div>
                    <div style="margin-top: 15px;">
                      <el-form-item label="测试步骤名称：" prop="name">
                        <el-input v-model="scope.row.name" placeholder="请输入测试步骤名称" size="small" />
                      </el-form-item>
                      <el-form-item label="选择接口：" prop="api_id">
                        <el-select
                          v-model="scope.row.api_id"
                          placeholder="请选择HttpRunner项目下的接口"
                          size="small"
                          style="width: 100%;"
                        >
                          <el-option
                            v-for="i in apiOption"
                            :key="'api' + i.value"
                            :label="i.label"
                            :value="i.value"
                          />
                        </el-select>
                      </el-form-item>
                      <el-collapse>
                        <el-collapse-item title="其他内容">
                          <div style="height: 200px; overflow-y: auto;">
                            <el-form-item label="提取器：" prop="extracts">
                              <el-button
                                type="primary"
                                size="mini"
                                icon="el-icon-plus"
                                plain
                                @click="addExtracts(scope)"
                              >添加</el-button>
                              <div v-for="(item, index) in scope.row.extracts" :key="index" style="margin-top: 5px;">
                                <el-col :span="6">
                                  <el-input
                                    v-model="item.name"
                                    placeholder="变量名"
                                    style="width: 200px"
                                  />
                                </el-col>
                                <el-col :span="7">
                                  <el-input
                                    v-model="item.value"
                                    placeholder="提取规则"
                                    style="width: 100%"
                                  />
                                </el-col>
                                <el-button
                                  type="text"
                                  style="padding-right: 10px"
                                  @click="removeExtracts(scope, index)"
                                >
                                  <i class="el-icon-remove-outline" />
                                </el-button>
                              </div>
                            </el-form-item>
                            <el-form-item label="断言：" prop="validates">
                              <el-button
                                type="primary"
                                size="mini"
                                icon="el-icon-plus"
                                plain
                                @click="addValidates(scope)"
                              >添加</el-button>
                              <div v-for="(item, index) in scope.row.validates" :key="index" style="margin-top: 5px;">
                                <el-form-item>
                                  <el-col :span="4">
                                    <el-input
                                      v-model="item.assert_extract"
                                      placeholder="断言表达式"
                                      style="width: 100%"
                                    />
                                  </el-col>
                                  <el-col class="line" :span="3">
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
                                  <el-col :span="6">
                                    <el-input
                                      v-model="item.expect_text"
                                      placeholder="断言预期值"
                                      style="width: 100%"
                                    />
                                  </el-col>
                                  <el-button
                                    type="text"
                                    style="padding-right: 10px"
                                    @click="removeValidates(scope,index)"
                                  >
                                    <i class="el-icon-remove-outline" />
                                  </el-button>
                                </el-form-item>
                              </div>
                            </el-form-item>
                            <el-form-item label="变量：" prop="variables">
                              <el-button
                                type="primary"
                                size="mini"
                                icon="el-icon-plus"
                                plain
                                @click="addVariables(scope)"
                              >添加</el-button>
                              <div v-for="(item, index) in scope.row.variables" :key="index" style="margin-top: 5px;">
                                <el-col :span="6">
                                  <el-input
                                    v-model="item.name"
                                    placeholder="变量名"
                                    style="width: 200px"
                                  />
                                </el-col>
                                <el-col :span="7">
                                  <el-input
                                    v-model="item.value"
                                    placeholder="变量值"
                                    style="width: 100%"
                                  />
                                </el-col>
                                <el-button
                                  type="text"
                                  style="padding-right: 10px"
                                  @click="removeVariables(scope,index)"
                                >
                                  <i class="el-icon-remove-outline" />
                                </el-button>
                              </div>
                            </el-form-item>
                          </div>
                        </el-collapse-item>
                      </el-collapse>
                    </div>
                  </el-form>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
        <el-tab-pane label="公共变量" name="second" :lazy="true">
          <div style="height: 300px; overflow-y: auto;">
            <dict-dialog :dict-data="publicVariable" />
          </div>
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
          <el-button v-if="title != '编辑测试用例'" :loading="loading" type="primary" @click="createTestCase()">保存</el-button>
          <el-button v-if="title == '编辑测试用例'" :loading="loading" type="primary" @click="updateTestCase()">更新</el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { httpRunnerProjectList, run, getHttpRunnerApiIds, createHttpRunnerTestCase, httpRunnerTestCaseDetail, updateHttpRunnerTestCase } from '@/api/httprunner'
import aceCodeEditorDialog from '@/components/HttpRunner/aceCodeEditorDialog'
import dictDialog from '@/components/Api/dictDialog'

export default {
  components: {
    aceCodeEditorDialog,
    dictDialog
  },
  props: {
    title: {
      type: String,
      default: null
    },
    cid: {
      type: Number,
      default: 1
    }
  },
  data() {
    return {
      timeLineHeight: '',
      projectValue: '',
      projectLabel: '',
      projectOption: [],
      apiDetailInfo: {},
      testStepList: [{
        name: '',
        api_id: '',
        variables: [],
        extracts: [],
        validates: [],
        // 是否显示新增按钮
        show: 'true'
      }],
      apiValue: '',
      apiLabel: '',
      apiOption: [],
      casesFrom: {
        name: '',
        httprunner_project_id: '',
        public_variables: '',
        test_case_infos: [],
        pre_processor: '',
        post_processor: ''
      },
      publicVariable: [{
        name: '',
        value: '',
        // 是否显示新增按钮
        show: 'true'
      }],
      assertLabel: '',
      assertOption: [
        {
          value: 'contains',
          label: 'CONTAINS'
        },
        {
          value: 'eq',
          label: 'EQUAL'
        }
      ],
      variables: [],
      extracts: [],
      validates: [],
      activeName: 'first',
      language_python: 'python',
      pre_code: '',
      in_pre_code: '',
      post_code: '',
      in_post_code: '',
      result: '',
      loading: false
    }
  },
  mounted() {
    // 窗口滑动
    this.timeLineHeight = document.documentElement.clientHeight - 150
    window.onresize = () => { this.timeLineHeight = document.documentElement.clientHeight - 150 }
    this.initHttpRunnerProjectList()
    if (this.title === '编辑测试用例') {
      this.httpRunnerTestCaseDetail()
    }
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
    },
    async initHttpRunnerProjectList() {
      const resp = await httpRunnerProjectList(this.req)
      if (resp.success === true) {
        for (let i = 0; i < resp.items.length; i++) {
          this.projectOption.push({
            value: resp.items[i].id,
            label: resp.items[i].name
          })
        }
        this.total = resp.total
        // this.$message.success('查询成功！')
      } else {
        this.$message.error('查询失败！')
      }
    },
    changeProject(value) {
      this.projectValue = value
      this.projectLabel = this.projectOption.find(
        (item) => item.value === value
      ).label
      this.httpRunnerApiIds(value)
    },
    async httpRunnerApiIds(projectId) {
      const resp = await getHttpRunnerApiIds(projectId)
      if (resp.success === true) {
        for (let i = 0; i < resp.result.length; i++) {
          this.apiOption.push({
            value: resp.result[i].id,
            label: resp.result[i].name
          })
        }
        // this.$message.success('查询成功！')
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 添加测试步骤
    addTestStep(index) {
      const list = this.testStepList
      list[index].show = 'false'
      list.push({
        name: '',
        api_id: '',
        variables: [],
        extracts: [],
        validates: [],
        show: 'true'
      })
      this.testStepList = list
    },
    addExtracts(scope) {
      scope.row.extracts.push({ name: '', value: '' })
    },
    removeExtracts(scope, index) {
      scope.row.extracts.splice(index, 1)
    },
    addValidates(scope) {
      scope.row.validates.push({ assert_type: '', assert_extract: '', expect_text: '' })
    },
    changeAssert(value) {
      this.assert_type = value
      this.assertLabel = this.assertOption.find(
        (item) => item.value === value
      ).label
    },
    removeValidates(scope, index) {
      scope.row.validates.splice(index, 1)
    },
    addVariables(scope) {
      scope.row.variables.push({ name: '', value: '' })
    },
    removeVariables(scope, index) {
      scope.row.variables.splice(index, 1)
    },
    removeTestStep(index) {
      const list = this.testStepList
      if (index === 0 && list.length === 1) {
        list.splice(index, 1)
        list.push({
          name: '',
          api_id: '',
          variables: [],
          extracts: [],
          validates: [],
          show: 'true'
        })
      } else {
        list.splice(index, 1)
      }
      if (index === list.length) {
        list[index - 1].show = 'true'
      }
      this.testStepList = list
    },
    getPreCode(code) {
      this.in_pre_code = code
    },
    getPostCode(code) {
      this.in_post_code = code
    },
    async createTestCase() {
      const testSteps = []
      for (let i = 0; i < this.testStepList.length; i++) {
        const step = this.testStepList[i]
        const step_dict = {
          'name': step.name,
          'api_id': step.api_id,
          'variables': this.list_to_dict(step.variables),
          'extracts': this.list_to_dict(step.extracts),
          'validates': step.validates.map(item => {
            const assertType = item.assert_type
            const assertExtract = item.assert_extract
            const expectText = item.expect_text
            return { [assertType]: [assertExtract, expectText] }
          })
        }
        testSteps.push(step_dict)
      }
      const public_variables_dict = this.list_to_dict(this.publicVariable)
      this.casesFrom.public_variables = public_variables_dict
      this.casesFrom.test_case_infos = testSteps
      this.casesFrom.pre_processor = this.in_pre_code
      this.casesFrom.post_processor = this.in_post_code
      this.loading = true
      const resp = await createHttpRunnerTestCase(this.casesFrom)
      if (resp.success === true) {
        this.$message.success('创建成功！')
        this.loading = false
        this.closeDialog()
      } else {
        this.$message.error('创建失败！')
      }
    },
    async updateTestCase() {
      const testSteps = []
      for (let i = 0; i < this.testStepList.length; i++) {
        const step = this.testStepList[i]
        const step_dict = {
          'name': step.name,
          'api_id': step.api_id,
          'variables': this.list_to_dict(step.variables),
          'extracts': this.list_to_dict(step.extracts),
          'validates': step.validates.map(item => {
            const assertType = item.assert_type
            const assertExtract = item.assert_extract
            const expectText = item.expect_text
            return { [assertType]: [assertExtract, expectText] }
          })
        }
        testSteps.push(step_dict)
      }
      const public_variables_dict = this.list_to_dict(this.publicVariable)
      this.casesFrom.public_variables = public_variables_dict
      this.casesFrom.test_case_infos = testSteps
      this.casesFrom.pre_processor = this.in_pre_code
      this.casesFrom.post_processor = this.in_post_code
      this.loading = true
      const resp = await updateHttpRunnerTestCase(this.cid, this.casesFrom)
      if (resp.success === true) {
        this.$message.success('更新成功！')
        this.loading = false
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
    },
    async httpRunnerTestCaseDetail() {
      const resp = await httpRunnerTestCaseDetail(this.cid)
      if (resp.success === true) {
        this.casesFrom = resp.result
        if (Object.keys(this.casesFrom.config).length !== 0) {
          this.publicVariable = this.dict_to_list(resp.result.config)
          this.publicVariable[this.publicVariable.length - 1]['show'] = 'true'
        }
        const testStepsResult = []
        const testSteps = JSON.parse(this.casesFrom.teststeps.replace(/'/g, '"'))
        for (let i = 0; i < testSteps.length; i++) {
          if (testSteps[i].variables !== undefined) {
            this.variables = this.dict_to_list(testSteps[i].variables)
          }
          if (testSteps[i].extracts !== undefined) {
            this.extracts = this.dict_to_list(testSteps[i].extracts)
          }
          if (testSteps[i].validates !== undefined) {
            this.validates = this.data_list(testSteps[i].validates)
          }
          testStepsResult.push({
            name: testSteps[i].name,
            api_id: testSteps[i].api_id,
            variables: this.variables,
            extracts: this.extracts,
            validates: this.validates
          })
        }
        this.testStepList = testStepsResult
        this.testStepList[this.testStepList.length - 1]['show'] = 'true'
        this.pre_code = resp.result.pre_processor
        this.post_code = resp.result.post_processor
        this.httpRunnerApiIds(resp.result.httprunner_project_id)
        // this.$message.success('查询成功！')
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 列表转换字典
    list_to_dict(lst) {
      if (lst !== undefined) {
        const dict = {}
        for (let i = 0; i < lst.length; i++) {
          const item = lst[i]
          if (item.name === '' && item.value === '') {
            return dict
          }
          dict[item.name] = item.value
        }
        return dict
      }
    },
    // 字典转换列表
    dict_to_list(dit) {
      if (dit !== undefined) {
        const result = Object.entries(dit).map(([name, value]) => {
          return { 'name': name, 'value': value }
        })
        return result
      }
    },
    // 断言列表数据处理
    data_list(lst) {
      if (lst !== undefined) {
        const output = lst.map(item => {
          const assertType = Object.keys(item)[0] // 获取键名，如 "eq"
          const [assertExtract, expectText] = item[assertType] // 获取键值数组，如 ["content.msgCode", "SUCCESS"]
          return { assert_type: assertType, assert_extract: assertExtract, expect_text: expectText }
        })
        return output
      }
    }
  }
}
</script>
<style scoped>
#image {
  text-align: left;
}
.container {
  position: relative;
}
.btn {
  position: absolute;
  right: 0;
}
.label-text {
  font-family: "Lucida Calligraphy", cursive, serif, sans-serif;
  font-size: 20px;
  font-weight: bolder;
  margin-top: 5px;
}
</style>
