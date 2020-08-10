<template>
  <el-card class="box-card-component" style="margin-left:8px;">
      <div slot="header" class="clearfix">
    <span>操作日志</span>
    </div>
    <div class="block">
      <el-timeline>
        <el-timeline-item
          v-for="(activity, index) in activities"
          :key="index"
          :icon="activity.icon"
          :type="activity.type"
          :color="activity.color"
          :size="activity.size"
          :timestamp="activity.timestamp"
        >{{activity.user}}&nbsp;&nbsp;{{ activity.content }}</el-timeline-item>
      </el-timeline>
    </div>
  </el-card>
</template>

<script>
 export default {
    data() {
      return {
        activities: [{
          user: 'hanfuming',
          content: '申请新的项目',
          timestamp: '2018-04-12 20:46',
          size: 'large',
          type: 'primary',
          icon: 'el-icon-more'
        }, {
          user: 'hanfuming',
          content: '支持自定义颜色',
          timestamp: '2018-04-03 20:46',
          color: '#0bbd87'
        }, {
          user: 'hanfuming',
          content: '支持自定义尺寸',
          timestamp: '2018-04-03 20:46',
          size: 'large'
        }, {
          user: 'hanfuming',
          content: '默认样式的节点',
          timestamp: '2018-04-03 20:46'
        },
        {
          user: 'hanfuming',
          content: '默认样式的节点',
          timestamp: '2018-04-03 20:46'
        },
        {
          user: 'hanfuming',
          content: '默认样式的节点',
          timestamp: '2018-04-03 20:46'
        }
        ]
      };
    }
  };
</script>