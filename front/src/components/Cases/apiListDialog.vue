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
            接口名称:
            <el-input v-model="apiSearchFrom.name" size="mini" placeholder="请输入接口名称" style="width: 70%;margin-right: 5px;" class="filter-item" />
          </div>
        </el-col>
        <el-col :span="8">
          <div class="demo-input-suffix">
            接口地址:
            <el-input v-model="apiSearchFrom.api_path" size="mini" placeholder="请输入接口地址" style="width: 70%;margin-right: 5px;" class="filter-item" />
          </div>
        </el-col>
        <el-col :span="8">
          <div class="demo-input-suffix">
            请求方法:
            <el-input v-model="apiSearchFrom.method" size="mini" placeholder="请输入请求方法" style="width: 70%;margin-right: 5px;" class="filter-item" />
          </div>
        </el-col>
      </el-row>
      <div style="text-align: right;margin-top: 10px;">
        <el-button class="filter-item" size="mini" icon="el-icon-delete" @click="clearSearch()">重置</el-button>
        <el-button class="filter-item" size="mini" type="primary" icon="el-icon-search" @click="getAllApisList()">搜索</el-button>
      </div>
    </div>
    <el-table
      :data="apisData"
      border
      style="width: 100%;margin-top: 10px;"
      @cell-click="selectApi"
    >
      <el-table-column label="ID" type="index" width="80" />
      <el-table-column prop="name" label="接口名称" width="180" />
      <el-table-column prop="api_path" label="接口地址" idth="250" />
      <el-table-column prop="method" label="请求方式" width="100" />
      <el-table-column prop="module.name" label="所属模块" width="100" />
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
import { getAllApisList } from '@/api/apis'

export default {
  name: 'ApiInfoList',
  components: { },
  props: {},
  data() {
    return {
      showTitle: '接口列表',
      dialogVisible: true,
      apisData: [],
      apiSearchFrom: {
        name: '',
        api_path: '',
        method: ''
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
    this.getAllApisList()
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
    },
    // 获取模块下的测试用例列表
    async getAllApisList() {
      const resp = await getAllApisList(this.req, this.apiSearchFrom)
      if (resp.success === true) {
        this.total = resp.total
        for (let i = 0; i < resp.items.length; i++) {
          resp.items[i].create_time = this.$moment(
            resp.items[i].create_time
          ).format('YYYY-MM-DD HH:mm:ss')
        }
        this.apisData = resp.items
        this.$message.success('查询成功！')
      } else {
        this.$message.error('查询失败！')
      }
    },
    selectApi(row) {
      const apiData = {
        id: row.id,
        name: row.name
      }
      this.$emit('getApiData', apiData)
      this.closeDialog()
    },
    // 跳转到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.req.page = val
      this.getAllApisList()
    },
    clearSearch() {
      this.apiSearchFrom.name = ''
      this.apiSearchFrom.api_path = ''
      this.apiSearchFrom.method = ''
      this.getAllApisList()
    }
  }
}
</script>
