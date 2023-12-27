<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="80%"
    :before-close="closeDialog"
    :close-on-click-modal="false"
  >
    <div v-if="title == 'detail'" class="div-line">
      <el-form
        ref="ruleForm"
        :model="testCaseForm"
        label-width="120px"
        class="demo-ruleForm"
      >
        <el-col>
          <el-form-item label="用例名称：" prop="name">{{ testCaseForm.name }}</el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="项目名称：" prop="project_name">{{ testCaseForm.project_name }}</el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="模块名称：" prop="module_name">{{ testCaseForm.module_name }}</el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="标签：" prop="test_label">
            {{ testCaseForm.test_label | testLabel }}
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="用例类型：" prop="type">
            {{ testCaseForm.type | caseType }}
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="重要程度：" prop="importance">
            {{ testCaseForm.importance | caseImportance }}
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="优先级：" prop="priority">
            {{ testCaseForm.priority | priorityType }}
          </el-form-item>
        </el-col>
        <el-form-item label="前置条件：" prop="precondition">
          <div class="w-e-text" style="height: 100px; overflow-y: auto;" v-html="testCaseForm.precondition" />
        </el-form-item>
        <el-form-item label="测试用例步骤：" prop="test_steps">
          <el-table
            :data="testCaseForm.test_steps"
            border
            style="width: 100%"
          >
            <el-table-column
              type="index"
              label="ID"
              width="80"
            />
            <el-table-column
              prop="test_step"
              label="测试步骤描述"
              width="auto"
            />
            <el-table-column
              prop="test_data"
              label="测试数据"
              width="auto"
            />
            <el-table-column
              prop="expected_result"
              label="预期结果"
              width="auto"
            />
            <el-table-column
              prop="api_name"
              label="接口名称"
              width="auto"
            >
              <template slot-scope="scope">
                <el-link type="primary" @click="showApiDetail(scope.row)">{{ scope.row.api_name }}</el-link>
              </template>
            </el-table-column>
            <el-table-column
              prop="remark"
              label="备注"
            />
          </el-table>
        </el-form-item>
        <el-form-item label="需求版本信息：" prop="version_info">
          <el-table
            :data="testCaseForm.version_info"
            border
            style="width: 100%"
          >
            <el-table-column
              label="ID"
              type="index"
              width="80"
            />
            <el-table-column
              prop="name"
              label="需求名称"
              width="auto"
            />
            <el-table-column
              prop="project_name"
              label="项目名称"
              width="auto"
            />
            <el-table-column
              prop="version_number"
              label="版本号"
              width="auto"
            />
            <el-table-column
              prop="requirements_type"
              label="需求类型"
            >
              <template slot-scope="{ row }">
                {{ row.requirements_type | requirementsType }}
              </template>
            </el-table-column>
            <el-table-column
              prop="option"
              label="操作"
              fixed="right"
              width="150"
            >
              <template slot-scope="scope">
                <el-button
                  type="primary"
                  size="mini"
                  icon="el-icon-view"
                  @click="showDemand(scope.row)"
                />
              </template>
            </el-table-column>
          </el-table>
        </el-form-item>
        <el-form-item label="备注：" prop="remark">
          <div class="w-e-text" style="height: 100px; overflow-y: auto;" v-html="testCaseForm.remark" />
        </el-form-item>
        <el-form-item style="text-align: right">
          <el-button @click="closeDialog">返回</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-if="title != 'detail'">
      <el-form
        ref="ruleForm"
        :model="testCaseForm"
        :rules="rules"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="用例名称" prop="name">
          <el-input v-model="testCaseForm.name" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="项目" prop="project">
              <el-select
                v-model="projectValue"
                size="small"
                placeholder="请选择项目"
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
          </el-col>
          <el-col :span="6">
            <el-form-item label="模块" prop="module">
              <el-select
                ref="selectTree"
                v-model="moduleValue"
                size="small"
                class="main-select-tree"
                placeholder="请选择模块"
              >
                <el-option style="height: 100%; padding: 0;" value="" />
                <el-tree
                  ref="selectelTree"
                  class="main-select-el-tree"
                  :data="moduleData"
                  :props="treeProps"
                  :expand-on-click-node="expandOnClickNode"
                  highlight-current
                  default-expand-all
                  style="font-weight: normal;"
                  @node-click="handleNodeClick"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="标签" prop="test_label">
              <el-select
                v-model="testLableValue"
                size="small"
                placeholder="请选择测试标签"
                @change="changeTestLable"
              >
                <el-option
                  v-for="item in testLableOption"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="用例类型" prop="type">
              <el-select
                v-model="typeValue"
                size="small"
                placeholder="请选择用例类型"
                @change="changeType"
              >
                <el-option
                  v-for="item in typeOption"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="重要程度" prop="importance">
              <el-select
                v-model="importanceValue"
                size="small"
                placeholder="请选择用例重要程度"
                @change="changeImportance"
              >
                <el-option
                  v-for="item in importanceOption"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="优先级" prop="priority">
              <el-select
                v-model="priorityValue"
                size="small"
                placeholder="请选择用例重要程度"
                @change="changePriority"
              >
                <el-option
                  v-for="item in priorityOption"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="前置条件" prop="precondition">
          <div id="editor_precondition" />
        </el-form-item>
        <el-form-item label="测试步骤" prop="test_steps">
          <div id="test-step">
            <el-table
              size="mini"
              :data="testStepData"
              border
              style="width: 100%"
            >
              <el-table-column
                label="#"
                type="index"
                width="50"
              />
              <el-table-column
                prop="test_step"
                label="步骤描述"
                width="auto"
                :style="{ 'width': '100%' }"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <el-input v-model="scope.row.test_step" type="textarea" :rows="1" placeholder="请输入测试用例步骤描述" />
                </template>
              </el-table-column>
              <el-table-column
                prop="test_data"
                label="测试数据"
                width="auto"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <el-input v-model="scope.row.test_data" type="textarea" :rows="1" placeholder="请输入测试用例测试数据" />
                </template>
              </el-table-column>
              <el-table-column
                prop="expected_result"
                label="预期结果"
                width="auto"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <el-input v-model="scope.row.expected_result" type="textarea" :rows="1" placeholder="请输入测试用例预期结果" />
                </template>
              </el-table-column>
              <el-table-column
                prop="api_id"
                label="接口"
                width="200"
              >
                <template slot-scope="scope">
                  <div class="cell-container">
                    <el-button v-if="scope.row.api_id === 0" type="text" size="mini" @click="selectApi(scope.$index)">查看接口</el-button>
                    <el-link v-else type="primary" @click="showApiDetail(scope.row)">{{ scope.row.api_name }}</el-link>
                    <el-button v-if="scope.row.api_id !== 0" type="danger" size="mini" class="el-icon-close custom-button" circle @click="clearApiId(scope.row)" />
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                prop="remark"
                label="备注"
                width="180"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <el-input v-model="scope.row.remark" type="textarea" :rows="1" placeholder="请输入备注信息" />
                </template>
              </el-table-column>
              <el-table-column
                prop="option"
                label="操作"
                fixed="right"
                width="100"
              >
                <template slot-scope="scope">
                  <el-button
                    type="danger"
                    size="mini"
                    icon="el-icon-delete"
                    :disabled="scope.row.isDelete"
                    @click="deleteTestSteps(scope.$index)"
                  />
                </template>
              </el-table-column>
            </el-table>
          </div>
          <el-button type="primary" size="small" plain @click="addTestSteps()">新增测试步骤</el-button>
        </el-form-item>
        <el-form-item label="关联需求" prop="version_number">
          <div id="version_number">
            <el-table
              size="mini"
              :data="versionNumberData"
              border
              style="width: 100%"
            >
              <el-table-column
                label="#"
                type="index"
                width="50"
              />
              <el-table-column
                prop="name"
                label="需求名称"
                width="auto"
              />
              <el-table-column
                prop="project_name"
                label="项目"
                width="auto"
              />
              <el-table-column
                prop="version_number"
                label="版本号"
                width="auto"
              />
              <el-table-column
                prop="requirements_type"
                label="需求类型"
                width="auto"
              >
                <template slot-scope="{ row }">
                  {{ row.requirements_type | requirementsType }}
                </template>
              </el-table-column>
              <el-table-column
                prop="option"
                label="操作"
                fixed="right"
                width="150"
              >
                <template slot-scope="scope">
                  <el-button
                    type="primary"
                    size="mini"
                    icon="el-icon-view"
                    :disabled="scope.row.isDelete"
                    @click="showDemand(scope.row)"
                  />
                  <el-button
                    type="danger"
                    size="mini"
                    icon="el-icon-delete"
                    :disabled="scope.row.isDelete"
                    @click="deleteDemand(scope.$index)"
                  />
                </template>
              </el-table-column>
            </el-table>
          </div>
          <el-button type="primary" size="small" round @click="addDemand()">添加需求</el-button>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <div id="editor_remark" />
        </el-form-item>
        <el-form-item style="text-align: right">
          <el-button @click="closeDialog">取消</el-button>
          <el-button
            v-if="title != 'edit'"
            type="primary"
            @click="submitTestCase('ruleForm')"
          >确定</el-button>
          <el-button
            v-if="title == 'edit'"
            type="primary"
            @click="submitTestCase('ruleForm')"
          >更新</el-button>
        </el-form-item>
      </el-form>
      <api-list-dialog v-if="dialogFlag" @getApiData="getApiData" @cancel="closeApiListDialog" />
      <demand-list-dialog v-if="dialogDemandFlag" @getDemandInfo="getDemandInfo" @cancel="closeDemandDialog" />
    </div>
    <el-drawer
      :title="apiDetailTitle"
      :visible.sync="drawer"
      direction="rtl"
      size="55%"
      :append-to-body="true"
    >
      <api-dialog v-if="drawer" :title="apiDetailTitle" :cid="currentApiId" @close="closeDrawer()" />
    </el-drawer>
    <demand-detail-dialog v-if="dialogDemandDetailFlag" :title="demandDetailTitle" :did="currentDemandId" @cancel="closeDemandDialog" />
  </el-dialog>
