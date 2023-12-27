<template>
  <div class="test-data" :style="{'max-height': timeLineHeight +'px'}" style="margin-left: 10px; margin-right: 10px; overflow-y:scroll;">
    <div style="height: 50px; margin-top: 10px;">
      <span style="float: left; line-height: 36px;">基础数据类型：</span>
      <el-cascader
        v-model="testDataType"
        :options="options"
        :props="props"
        clearable
        placeholder="请输入基础数据类型"
        style="width: 45%; float: left"
      />
      <el-button
        type="primary"
        style="float: left; margin-left: 20px;"
        @click="templateClick()"
      >生成</el-button>
      <el-button
        v-clipboard:copy="JSON.stringify(dataResult)"
        v-clipboard:error="onError"
        v-clipboard:success="onCopy"
        style="float:right"
        size="mini"
        type="text"
        icon="el-icon-copy-document"
        round
        class="copy-btn"
      >复制</el-button>
    </div>
    <json-viewer :value="dataResult" :expand-depth="5" copyable boxed />
    <div class="test_data_time" style="margin-top: 30px;">
      <div style="height: 50px; margin-top: 10px;">
        <span>时间数据类型：</span>
        <el-select v-model="time_value" placeholder="请选择..." @change="changeTimeData">
          <el-option
            v-for="item in timeTypeOption"
            :key="item.time_value"
            :label="item.label"
            :value="item.time_value"
          />
        </el-select>
        <el-button
          v-if="time_value !== undefined"
          style="margin-left: 20px;"
          type="primary"
          @click="changeTimeData()"
        >再点一下</el-button>
        <el-button
          v-clipboard:copy="getTimeData"
          v-clipboard:error="onError"
          v-clipboard:success="onCopy"
          style="float:right"
          size="mini"
          type="text"
          icon="el-icon-copy-document"
          round
          class="copy-btn"
        >复制</el-button>
      </div>
      <div class="div-line" style="height: 100px">
        <el-input
          v-model="getTimeData"
          type="textarea"
          :rows="3"
          placeholder="生成的数据"
        />
      </div>
    </div>
    <div class="test_random_number">
      <div style="height: 50px; margin-top: 10px;">
        <span style="float: left; line-height: 36px">随机生成数字：</span>
        <el-input
          v-model="numberLength"
          placeholder="请输入生成随机数字的长度"
          style="width: 20%; float: left"
        />
        <el-button
          type="primary"
          style="float: left; margin-left: 20px;"
          @click="sendRandomNumber()"
        >生成</el-button>
        <el-button
          v-clipboard:copy="numberResult"
          v-clipboard:error="onError"
          v-clipboard:success="onCopy"
          style="float:right"
          size="mini"
          type="text"
          icon="el-icon-copy-document"
          round
          class="copy-btn"
        >复制</el-button>
      </div>
      <div class="div-line" style="height: 100px">
        <el-input
          v-model="numberResult"
          type="textarea"
          :rows="3"
          placeholder="生成的数据"
        />
      </div>
    </div>
    <div class="test_random_cn">
      <div style="height: 50px; margin-top: 10px;">
        <span style="float: left; line-height: 36px">随机生成汉字：</span>
        <el-input
          v-model="cnLength"
          placeholder="请输入生成随机汉字的长度"
          style="width: 20%; float: left"
        />
        <el-button
          type="primary"
          style="float: left; margin-left: 20px;"
          @click="sendRandomCn()"
        >生成</el-button>
        <el-button
          v-clipboard:copy="cnResult"
          v-clipboard:error="onError"
          v-clipboard:success="onCopy"
          style="float:right"
          size="mini"
          type="text"
          icon="el-icon-copy-document"
          round
          class="copy-btn"
        >复制</el-button>
      </div>
      <div class="div-line" style="height: 100px">
        <el-input
          v-model="cnResult"
          type="textarea"
          :rows="3"
          placeholder="生成的数据"
        />
      </div>
    </div>
    <div class="test_random_letter">
      <div style="height: 50px; margin-top: 10px;">
        <span style="float: left; line-height: 36px">随机生成字母：</span>
        <el-input
          v-model="letterLength"
          placeholder="请输入生成随机字母的长度"
          style="width: 20%; float: left"
        />
        <el-button
          type="primary"
          style="float: left; margin-left: 20px;"
          @click="sendRandomLetter()"
        >生成</el-button>
        <el-button
          v-clipboard:copy="letterResult"
          v-clipboard:error="onError"
          v-clipboard:success="onCopy"
          style="float:right"
          size="mini"
          type="text"
          icon="el-icon-copy-document"
          round
          class="copy-btn"
        >复制</el-button>
      </div>
      <div class="div-line" style="height: 100px">
        <el-input
          v-model="letterResult"
          type="textarea"
          :rows="3"
          placeholder="生成的数据"
        />
      </div>
    </div>
  </div>
