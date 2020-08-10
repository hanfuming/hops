<template>
  <div class="app-container">
    <el-card class="box-card" style="margin-bottom:10px;">
      <div slot="header" class="clearfix">
        <span>作业信息</span>
      </div>
      <div :data="job">
        <el-row>
          <el-col :span="8">
            作业名称：
            <i>{{ job.name }}</i>
          </el-col>
          <el-col :span="8">
            执行结果：
            <i style="color:#409EFF">{{ job.result }}</i>
          </el-col>
          <el-col :span="8">
            启动人：
            <i>{{ job.user }}</i>
          </el-col>
        </el-row>
        <el-row style="margin-top:15px;">
          <el-col :span="8">
            开始时间：
            <i>{{ job.startTime }}</i>
          </el-col>
          <el-col :span="8">
            结束时间：
            <i>{{ job.endTime }}</i>
          </el-col>
          <el-col :span="8">
            总耗时：
            <i>{{ job.totalTime }}</i>
          </el-col>
        </el-row>
      </div>
    </el-card>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>作业步骤</span>
      </div>
      <div>
        <el-steps :active="active" finish-status="success" direction="vertical">
          <el-step v-for="item in stepList" :key="item">
            <template slot="description">
              <div>
                <el-card class="box-card" :body-style="{ padding: '0px' }">
                  <div slot="header" class="clearfix" style="font-size:16px;">
                    <span>{{ item.stepName }}</span>
                  </div>
                  <div>
                    <el-table
                      :data="item.step"
                      style="width: 96%;margin-left:20px;margin-right:20px;"
                    >
                      <el-table-column prop="orderNum" label="序号" width="50px;" />
                      <el-table-column prop="scriptName" label="脚本名称" />
                      <el-table-column prop="hostNum" label="执行主机数" width="100px;" />
                      <el-table-column prop="startTime" label="开始时间" />
                      <el-table-column prop="endTime" label="结束时间" />
                      <el-table-column prop="totalTime" label="总耗时" width="80px;" />
                      <el-table-column prop="status" label="状态" />
                      <el-table-column label="操作" width="140px">
                        <template slot-scope="scope">
                          <el-button type="text" size="small">执行详情</el-button>
                          <el-button type="text" size="small">强制终止</el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                  </div>
                </el-card>
              </div>
            </template>
          </el-step>
          <el-step icon="el-icon-circle-check" />
        </el-steps>
      </div>
    </el-card>
  </div>
</template>
<script>
export default {
  data() {
    return {
      job: {
        name: '版本更新',
        result: '正在执行',
        user: 'root',
        startTime: '2020-04-10-20:12:21',
        endTime: '2020-04-10-20:12:25',
        totalTime: '30s'
      },
      active: 1,
      stepList: [
        {
          stepName: '停服',
          step: [
            {
              orderNum: '1',
              scriptName: 'stop.sh',
              hostNum: '1',
              startTime: '2020-2-10-15:23',
              endTime: '2020-2-10-15:23',
              totalTime: '32',
              status: '执行中'
            },
            {
              orderNum: '2',
              scriptName: 'stop.sh',
              hostNum: '1',
              startTime: '2020-2-10-15:23',
              endTime: '2020-2-10-15:23',
              totalTime: '32',
              status: '执行中'
            }
          ]
        },
        {
          stepName: '开服',
          step: [
            {
              orderNum: '1',
              scriptName: 'stop.sh',
              hostNum: '1',
              startTime: '2020-2-10-15:23',
              endTime: '2020-2-10-15:23',
              totalTime: '32',
              status: '执行中'
            }
          ]
        }
      ]
    }
  },
  computed: {},
  watch: {},
  mounted() {},
  methods: {
    next() {
      if (this.active++ > 2) this.active = 0
    }
  }
}
</script>

