<template>
  <div :style="{'max-height': timeLineHeight +'px'}" style="margin-left: 10px; margin-right: 10px; overflow-y:scroll;">
    <el-form
      ref="ruleForm"
      :model="suiteFrom"
      label-width="180px"
      class="demo-ruleForm"
    >
      <el-form-item label="HttpRunner项目：">
        <el-select
          v-model="suiteFrom.httprunner_project_id"
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
      <el-form-item label="测试用例集名称：" prop="name">
        <el-input v-model="suiteFrom.name" placeholder="请输入测试用例集名称" />
      </el-form-item>
      <el-tabs v-model="activeName">
        <el-tab-pane label="测试用例" name="first" prop="testSteps">
          <div style="height: 600px; overflow-y: auto;">
            <el-table :data="testCaseList">
              <el-table-column>
                <template slot-scope="scope">
                  <el-form label-width="120px">
                    <div class="container">
                      <span class="label-text">TestCase: {{ scope.$index + 1 }}</span>
                      <el-button
                        v-if="scope.row.show === 'true'"
                        type="success"
                        class="btn"
                        icon="el-icon-circle-plus-outline"
                        size="mini"
                        style="margin-right: 50px;"
                        plain
                        @click="addTestCase(scope.$index)"
                      />
                      <el-button
                        class="btn"
                        type="danger"
                        size="mini"
                        icon="el-icon-delete"
                        plain
                        @click="removeTestCase(scope.$index)"
                      />
                    </div>
                    <div style="margin-top: 15px;">
                      <el-form-item label="测试步骤名称：" prop="name">
                        <el-input v-model="scope.row.name" placeholder="请输入测试用例名称" size="small" />
                      </el-form-item>
                      <el-form-item label="选择测试用例：" prop="case_id">
                        <el-select
                          v-model="scope.row.case_id"
                          placeholder="请选择HttpRunner项目下的测试用例"
                          size="small"
                          style="width: 100%;"
                        >
                          <el-option
                            v-for="i in casesOption"
                            :key="'api' + i.value"
                            :label="i.label"
                            :value="i.value"
                          />
                        </el-select>
                      </el-form-item>
                      <el-collapse>
                        <el-collapse-item title="其他内容">
                          <div style="height: 200px; overflow-y: auto;">
                            <el-form-item label="参数：" prop="extracts">
                              <el-button
                                type="primary"
                                size="mini"
                                icon="el-icon-plus"
                                plain
                                @click="addParams(scope)"
                              >添加</el-button>
                              <div v-for="(item, index) in scope.row.params" :key="index" style="margin-top: 5px;">
                                <el-col :span="6">
                                  <el-input
                                    v-model="item.name"
                                    placeholder="参数名"
                                    style="width: 200px"
                                  />
                                </el-col>
                                <el-col :span="7">
                                  <el-input
                                    v-model="item.value"
                                    placeholder="参数值"
                                    style="width: 100%"
                                  />
                                </el-col>
                                <el-button
                                  type="text"
                                  style="padding-right: 10px"
                                  @click="removeParams(scope, index)"
                                >
                                  <i class="el-icon-remove-outline" />
                                </el-button>
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
      </el-tabs>
      <el-form-item style="text-align: right; margin-top: 20px;">
        <div class="dialog-footer">
          <el-button @click="closeDialog()">取消</el-button>
          <el-button v-if="title != '编辑测试用例集'" :loading="loading" type="primary" @click="createSuite()">保存</el-button>
          <el-button v-if="title == '编辑测试用例集'" :loading="loading" type="primary" @click="updateSuite()">更新</el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { httpRunnerProjectList, getHttpRunnerTestCaseIds, createHttpRunnerSuite, updateHttpRunnerSuite, httpRunnerSuiteDetail } from '@/api/httprunner'
import dictDialog from '@/components/Api/dictDialog'

