<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="800px"
    :before-close="closeDialog"
  >
    <el-form
      ref="ruleForm"
      class="demo-ruleForm"
    >
      <el-form-item>
        <el-table
          ref="multipleTable"
          :data="datas"
          border
          style="width: 100%"
          @select="selectionOneApi"
          @select-all="selectionAllApi"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="接口ID" width="70" />
          <el-table-column prop="name" label="接口名称" width="150" />
          <el-table-column prop="api_path" label="接口地址" />
          <el-table-column label="httpRunner项目接口名称">
            <template slot-scope="scope">
              <el-input
                v-model="scope.row.value"
                :required="true"
                placeholder="请输入httpRunner项目接口名称"
              />
              <span v-if="isInputEmpty" style="color: red;">*接口名称不能为空</span>
            </template>
          </el-table-column>>
        </el-table>
      </el-form-item>
      <el-form-item style="text-align: right">
        <div class="dialog-footer">
          <el-button @click="backDialog()">返回上一步</el-button>
          <el-button
            type="primary"
            :disabled="saveFlag"
            @click="createHttpRunnerApi"
          >创建HttpRunner工程接口</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import { createHttpRunnerApi } from '@/api/httprunner'

export default {
  components: {},
  props: {
    datas: {
      type: Array,
      default: null
    },
    project: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      showTitle: '创建HttpRunner工程接口',
      dialogVisible: true,
      httprunner_api_name: '',
      apiInfoList: [],
      saveFlag: false
    }
  },
  computed: {
    isInputEmpty() {
      // 检查输入框的值是否为空
      return this.httprunner_api_name.trim() === ''
    }
  },
  mounted() {
  },
  methods: {
    closeDialog() {
      this.$emit('cancel', {})
    },
    backDialog() {
      this.dialogVisible = false
      this.$emit('visible', this.dialogVisible)
    },
    // 选择所有接口信息
    selectionAllApi(val) {
      for (let i = 0; i < val.length; i++) {
        this.apiInfoList.push({
          'name': val[i].value,
          'base_api_id': val[i].id,
          'httprunner_project_id': this.project
        })
        this.httprunner_api_name = val[i].value
      }
    },
    // 选择一条接口
    selectionOneApi(val) {
      for (let i = 0; i < val.length; i++) {
        this.apiInfoList.push({
          'name': val[i].value,
          'base_api_id': val[i].id,
          'httprunner_project_id': this.project
        })
        this.httprunner_api_name = val[i].value
      }
    },
    // 创建接口
    async createHttpRunnerApi() {
      for (let i = 0; i < this.apiInfoList.length; i++) {
        const req = this.apiInfoList[i]
        if (this.isInputEmpty) {
          // 输入内容为空，显示必填提示，不进行提交操作
          this.$message.error('请输入接口名称')
          return
        }
        const resp = await createHttpRunnerApi(req)
        if (resp.success === true) {
          this.closeDialog()
          this.$message.success('创建成功！')
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
