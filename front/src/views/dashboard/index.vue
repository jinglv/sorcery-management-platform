<template>
  <div class="dashboard-container">
    <el-row type="flex" class="row-bg" justify="space-between">
      <el-col :span="20">
        <span class="title">HttpRunner项目统计</span>
        <div style="margin-top: 5px;">
          <el-table
            :data="statisticsData"
            height="250"
            border
            style="width: 90%"
          >
            <el-table-column
              prop="project_name"
              label="项目名称"
              width="200"
            />
            <el-table-column
              prop="apis_count"
              label="Apis总数"
              width="150"
            />
            <el-table-column
              prop="test_cases_count"
              label="TestCase总数"
              width="150"
            />
            <el-table-column
              prop="test_suite_count"
              label="TestSuite总数"
            />
          </el-table>
        </div>
      </el-col>
      <el-col :span="20">
        <div style="margin-top: 5px;">
          <div id="cahrts-hr" style="width: 100%;height: 250px;" />
        </div>
      </el-col>
    </el-row>
    <el-row type="flex" class="row-bg" justify="space-between">
      <el-col :span="20">
        <span class="title">项目统计</span>
        <div style="margin-top: 5px;">
          <el-table
            :data="statisticsData"
            height="250"
            border
            style="width: 90%"
          >
            <el-table-column
              prop="project_name"
              label="项目名称"
              width="200"
            />
            <el-table-column
              prop="apis_count"
              label="Apis总数"
              width="150"
            />
            <el-table-column
              prop="test_cases_count"
              label="TestCase总数"
              width="150"
            />
            <el-table-column
              prop="test_suite_count"
              label="TestSuite总数"
            />
          </el-table>
        </div>
      </el-col>
      <el-col :span="20">
        <div style="margin-top: 5px;">
          <span class="title">测试执行统计</span>
          <el-table
            :data="statisticsData"
            height="250"
            border
            style="width: 90%"
          >
            <el-table-column
              prop="project_name"
              label="项目名称"
              width="180"
            />
            <el-table-column
              prop="apis_count"
              label="Apis总数"
              width="120"
            />
            <el-table-column
              prop="test_cases_count"
              label="TestCase总数"
              width="120"
            />
            <el-table-column
              prop="test_suite_count"
              label="TestSuite总数"
            />
          </el-table>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getStatisticsList, getStatisticsTotal } from '@/api/commons'

export default {
  name: 'Dashboard',
  data() {
    return {
      statisticsData: []
    }
  },
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  mounted() {
    this.initStatisticsList()
    this.statisticsTotal()
  },
  methods: {
    async initStatisticsList() {
      const resp = await getStatisticsList()
      if (resp.success === true) {
        this.statisticsData = resp.result
        // this.$message.success("查询成功！")
      } else {
        this.$message.error('查询失败！')
      }
    },
    async statisticsTotal() {
      const resp = await getStatisticsTotal()
      if (resp.success === true) {
        const result = resp.result
        const cahrtsHrData = Object.entries(result).map(([name, value]) => ({ value, name }))
        this.totalStatistics(cahrtsHrData)
      } else {
        this.$message.error('查询失败！')
      }
    },
    totalStatistics(cahrtsHrData) {
      // 基于准备好的dom，初始化echarts实例
      var chartDom = document.getElementById('cahrts-hr')
      // 绘制图标
      var myChart = this.$echarts.init(chartDom)
      var option
      option = {
        title: { // 组件标题
          text: 'HttpRunner总数统计',
          subtext: 'Fake Data',
          left: 'center'
        },
        tooltip: { // 提示组件
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '总数',
            type: 'pie',
            radius: '50%',
            data: cahrtsHrData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      option && myChart.setOption(option)
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}

.dashboard-backgroud {
  text-align: center;
}
.el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
  }
.title {
  font-family: "Lucida Calligraphy", cursive, serif, sans-serif;
  font-size: 20px;
  font-weight: bolder;
}
</style>
