<template>
  <div id="yapi-api">
    <el-form :inline="true" :model="yapiFrom" class="demo-form-inline">
      <el-form-item label="Yapi基础地址">
        <el-input v-model="yapiFrom.yapiBaseUrl" placeholder="请输入Yapi基础地址" style="width: 250px;" />
      </el-form-item>
      <el-form-item label="Yapi项目Token">
        <el-input v-model="yapiFrom.yapiToken" placeholder="请输入Yapi项目Token" style="width: 600px;" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="getYapiProjectInfo()">查询</el-button>
      </el-form-item>
    </el-form>
    <el-form v-show="showFlag" :inline="true" class="demo-form-inline">
      <el-form-item label="Yapi项目名称:">{{ project_name }}</el-form-item>
    </el-form>
    <div style="text-align: left">
      <el-form :inline="true">
        <el-form-item label="Yapi项目分类">
          <el-select
            v-model="categoryName"
            size="medium"
            placeholder="请选择项目分类"
            @change="changeCategory"
          >
            <el-option
              v-for="item in categoryOption"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="接口总数量:" style="float: right">{{ total }}</el-form-item>
      </el-form>
    </div>
    <div style="overflow-y: auto;">
      <el-table
        :data="apiData"
        border
        stripe
        style="width: 100%"
      >
        <el-table-column
          prop="api_id"
          label="接口ID"
          width="200"
        />
        <el-table-column
          prop="api_name"
          label="接口名称"
          width="250"
        />
        <el-table-column
          prop="api_path"
          label="接口地址"
        />
        <el-table-column fixed="right" label="操作" width="250">
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="apiDetailDialog(scope.row)"
            >查看接口详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        background
        layout="prev, pager, next"
        style="text-align: right"
        :page-size="req.size"
        :total="total"
        @current-change="handleCurrentChange"
      />
    </div>
    <el-drawer
      :title="apiDetailTitle"
      :visible.sync="drawer"
      direction="rtl"
      size="50%"
    >
      <yapi-api-detail-dialog v-if="drawer" :url="yapiFrom.yapiBaseUrl" :token="yapiFrom.yapiToken" :aid="apiId" @close="closeDrawer()" />
    </el-drawer>
  </div>
</template>

<script>
import { getYapiProjectInfo, getYapiCategoryList, getYapiApiList } from '@/api/infos'
import yapiApiDetailDialog from '@/components/Infos/yapiApiDetailDialog'

export default {
  components: {
    yapiApiDetailDialog
  },
  data() {
    return {
      yapiFrom: {
        yapiBaseUrl: 'https://yapiprd.seres.cn',
        yapiToken: '77ec4ce849828d1cf036dde73bfc604c7b5ecf45311ad27dc4184fb93173a14d'
      },
      project_id: 1,
      project_name: '',
      categoryOption: [],
      categoryId: 1,
      categoryName: '',
      categoryListFrom: {
        yapi_base_url: '',
        yapi_token: ''
      },
      showFlag: false,
      apiData: [],
      req: {
        page: 1,
        size: 6
      },
      total: 0,
      drawer: false,
      apiId: 0,
      apiDetailTitle: ''
    }
  },
  mounted() {
  },
  methods: {
    // 获取Yapi项目信息
    async getYapiProjectInfo() {
      const req = {
        yapi_base_url: this.yapiFrom.yapiBaseUrl,
        yapi_token: this.yapiFrom.yapiToken
      }
      const resp = await getYapiProjectInfo(req)
      if (resp.success === true) {
        this.project_id = resp.result.project_id
        this.project_name = resp.result.project_name
        this.$message.success('查询成功！')
        this.showFlag = true
        this.clickCategoryList()
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 项目分类列表
    async clickCategoryList() {
      const req = {
        project_id: this.project_id,
        yapi_base_url: this.yapiFrom.yapiBaseUrl,
        yapi_token: this.yapiFrom.yapiToken
      }
      const resp = await getYapiCategoryList(req)
      if (resp.success === true) {
        this.categoryId = resp.result[0].category_id
        this.categoryName = resp.result[0].category_name
        for (let i = 0; i < resp.result.length; i++) {
          this.categoryOption.push({
            value: resp.result[i].category_id,
            label: resp.result[i].category_name
          })
        }
        this.apiList(this.categoryId)
        // this.$message.success("查询成功！")
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 项目分类接口列表
    async apiList(categoryId) {
      const req = {
        category_id: categoryId,
        yapi_base_url: this.yapiFrom.yapiBaseUrl,
        yapi_token: this.yapiFrom.yapiToken,
        page: this.req.page,
        size: this.req.size
      }
      const resp = await getYapiApiList(req)
      if (resp.success === true) {
        this.apiData = resp.result.list
        this.total = resp.result.count
        // this.$message.success("查询成功！")
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 修改选中分类
    changeCategory(value) {
      this.categoryId = value
      this.apiList(value)
    },
    // 跳转到第几页
    handleCurrentChange(val) {
      this.req.page = val
      this.apiList(this.categoryId)
    },
    // 创建模块关闭
    closeDialog() {
      this.dialogFlag = false
      this.apiList(this.categoryId)
    },
    // 查看接口详情
    apiDetailDialog(row) {
      // 点击获取用例
      this.apiId = row.api_id
      this.drawer = true
      this.apiDetailTitle = '查看接口详情'
    },
    // 传递子组件，关闭抽屉
    closeDrawer() {
      this.drawer = false
    }
  }
}
</script>
