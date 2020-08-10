<template>
  <div class="app-container">
    <el-card class="box-card">
      <div style="margin:10px 200px 30px 50px; min-width:500px; max-width:800px;">
        <el-form ref="form" :model="form" :rules="rules" label-width="100px" label-position="left">
          <el-form-item label="作业名称:" prop="scriptName">
            <el-input v-model="form.scriptName" />
          </el-form-item>
          <div style="margin-top:30px;">
            <el-card class="box-card">
              <div slot="header" class="clearfix" style="line-height:32px;">
                <span>
                  <i class="el-icon-folder" />源文件
                </span>
                <span
                  slot="tip"
                  style="padding-left:20px;"
                  class="el-upload__tip"
                >注意：本地文件上传会有同名文件覆盖风险</span>
              </div>
              <div>
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
                  <el-button size="small" type="primary">
                    <i class="el-icon-upload2" />添加本地文件
                  </el-button>
                </el-upload>
              </div>
            </el-card>
          </div>
          <div style="margin-top:30px;">
            <el-card class="box-card">
              <div slot="header" class="clearfix">
                <span>
                  <i class="el-icon-folder" />目标文件
                </span>
              </div>
              <div>
                <el-form-item label="目标路径:" prop="scriptName">
                  <el-input v-model="form.scriptName" />
                </el-form-item>
                <el-form-item label="服务器账户:" prop="scriptName">
                  <el-input v-model="form.scriptName" />
                </el-form-item>
                <el-form-item label="目标机器:" prop="scriptName">
                  <el-button type="primary" size="medium" @click="dialogVisible = true">
                    <span v-if="len">
                      <i class="el-icon-s-platform" />
                      &nbsp;已选择{{ len }}台
                    </span>
                    <span v-else>
                      <i class="el-icon-s-platform" />&nbsp;选择服务器
                    </span>
                  </el-button>
                </el-form-item>
              </div>
            </el-card>
          </div>
          <el-form-item style="margin-top:30px;">
            <el-button type="primary" @click="submitForm('form')">开始分发</el-button>
            <el-button type="danger" @click="resetForm('form')">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
    <el-dialog
      title="选择目标服务器"
      :visible.sync="dialogVisible"
      width="630px"
      :before-close="handleClose"
    >
      <el-transfer
        v-model="form.scriptHost"
        :props="{
          key: 'innerIP',
          label: 'innerIP'
        }"
        filterable
        :filter-method="filterMethod"
        filter-placeholder="请输入名称"
        :data="data"
      />
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submit(scriptHost);dialogVisible = false">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { getHostList } from '@/api/assets/host'

export default {
  data() {
    return {
      dialogVisible: false,
      data: null,
      len: null,
      fileList: [
        {
          name: 'food.jpeg',
          url:
            'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
        },
        {
          name: 'food2.jpeg',
          url:
            'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
        }
      ],
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
        scriptUser: [
          { required: true, message: '请选择执行用户', trigger: 'change' }
        ],
        scriptHost: [
          { required: true, message: '请选择目标主机', trigger: 'blur' }
        ],
        scriptSource: [
          { required: true, message: '请选择脚本来源', trigger: 'change' }
        ],
        scriptype: [
          { required: true, message: '请选择脚本类型', trigger: 'change' }
        ]
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          alert('submit!')
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    fetchData() {
      getHostList().then(response => {
        this.data = response.data.items
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
        })
        .catch(_ => {})
    }
  }
}
</script>
