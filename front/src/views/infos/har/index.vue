<template>
  <div id="har-api">
    <div id="upload-file">
      <el-row :gutter="20">
        <el-col :span="3">
          <div class="grid-content">
            <span class="label-title">上传Har文件:</span>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content">
            <el-upload
              ref="upload"
              class="upload-demo"
              action="#"
              :limit="1"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :file-list="fileList"
              :before-upload="uploadFile"
              :http-request="httpRequest"
              :auto-upload="false"
            >
              <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
              <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
              <div slot="tip" class="el-upload__tip" style="color:red">只能上传后缀为.har的文件</div>
            </el-upload>
          </div>
        </el-col>
      </el-row>
    </div>
    <div id="api-file-list" style="margin-top: 30px;">
      <el-button size="small" type="primary" @click="harFileList">查看上传文件列表</el-button>
      <el-table
        :data="harFileData"
        border
        stripe
        style="width: 100%; margin-top: 10px;"
      >
        <el-table-column
          prop="file_name"
          label="Har文件名称"
        />
        <el-table-column fixed="right" label="操作" width="450">
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="showApiInfo(scope.row)"
            >查看文件接口解析信息</el-button>
            <el-button
              type="text"
              @click="showApiInfoList(scope.row)"
            >查看接口列表</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <!--引入子组件-->
    <har-api-info-dialog v-if="harInfoFlag" :fn="fileName" @cancel="closeDialog" />
    <api-info-list-dialog v-if="apiInfoListFlag" :fn="fileName" @cancel="closeDialog" />
  </div>
</template>
<script>
import { uploadFile } from '@/api/commons'
import { harApiInfo, harFileList } from '@/api/infos'
import harApiInfoDialog from '@/components/Infos/harApiInfoDialog'
import ApiInfoListDialog from '@/components/Infos/apiInfoListDialog.vue'

export default {
  components: {
    harApiInfoDialog,
    ApiInfoListDialog
  },
  data() {
    return {
      apiData: [],
      harFileData: [],
      fileList: [],
      fileName: '',
      harInfoFlag: false,
      apiInfoListFlag: false
    }
  },
  methods: {
    submitUpload() {
      this.$refs.upload.submit()
    },
    handleRemove(file, fileList) {
      console.log(file, fileList)
    },
    handlePreview(file) {
      console.log(file)
    },
    // 上传文件
    async uploadFile(file) {
      const fb = new FormData()
      fb.append('file', file)
      const resp = await uploadFile(fb)
      if (resp.success === true) {
        // 获取文件名
        this.fileName = resp.result.name
        this.$message.success('上传成功！')
      } else {
        console.log('上传失败', resp)
        this.$message.error(resp.error.message)
      }
    },
    // 覆盖默认的上传行为，可以自定义上传的实现，避免使用框架自动上传功能
    httpRequest() {},
    async harFileList() {
      const resp = await harFileList()
      if (resp.success === true) {
        this.harFileData = resp.result
        this.$message.success('查询文件成功！')
      } else {
        this.$message.error(resp.error.message)
      }
    },
    // 查看接口信息
    showApiInfo(row) {
      this.fileName = row.file_name
      this.harInfoFlag = true
    },
    showApiInfoList(row) {
      this.fileName = row.file_name
      this.apiInfoListFlag = true
    },
    // 关闭弹窗
    closeDialog() {
      this.harInfoFlag = false
      this.apiInfoListFlag = false
    },
    async harApiInfo() {
      const req = {
        'har_file': this.fileName
      }
      const resp = await harApiInfo(req)
      if (resp.success === true) {
        this.apiData = resp.result
        this.$message.success('Har文件解析成功！')
      } else {
        this.$message.error(resp.error.message)
      }
    }
  }
}
</script>

<style>
  .el-row {
    margin-bottom: 20px;
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
    line-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
  .label-title {
  font-family: "Liberation Mono", monospace, serif, sans-serif;
  font-size: 16px;
  line-height: 42px;
}
</style>
