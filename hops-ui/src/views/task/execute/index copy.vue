<template>
  <div class="app-container">
    <el-card class="box-card">
      <div style="margin:30px 200px 30px 50px; min-width:500px; max-width:800px;">
        <el-form ref="form" :model="form" :rules="rules" label-width="100px">
          <el-form-item label="脚本名称:" prop="scriptName">
            <el-input v-model="form.scriptName" />
          </el-form-item>
          <el-form-item label="服务器账户:" prop="scriptUser">
            <el-select v-model="form.scriptUser" placeholder="请选择执行用户">
              <el-option label="root" value="root" />
              <el-option label="user1" value="user1" />
            </el-select>
          </el-form-item>
          <el-form-item label="目标服务器:" prop="scriptHost">
            <!-- <el-input v-model="form.scriptHost" /> -->
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
          <el-form-item label="脚本来源:" prop="scriptSource">
            <el-radio-group v-model="form.scriptSource">
              <el-radio v-model="radio" label="handwork">手工录入</el-radio>
              <el-radio v-model="radio" label="clone">脚本克隆</el-radio>
              <el-radio v-model="radio" label="local">本地脚本</el-radio>
              <el-radio v-model="radio" label="public">公共脚本</el-radio>
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
          <el-form-item v-if="form.scriptSource == 'public'" label="公共脚本">
            <el-select v-model="form.region" placeholder="请选择脚本">
              <el-option label="脚本1" value="shanghai" />
              <el-option label="脚本2" value="beijing" />
            </el-select>
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
          <el-form-item label="脚本参数:">
            <el-input v-model="form.parameter" />
          </el-form-item>
          <el-form-item label="超时时间(s):">
            <el-input v-model="form.timeout" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('form')">执行脚本</el-button>
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
import "codemirror/mode/shell/shell.js";
import "codemirror/mode/python/python.js";
import "codemirror/mode/javascript/javascript.js";
import "codemirror/theme/cobalt.css";
import "codemirror/addon/selection/active-line";
import { fastExecuteScript } from "@/api/task/execute";
import { getHostList } from "@/api/assets/host";

export default {
  data() {
    // const data = [
    //   { label: '10.0.0.1/game1', key: '10.0.0.1' },
    //   { label: '10.0.0.1', key: '10.0.0.2' },
    //   { label: '10.0.0.1', key: '10.0.0.3' },
    //   { label: '10.0.0.1', key: '10.0.0.4' },
    //   { label: '10.0.0.1', key: '10.0.0.5' },
    //   { label: '10.0.0.1', key: '10.0.0.6' }
    // ]
    return {
      dialogVisible: false,
      data: null,
      // value: [],
      len: null,
      cmOptions: {
        // codemirror options
        tabSize: 4,
        mode: "text/shell",
        theme: "cobalt",
        lineNumbers: true,
        line: true,
        lineWrapping: true,
        styleActiveLine: true
        // more codemirror options, 更多 codemirror 的高级配置...
      },
      form: {
        scriptName: "",
        scriptUser: "",
        scriptHost: [],
        delivery: false,
        // value: [],
        scriptSource: "",
        scriptype: "",
        scriptContent: "",
        parameter: ""
      },
      rules: {
        scriptName: [
          { required: true, message: "请输入脚本名称", trigger: "blur" }
        ],
        scriptUser: [
          { required: true, message: "请选择执行用户", trigger: "change" }
        ],
        scriptHost: [
          { required: true, message: "请选择目标主机", trigger: "blur" }
        ],
        scriptSource: [
          { required: true, message: "请选择脚本来源", trigger: "change" }
        ],
        scriptype: [
          { required: true, message: "请选择脚本类型", trigger: "change" }
        ]
      }
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          fastExecuteScript(this.form)
            .then(response => {
              if (response.code) {
                this.$message.success("执行脚本已提交");
              }
            })
            .catch(err => {
              console.log(err);
            });
          this.$router.push({ path: "/taskManager/taskInstanceList" });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    fetchData() {
      getHostList().then(response => {
        this.data = response.data.items;
      });
    },
    submit(scriptHost) {
      console.log(this.form.scriptHost.length);
      this.len = this.form.scriptHost.length;
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    shellCode(formName) {
      this.form.scriptContent = "#!/bin/bash";
    },
    pythonCode(formName) {
      this.form.scriptContent = "#!/user/bin/env python";
    },
    handleClose(done) {
      this.$confirm("确认关闭？")
        .then(_ => {
          done();
        })
        .catch(_ => {});
    }
  }
};
</script>
<style lang="scss" scoped>
.code-mirror {
  font-size: 22px;
  line-height: 120%;
}
</style>

