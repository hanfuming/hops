<template>
  <div>
    <el-card class="box-card">
      <el-form :inline="true" :model="taskform" class="demo-form-inline">
        <el-form-item label="作业名称">
          <el-input v-model="taskform.taskname" placeholder="作业名称" size="small" style="width:500px;" />
        </el-form-item>
        <draggable v-model="taskform.stepList">
          <transition-group tag="div" class="drop-wrapper">
            <div v-for="(ele, index) in taskform.stepList" :key="index" class="items">
              <el-card class="box-card" style="margin-top:10px;">
                <div slot="header" class="clearfix" style="height:20px;line-height:20px;">
                  <el-form-item label="步骤名称:" :prop="'stepList[' + index + '].stepName'">
                    <el-input v-model="ele.stepName" placeholder="步骤名称" size="small" />
                  </el-form-item>
                  <el-button style="float: right;" type="text" @click="delStep(index)">
                    <i class="el-icon-delete" />
                  </el-button>
                </div>
                <div>
                  <div style="margin-bottom:10px;">
                    <span class="itemspantitel">脚本名称</span>
                    <span class="itemspantitel">服务器账户</span>
                    <span class="itemspantitel">服务器数</span>
                    <span sclass="itemspantitel">脚本参数</span>
                  </div>
                  <draggable v-model="ele.step">
                    <transition-group tag="div" class="drop-wrapper">
                      <div
                        v-for="(ele1, index1) in ele.step"
                        :key="index1"
                        style="height:45px;"
                      >
                        <el-form-item>
                          <el-input v-model="ele1.scriptName" placeholder="脚本名称" size="small" />
                        </el-form-item>
                        <el-form-item>
                          <el-input v-model="ele1.user" placeholder="服务器账户" size="small" />
                        </el-form-item>
                        <el-form-item>
                          <el-input v-model="ele1.hostNum" placeholder="服务器数" size="small" />
                        </el-form-item>
                        <el-form-item>
                          <el-input v-model="ele1.parameter" placeholder="脚本参数" size="small" style="width:300px;" />
                        </el-form-item>
                        <el-button style="float: right;" type="text">
                          <i class="el-icon-rank" style="font-size:18px;margin-top:-10px" />
                        </el-button>
                        <el-button style="float: right;" type="text" @click="delItem(index,index1)">
                          <i class="el-icon-close" style="font-size:18px;margin-top:-10px" />
                        </el-button>
                      </div>
                    </transition-group>
                  </draggable>
                  <el-link
                    type="primary"
                    icon="el-icon-plus"
                    :underline="false"
                    @click="addItem(index)"
                  >新增节点</el-link>
                </div>
              </el-card>
            </div>
          </transition-group>
        </draggable>
        <el-button type="success" style="margin-top:20px;" size="small" @click="addStep">添加步骤</el-button>
      </el-form>
    </el-card>
    <div style="text-align:center">
      <el-button type="primary" style="margin-top:20px;" size="small" @click="saveForm">保存</el-button>
      <el-button type="warning" style="margin-top:20px;" size="small"><router-link to="/taskManager/jobdetails/jobstart">去执行</router-link></el-button>
    </div>
  </div>
</template>
<script>
import draggable from 'vuedraggable'

export default {
  components: {
    draggable
  },
  data() {
    return {
      taskform: {
        taskname: '版本更新',
        stepList: [
          {
            stepName: '停服',
            step: [
              {
                scriptName: 'stop.sh',
                user: 'root',
                hostNum: '1',
                parameter: 'stop'
              },
              {
                scriptName: 'update.sh',
                user: 'root',
                hostNum: '1',
                parameter: 'update'
              }
            ]
          },
          {
            stepName: '开服',
            step: [
              {
                scriptName: 'start.sh',
                user: 'root',
                hostNum: '1',
                parameter: 'start'
              },
              {
                scriptName: 'start.sh',
                user: 'root',
                hostNum: '1',
                parameter: 'start'
              }
            ]
          }
        ]
      }
    }
  },
  methods: {
    addStep() {
      var step = {
        stepName: '',
        step: [{	scriptName: '',
          user: '',
          hostNum: '',
          parameter: ''
        }]
      }
      this.taskform.stepList.push(step)
    },
    delStep(index) {
      this.taskform['stepList'].splice(index, 1)
    },
    addItem(stepIndex) {
      var items = {	scriptName: '',
        user: '',
        hostNum: '',
        parameter: ''
      }
      this.taskform.stepList[stepIndex].step.push(items)
    },
    delItem(stepIndex, itemIndex) {
      this.taskform['stepList'][stepIndex]['step'].splice(itemIndex, 1)
    },
    saveForm() {
      console.log(this.taskform)
    }
  }
}
</script>

<style scoped>
.itemspantitel {
  display: inline-block;
  width: 190px;
}
</style>

