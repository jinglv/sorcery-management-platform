<template>
  <div class="test-suite">
    <div class="filter-container">
      <el-row :gutter="24">
        <el-col :span="6">
          <div class="demo-input-suffix">
            用例集名称:
            <el-input v-model="suiteFrom.name" placeholder="请输入用例集名称" style="width: 70%;margin-right: 5px;" class="filter-item" />
          </div>
        </el-col>
        <el-col :span="6">
          <div class="demo-input-suffix">
            需求版本号:
            <el-input v-model="suiteFrom.name" placeholder="请输入需求版本号" style="width: 70%;margin-right: 5px;" class="filter-item" />
          </div>
        </el-col>
        <el-col :span="6">
          <div class="demo-input-suffix">
            执行状态:
            <el-select
              v-model="statusValue"
              placeholder="请选择用例集执行状态"
              @change="changeStatusValue"
            >
              <el-option
                v-for="item in statusOption"
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
        <el-button class="filter-item" type="primary" icon="el-icon-search" @click="getSuiteList()">搜索</el-button>
      </div>
    </div>
    <div style="text-align: left; margin-top: 10px;">
      <el-button class="el-icon-circle-plus-outline" type="primary" @click="createTestSuite()">创建用例集</el-button>
    </div>
    <div style="margin-top: 10px">
      <el-table
        :data="testSuiteData"
        border
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="用例集名称" width="auto" />
        <el-table-column prop="version_number" label="需求版本号" width="auto" />
        <el-table-column prop="case_number" label="用例数量" width="auto" />
        <el-table-column prop="status" label="执行状态" width="180">
          <template slot-scope="{ row }">
            <el-tag :type="testSuiteStatusType(row.status)" effect="dark">
              {{ row.status | testSuiteStatus }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="auto" />
        <el-table-column fixed="right" label="操作">
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="showTestSuite(scope.row)"
            >执行</el-button>
            <el-button
              type="text"
              @click="showTestSuite(scope.row)"
            >查看</el-button>
            <el-button
              type="text"
              @click="editTestSuite(scope.row)"
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
    <!-- 创建测试用例集 -->
    <test-suite-dialog
      v-if="dialogFlag"
      :title="testSuiteTitle"
      :sid="currentSuiteId"
      @cancel="closeDialog"
    />
  </div>
</template>
<script>
import TestSuiteDialog from '@/components/Cases/testSuiteDialog'
import { getSuiteList } from '@/api/cases'

export default {
  name: 'CaseSuite',
  components: {
    TestSuiteDialog
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
    }
  },
  data() {
    return {
      testSuiteTitle: 'create',
      dialogFlag: false,
      testSuiteData: [],
      suiteFrom: {
        'name': '',
        'version_number': '',
        'status': 0
      },
      req: {
        page: 1,
        size: 10
      },
      // 分页页数
      total: 10,
      statusValue: '',
      statusLabel: '',
      statusOption: [
        {
          value: 1,
          label: '未执行'
        },
        {
          value: 2,
          label: '执行中'
        },
        {
          value: 3,
          label: '已执行'
        }
      ],
      currentSuiteId: 0
    }
  },
  mounted() {
    this.getSuiteList()
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
    changeStatusValue(value) {
      this.statusValue = value
      this.statusLabel = this.statusOption.find(
        (item) => item.value === value
      ).label
      this.suiteFrom.status = value
    },
    // 创建用例集
    createTestSuite() {
      this.dialogFlag = true
      this.testSuiteTitle = 'create'
    },
    closeDialog() {
      this.dialogFlag = false
      this.getSuiteList()
    },
    showTestSuite(row) {
      this.currentSuiteId = row.id
      this.dialogFlag = true
      this.testSuiteTitle = 'detail'
    },
    editTestSuite(row) {
      this.currentSuiteId = row.id
      this.dialogFlag = true
      this.testSuiteTitle = 'edit'
    },
    // 获取测试用例集列表
    async getSuiteList() {
      const resp = await getSuiteList(this.req, JSON.stringify(this.suiteFrom))
      if (resp.success === true) {
        this.total = resp.total
        for (let i = 0; i < resp.items.length; i++) {
          resp.items[i].create_time = this.$moment(
            resp.items[i].create_time
          ).format('YYYY-MM-DD HH:mm:ss')
        }
        this.testSuiteData = resp.items
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
      this.statusValue = ''
      this.suiteFrom.status = 0
      this.suiteFrom.name = ''
      this.suiteFrom.version_number = ''
      this.getSuiteList()
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
