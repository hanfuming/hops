<template>
  <div class="app-container">
    <el-form :inline="true" :model="searchForm" class="demo-form-inline">
      <el-form-item label="脚本名称">
        <el-input v-model="searchForm.name" size="small" placeholder="脚本名称" />
      </el-form-item>
      <el-form-item label="创建人">
        <el-input v-model="searchForm.user" size="small" placeholder="创建人" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="small" @click="onSubmit">查询</el-button>
      </el-form-item>
    </el-form>
    <el-button
      style="float:right"
      type="primary"
      icon="el-icon-plus"
      size="small"
      @click="dialogFormVisible = true"
    >新建脚本</el-button>
    <el-table :data="jobData" style="width: 100%">
      <el-table-column prop="scriptId" label="ID" />
      <el-table-column prop="scriptName" label="脚本名称" />
      <el-table-column prop="user" label="创建人" />
      <el-table-column prop="createTime" label="创建时间" width="180" />
      <el-table-column prop="changeUser" label="最后修改人" />
      <el-table-column prop="changeTime" label="最后修改时间" width="180" />
      <el-table-column label="操作" width="200px;">
        <template slot-scope="scope">
          <el-button type="text" size="small">去执行</el-button>
          <el-divider direction="vertical" />
          <el-button type="text" size="small">编辑</el-button>
          <el-button type="text" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      title="新建脚本"
      width="60%"
      :visible.sync="dialogFormVisible"
      :before-close="handleClose"
    >
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="脚本名称:" prop="scriptName">
          <el-input v-model="form.scriptName" />
        </el-form-item>
        <el-form-item label="脚本来源:" prop="scriptSource">
          <el-radio-group v-model="form.scriptSource">
            <el-radio v-model="radio" label="handwork">手工录入</el-radio>
            <el-radio v-model="radio" label="clone">脚本克隆</el-radio>
            <el-radio v-model="radio" label="local">本地脚本</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="form.scriptSource == 'clone'" label="克隆地址:" label-width="200px">
          <el-input v-model="form.addr" placeholder="克隆地址">
            <el-button slot="append" type="text" style="width:80px;">确定</el-button>
          </el-input>
        </el-form-item>
        <el-form-item v-if="form.scriptSource == 'local'">
          <el-upload
            class="upload-demo"
            action="https://jsonplaceholder.typicode.com/posts/"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            multiple
            :limit="3"
            :on-exceed="handleExceed"
            :file-list="fileList"
          >
            <el-button size="small" type="primary">点击上传</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item label="脚本内容:" prop="scriptype">
          <el-card class="box-card" :body-style="{ padding: '0px' }">
            <div slot="header" class="clearfix" style="height:10px;line-height:10px;">
              <el-radio-group v-model="form.scriptype">
                <el-radio label="shell" @change="shellCode('form')" />
                <el-radio label="python" @change="pythonCode('form')" />
              </el-radio-group>
            </div>
            <div>
              <codemirror v-model="form.scriptContent" :options="cmOptions" class="code-mirror" />
            </div>
          </el-card>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="dialogFormVisible = false">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import 'codemirror/mode/shell/shell.js'
import 'codemirror/mode/python/python.js'
import 'codemirror/mode/javascript/javascript.js'
import 'codemirror/theme/cobalt.css'
import 'codemirror/addon/selection/active-line'
export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        执行成功: 'success',
        执行失败: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      cmOptions: {
        // codemirror options
        tabSize: 4,
        mode: 'text/shell',
        theme: 'cobalt',
        lineNumbers: true,
        line: true,
        lineWrapping: true,
        styleActiveLine: true
        // more codemirror options, 更多 codemirror 的高级配置...
      },
      searchForm: {
        name: '',
        user: ''
      },
      form: {
        scriptName: '',
        scriptUser: '',
        scriptHost: '',
        delivery: false,
        type: [],
        scriptSource: '',
        scriptype: '',
        scriptContent: ''
      },
      rules: {
        scriptName: [
          { required: true, message: '请输入脚本名称', trigger: 'blur' }
        ],
        scriptSource: [
          { required: true, message: '请选择脚本来源', trigger: 'change' }
        ],
        scriptype: [
          { required: true, message: '请选择脚本类型', trigger: 'change' }
        ]
      },
      jobData: [
        {
          scriptId: '111',
          scriptName: '版本更新',
          user: 'admin',
          createTime: '2020-04-10-20:22',
          changeUser: 'admin',
          changeTime: '2020-04-10-19:22'
        },
        {
          scriptId: '112',
          scriptName: '版本更新',
          user: 'admin',
          createTime: '2020-04-10-20:22',
          changeUser: 'admin',
          changeTime: '2020-04-10-19:22'
        }
      ],
      listLoading: true,
      dialogFormVisible: false
    }
  },
  // created() {
  //   this.productData()
  // },
  methods: {
    // productData() {
    //   this.listLoading = true
    //   getProductList().then(response => {
    //     this.deptOptions = response.data.items
    //     this.listLoading = false
    //   })
    // },
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
        })
        .catch(_ => {})
    },
    onSubmit() {
      console.log('submit!')
    }
    // handleClick(row) {
    //   console.log(row)
    // }
  }
}
</script>