</template>

<script>
import jsonViewer from 'vue-json-viewer'
import { getTestData, getTimeData, getRandomNumberData, getRandomCnData, getRandomLetterData } from '@/api/tests'

export default {
  components: {
    jsonViewer
  },
  data() {
    return {
      testDataType: '',
      props: { multiple: true },
      options: [
        {
          value: 'name',
          label: '中文姓名'
        },
        {
          value: 'telephone',
          label: '电话号码'
        },
        {
          value: 'address',
          label: '地址'
        },
        {
          value: 'id_card',
          label: '身份证号码'
        },
        {
          value: 'country',
          label: '国家'
        },
        {
          value: 'province',
          label: '省'
        },
        {
          value: 'city',
          label: '市'
        },
        {
          value: 'postcode',
          label: '邮编'
        }
      ],
      dataResult: '',
      time_value: undefined,
      timeTypeOption: [
        {
          time_value: 1,
          label: '时间戳-秒'
        },
        {
          time_value: 2,
          label: '时间戳-毫秒'
        },
        {
          time_value: 3,
          label: '格式化时间 年-月-日 时:分:秒'
        },
        {
          time_value: 4,
          label: '格式化时间 年-月-日'
        }
      ],
      getTimeData: '',
      numberLength: '',
      numberResult: '',
      cnLength: '',
      cnResult: '',
      letterLength: '',
      letterResult: '',
      timeLineHeight: ''
    }
  },
  mounted() {
    // 窗口滑动
    this.timeLineHeight = document.documentElement.clientHeight - 150
    window.onresize = () => { this.timeLineHeight = document.documentElement.clientHeight - 150 }
  },
  methods: {
    // 点击生成数据
    async templateClick() {
      const req = {
        'data_type': this.testDataType.toString()
      }
      const resp = await getTestData(req)
      if (resp.success === true) {
        // this.dataResult = JSON.stringify(resp.result, null, 2)
        this.dataResult = resp.result
      } else {
        this.$message.error('生成失败！')
      }
    },
    // 复制成功时的回调函数
    onCopy(e) {
      this.$message.success('内容已复制到剪切板！')
    },
    // 复制失败时的回调函数
    onError(e) {
      this.$message.error('抱歉，复制失败！')
    },
    // 选中项，生成对应的时间数据
    changeTimeData() {
      this.getTimeDataInfo()
    },
    // 选中选项，生成对应的基础数据
    changeBaseData() {
      this.getBaseDataInfo()
    },
    async getTimeDataInfo() {
      const resp = await getTimeData(this.time_value)
      if (resp.success === true) {
        this.getTimeData = resp.result.time_data
      }
    },
    async sendRandomNumber() {
      const resp = await getRandomNumberData(this.numberLength)
      if (resp.success === true) {
        this.numberResult = resp.result.number
      } else {
        this.$message.error('生成失败！')
      }
    },
    async sendRandomCn() {
      const resp = await getRandomCnData(this.cnLength)
      if (resp.success === true) {
        this.cnResult = resp.result.cn
      } else {
        this.$message.error('生成失败！')
      }
    },
    async sendRandomLetter() {
      const resp = await getRandomLetterData(this.letterLength)
      if (resp.success === true) {
        this.letterResult = resp.result.letters
      } else {
        this.$message.error('生成失败！')
      }
    }
  }
}
</script>

<style>
  .text {
    font-size: 14px;
  }

  .item {
    padding: 18px 0;
  }

  .box-card {
    width: 100%;
  }
</style>
