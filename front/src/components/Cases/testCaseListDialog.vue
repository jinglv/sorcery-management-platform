<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="70%"
    :before-close="closeDialog"
    :append-to-body="true"
  >
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
    <div style="margin-top: 10px">
      <el-table
        :data="testCaseData"
        border
        style="width: 100%"
        @cell-click="selectTestCase"
      >
        <el-table-column prop="id" label="用例ID" width="80" />
        <el-table-column prop="name" label="用例名称" width="auto" />
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
        <el-table-column prop="create_time" label="创建时间" />
      </el-table>
    </div>
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
  </el-dialog>
</template>

<script>
import { projectList } from '@/api/projects'
import { getCasesList } from '@/api/cases'
import { getModuleTree } from '@/api/modules'

export default {
  name: 'ApiInfoList',
  components: { },
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
    }
  },
  props: {},
  data() {
    return {
      showTitle: '测试用例列表',
      dialogVisible: true,
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
      drawer: false
    }
  },
  mounted() {
    this.initProjectList()
    this.getCasesList()
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
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
      this.typeValue = 0
      if (this.typeValue === 0) {
        this.typeValue = ''
      }
      this.importanceValue = 0
      if (this.importanceValue === 0) {
        this.importanceValue = ''
      }
      this.casesFrom.name = ''
      this.getCasesList()
    },
    selectTestCase(row) {
      const testCaseData = {
        id: row.id,
        name: row.name,
        project_name: row.project_name,
        module_name: row.module_name,
        type: row.type,
        test_label: row.test_label,
        importance: row.importance
      }
      this.$emit('getTestCaseData', testCaseData)
      this.closeDialog()
    }
  }
}
</script>
