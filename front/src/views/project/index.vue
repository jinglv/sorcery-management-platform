<template>
  <div class="project">
    <div class="filter-container">
      <el-input v-model="projectForm.name" placeholder="项目名称" style="width: 30%;margin-right: 5px;" class="filter-item" />
      <el-button class="filter-item" icon="el-icon-delete" @click="clearSearch()">重置</el-button>
      <el-button class="filter-item" type="primary" icon="el-icon-search" @click="initProjectList()">搜索</el-button>
    </div>
    <div style="text-align: left; width: 100%; margin-top: 10px;">
      <el-button type="primary" icon="el-icon-circle-plus-outline" @click="showDialog()">创建项目</el-button>
    </div>
    <div
      v-for="(item, index) in projectData"
      :key="index"
      class="text item"
    >
      <el-col :span="7" class="project-card">
        <el-card style="width: 85%; height: 55%; margin-top:10px">
          <div slot="header" class="clearfix">
            <span>{{ item.name }}</span>
            <div style="float: right">
              <el-dropdown>
                <span class="el-dropdown-link">
                  <i class="el-icon-setting" />
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item>
                    <el-button
                      type="text"
                      @click="showDetail(item.id)"
                    >详情</el-button>
                  </el-dropdown-item>
                  <el-dropdown-item>
                    <el-button
                      type="text"
                      @click="showEdit(item.id)"
                    >编辑</el-button>
                  </el-dropdown-item>
                  <el-dropdown-item>
                    <el-button
                      type="text"
                      @click="deleteProject(item.id)"
                    >删除</el-button>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </div>
          </div>
          {{ item.address }}
          <img
            :src="item.image"
            class="image"
            style="height: 250px; width: 80%; display: block; margin: 0 auto;"
          >
        </el-card>
      </el-col>
    </div>

    <!--分页-->
    <div class="pagination-container">
      <el-pagination
        background
        layout="total, prev, pager, next"
        :page-size="req.size"
        :total="total"
        @current-change="handleCurrentChange"
      />
    </div>
    <!--引入子组件-->
    <project-dialog
      v-if="dialogFlag"
      :title="dialogTitle"
      :pid="currentPorjectId"
      @cancel="closeDialog"
    />
  </div>
</template>

<script>
import ProjectDialog from '@/components/Project/projectDialog.vue'
import { projectList, deleteProject } from '@/api/projects'

export default {
  name: 'Porject',
  components: {
    ProjectDialog
  },
  data() {
    return {
      dialogFlag: false,
      dialogTitle: 'create',
      projectForm: {
        name: ''
      },
      currentPorjectId: '',
      projectData: [],
      req: {
        page: 1,
        size: 6
      },
      // 分页页数
      total: 10
    }
  },
  mounted() {
    // 组件加载的时候 进行调用
    this.initProjectList()
  },
  methods: {
    async initProjectList() {
      const resp = await projectList(this.req, JSON.stringify(this.projectForm))
      if (resp.success === true) {
        // 处理加载的图片路径
        for (let i = 0; i < resp.items.length; i++) {
          resp.items[i].image = '/static/images/' + resp.items[i].image
        }
        this.projectData = resp.items
        this.total = resp.total
        // this.$message.success('查询成功！')
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 清除搜索
    clearSearch() {
      this.projectForm.name = ''
      this.initProjectList()
    },
    // 展示子组件
    showDialog() {
      this.currentPorjectId = 0
      this.dialogTitle = 'create'
      this.dialogFlag = true
    },
    // 关闭子组件，子组件的closeDialog回调父组件
    closeDialog() {
      this.dialogFlag = false
      this.initProjectList()
    },
    // 跳转到第几页
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`)
      this.req.page = val
      this.initProjectList()
    },
    // 展示项目详情
    showDetail(id) {
      this.currentPorjectId = id
      this.dialogTitle = 'detail'
      this.dialogFlag = true
    },
    // 编辑项目
    showEdit(id) {
      this.currentPorjectId = id
      this.dialogTitle = 'edit'
      this.dialogFlag = true
    },
    // 删除项目
    async deleteProject(id) {
      await deleteProject(id).then((resp) => {
        this.$confirm('删除任务, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          center: true
        }).then(() => {
          if (resp.success === true) {
            this.initProjectList()
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
.pagination-container{
  width: 100px;
  height: 100px;
  position: absolute;
  right: 10%;
  bottom: 0;
}
</style>