export default {
  components: {
    dictDialog
  },
  props: {
    title: {
      type: String,
      default: null
    },
    sid: {
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
      testCaseList: [{
        name: '',
        case_id: '',
        params: [],
        variables: [],
        // 是否显示新增按钮
        show: 'true'
      }],
      apiValue: '',
      apiLabel: '',
      casesOption: [],
      suiteFrom: {
        name: '',
        httprunner_project_id: '',
        public_variables: '',
        test_cases: []
      },
      publicVariable: [{
        name: '',
        value: '',
        // 是否显示新增按钮
        show: 'true'
      }],
      params: [],
      variables: [],
      assertLabel: '',
      activeName: 'first',
      loading: false
    }
  },
  mounted() {
    // 窗口滑动
    this.timeLineHeight = document.documentElement.clientHeight - 150
    window.onresize = () => { this.timeLineHeight = document.documentElement.clientHeight - 150 }
    this.initHttpRunnerProjectList()
    if (this.title === '编辑测试用例集') {
      this.httpRunnerSuiteDetail()
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
      this.httpRunnerTestCaseIds(value)
    },
    async httpRunnerTestCaseIds(projectId) {
      const resp = await getHttpRunnerTestCaseIds(projectId)
      if (resp.success === true) {
        for (let i = 0; i < resp.result.length; i++) {
          this.casesOption.push({
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
    addTestCase(index) {
      const list = this.testCaseList
      list[index].show = 'false'
      list.push({
        name: '',
        case_id: '',
        params: [],
        variables: [],
        show: 'true'
      })
      this.testCaseList = list
    },
    addParams(scope) {
      scope.row.params.push({ name: '', value: '' })
    },
    removeParams(scope, index) {
      scope.row.params.splice(index, 1)
    },
    addVariables(scope) {
      scope.row.variables.push({ name: '', value: '' })
    },
    removeVariables(scope, index) {
      scope.row.variables.splice(index, 1)
    },
    removeTestCase(index) {
      const list = this.testCaseList
      if (index === 0 && list.length === 1) {
        list.splice(index, 1)
        list.push({
          name: '',
          case_id: '',
          params: [],
          variables: [],
          show: 'true'
        })
      } else {
        list.splice(index, 1)
      }
      if (index === list.length) {
        list[index - 1].show = 'true'
      }
      this.testCaseList = list
    },
    async createSuite() {
      const testCases = []
      for (let i = 0; i < this.testCaseList.length; i++) {
        const case_info = this.testCaseList[i]
        const case_dict = {
          'name': case_info.name,
          'case_id': case_info.case_id,
          'params': this.params_data_dict(case_info.params),
          'variables': this.list_to_dict(case_info.variables)
        }
        testCases.push(case_dict)
      }
      const public_variables_dict = this.list_to_dict(this.publicVariable)
      this.suiteFrom.public_variables = public_variables_dict
      this.suiteFrom.test_cases = testCases
      this.loading = true
      const resp = await createHttpRunnerSuite(this.suiteFrom)
      if (resp.success === true) {
        this.$message.success('创建成功！')
        this.loading = false
        this.closeDialog()
      } else {
        this.$message.error('创建失败！')
      }
    },
    async updateSuite() {
      const testCases = []
      for (let i = 0; i < this.testCaseList.length; i++) {
        const case_info = this.testCaseList[i]
        const case_dict = {
          'name': case_info.name,
          'case_id': case_info.case_id,
          'params': this.params_data_dict(case_info.params),
          'variables': this.list_to_dict(case_info.variables)
        }
        testCases.push(case_dict)
      }
      const public_variables_dict = this.list_to_dict(this.publicVariable)
      this.suiteFrom.public_variables = public_variables_dict
      this.suiteFrom.test_cases = testCases
      this.loading = true
      const resp = await updateHttpRunnerSuite(this.sid, this.suiteFrom)
      if (resp.success === true) {
        this.$message.success('更新成功！')
        this.loading = false
        this.closeDialog()
      } else {
        this.$message.error('更新失败！')
      }
    },
    async httpRunnerSuiteDetail() {
      const resp = await httpRunnerSuiteDetail(this.sid)
      if (resp.success === true) {
        this.suiteFrom = resp.result
        const config_content = JSON.parse(resp.result.config.replace(/'/g, '"'))
        if (Object.keys(config_content).length !== 0) {
          this.publicVariable = this.dict_to_list(config_content)
          this.publicVariable[this.publicVariable.length - 1]['show'] = 'true'
        }
        const testCasesResult = []
        const testCases = JSON.parse(this.suiteFrom.test_cases.replace(/'/g, '"'))
        for (let i = 0; i < testCases.length; i++) {
          if (testCases[i].params !== undefined) {
            this.params = this.params_data_list(testCases[i].params)
          }
          if (testCases.variables !== undefined) {
            this.variables = this.dict_to_list(testCases.variables)
          }
          testCasesResult.push({
            name: testCases[i].name,
            case_id: testCases[i].case_id,
            params: this.params,
            variables: this.variables
          })
        }
        this.testCaseList = testCasesResult
        this.testCaseList[this.testCaseList.length - 1]['show'] = 'true'
        this.httpRunnerTestCaseIds(resp.result.httprunner_project_id)
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
    dict_to_list(dic) {
      if (dic !== undefined) {
        const result = Object.entries(dic).map(([name, value]) => {
          return { 'name': name, 'value': value }
        })
        return result
      }
    },
    params_data_dict(lst) {
      const output = {}
      lst.forEach(item => {
        const name = item['name']
        const value = item['value']
        if (output[name]) {
          output[name].push(value)
        } else {
          output[name] = [value]
        }
      })
      return output
    },
    params_data_list(dic) {
      /**
       * 将数据 {"aa": 111, "bb": 222}转换为
       * [{"name": "aa", "value": 111}, {"name": "bb", "value": 222}]
       */
      const output = Object.entries(dic).flatMap(([name, values]) => {
        return values.map(value => ({ name, value }))
      })
      return output
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
