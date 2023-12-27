<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="1200px"
    :before-close="closeDialog"
  >
    <el-table
      :data="apisData"
      border
      style="width: 100%"
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="文件名称" width="180" />
      <el-table-column prop="url" label="接口URL" />
      <el-table-column prop="method" label="请求方式" width="100" />
      <el-table-column prop="create_time" label="创建时间" width="200" />
      <el-table-column fixed="right" label="操作" width="150">
        <template slot-scope="scope">
          <el-button
            type="text"
            @click="caseRowApiInfo(scope.row)"
          >查看</el-button>
          <el-button
            type="text"
            @click="caseRowApiSend(scope.row)"
          >发送</el-button>
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
    <el-drawer
      :title="apiTitle"
      :visible.sync="drawer"
      :modal="false"
      direction="rtl"
      size="50%"
    >
      <api-request-dialog v-if="drawer" :title="apiTitle" :aid="currentApiId" @close="closeDrawer()" />
    </el-drawer>
  </el-dialog>
</template>

<script>
import { apiInfoList } from '@/api/infos'
import apiRequestDialog from './apiRequestDialog.vue'

export default {
  name: 'ApiInfoList',
  components: { apiRequestDialog },
  props: {
    fn: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      showTitle: '',
      dialogVisible: true,
      apiTitle: '',
      currentApiId: 0,
      apisData: [],
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
    this.apiInfoList()
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
    },
    async apiInfoList() {
      const resp = await apiInfoList(this.req, this.fn)
      if (resp.success === true) {
        this.apisData = resp.items
        this.total = resp.total
      } else {
        this.$message.error(resp.error.message)
      }
    },
    // 查看用例详情
    caseRowApiInfo(row) {
      // 点击用例，获取用例id
      this.currentApiId = row.id
      this.drawer = true
      this.apiTitle = '接口详情'
    },
    // 编辑测试用例
    caseRowApiSend(row) {
      // 点击用例，获取用例id
      this.currentApiId = row.id
      this.drawer = true
      this.apiTitle = '发送接口'
    },
    // 传递子组件，关闭抽屉
    closeDrawer() {
      this.drawer = false
    },
    // 跳转到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.req.page = val
      this.getCaseList(this.currentModule)
    }
  }
}
</script>
