<template>
  <div class="test-case">
    <div class="filter-container">
      <el-row :gutter="24">
        <el-col :span="6">
          <div class="demo-input-suffix">
            用例名称:
            <el-input v-model="casesFrom.name" placeholder="请输入用例名称" style="width: 70%;margin-right: 5px;" class="filter-item" />
          </div>
        </el-col>
        <el-col :span="6">
          <div class="demo-input-suffix">
            项目名称:
            <el-select
              v-model="projectValue"
              placeholder="请选择用例类型"
              @change="changeProject"
            >
              <el-option
                v-for="item in projectOption"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="demo-input-suffix">
            模块名称:
            <el-select
              ref="selectTree"
              v-model="moduleValue"
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
          </div>
        </el-col>
        <el-col :span="6">
          <div class="demo-input-suffix">
            用例类型:
            <el-select
              v-model="typeValue"
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
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="24" style="margin-top: 15px;">
        <el-col :span="6">
          <div class="demo-input-suffix">
            用例标签:
            <el-select
              v-model="testLableValue"
              placeholder="请选择用例标签"
              @change="changeTestLable"
            >
              <el-option
                v-for="item in testLableOption"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="demo-input-suffix">
            重要程度:
            <el-select
              v-model="importanceValue"
              placeholder="请选择重要程度"
              @change="changeImportance"
            >
              <el-option
                v-for="item in importanceOption"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>
        </el-col>
      </el-row>
      <div style="text-align: right;margin-top: 10px;">
        <el-button class="filter-item" icon="el-icon-delete" @click="clearSearch()">重置</el-button>
        <el-button class="filter-item" type="primary" icon="el-icon-search" @click="getCasesList()">搜索</el-button>
      </div>
    </div>
    <div style="text-align: left; margin-top: 10px;">
      <el-button class="el-icon-circle-plus-outline" type="primary" @click="createTestCase()">创建测试用例</el-button>
    </div>
    <div style="margin-top: 10px">
      <el-table
        :data="testCaseData"
        border
        style="width: 100%"
      >
        <el-table-column prop="id" label="用例ID" width="80" />
        <el-table-column prop="name" label="用例名称" width="auto" show-overflow-tooltip />
        <el-table-column prop="project_name" label="项目名称" width="auto" />
        <el-table-column prop="module_name" label="模块名称" width="auto" />
        <el-table-column prop="type" label="测试用例类型" width="auto">
          <template slot-scope="{ row }">
            {{ row.type | caseType }}
          </template>
        </el-table-column>
        <el-table-column prop="test_label" label="用例标签" width="auto">
          <template slot-scope="{ row }">
            {{ row.test_label | testLabel }}
          </template>
        </el-table-column>
        <el-table-column prop="importance" label="重要程度" width="auto">
          <template slot-scope="{ row }">
            <el-tag :type="caseImportanceType(row.importance)" effect="plain">
              {{ row.importance | caseImportance }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="auto" />
        <el-table-column fixed="right" label="操作">
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="showTestCase(scope.row)"
            >查看</el-button>
            <el-button
              type="text"
              @click="editTestCase(scope.row)"
            >编辑</el-button>
            <el-button
              type="text"
              @click="deleteTestCase(scope.row)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!--分页-->
      <div style="width: 100%; text-align: right">
        <el-pagination
          background
          :total="total"
          :page-size="req.size"
          layout="total, prev, pager, next"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
    <!-- 创建测试用例 -->
    <test-cases-dialog
      v-if="dialogFlag"
      :title="testCaseTitle"
      :case="currentTestCaseId"
      @cancel="closeDialog"
    />
  </div>
</template>
<script>
import TestCasesDialog from '@/components/Cases/testCasesDialog'
import { projectList } from '@/api/projects'
import { getCasesList } from '@/api/cases'
import { getModuleTree } from '@/api/modules'

export default {
  name: 'CaseManage',
  components: {
    TestCasesDialog
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
    testCaseStatus(value) {
      if (value === 1) {
        return '未执行'
      } else if (value === 2) {
        return '执行中'
      } else if (value === 3) {
        return '已完成'
      } else {
        return '未知状态'
      }
    },
    resultStatus(value) {
      if (value === 1) {
        return '失败'
      } else if (value === 2) {
        return '通过'
      } else {
        return '未知状态'
      }
    }
  },
  data() {
    return {
      testCaseTitle: 'create',
      dialogFlag: false,
      testCaseData: [],
      expandOnClickNode: true,
      treeProps: {
        children: 'children',
        label: 'label'
      },
      moduleValue: null,
      moduleData: [],
      projectValue: '',
      projectLabel: '',
      projectOption: [],
      casesFrom: {
        'name': '',
        'project_id': 0,
        'module_id': 0,
        'type': 0,
        'test_label': 0,
        'importance': 0,
        'priority': 0
      },
      req: {
        page: 1,
        size: 10
      },
      // 分页页数
      total: 10,
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
      currentTestCaseId: 0
    }
  },
  mounted() {
    this.initProjectList()
    // this.initModuleAllList()
    this.getCasesList()
  },
  methods: {
    testCaseStatusType(value) {
      if (value === 1) {
        return 'danger'
      } else if (value === 2) {
        return 'info'
      } else if (value === 3) {
        return 'success'
      } else {
        return ''
      }
    },
    resultStatusType(value) {
      if (value === 1) {
        return 'danger'
      } else if (value === 2) {
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
    // 创建用例集
    createTestCase() {
      this.dialogFlag = true
      this.testCaseTitle = 'create'
    },
    showTestCase(row) {
      this.currentTestCaseId = row.id
      this.dialogFlag = true
      this.testCaseTitle = 'detail'
    },
    editTestCase(row) {
      this.currentTestCaseId = row.id
      this.dialogFlag = true
      this.testCaseTitle = 'edit'
    },
    closeDialog() {
      this.dialogFlag = false
      this.getCasesList()
    },
    // 初始化项目列表
    async initProjectList() {
      const req_body = {
        'name': ''
      }
      const resp = await projectList(this.req, req_body)
      if (resp.success === true) {
        // this.projectValue = resp.items[0].id
        // this.projectLabel = resp.items[0].name
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
    // 修改选中项目
    changeProject(value) {
      console.log('change project -->', value)
      this.projectValue = value
      this.projectLabel = this.projectOption.find(
        (item) => item.value === value
      ).label
      console.log('选中项目名称', this.projectLabel)
      this.initModuleList(value)
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
    // 获取测试用例列表
    async getCasesList() {
      const resp = await getCasesList(this.req, JSON.stringify(this.casesFrom))
      if (resp.success === true) {
        this.total = resp.total
        for (let i = 0; i < resp.items.length; i++) {
          resp.items[i].create_time = this.$moment(
            resp.items[i].create_time
          ).format('YYYY-MM-DD HH:mm:ss')
        }
        this.testCaseData = resp.items
        this.$message.success('查询成功！')
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 跳转到第几页
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`)
      this.req.page = val
      this.getCasesList()
    },
    // 清除搜索
    clearSearch() {
      this.projectValue = ''
      this.casesFrom.project_id = 0

      this.moduleValue = ''
      this.casesFrom.module_id = 0

      this.typeValue = ''
      this.casesFrom.type = 0

      this.testLableValue = ''
      this.casesFrom.test_label = 0

      this.importanceValue = ''
      this.casesFrom.importance = 0

      this.casesFrom.name = ''
      this.getCasesList()
    },
    // 点击节点的响应
    handleNodeClick(node) {
      this.moduleValue = node.label
      this.$refs.selectTree.blur()
      this.casesFrom.module_id = node.id
      console.log(node.label)
    },
    // 获取选中的用例类型
    changeType(value) {
      this.typeValue = value
      this.typeLabel = this.typeOption.find(
        (item) => item.value === value
      ).label
      this.casesFrom.type = value
    },
    changeImportance(value) {
      this.importanceValue = value
      this.importanceLabel = this.importanceOption.find(
        (item) => item.value === value
      ).label
      this.casesFrom.importance = value
    },
    changeTestLable(value) {
      this.testLableValue = value
      this.testLableLabel = this.testLableOption.find(
        (item) => item.value === value
      ).label
      this.casesFrom.test_label = value
    }
  }
}
</script>
<style scoped>
.custom-tree-node {
  width: 100%;
}
.label-title {
  font-family: "Liberation Mono", monospace, serif, sans-serif;
  font-size: 24px;
}
.label-text {
  font-family: "Lucida Calligraphy", cursive, serif, sans-serif;
  font-size: 20px;
  font-weight: bolder;
  float: left;
  margin-top: 5px;
}
.flex-container {
  display: flex;
}

.el-container {
  text-align: center;
  line-height: 38px;
}
</style>
