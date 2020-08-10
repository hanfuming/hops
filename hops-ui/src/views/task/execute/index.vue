<template>
  <div class="app-container">
    <el-card class="box-card">
      <div style="margin:30px 200px 30px 50px; min-width:500px; max-width:800px;">
        <el-form :model="execute_form" ref="execute_form" :rules="execute_form_rules" label-width="100px">
          <el-form-item label="目标主机:" prop="execute_host">
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
          <el-form-item label="远程命令:" prop="execute">
            <el-input v-model="execute_form.execute" />
          </el-form-item>
          <el-form-item>
            <el-button style="float:right;" type="primary" @click="submitForm('execute_form')">立即执行</el-button>
          </el-form-item>
        </el-form>
        <el-form :model="output" label-width="100px">
          <el-form-item label="执行结果:">
            <el-card v-loading="loading" element-loading-background="rgba(0, 0, 0, 0.8)" class="box-card" :body-style="{ padding: '0px' }">
              <div>
                <codemirror v-model="output.execute_output" :options="cmOptions" class="code-mirror" />
              </div>
            </el-card>
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
        v-model="execute_form.execute_host"
        :props="{
          key: 'innerIP',
          label: 'innerIP'
        }"
        :titles="['主机列表', '已选主机']"
        filterable
        filter-placeholder="请输入ip"
        :data="data"
      />
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submit('execute_host');dialogVisible = false">确 定</el-button>
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
import { executeCmd } from "@/api/task/execute";
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
      loading: false,
      cmOptions: {
        // codemirror options
        tabSize: 4,
        mode: "text/shell",
        theme: "cobalt",
        lineSeparator: "\\n",
        // lineNumbers: true,
        line: true,
        lineWrapping: true,
        styleActiveLine: true,
        // more codemirror options, 更多 codemirror 的高级配置...
      },
      execute_form: {
        execute_host: [],
        execute: ""
      },
      output: {
        execute_output: null,
      },
      execute_form_rules: {
        execute: [
          { required: true, message: "请输入执行命令", trigger: "blur" },
        ],
        execute_host: [
          { required: true, message: "请选择目标主机", trigger: "blur" },
        ],
      },
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.loading = true
          executeCmd(this.execute_form)
            .then((response) => {
              if (response.code) {
                this.output.execute_output=response.data
                this.$message.success("执行完毕");
                this.loading = false
              } 
            })
            .catch((err) => {
              this.loading = false
            });
          // this.$router.push({ path: "/taskManager/taskInstanceList" });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    fetchData() {
      getHostList().then((response) => {
        this.data = response.data.items;
      });
    },
    submit(execute_host) {
      console.log(this.execute_form.execute_host.length);
      this.len = this.execute_form.execute_host.length;
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
        .then((_) => {
          done();
        })
        .catch((_) => {});
    },
  },
};
</script>
<style lang="scss" scoped>
.code-mirror {
  font-size: 14px;
  line-height: 120%;
}
</style>

