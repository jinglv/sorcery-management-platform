<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="1200px"
    :before-close="closeDialog"
  >
    <el-form
      ref="ruleForm"
      class="demo-ruleForm"
    >
      <el-form-item>
        <el-table
          :data="apiData"
          style="width: 100%"
        >
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item label="接口URL:" :inline="true">
                  <span>{{ props.row.url }}</span>
                </el-form-item>
                <br>
                <el-form-item label="接口请求方式:" style="margin-top: 10px;" :inline="true">
                  <span>{{ props.row.method }}</span>
                </el-form-item>
                <br>
                <el-form-item label="接口请求头信息:" style="margin-top: 10px;" :inline="true">
                  <el-table
                    :data="props.row.request_headers"
                    border
                    style="width: 600px"
                  >
                    <el-table-column
                      prop="name"
                      label="name"
                      width="200"
                    />
                    <el-table-column
                      prop="value"
                      label="value"
                    />
                    <el-table-column prop="操作" label="操作">
                      <template slot-scope="scope">
                        <el-button
                          type="text"
                          @click.native.prevent="deleteRow(scope.$index, props.row.request_headers)"
                        >
                          <i class="el-icon-delete" />
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-form-item>
                <br>
                <el-form-item label="接口请求参数:" style="margin-top: 10px;" :inline="true">
                  <el-table
                    :data="props.row.request_params"
                    border
                    style="width: 600px; margin-left: 13px;"
                  >
                    <el-table-column
                      prop="name"
                      label="name"
                      width="200"
                    />
                    <el-table-column
                      prop="value"
                      label="value"
                    />
                  </el-table>
                </el-form-item>
                <br>
                <el-form-item label="接口请求主体:" style="margin-top: 10px;" :inline="true">
                  <json-viewer :value="props.row.request_body" :expand-depth="3" />
                </el-form-item>
                <br>
                <el-form-item label="接口响应头信息:" style="margin-top: 10px;" :inline="true">
                  <el-table
                    :data="props.row.response_headers"
                    border
                    style="width: 600px"
                  >
                    <el-table-column
                      prop="name"
                      label="name"
                      width="200"
                    />
                    <el-table-column
                      prop="value"
                      label="value"
                    />
                  </el-table>
                </el-form-item>
                <br>
                <el-form-item label="接口响应主体:" style="margin-top: 10px;" :inline="true">
                  <json-viewer :value="props.row.response_body" :expand-depth="3" />
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column prop="url" label="接口URL" width="600" />
          <el-table-column prop="method" label="接口请求方式" />
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button
                type="text"
                @click.native.prevent="deleteRow(scope.$index, apiData)"
              >
                <i class="el-icon-delete" />
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-form-item>
    </el-form>
    <div class="dialog-footer" style="text-align: right">
      <el-button @click="closeDialog()">返回</el-button>
      <el-button
        type="primary"
        @click="saveApis()"
      >保存</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { harApiInfo, saveApiInfo } from '@/api/infos'
import jsonViewer from 'vue-json-viewer'

export default {
  components: {
    jsonViewer
  },
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
      apiData: [],
      apiFrom: {
        name: '',
        url: '',
        method: '',
        request_headers: [],
        request_params: [],
        request_body: '',
        response_body: ''
      }
    }
  },
  mounted() {
    this.harApiInfo()
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
    },
    async harApiInfo() {
      const req = {
        'har_file': this.fn
      }
      const resp = await harApiInfo(req)
      if (resp.success === true) {
        this.apiData = resp.result
        this.$message.success('Har文件解析成功!')
      } else {
        this.$message.error(resp.error.message)
      }
    },
    deleteRow(index, rows) {
      rows.splice(index, 1)
    },
    async saveApis() {
      const data = this.apiData
      for (let i = 0; i < data.length; i++) {
        this.apiFrom.name = this.fn
        this.apiFrom.url = data[i].url
        this.apiFrom.method = data[i].method
        this.apiFrom.request_headers = data[i].request_headers
        this.apiFrom.request_params = data[i].request_params
        this.apiFrom.request_body = data[i].request_body
        this.apiFrom.response_body = data[i].response_body
        const resp = await saveApiInfo(this.apiFrom)
        if (resp.success === true) {
          this.$message.success('接口保存成功!')
        } else {
          this.$message.error(resp.error.message)
        }
      }
    }
  }
}
</script>
<style scoped>
#image {
  text-align: left;
}
</style>
