<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="70%"
    :before-close="closeDialog"
    :append-to-body="true"
    :close-on-click-modal="false"
  >
    <el-form
      ref="ruleForm"
      :model="demandForm"
      :rules="rules"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="需求名称" prop="name">
        <el-input v-model="demandForm.name" />
      </el-form-item>
      <el-form-item label="项目" prop="project_id">
        <el-select
          v-model="projectValue"
          placeholder="请选择项目"
          style="width: 100%;"
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
      <el-form-item label="版本号" prop="version_number">
        <el-input v-model="demandForm.version_number" />
      </el-form-item>
      <el-form-item label="需求类型" prop="requirements_type">
        <el-select
          v-model="typeValue"
          placeholder="请选择需求类型"
          style="width: 100%;"
          @change="changeType"
        >
          <el-option
            v-for="item in typeOption"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="需求" prop="requirements">
        <el-input v-model="demandForm.requirements" placeholder="请输入需求链接地址或者上传需求文档……" />
        <el-upload
          class="upload-demo"
          action="#"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :before-remove="beforeRemove"
          multiple
          :limit="3"
          :on-exceed="handleExceed"
          :file-list="fileList"
          :http-request="httpRequest"
          :before-upload="beforeUpload"
        >
          <el-button size="small" type="primary">点击上传</el-button>
          <div slot="tip" class="el-upload__tip">只能上传文本和图片格式，且不超过2MB</div>
        </el-upload>
      </el-form-item>
      <el-form-item label="需求分析" prop="demand_analysis">
        <div id="editor_demand" />
      </el-form-item>
      <el-form-item label="描述" prop="describe">
        <el-input v-model="demandForm.describe" />
      </el-form-item>
      <el-form-item style="text-align: right">
        <el-button @click="closeDialog">取消</el-button>
        <el-button
          v-if="title != 'edit'"
          type="primary"
          @click="createDemand('ruleForm')"
        >确定</el-button>
        <el-button
          v-if="title == 'edit'"
          type="primary"
          @click="updateDemand('ruleForm')"
        >更新</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import { projectList } from '@/api/projects'
import { uploadFile } from '@/api/commons'
import { createDemand, getDemandDetail, updateDemandDetail } from '@/api/cases'
import { getToken } from '@/utils/auth'
import E from 'wangeditor'
import hljs from 'highlight.js'

