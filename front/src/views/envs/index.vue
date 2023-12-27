<template>
  <div class="evns">
    <div class="filter-container">
      <el-row :gutter="24">
        <el-col :span="6">
          <div class="demo-input-suffix">
            项目名称:
            <el-select
              v-model="projectValue"
              placeholder="请选择项目"
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
            环境名称:
            <el-input v-model="envsFrom.name" placeholder="请输入环境名称" style="width: 60%;margin-right: 5px;" class="filter-item" />
          </div>
        </el-col>
        <el-col :span="6">
          <div class="demo-input-suffix">
            环境标识:
            <el-input v-model="envsFrom.env" placeholder="请输入环境标识" style="width: 60%;margin-right: 5px;" class="filter-item" />
          </div>
        </el-col>
        <el-col :span="6">
          <div class="demo-input-suffix">
            请求协议:
            <el-select
              v-model="httpValue"
              placeholder="请选择协议"
              @change="changeProtocol"
            >
              <el-option
                v-for="item in httpOption"
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
        <el-button class="filter-item" type="primary" icon="el-icon-search" @click="initEnvsList()">搜索</el-button>
      </div>
    </div>
    <div class="envs-create" style="margin-top: 10px;">
      <el-button class="filter-item" type="primary" icon="el-icon-circle-plus-outline" @click="createEnv()">创建</el-button>
    </div>
    <div class="envs-list" style="margin-top: 10px;">
      <el-table
        :data="envsData"
        border
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="环境名称" width="auto" />
        <el-table-column prop="project_name" label="项目名称" width="auto" />
        <el-table-column prop="env" label="环境标识" width="auto" />
        <el-table-column prop="protocol" label="请求协议" width="auto" />
        <el-table-column prop="base_url" label="URL" width="auto" />
        <el-table-column prop="create_time" label="创建时间" width="auto" />
        <el-table-column fixed="right" label="操作">
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="viewRowEnvsInfo(scope.row)"
            >查看</el-button>
            <el-button
              type="text"
              @click="editRowEnvsEdit(scope.row)"
            >编辑</el-button>
            <el-button
              type="text"
              @click="deleteRowEnvs(scope.row)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <!--环境模块-->
    <envs-dialog v-if="dialogEnvsFlag" :title="envsTitle" :eid="currentEnvs" :pid="projactCrruentId" @cancel="closeEnvDialog" />
  </div>
</template>

<script>
import { projectList } from '@/api/projects'
import { envsList, deleteEnvs } from '@/api/envs'
import EnvsDialog from '@/components/Envs/envsDialog'

export default ({
  name: 'Envs',
  components: {
    EnvsDialog
  },
  data() {
    return {
      projactCrruentId: 0,
      projectValue: '',
      projectLabel: '',
      projectOption: [],
      envsFrom: {
        'name': '',
        'project_id': 0,
        'env': '',
        'browser': '',
        'protocol': '',
        'base_url': ''
      },
      httpValue: undefined,
      httpLabel: '',
      httpOption: [
        {
          value: 1,
          label: 'http://'
        },
        {
          value: 2,
          label: 'https://'
        }
      ],
      req: {
        page: 1,
        size: 10
      },
      total: 10,
      envsData: [],
      dialogEnvsFlag: false,
      currentEnvs: 0, // 当前选中的环境信息
      envsTitle: 'create'
    }
  },
  mounted() {
    this.initProjectList()
    this.initEnvsList()
  },
  methods: {
    // 初始化项目列表
    async initProjectList() {
      const req_body = {
        'name': ''
      }
      const resp = await projectList(this.req, req_body)
      if (resp.success === true) {
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
      this.projectValue = value
      this.projectLabel = this.projectOption.find(
        (item) => item.value === value
      ).label
    },
    // 获取选中的协议值
    changeProtocol(value) {
      this.httpValue = value
      this.httpLabel = this.httpOption.find(
        (item) => item.value === value
      ).label
    },
    // 分页查询项目列表
    async initEnvsList() {
      this.envsFrom.project_id = this.projectValue === '' ? 0 : this.projectValue
      this.envsFrom.protocol = this.httpLabel
      const resp = await envsList(this.req, JSON.stringify(this.envsFrom))
      if (resp.success === true) {
        const resData = resp.items
        this.envsData = resData
        for (let i = 0; i < resData.length; i++) {
          resData[i].create_time = this.$moment(
            resData[i].create_time
          ).format('YYYY-MM-DD HH:mm:ss')
        }
        this.total = resp.total
        this.$message.success('查询成功！')
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 清除搜索
    clearSearch() {
      this.projectValue = 0
      if (this.projectValue === 0) {
        this.projectValue = ''
      }
      this.envsFrom.name = ''
      this.envsFrom.env = ''
      this.httpLabel = ''
      this.httpValue = undefined
      this.initEnvsList()
    },
    // 创建模块
    createEnv() {
      this.dialogEnvsFlag = true
    },
    // 创建模块关闭
    closeEnvDialog() {
      this.dialogEnvsFlag = false
      this.initEnvsList()
    },
    // 查看用例详情
    viewRowEnvsInfo(row) {
      // 点击用例，获取用例id
      this.currentEnvs = row.id
      this.dialogEnvsFlag = true
      this.envsTitle = 'view'
    },
    // 编辑测试用例
    editRowEnvsEdit(row) {
      // 点击用例，获取用例id
      this.currentEnvs = row.id
      this.dialogEnvsFlag = true
      this.envsTitle = 'edit'
    },
    // 删除测试用例
    async deleteRowEnvs(row) {
      await deleteEnvs(row.id).then((resp) => {
        this.$confirm('删除任务, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          center: true
        }).then(() => {
          if (resp.success === true) {
            this.initEnvsList()
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
})
</script>