</template>

<script>
import { projectList } from '@/api/projects'
import { getModuleTree } from '@/api/modules'
import { createTestCase, getTestCasesDetail, updateTestCase } from '@/api/cases'
import { getToken } from '@/utils/auth'
import DemandListDialog from '@/components/Cases/demandListDialog'
import DemandDetailDialog from '@/components/Cases/demandDetailDialog'
import ApiListDialog from '@/components/Cases/apiListDialog'
import ApiDialog from '@/components/Api/apiDialog'
import E from 'wangeditor'
import hljs from 'highlight.js'

export default {
  name: 'DemandDialog',
  components: {
    ApiListDialog,
    ApiDialog,
    DemandListDialog,
    DemandDetailDialog
  },
  filters: {
    caseType(value) {
      if (value === 1) {
        return '功能测试用例'
      } else if (value === 2) {
        return '接口测试用例'
      } else {
        return '未知类型'
      }
    },
    testLabel(value) {
      if (value === 1) {
        return '正向场景测试用例'
      } else if (value === 2) {
        return '异常场景测试用例'
      } else {
        return ''
      }
    },
    caseImportance(value) {
      if (value === 1) {
        return 'P0'
      } else if (value === 2) {
        return 'P1'
      } else if (value === 3) {
        return 'P2'
      } else if (value === 4) {
        return 'P3'
      } else {
        return ''
      }
    },
    priorityType(value) {
      if (value === 1) {
        return '高'
      } else if (value === 2) {
        return '中'
      } else if (value === 3) {
        return '低'
      } else {
        return ''
      }
    },
    requirementsType(value) {
      if (value === 'business') {
        return '业务类需求'
      } else if (value === 'improve') {
        return 'Bug改进类需求'
      } else if (value === 'technical') {
        return '技术类需求'
      } else {
        return ''
      }
    }
  },
  props: {
    title: {
      type: String,
      default: null
    },
    case: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      showTitle: '',
      dialogVisible: true,
      testCaseForm: {
        name: '',
        version_number: [],
        project_id: '',
        module_id: 0,
        test_label: '',
        type: '',
        importance: '',
        priority: '',
        precondition: '',
        test_steps: [],
        remark: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入需求名称', trigger: 'blur' }
        ]
      },
      moduleValue: null,
      moduleData: [],
      expandOnClickNode: true,
      treeProps: {
        children: 'children',
        label: 'label'
      },
      projectValue: '',
      projectLabel: '',
      projectOption: [],
      testLableValue: '',
      testLableLabel: '',
      testLableOption: [
        {
          value: 1,
          label: '正向场景测试用例'
        },
        {
          value: 2,
          label: '异常场景测试用例'
        }
      ],
      typeValue: '',
      typeLabel: '',
      typeOption: [
        {
          value: 1,
          label: '功能测试用例'
        },
        {
          value: 2,
          label: '接口测试用例'
        }
      ],
      importanceValue: '',
      importanceLabel: '',
      importanceOption: [
        {
          value: 1,
          label: 'P0'
        },
        {
          value: 2,
          label: 'P1'
        },
        {
          value: 3,
          label: 'P2'
        },
        {
          value: 4,
          label: 'P3'
        }
      ],
      priorityValue: '',
      priorityLabel: '',
      priorityOption: [
        {
          value: 1,
          label: '高'
        },
        {
          value: 2,
          label: '中'
        },
        {
          value: 3,
          label: '低'
        }
      ],
      testStepData: [
        {
          test_step: '',
          test_data: '',
          expected_result: '',
          api_id: 0,
          api_name: '',
          remark: '',
          isDelete: true
        }
      ],
      currentIndex: 0,
      currentApiId: 0,
      apiDetailTitle: '',
      versionNumberData: [],
      versionNumbers: [],
      fileList: [],
      imageVisible: false,
      disabled: false,
      editor_precondition: null,
      editor_remark: null,
      editor_demand: null,
      dialogFlag: false,
      drawer: false,
      dialogDemandFlag: false,
      currentDemandId: 0,
      demandDetailTitle: '',
      dialogDemandDetailFlag: false
    }
  },
  created() {
    if (this.title === 'detail') {
      this.showTitle = '测试用例详情'
      this.getTestCaseDetail()
    } else {
      this.showTitle = '创建测试用例'
      // 组件打开则进行加载
      // 使用时钟函数进行延迟，否则获取不到元素 -- 等元素加载完成后再进行创建E
      this.$nextTick(() => {
        this.editor_precondition = new E('#editor_precondition')
        this.editor_precondition.highlight = hljs
        // 富文本组价设置图片上传接口
        this.editor_precondition.config.uploadImgServer = '/api/commons/editor/file/image'
        this.editor_precondition.config.uploadFileName = 'file'
        this.editor_precondition.config.uploadImgHeaders = {
          Authorization: 'Bearer ' + getToken()
        }
        // 富文本组价设置视频上传接口
        this.editor_precondition.config.uploadVideoServer = '/api/commons/editor/file/video'
        this.editor_precondition.config.uploadVideoName = 'file'
        this.editor_precondition.config.uploadVideoHeaders = {
          Authorization: 'Bearer ' + getToken()
        }
        // 创建
        this.editor_precondition.create()

        this.editor_remark = new E('#editor_remark')
        this.editor_remark.highlight = hljs
        // 富文本组价设置图片上传接口
        this.editor_remark.config.uploadImgServer = '/api/commons/editor/file/image'
        this.editor_remark.config.uploadFileName = 'file'
        this.editor_remark.config.uploadImgHeaders = {
          Authorization: 'Bearer ' + getToken()
        }
        // 富文本组价设置视频上传接口
        this.editor_remark.config.uploadVideoServer = '/api/commons/editor/file/video'
        this.editor_remark.config.uploadVideoName = 'file'
        this.editor_remark.config.uploadVideoHeaders = {
          Authorization: 'Bearer ' + getToken()
        }
        this.editor_remark.create()
      })
      if (this.title === 'edit') {
        this.showTitle = '编辑测试用例'
        this.getTestCaseDetail()
      }
    }
  },
  mounted() {
    this.initProjectList()
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
      if (this.title !== 'detail') {
        // 关闭弹窗，销毁E
        this.editor_precondition.destroy()
        this.editor_precondition = null

        this.editor_remark.destroy()
        this.editor_remark = null
      }
    },
    // 初始化项目列表
    async initProjectList() {
      const req_body = {
        'name': ''
      }
      const resp = await projectList(this.req, req_body)
      if (resp.success === true) {
        // 在初始化项目信息，同时初始化项目下的模块信息
        for (let i = 0; i < resp.items.length; i++) {
          this.projectOption.push({
            value: resp.items[i].id,
            label: resp.items[i].name
          })
        }
        // this.$message.success("查询成功！")
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 查询模块列表
    async initModuleList(pid) {
      const resp = await getModuleTree(pid)
      if (resp.success === true) {
        this.moduleData = resp.result
        // this.$message.success("查询成功！")
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 修改选中项目
    changeProject(value) {
      this.projectValue = value
      this.projectLabel = this.projectOption.find(
        (item) => item.value === value
      ).label
      this.testCaseForm.project_id = value
      this.initModuleList(value)
    },
    // 点击节点的响应
    handleNodeClick(node) {
      this.moduleValue = node.label
      this.$refs.selectTree.blur()
      this.testCaseForm.module_id = node.id
    },
    changeTestLable(value) {
      this.testLableValue = value
      this.testLableLabel = this.testLableOption.find(
        (item) => item.value === value
      ).label
      this.testCaseForm.test_label = value
    },
    changeType(value) {
      this.typeValue = value
      this.typeLabel = this.typeOption.find(
        (item) => item.value === value
      ).label
      this.testCaseForm.type = value
    },
    changeImportance(value) {
      this.importanceValue = value
      this.importanceLabel = this.importanceOption.find(
        (item) => item.value === value
      ).label
      this.testCaseForm.importance = value
    },
    changePriority(value) {
      this.priorityValue = value
      this.priorityLabel = this.priorityOption.find(
        (item) => item.value === value
      ).label
      this.testCaseForm.priority = value
    },
    // 添加测试用例步骤
    addTestSteps() {
      // 新添加，将原有的不可删除变更为可删除
      this.testStepData[0].isDelete = false
      const rowData = {
        test_step: '',
        test_data: '',
        expected_result: '',
        api_id: 0,
        api_name: '',
        remark: '',
        isDelete: false
      }
      this.testStepData.push(rowData)
    },
    deleteTestSteps(index) {
      this.testStepData.splice(index, 1)
      // 删除行，删除的只剩下1时，可删除变更为不可删除
      if (this.testStepData.length === 1) {
        this.testStepData[0].isDelete = true
      }
    },
    selectApi(index) {
      this.currentIndex = index
      this.dialogFlag = true
    },
    clearApiId(row) {
      row.api_id = 0
    },
    closeApiListDialog() {
      this.dialogFlag = false
    },
    getApiData(data) {
      const apiData = this.testStepData[this.currentIndex]
      apiData.api_id = data.id
      apiData.api_name = data.name
    },
    showApiDetail(row) {
      this.drawer = true
      this.currentApiId = row.api_id
      this.apiDetailTitle = '接口详情'
    },
    // 传递子组件，关闭抽屉
    closeDrawer() {
      this.drawer = false
    },
    // 添加需求
    addDemand() {
      this.dialogDemandFlag = true
    },
    closeDemandDialog() {
      this.dialogDemandFlag = false
      this.dialogDemandDetailFlag = false
    },
    getDemandInfo(data) {
      this.versionNumberData.push(data)
      this.versionNumbers.push(data.version_number)
    },
    showDemand(row) {
      this.dialogDemandDetailFlag = true
      this.demandDetailTitle = '需求详情'
      this.currentDemandId = row.id
    },
    deleteDemand(index) {
      this.versionNumberData.splice(index, 1)
    },
    // 创建测试用例
    submitTestCase(formName) {
      this.$refs[formName].validate((valid) => {
        this.testCaseForm.version_number = this.versionNumbers
        this.testCaseForm.test_steps = this.testStepData
        const pre_content = this.editor_precondition.txt.html()
        this.testCaseForm.precondition = pre_content
        const remark_content = this.editor_remark.txt.html()
        this.testCaseForm.remark = remark_content
        if (valid) {
          if (this.title === 'create') {
            createTestCase(this.testCaseForm).then((resp) => {
              if (resp.success === true) {
                this.closeDialog()
                this.$message.success('创建成功！')
              } else {
                this.$message.error(resp.error.message)
              }
            })
          } else if (this.title === 'edit') {
            updateTestCase(this.case, this.testCaseForm).then((resp) => {
              if (resp.success === true) {
                this.closeDialog()
                this.$message.success('更新成功！')
              } else {
                this.$message.error(resp.error.message)
              }
            })
          }
        }
      })
    },
    async getTestCaseDetail() {
      const resp = await getTestCasesDetail(this.case)
      if (resp.success === true) {
        const res = resp.result
        this.testCaseForm = res
        if (this.title === 'edit') {
          this.projectValue = res.project_id
          this.initModuleList(res.project_id)
          this.moduleValue = res.module_name
          this.testLableValue = res.test_label
          this.typeValue = res.type
          this.importanceValue = res.importance
          this.priorityValue = res.priority
          const resSteps = res.test_steps
          const steps = []
          for (let i = 0; i < resSteps.length; i++) {
            const stepDict = resSteps[i]
            stepDict['isDelete'] = false
            steps.push(stepDict)
          }
          this.currentApiId = res.api_id
          this.testStepData = steps
          this.versionNumberData = res.version_info
          this.currentDemandId = res.version_info.id
          this.versionNumbers = JSON.parse(res.version_number.replace(/'/g, '"'))
          // 设置富文本中获取的数据
          // 前置条件
          this.editor_precondition.txt.html(resp.result.precondition)
          this.editor_remark.txt.html(resp.result.remark)
        }
        this.$message.success('查询成功')
      } else {
        this.$message.error(resp.error.message)
      }
    }
  }
}
</script>
<style scoped>
#image {
  text-align: left;
}

#editor_precondition {
  border: 1px solid #ccc;
  z-index: 100; /* 按需定义 */
}

#editor_remark {
  border: 1px solid #ccc;
  z-index: 100; /* 按需定义 */
}

.cell-container {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.custom-button {
  margin-left: 10px; /* 设置按钮距离右边的间距 */
}

</style>