export default {
  name: 'DemandDialog',
  components: {},
  props: {
    title: {
      type: String,
      default: null
    },
    did: {
      type: Number,
      default: 1
    }
  },
  data() {
    return {
      showTitle: '',
      dialogVisible: true,
      demandForm: {
        name: '',
        project_id: 0,
        version_number: '',
        requirements_type: '',
        requirements: '',
        requirements_upload_file: [],
        demand_analysis: '',
        describe: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入需求名称', trigger: 'blur' }
        ],
        project_id: [
          { required: true, message: '请选择项目', trigger: 'blur' }
        ],
        version_number: [
          { required: true, message: '请输入需求版本号', trigger: 'blur' }
        ],
        requirements_type: [
          { required: true, message: '请选择需求类型', trigger: 'blur' }
        ]
      },
      typeValue: '',
      typeLabel: '',
      typeOption: [
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
      projectValue: '',
      projectLabel: '',
      projectOption: [],
      fileList: [],
      disabled: false,
      editor_demand: null
    }
  },
  created() {
    this.showTitle = '创建需求'
    // 组件打开则进行加载
    // 使用时钟函数进行延迟，否则获取不到元素 -- 等元素加载完成后再进行创建E
    this.$nextTick(() => {
      this.editor_demand = new E('#editor_demand')
      this.editor_demand.highlight = hljs
      // 富文本组价设置图片上传接口
      this.editor_demand.config.uploadImgServer = '/api/commons/editor/file/image'
      this.editor_demand.config.uploadFileName = 'file'
      this.editor_demand.config.uploadImgHeaders = {
        Authorization: 'Bearer ' + getToken()
      }
      // 富文本组价设置视频上传接口
      this.editor_demand.config.uploadVideoServer = '/api/commons/editor/file/video'
      this.editor_demand.config.uploadVideoName = 'file'
      this.editor_demand.config.uploadVideoHeaders = {
        Authorization: 'Bearer ' + getToken()
      }
      // 创建
      this.editor_demand.create()
    })
    // 判断不同操作
    if (this.title === 'edit') {
      this.showTitle = '需求详情'
      this.getDemandDetail()
    }
  },
  mounted() {
    this.initProjectList()
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
      // 关闭弹窗，销毁E
      this.editor_demand.destroy()
      this.editor_demand = null
    },
    changeType(value) {
      this.typeValue = value
      this.typeLabel = this.typeOption.find(
        (item) => item.value === value
      ).label
      this.demandForm.requirements_type = value
    },
    // 创建需求详情
    createDemand(formName) {
      this.$refs[formName].validate((valid) => {
        // 获取编辑框的内容
        const content = this.editor_demand.txt.html()
        this.demandForm.demand_analysis = content
        if (valid) {
          createDemand(this.demandForm).then((resp) => {
            if (resp.success === true) {
              this.closeDialog()
              this.$message.success('创建成功！')
            } else {
              this.$message.error(resp.error.message)
            }
          })
        }
      })
    },
    handleRemove(file, fileList) {
      console.log(file, fileList)
    },
    handlePreview(file) {
      console.log('上传成功', file)
    },
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`)
    },
    // 覆盖默认的上传行为，可以自定义上传的实现，避免使用框架自动上传功能
    httpRequest() {},
    // 上传文件
    async beforeUpload(file) {
      const fb = new FormData()
      fb.append('file', file)
      const resp = await uploadFile(fb)
      if (resp.success === true) {
        // 获取文件名
        const fileName = resp.result.name
        this.demandForm.requirements_upload_file.push(fileName)
        const filePath = '/static/file/' + fileName
        const fileInfo = {
          name: file.name,
          url: filePath
        }
        this.fileList.push(fileInfo)
        console.info('已上传文件：', fileName)
        this.$message.success('上传成功！')
      } else {
        this.$message.error(resp.error.message)
      }
    },
    async getDemandDetail() {
      const resp = await getDemandDetail(this.did)
      if (resp.success === true) {
        this.demandForm = resp.result
        this.projectValue = resp.result.project_id
        this.typeValue = resp.result.requirements_type
        this.editor_demand.txt.html(resp.result.demand_analysis)
        const files = JSON.parse(resp.result.requirements_upload_file.replace(/'/g, '"'))
        if (files.length > 0) {
          for (let i = 0; i < files.length; i++) {
            const fileInfos = {
              name: files[i],
              url: '/static/file/' + files[i]
            }
            this.fileList.push(fileInfos)
            this.demandForm.requirements_upload_file = []
            this.demandForm.requirements_upload_file.push(files[i])
          }
        } else {
          this.demandForm.requirements_upload_file = []
        }
        this.$message.success('查询成功')
      } else {
        this.$message.error(resp.error.message)
      }
    },
    updateDemand(formName) {
      this.$refs[formName].validate((valid) => {
        // 获取编辑框的内容
        const content = this.editor_demand.txt.html()
        this.demandForm.demand_analysis = content
        if (valid) {
          updateDemandDetail(this.did, this.demandForm).then((resp) => {
            if (resp.success === true) {
              this.closeDialog()
              this.$message.success('更新成功！')
            } else {
              this.$message.error(resp.error.message)
            }
          })
        }
      })
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
      this.demandForm.project_id = value
    }
  }
}
</script>
<style scoped>
#image {
  text-align: left;
}

#editor_requirements {
  border: 1px solid #ccc;
  z-index: 100; /* 按需定义 */
}

#editor_demand {
  border: 1px solid #ccc;
  z-index: 100; /* 按需定义 */
}
</style>
