<template>
  <div class="data-search">
    <div style="height: 50px; margin-top: 10px;">
      <span style="float: left; line-height: 36px;">搜索条件：</span>
      <el-input
        v-model="searchKey"
        placeholder="请输入搜索条件"
        style="width: 35%; float: left"
      />
      <span style="float: left; line-height: 36px; margin-left: 20px;">条件赋值：</span>
      <el-input
        v-model="searchValue"
        placeholder="请输入条件赋值"
        style="width: 35%; float: left"
      />
      <el-button
        type="primary"
        style="float: left; margin-left: 20px;"
        @click="searchClick()"
      >生成</el-button>
      <el-button
        v-clipboard:copy="JSON.stringify(searchResult)"
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
    <el-card class="box-card" style="height: 580px; overflow-y: auto;">
      <div v-for="(item, index) in searchResult" :key="index" class="text item">
        {{ item }}
      </div>
    </el-card>
    <div class="dialog-footer" style="float: right; margin-top: 20px;">
      共【{{ num }}】条
    </div>
  </div>
</template>

<script>
import { getDataSearchList } from '@/api/tests'

export default {
  data() {
    return {
      templateDataResult: '',
      searchKey: '',
      searchValue: '',
      searchResult: [],
      num: 0
    }
  },
  mounted() {
  },
  methods: {
    async searchClick() {
      const req = {
        'search_data_key': this.searchKey,
        'search_data_value': this.searchValue
      }
      const resp = await getDataSearchList(req)
      if (resp.success === true) {
        this.searchResult = resp.result
        this.num = resp.result.length
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
