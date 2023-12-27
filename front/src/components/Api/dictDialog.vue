<template>
  <div>
    <el-table
      :data="dictData"
      style="width: 100%"
    >
      <el-table-column label="Name" width="300">
        <template slot-scope="scope">
          <el-input
            v-model="scope.row.name"
            size="small"
            placeholder="请输入Name"
          />
        </template>
      </el-table-column>
      <el-table-column label="Value" width="300">
        <template slot-scope="scope">
          <el-input
            v-model="scope.row.value"
            size="small"
            placeholder="请输入value"
          />
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button
            v-if="scope.row.show === 'true'"
            type="success"
            size="mini"
            icon="el-icon-circle-plus-outline"
            plain
            @click="pushNewHeaders(scope.$index)"
          />
          <el-button
            type="danger"
            size="mini"
            icon="el-icon-delete"
            plain
            @click="deleteHeaders(scope.$index)"
          />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'DictDialog',
  props: {
    dictData: {
      type: Array,
      default: null
    }
  },
  data() {
    return {
    }
  },
  methods: {
    pushNewHeaders(index) {
      const list = this.dictData
      list[index].show = 'false'
      list.push({
        name: '',
        value: '',
        show: 'true'
      })
      this.dictData = list
    },
    deleteHeaders(index) {
      const list = this.dictData
      if (index === 0 && list.length === 1) {
        list.splice(index, 1)
        list.push({
          name: '',
          value: '',
          show: 'true'
        })
      } else {
        list.splice(index, 1)
      }
      if (index === list.length) {
        list[index - 1].show = 'true'
      }
      this.dictData = list
    }
  }
}
</script>
