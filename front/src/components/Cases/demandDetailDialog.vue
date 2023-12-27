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
      :model="demandDetailForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-col :span="8">
        <el-form-item label="需求名称：" prop="name">{{ demandDetailForm.name }}</el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item label="项目：" prop="project_name">{{ demandDetailForm.project_name }}</el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item label="需求类型：" prop="requirements_type">
          {{ demandDetailForm.requirements_type | requirementsType }}
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item label="需求连接：" prop="requirements">{{ demandDetailForm.requirements }}</el-form-item>
      </el-col>
      <el-form-item label="需求文件：" prop="requirements_upload_file">
        <div v-for="(file, index) in fileList" :key="index">
          <el-link :href="file.url" target="_blank">{{ file.name }}</el-link>
        </div>
      </el-form-item>
      <el-form-item label="需求分析：" prop="requirements">
        <div class="w-e-text" style="height: 400px; overflow-y: auto;" v-html="demandDetailForm.demand_analysis" />
      </el-form-item>
      <el-form-item label="描述：" prop="describe">{{ demandDetailForm.describe }}</el-form-item>
      <el-form-item style="text-align: right">
        <el-button @click="closeDialog">返回</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import { getDemandDetail } from '@/api/cases'

export default {
  name: 'DemandDetailDialog',
  components: {},
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
      demandDetailForm: {
        name: '',
        project_name: '',
        version_number: '',
        requirements_type: '',
        requirements: '',
        requirements_upload_file: [],
        demand_analysis: '',
        describe: ''
      },
      fileList: []
    }
  },
  created() {
    this.showTitle = this.title
    this.getDemandDetail()
  },
  mounted() {
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
    },
    async getDemandDetail() {
      const resp = await getDemandDetail(this.did)
      if (resp.success === true) {
        this.demandDetailForm = resp.result
        const files = JSON.parse(resp.result.requirements_upload_file.replace(/'/g, '"'))
        if (files.length > 0) {
          for (let i = 0; i < files.length; i++) {
            const fileInfos = {
              name: files[i],
              url: '/static/file/' + files[i]
            }
            this.fileList.push(fileInfos)
          }
        } else {
          this.demandDetailForm.requirements_upload_file = []
        }
        this.$message.success('查询成功')
      } else {
        this.$message.error(resp.error.message)
      }
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
