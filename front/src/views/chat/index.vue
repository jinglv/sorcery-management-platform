<template>
  <div class="chat">
    <JwChat-index
      ref="jwChat"
      v-model="inputMsg"
      :tale-list="taleList"
      :scroll-type="scrollType"
      :tool-config="tool"
      :placeholder="placeholder"
      :config="config"
      :win-bar-config="winBarConfig"
      :show-right-box="showRightBox"
      width="1200px"
      height="750px"
      @enter="bindEnter"
      @clickTalk="talkEvent"
    />
  </div>
</template>

<script>
import { chatgpt } from '@/api/chat'
import Chatgpt from '../../assets/images/chatgpt.png'
import Keai from '../../assets/images/keai.png'

export default {
  name: 'Chat',
  data() {
    return {
      scrollType: 'scroll', // scroll  noroll 俩种类型
      placeholder: '欢迎使用Chat小助手...',
      inputMsg: '',
      taleList: [],
      tool: {
        showEmoji: false,
        callback: this.toolEvent
      },
      config: {
        img: Chatgpt,
        name: 'Chat',
        dept: '最简单、最便捷',
        callback: this.bindCover,
        historyConfig: {
          show: false,
          tip: '加载更多提示框,可以直接使用组件的',
          callback: this.bindLoadHistory
        }
      },
      showRightBox: false,
      winBarConfig: {
        active: 'win01',
        width: '280px',
        listHeight: '60px',
        list: [
          {
            id: 'win00',
            img: Chatgpt,
            name: 'JwChat',
            dept: '最简单、最便捷',
            readNum: 1
          },
          {
            id: 'win01',
            img: Chatgpt,
            name: '阳光明媚爱万物',
            dept: '沙拉黑油',
            readNum: 12
          }
        ],
        callback: this.bindWinBar
      }
    }
  },
  mounted() {
  },
  methods: {
    /**
     * @description: 点击加载更多的回调函数
     * @param {*}
     * @return {*}
     */
    async bindLoadHistory() {
      const history = new Array(3).fill().map((i, j) => {
        return {
          date: '2020/05/20 23:19:07',
          text: { text: j + new Date() },
          mine: false,
          name: 'JwChat',
          img: 'image/three.jpeg'
        }
      })
      const list = history.concat(this.taleList)
      this.taleList = list
      console.log('加载历史', list, history)
      //  加载完成后通知组件关闭加载动画
      this.config.historyConfig.tip = '加载完成'
      this.$nextTick(() => {
        this.$refs.jwChat.finishPullDown()
      })
    },
    async bindEnter(e) {
      console.log(e)
      const msg = this.inputMsg
      if (!msg) return
      const msgObj = {
        'date': '2020/05/20 23:19:07',
        'text': { 'text': msg },
        'mine': true,
        'name': 'Jean',
        'img': Keai
      }
      this.taleList.push(msgObj)

      const req = {
        'question': msg
      }
      const resp = await chatgpt(req)
      if (resp.success === true) {
        const respObj = {
          'date': '2020/06/25 21:19:07',
          'text': { 'text': resp.result.answer },
          'mine': false,
          'name': 'Chat',
          'img': Chatgpt
        }
        this.taleList.push(respObj)
      }
      this.winBarConfig.list.push(this.taleList)
    },
    // 切换用户窗口，加载对应的历史记录
    bindWinBar(play = {}) {
      const { type, data = {}} = play
      console.log(play)
      if (type === 'winBar') {
        const { id, dept, name, img } = data
        this.config = { ...this.config, id, dept, name, img }
        this.winBarConfig.active = id
        // if (id === 'win00') {
        //   this.taleList = getListArr()
        // } else this.taleList = getListArr((Math.random() * 4) >> 0)
      }
      if (type === 'winBtn') {
        const { target: { id } = {}} = data
        const { list } = this.winBarConfig
        this.winBarConfig.list = list.reduce((p, i) => {
          if (id !== i.id) p.push(i)
          return p
        }, [])
      }
    },
    toolEvent(type, obj) {
      console.log('tools', type, obj)
    },
    talkEvent(play) {
      console.log(play)
    }
  }
}
</script>

<style>
.chat {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  display:flex;
  justify-content:center;
  align-items:center;
}
</style>
