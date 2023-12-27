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
        :model="testSuiteSearchForm"
        label-width="120px"
        class="demo-ruleForm"
      >
        <el-form-item label="用例集名称：" prop="name">{{ testSuiteSearchForm.name }}</el-form-item>
        <el-form-item label="执行状态：" prop="status">
          <el-tag :type="testSuiteStatusType(testSuiteSearchForm.status)" effect="dark">
            {{ testSuiteSearchForm.status | testSuiteStatus }}
          </el-tag>
        </el-form-item>
        <el-form-item label="需求版本号" prop="version_number">
          <el-table
            size="mini"
            :data="testSuiteSearchForm.version_info"
            border
            style="width: 100%"
          >
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
          </el-table>
        </el-form-item>
        <el-form-item label="测试用例：" prop="test_cases">
          <el-table
            size="mini"
            :data="testSuiteSearchForm.test_cases"
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
              label="用例名称"
              width="auto"
              show-overflow-tooltip
            />
            <el-table-column
              prop="project_name"
              label="项目名称"
              width="auto"
              show-overflow-tooltip
            />
            <el-table-column
              prop="module_name"
              label="模块名称"
              width="auto"
              show-overflow-tooltip
            />
            <el-table-column
              prop="type"
              label="测试用例类型"
              width="200"
            >
              <template slot-scope="{ row }">
                {{ row.type | caseType }}
              </template>
            </el-table-column>
            <el-table-column
              prop="test_label"
              label="用例标签"
              width="180"
              show-overflow-tooltip
            >
              <template slot-scope="{ row }">
                {{ row.test_label | testLabel }}
              </template>
            </el-table-column>
            <el-table-column
              prop="importance"
              label="重要程度"
              width="180"
              show-overflow-tooltip
            >
              <template slot-scope="{ row }">
                <el-tag :type="caseImportanceType(row.importance)" effect="plain">
                  {{ row.importance | caseImportance }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-form-item>
        <el-form-item label="描述：" prop="describe">
          <div class="w-e-text" style="height: 100px; overflow-y: auto;" v-html="testSuiteSearchForm.describe" />
        </el-form-item>
        <el-form-item style="text-align: right">
          <el-button @click="closeDialog">返回</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-if="title != 'detail'">
      <el-form
        ref="ruleForm"
        :model="testSuiteForm"
        :rules="rules"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="用例集名称" prop="name">
          <el-input v-model="testSuiteForm.name" />
        </el-form-item>
        <el-form-item label="需求版本" prop="version_number">
          <div id="version_number">
            <el-table
              size="mini"
              :data="versionNumberData"
              border
              style="width: 100%"
            >
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
          <el-button type="primary" size="small" round :disabled="addDemandFlag" @click="addDemand()">添加需求</el-button>
        </el-form-item>
        <el-form-item label="测试用例" prop="test_steps">
          <div id="test-step">
            <el-table
              size="mini"
              :data="testCaseData"
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
                label="用例名称"
                width="auto"
                show-overflow-tooltip
              />
              <el-table-column
                prop="project_name"
                label="项目名称"
                width="auto"
                show-overflow-tooltip
              />
              <el-table-column
                prop="module_name"
                label="模块名称"
                width="auto"
                show-overflow-tooltip
              />
              <el-table-column
                prop="type"
                label="测试用例类型"
                width="200"
              >
                <template slot-scope="{ row }">
                  {{ row.type | caseType }}
                </template>
              </el-table-column>
              <el-table-column
                prop="test_label"
                label="用例标签"
                width="180"
                show-overflow-tooltip
              >
                <template slot-scope="{ row }">
                  {{ row.test_label | testLabel }}
                </template>
              </el-table-column>
              <el-table-column
                prop="importance"
                label="重要程度"
                width="180"
                show-overflow-tooltip
              >
                <template slot-scope="{ row }">
                  <el-tag :type="caseImportanceType(row.importance)" effect="plain">
                    {{ row.importance | caseImportance }}
                  </el-tag>
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
                    @click="deleteTestCase(scope.$index)"
                  />
                </template>
              </el-table-column>
            </el-table>
          </div>
          <el-button type="primary" size="small" plain @click="addTestCase()">添加测试用例</el-button>
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
      <demand-list-dialog v-if="dialogDemandFlag" @getDemandInfo="getDemandInfo" @cancel="closeDemandDialog" />
      <demand-detail-dialog v-if="dialogDemandDetailFlag" :title="demandDetailTitle" :did="currentDemandId" @cancel="closeDemandDialog" />
      <test-case-list-dialog v-if="testCaseListDialogFlag" @getTestCaseData="getTestCaseData" @cancel="closeDemandDialog" />
    </div>
  </el-dialog>
</template>

<script>
import { createCaseSuite, updateTestCase, getCaseSuiteDetail } from '@/api/cases'
import { getToken } from '@/utils/auth'
import DemandListDialog from '@/components/Cases/demandListDialog'
import DemandDetailDialog from '@/components/Cases/demandDetailDialog'
import TestCaseListDialog from '@/components/Cases/testCaseListDialog'
import E from 'wangeditor'
import hljs from 'highlight.js'

export default {
  name: 'TestSuiteDialog',
  components: {
    DemandListDialog,
    DemandDetailDialog,
    TestCaseListDialog
  },
  filters: {
    testSuiteStatus(value) {
      if (value === 1) {
        return '未执行'
      } else if (value === 2) {
        return '执行中'
      } else if (value === 3) {
        return '已完成'
      } else {
        return ''
      }
    },
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
    sid: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      showTitle: '',
      dialogVisible: true,
      testSuiteForm: {
        name: '',
        version_number: '',
        case_ids: [],
        describe: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入用例集名称', trigger: 'blur' }
        ]
      },
      testSuiteSearchForm: {},
      testCaseData: [],
      addDemandFlag: false,
      versionNumberData: [],
      fileList: [],
      disabled: false,
      editor_remark: null,
      testCaseListDialogFlag: false,
      dialogDemandFlag: false,
      currentDemandId: 0,
      demandDetailTitle: '',
      dialogDemandDetailFlag: false
    }
  },
  created() {
    if (this.title === 'detail') {
      this.showTitle = '测试用例集详情'
      this.getTestCaseSuiteDetail()
    } else {
      this.showTitle = '创建测试用例集'
      // 组件打开则进行加载
      // 使用时钟函数进行延迟，否则获取不到元素 -- 等元素加载完成后再进行创建E
      this.$nextTick(() => {
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
        this.showTitle = '编辑测试用例集'
        this.getTestCaseSuiteDetail()
      }
    }
  },
  mounted() {
  },
  methods: {
    testSuiteStatusType(value) {
      if (value === 1) {
        return 'warning'
      } else if (value === 2) {
        return 'info'
      } else if (value === 3) {
        return 'success'
      } else {
        return ''
      }
    },
    caseImportanceType(value) {
      if (value === 1) {
        return 'danger'
      } else if (value === 2) {
        return 'warning'
      } else if (value === 3) {
        return 'info'
      } else if (value === 4) {
        return 'success'
      } else {
        return ''
      }
    },
    closeDialog() {
      this.$emit('cancel', {})
      if (this.title !== 'detail') {
        this.editor_remark.destroy()
        this.editor_remark = null
      }
    },
    // 添加测试用例步骤
    addTestCase() {
      this.testCaseListDialogFlag = true
    },
    deleteTestCase(index) {
      this.testCaseData.splice(index, 1)
    },
    // 添加需求
    addDemand() {
      this.dialogDemandFlag = true
    },
    closeDemandDialog() {
      this.dialogDemandFlag = false
      this.dialogDemandDetailFlag = false
      this.testCaseListDialogFlag = false
    },
    getDemandInfo(data) {
      this.versionNumberData.push(data)
      this.testSuiteForm.version_number = data.version_number
      this.addDemandFlag = true
    },
    showDemand(row) {
      this.dialogDemandDetailFlag = true
      this.demandDetailTitle = '需求详情'
      this.currentDemandId = row.id
    },
    deleteDemand(index) {
      this.versionNumberData.splice(index, 1)
      this.addDemandFlag = false
    },
    getTestCaseData(data) {
      this.testCaseData.push(data)
      this.testSuiteForm.case_ids.push(data.id)
    },
    // 创建测试用例
    submitTestCase(formName) {
      this.$refs[formName].validate((valid) => {
        const remark_content = this.editor_remark.txt.html()
        this.testSuiteForm.describe = remark_content
        if (valid) {
          if (this.title === 'create') {
            createCaseSuite(this.testSuiteForm).then((resp) => {
              if (resp.success === true) {
                this.closeDialog()
                this.$message.success('创建成功！')
              } else {
                this.$message.error(resp.error.message)
              }
            })
          } else if (this.title === 'edit') {
            updateTestCase(this.sid, this.testSuiteForm).then((resp) => {
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
    async getTestCaseSuiteDetail() {
      const resp = await getCaseSuiteDetail(this.sid)
      if (resp.success === true) {
        const res = resp.result
        this.testSuiteSearchForm = res
        if (this.title === 'edit') {
          this.testSuiteForm = res
          this.versionNumberData = res.version_info
          this.testCaseData = res.test_cases
          // 设置富文本中获取的数据
          this.editor_remark.txt.html(res.describe)
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
