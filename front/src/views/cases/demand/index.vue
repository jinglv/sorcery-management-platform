<template>
  <div class="demand">
    <div class="filter-container">
      <el-row :gutter="24">
        <el-col :span="6">
          <div class="demo-input-suffix">
            需求名称:
            <el-input v-model="demandSearchFrom.name" placeholder="请输入需求名称" style="width: 64%;margin-right: 5px;" class="filter-item" />
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
            版本号:
            <el-input v-model="demandSearchFrom.version_number" placeholder="请输入版本号" style="width: 64%;margin-right: 5px;" class="filter-item" />
          </div>
        </el-col>
        <el-col :span="6">
          <div class="demo-input-suffix">
            需求类型:
            <el-select
              v-model="demandValue"
              placeholder="请选择需求类型"
              @change="demandType"
            >
              <el-option
                v-for="item in demandOption"
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
        <el-button class="filter-item" type="primary" icon="el-icon-search" @click="getDemandList()">搜索</el-button>
      </div>
    </div>
    <div style="text-align: left; margin-top: 10px;">
      <el-button class="el-icon-circle-plus-outline" type="primary" @click="createDemand()">创建需求</el-button>
    </div>
    <div style="margin-top: 10px">
      <el-table
        :data="demandDate"
        border
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="需求名称" width="auto" />
        <el-table-column prop="project.name" label="项目" width="auto" />
        <el-table-column prop="version_number" label="版本号" width="auto" />
        <el-table-column prop="requirements_type" label="需求类型" width="auto">
          <template slot-scope="{ row }">
            {{ row.requirements_type | requirementsType }}
          </template>
        </el-table-column>
        <el-table-column prop="requirements_detail" label="需求详情" width="auto">
          <template slot-scope="scope">
            <el-button
              type="text"
              size="small"
              @click="demandRowInfo(scope.row)"
            >显示详情内容</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="auto" />
        <el-table-column fixed="right" label="操作">
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="editDemandInfo(scope.row)"
            >编辑</el-button>
            <el-button
              type="text"
              @click="deleteDemandInfo(scope.row)"
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
    <!-- 创建需求 -->
    <demand-dialog
      v-if="dialogFlag"
      :title="demandTitle"
      :did="currentDemandId"
      @cancel="closeDialog"
    />
    <demand-detail-dialog v-if="dialogDemandDetailFlag" :title="demandDetailTitle" :did="currentDemandId" @cancel="closeDialog" />
  </div>
</template>
<script>
import { projectList } from '@/api/projects'
import { getDemandList, deleteDemand } from '@/api/cases'
import DemandDialog from '@/components/Cases/demandDialog'
import DemandDetailDialog from '@/components/Cases/demandDetailDialog'

export default {
  name: 'DemandManage',
  components: {
    DemandDialog,
    DemandDetailDialog
  },
  filters: {
    requirementsType(value) {
      if (value === 'business') {
        return '业务类需求'
      } else if (value === 'improve') {
        return 'Bug改进类需求'
      } else if (value === 'technical') {
        return '技术类需求'
      } else {
        return '未知类型'
      }
    }
  },
  data() {
    return {
      demandTitle: '',
      projectValue: '',
      projectLabel: '',
      projectOption: [],
      demandDate: [],
      dialogFlag: false,
      demandSearchFrom: {
        'name': '',
        'project_id': 0,
        'version_number': '',
        'requirements_type': '',
        'create_time': ''
      },
      demandValue: '',
      demandLabel: '',
      demandOption: [
        {
          value: 'business',
          label: '业务类需求'
        },
        {
          value: 'improve',
          label: '改进类需求'
        },
        {
          value: 'technical',
          label: '技术类需求'
        }
      ],
      currentDemandId: 0,
      dialogDemandDetailFlag: false,
      demandDetailTitle: '',
      req: {
        page: 1,
        size: 10
      },
      // 分页页数
      total: 10
    }
  },
  mounted() {
    this.initProjectList()
    this.getDemandList()
  },
  methods: {
    // 创建需求
    createDemand() {
      this.dialogFlag = true
      this.demandTitle = 'create'
    },
    demandType(value) {
      this.demandValue = value
      this.demandLabel = this.demandOption.find(
        (item) => item.value === value
      ).label
      this.demandSearchFrom.requirements_type = value
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
      this.demandSearchFrom.project_id = value
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
        this.demandDate = resp.items
        this.$message.success('查询成功！')
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 创建模块关闭
    closeDialog() {
      this.dialogFlag = false
      this.dialogDemandDetailFlag = false
      this.getDemandList()
    },
    // 跳转到第几页
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`)
      this.req.page = val
      // this.initProjectList()
    },
    // 清除搜索
    clearSearch() {
      this.demandSearchFrom.name = ''
      this.demandSearchFrom.version_number = ''
      this.demandSearchFrom.project_id = 0
      this.projectValue = ''
      this.demandSearchFrom.requirements_type = ''
      this.demandValue = ''
      this.getDemandList()
    },
    // 查看需求详情
    demandRowInfo(row) {
      // 点击用例，获取用例id
      this.currentDemandId = row.id
      this.dialogDemandDetailFlag = true
      this.demandDetailTitle = '需求详情'
    },
    // 编辑测试用例
    editDemandInfo(row) {
      // 点击用例，获取用例id
      this.currentDemandId = row.id
      this.dialogFlag = true
      this.demandTitle = 'edit'
    },
    // 删除需求信息
    deleteDemandInfo(row) {
      deleteDemand(row.id).then((resp) => {
        this.$confirm('删除任务, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          center: true
        }).then(() => {
          if (resp.success === true) {
            this.getDemandList()
          } else {
            this.$message.error(resp.error.msg)
          }
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
      })
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
