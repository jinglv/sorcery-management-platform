<template>
  <div class="apis">
    <div style="text-align: left; margin-top: 10px;">
      <el-form :inline="true">
        <el-form-item label="项目">
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
        </el-form-item>
        <el-form-item style="float: right">
          <el-button class="el-icon-circle-plus-outline" type="primary" @click="createApi()">创建接口</el-button>
        </el-form-item>
        <el-form-item style="float: right">
          <el-button class="el-icon-eleme" style="margin-left: 35px" @click="createEnv()">配置环境变量</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div style="margin-top: 10px">
      <el-card style="width: 24%; float: left" class="box-card card-height" :style="conheight">
        <el-button
          class="label-title"
          type="text"
          icon="el-icon-circle-plus-outline"
          @click="createRootModule"
        >{{ projectLabel }}-模块</el-button>
        <el-tree
          :data="moduleData"
          node-key="id"
          default-expand-all
          :expand-on-click-node="false"
          @node-click="nodeClick"
        >
          <span slot-scope="{ node, data }" class="custom-tree-node">
            <div class="el-icon-grape" style="float: left;margin-top: 10px;margin-right: 5px;" />
            <span class="label-text">{{ node.label }}</span>
            <span style="float: right">
              <el-button type="text" size="mini" @click="() => append(data)">
                <i class="el-icon-circle-plus-outline" />
              </el-button>
              <el-button
                type="text"
                size="mini"
                @click="() => remove(node, data)"
              >
                <i class="el-icon-delete" />
              </el-button>
            </span>
          </span>
        </el-tree>
      </el-card>
      <div style="width: 75%; float: right">
        <el-table
          :data="apisData"
          border
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="50" />
          <el-table-column prop="name" label="接口名称" width="auto" />
          <el-table-column prop="method" label="请求方法" width="auto" />
          <el-table-column prop="api_path" label="API Path" width="auto" />
          <el-table-column prop="module.name" label="所属模块" width="auto" />
          <el-table-column prop="create_time" label="创建时间" width="auto" />
          <el-table-column fixed="right" label="操作">
            <template slot-scope="scope">
              <el-button
                type="text"
                size="small"
                @click="caseRowApiInfo(scope.row)"
              >查看</el-button>
              <el-button
                type="text"
                size="small"
                @click="editRowApiInfo(scope.row)"
              >编辑</el-button>
              <el-button
                type="text"
                size="small"
                @click="deleteRowApiInfo(scope.row)"
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
    </div>
    <el-drawer
      :title="caseTitle"
      :visible.sync="drawer"
      direction="rtl"
      size="55%"
    >
      <api-dialog v-if="drawer" :title="caseTitle" :mid="currentModule" :pid="projectValue" :cid="currentCase" @close="closeDrawer()" @refresh="refreshApiList()" />
    </el-drawer>
    <!-- 创建模块 -->
    <module-dialog
      v-if="dialogFlag"
      :pid="projectValue"
      :plabel="projectLabel"
      :root-id="rootFlag"
      :parent-obj="parentObj"
      @cancel="closeDialog"
    />
    <!--环境模块-->
    <envs-dialog v-if="dialogEnvsFlag" :title="evnsTitle" :pid="projectValue" @cancel="closeEnvDialog" />
  </div>
</template>
<script>
import ModuleDialog from '@/components/Module/moduleDialog.vue'
import ApiDialog from '@/components/Api/apiDialog.vue'
import EnvsDialog from '@/components/Envs/envsDialog.vue'
import { projectList } from '@/api/projects'
import { getApisList, deleteApi } from '@/api/apis'
import { getModuleTree, deleteModule } from '@/api/modules'

export default {
  name: 'CaseModule',
  components: {
    ModuleDialog,
    ApiDialog,
    EnvsDialog
  },
  data() {
    return {
      projectValue: 1,
      projectLabel: '',
      rootFlag: true,
      projectOption: [],
      moduleData: [],
      dialogFlag: false,
      parentObj: {},
      apisData: [],
      drawer: false,
      caseTitle: '',
      currentModule: 0, // 当前选中的模块
      currentCase: 0, // 当前选中的用例
      req: {
        page: 1,
        size: 10
      },
      // 分页页数
      total: 10,
      dialogEnvsFlag: false,
      conheight: {
        height: ''
      },
      evnsTitle: 'create'
    }
  },
  mounted() {
    this.initProjectList()
  },
  created() {
    window.addEventListener('resize', this.getHeight)
    this.getHeight()
  },
  methods: {
    // 设置卡片高度自适应el-card
    getHeight() {
      this.conheight.height = window.innerHeight - 170 + 'px'
    },
    // 初始化项目列表
    async initProjectList() {
      const req_body = {
        'name': ''
      }
      const resp = await projectList(this.req, req_body)
      if (resp.success === true) {
        this.projectValue = resp.items[0].id
        this.projectLabel = resp.items[0].name
        // 在初始化项目信息，同时初始化项目下的模块信息
        this.initModuleList(this.projectValue)
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
    // 创建模块
    createRootModule() {
      this.parentObj = {}
      this.dialogFlag = true
      this.rootFlag = true
    },
    // 创建模块子节点
    append(data) {
      this.dialogFlag = true
      this.rootFlag = false
      this.parentObj = data
    },
    // 删除模块
    remove(node, data) {
      deleteModule(data.id).then((resp) => {
        if (resp.success === true) {
          this.$message.success('删除成功！')
          this.initModuleList(this.projectValue)
        } else {
          this.$message.error(resp.error.msg)
        }
      })
    },
    // 创建模块关闭
    closeDialog() {
      this.dialogFlag = false
      this.initModuleList(this.projectValue)
    },
    nodeClick(data) {
      this.currentModule = data.id
      this.getCaseList(data.id)
    },
    // 获取模块下的测试用例列表
    async getCaseList(mid) {
      const resp = await getApisList(mid, this.req)
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
    // 创建测试用例
    createApi() {
      if (this.currentModule === 0) {
        this.$message.warning('请选择模块!')
      } else {
        this.currentCase = 0
        this.drawer = true
        this.caseTitle = '创建接口'
      }
    },
    // 查看用例详情
    caseRowApiInfo(row) {
      // 点击用例，获取用例id
      this.currentCase = row.id
      this.drawer = true
      this.caseTitle = '接口详情'
    },
    // 编辑测试用例
    editRowApiInfo(row) {
      // 点击用例，获取用例id
      this.currentCase = row.id
      this.drawer = true
      this.caseTitle = '编辑接口'
    },
    // 删除测试用例
    deleteRowApiInfo(row) {
      // 点击用例，获取用例id
      this.currentCase = row.id
      this.$confirm('删除接口, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }).then(() => {
        const resp = deleteApi(this.currentCase)
        if (resp.success === true) {
          this.getCaseList(this.currentModule)
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
    },
    // 跳转到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.req.page = val
      this.getCaseList(this.currentModule)
    },
    // 传递子组件，关闭抽屉
    closeDrawer() {
      this.drawer = false
    },
    // 传递子组件，关闭抽屉，刷新列表
    refreshApiList() {
      this.getCaseList(this.currentModule)
    },
    // 创建模块
    createEnv() {
      this.dialogEnvsFlag = true
    },
    // 创建模块关闭
    closeEnvDialog() {
      this.dialogEnvsFlag = false
      this.initModuleList(this.projectValue)
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
</style>
