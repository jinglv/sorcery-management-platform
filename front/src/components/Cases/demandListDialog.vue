<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="900px"
    :before-close="closeDialog"
    :append-to-body="true"
  >
    <div class="filter-container">
      <el-row :gutter="24">
        <el-col :span="8">
          <div class="demo-input-suffix">
            需求名称:
            <el-input v-model="demandSearchFrom.name" size="mini" placeholder="请输入需求名称" style="width: 70%;margin-right: 5px;" class="filter-item" />
          </div>
        </el-col>
        <el-col :span="8">
          <div class="demo-input-suffix">
            版本号:
            <el-input v-model="demandSearchFrom.version_number" size="mini" placeholder="请输入版本号" style="width: 70%;margin-right: 5px;" class="filter-item" />
          </div>
        </el-col>
      </el-row>
      <div style="text-align: right;margin-top: 10px;">
        <el-button class="filter-item" size="mini" icon="el-icon-delete" @click="clearSearch()">重置</el-button>
        <el-button class="filter-item" size="mini" type="primary" icon="el-icon-search" @click="getAllApisList()">搜索</el-button>
      </div>
    </div>
    <el-table
      :data="demandData"
      border
      style="width: 100%;margin-top: 10px;"
      @cell-click="selectDemand"
    >
      <el-table-column label="ID" type="index" width="80" />
      <el-table-column prop="name" label="需求名称" width="180" />
      <el-table-column prop="project.name" label="项目" idth="250" />
      <el-table-column prop="version_number" label="版本号" width="100" />
      <el-table-column prop="requirements_type" label="需求类型" width="100">
        <template slot-scope="{ row }">
          {{ row.requirements_type | requirementsType }}
        </template>
      </el-table-column>
      <el-table-column prop="create_time" label="创建时间" width="200" />
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
  </el-dialog>
</template>

<script>
import { getDemandList } from '@/api/cases'

export default {
  name: 'DemandList',
  components: { },
  filters: {
    requirementsType(value) {
      if (value === 'business') {
        return '业务类需求'
      } else if (value === 'improve') {
        return '改进类需求'
      } else if (value === 'technical') {
        return '技术类需求'
      } else {
        return '未知类型'
      }
    }
  },
  props: {},
  data() {
    return {
      showTitle: '需求列表',
      dialogVisible: true,
      demandData: [],
      demandSearchFrom: {
        'name': '',
        'project_id': 0,
        'version_number': '',
        'requirements_type': '',
        'create_time': ''
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
    this.getDemandList()
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
    },
    // 获取需求列表
    async getDemandList() {
      const resp = await getDemandList(this.req, JSON.stringify(this.demandSearchFrom))
      if (resp.success === true) {
        this.total = resp.total
        for (let i = 0; i < resp.items.length; i++) {
          resp.items[i].create_time = this.$moment(
            resp.items[i].create_time
          ).format('YYYY-MM-DD HH:mm:ss')
        }
        this.demandData = resp.items
        this.$message.success('查询成功！')
      } else {
        this.$message.error('查询失败！')
      }
    },
    selectDemand(row) {
      const demandInfo = {
        id: row.id,
        name: row.name,
        project_name: row.project.name,
        version_number: row.version_number,
        requirements_type: row.requirements_type
      }
      this.$emit('getDemandInfo', demandInfo)
      this.closeDialog()
    },
    // 跳转到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.req.page = val
      this.getDemandList()
    },
    clearSearch() {
      this.demandSearchFrom.name = ''
      this.demandSearchFrom.version_number = ''
      this.getDemandList()
    }
  }
}
</script>
