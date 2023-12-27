<template>
  <div :style="{'max-height': timeLineHeight +'px'}" style="margin-left: 10px; margin-right: 10px; overflow-y:scroll;">
    <el-form
      :data="apiDetails"
      label-width="150px"
      class="demo-ruleForm"
    >
      <el-form-item label="接口名称：" prop="name">{{ apiDetails.name }}</el-form-item>
      <el-form-item label="接口地址：" prop="url">{{ apiDetails.path }}</el-form-item>
      <el-form-item label="请求方式：" prop="method">{{ apiDetails.method }}</el-form-item>
      <el-form-item label="请求头：">
        <el-table
          :data="headers"
          border
          style="width: 80%"
        >
          <el-table-column
            prop="name"
            label="请求头名"
            width="250"
          />
          <el-table-column
            prop="value"
            label="请求头值"
          />
        </el-table>
      </el-form-item>
      <el-form-item label="请求主体类型：" prop="method">{{ apiDetails.req_type }}</el-form-item>
      <el-form-item label="请求参数：">
        <el-table
          :data="bodys"
          border
          style="width: 80%"
        >
          <el-table-column
            prop="name"
            label="参数名称"
            width="180"
          />
          <el-table-column
            prop="type"
            label="参数值类型"
            width="180"
          />
          <el-table-column
            prop="description"
            label="参数说明"
            width="180"
          />
          <el-table-column
            prop="required"
            label="是否必填"
          >
            <template slot-scope="{ row }">
              {{ row.required | requiredContent }}
            </template>
          </el-table-column>
        </el-table>
      </el-form-item>
      <el-form-item label="响应参数：">
        <el-table
          :data="responses"
          border
          style="width: 80%"
        >
          <el-table-column
            prop="name"
            label="响应参数值"
            width="180"
          />
          <el-table-column
            prop="type"
            label="响应参数类型"
            width="180"
          />
          <el-table-column
            prop="description"
            label="说明"
          />
        </el-table>
      </el-form-item>
      <el-form-item style="text-align: right">
        <el-button @click="closeDialog()">返回</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { getYapiApiDetail } from '@/api/infos'

export default {
  name: 'ApiDetailDialog',
  filters: {
    requiredContent(value) {
      if (value === 1) {
        return '必填'
      } else if (value === 0) {
        return '非必填'
      } else {
        return '未知类型'
      }
    }
  },
  props: {
    aid: {
      type: Number,
      default: 1
    },
    url: {
      type: String,
      default: ''
    },
    token: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      apiDetailFrom: {
        api_id: 1,
        yapi_base_url: '',
        yapi_token: ''
      },
      apiDetails: '',
      headers: [],
      bodys: [],
      responses: [],
      timeLineHeight: ''
    }
  },
  mounted() {
    this.timeLineHeight = document.documentElement.clientHeight - 150
    window.onresize = () => { this.timeLineHeight = document.documentElement.clientHeight - 150 }
    this.apiDetailFrom.api_id = this.aid
    this.apiDetailFrom.yapi_base_url = this.url
    this.apiDetailFrom.yapi_token = this.token
    this.getApiDetail()
  },
  methods: {
    // 获取Yapi接口详情
    async getApiDetail() {
      const resp = await getYapiApiDetail(this.apiDetailFrom)
      if (resp.success === true) {
        this.$message.success('查询成功！')
        this.apiDetails = resp.result
        this.headers = resp.result.headers
        this.bodys = resp.result.req_body === '' ? [] : resp.result.req_body
        this.responses = resp.result.res_body
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 关闭
    closeDialog() {
      this.$emit('close')
    }
  }
}
</script>
