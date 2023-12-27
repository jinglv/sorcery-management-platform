<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="1200px"
    :before-close="closeDialog"
  >
    <div>
      <el-table :data="reaultData" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="报告名称" />
        <el-table-column prop="name" label="执行内容" />
        <el-table-column prop="type" label="类型" />
        <el-table-column prop="result" label="结果">
          <template slot-scope="{ row }">
            <el-tag :type="statusType(row.result)" effect="dark">
              {{ row.result }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" />
        <el-table-column fixed="right" label="操作" width="150">
          <template slot-scope="scope">
            <el-button
              type="text"
              size="small"
              @click="showReport(scope.row)"
            >查看报告</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div style="width: 100%; text-align: right">
      <el-pagination
        background
        layout="prev, pager, next"
        :page-size="req.size"
        :total="total"
        @current-change="handleCurrentChange"
      />
    </div>
  </el-dialog>
</template>

<script>
import { httpRunnerRunResult, httpRunnerRenderReportApi } from '@/api/httprunner'

export default {
  components: {},
  props: {
    type: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      showTitle: '查看执行结果',
      dialogVisible: true,
      reaultData: [],
      req: {
        page: 1,
        size: 5
      },
      // 分页页数
      total: 5
    }
  },
  mounted() {
    this.initHttpRunnerRunResultList()
  },
  methods: {
    statusType(value) {
      if (value === 'fail') {
        return 'danger'
      } else if (value === 'non') {
        return 'info'
      } else if (value === 'error') {
        return 'warning'
      } else if (value === 'success') {
        return 'success'
      } else {
        return '未知状态'
      }
    },
    closeDialog() {
      this.$emit('cancel', {})
    },
    async initHttpRunnerRunResultList() {
      const resp = await httpRunnerRunResult(this.req, this.type)
      if (resp.success === true) {
        if (this.type !== 'API') {
          const ids = []
          for (let i = 0; i < resp.items.length; i++) {
            if (resp.items[i].ids.length > 1) {
              ids.push(resp.items[i])
            }
          }
          console.info('ids:', ids)
          this.reaultData = ids
          this.total = ids.length
        } else {
          this.reaultData = resp.items
          this.total = resp.total
        }
        for (let i = 0; i < resp.items.length; i++) {
          resp.items[i].create_time = this.$moment(
            resp.items[i].create_time
          ).format('YYYY-MM-DD HH:mm:ss')
        }
        // this.$message.success('查询成功！')
      } else {
        this.$message.error('查询失败！')
      }
    },
    async showReport(row) {
      const reportContent = await httpRunnerRenderReportApi(row.name)
      // 保存进localStorage
      window.localStorage.removeItem('callbackHTML')
      window.localStorage.setItem('callbackHTML', reportContent)
      // 读取本地保存的html数据，使用新窗口打开
      const newWin = window.open('_', '_blank')
      newWin.document.write(localStorage.getItem('callbackHTML'))
      // 关闭输出流
      newWin.document.close()
    },
    // 跳转到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.req.page = val
      this.initHttpRunnerRunResultList()
    }
  }
}
</script>
<style scoped>
#image {
  text-align: left;
}
</style>
