<template>
  <div class="app-container">
    <div style="float:left;width:25%;">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>个人信息</span>
        </div>
        <div>
          <div style="text-align:center">
            <el-avatar :size="120" src="https://empty" @error="errorHandler">
              <img src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png">
            </el-avatar>
          </div>
          <ul style="padding-left: 0;">
            <li class="userinfolist">用户名称：{{ UserInfo.name }}</li>
            <li class="userinfolist">手机号码：{{ }}</li>
            <li class="userinfolist">用户邮箱：{{ }}</li>
            <li class="userinfolist">所属部门：{{ }}</li>
            <li class="userinfolist">所属角色：{{ UserInfo.roles }}</li>
            <li class="userinfolist">创建日期：{{ $moment().format('YYYY-MM-DD hh:mm') }}</li>
          </ul>
        </div>
      </el-card>
    </div>
    <div style="float:left;width:60%;margin-left:20px;">
      <el-card class="box-card" style="height:498px;">
        <div slot="header" class="clearfix">
          <span>基本资料</span>
        </div>
        <div>
          <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="资料管理" name="first">
              <el-form
                ref="ruleForm"
                :model="ruleForm"
                :rules="rules"
                label-width="100px"
                class="demo-ruleForm"
              >
                <el-form-item label="用户昵称" prop="name">
                  <el-input v-model="ruleForm.name" />
                </el-form-item>
                <el-form-item label="手机号码" prop="phone">
                  <el-input v-model="ruleForm.phone" />
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                  <el-input v-model="ruleForm.email" />
                </el-form-item>
                <el-form-item label="性别" prop="six">
                  <el-radio-group v-model="ruleForm.six">
                    <el-radio label="男" />
                    <el-radio label="女" />
                  </el-radio-group>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="submitForm('ruleForm')">保存</el-button>
                  <el-button @click="resetForm('ruleForm')">重置</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            <el-tab-pane label="修改密码" name="second">
              <el-form
                ref="pwdForm"
                :model="pwdForm"
                status-icon
                :rules="pwdRules"
                label-width="100px"
                class="demo-ruleForm"
              >
                <el-form-item label="旧密码" prop="oldPass">
                  <el-input v-model="pwdForm.oldPass" type="password" autocomplete="off" />
                </el-form-item>
                <el-form-item label="新密码" prop="newPass">
                  <el-input v-model="pwdForm.newPass" type="password" autocomplete="off" />
                </el-form-item>
                <el-form-item label="确认密码" prop="checkPass">
                  <el-input v-model="pwdForm.checkPass" type="password" autocomplete="off" />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="changPwd('pwdForm')">确认修改</el-button>
                  <el-button @click="resetPwdForm('pwdForm')">重置</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-card>
    </div>
  </div>
</template>
<script>
import { listUser } from '@/api/system/user'
import { changPass } from '@/api/system/user'
export default {
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.pwdForm.checkPass !== '') {
          this.$refs.pwdForm.validateField('checkPass')
        }
        callback()
      }
    }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.pwdForm.newPass) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      ruleForm: {
        name: '',
        phone: '',
        email: '',
        six: ''
      },
      rules: {
        name: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
        phone: [
          { required: true, message: '请输入手机号码', trigger: 'blur' },
          { min: 11, max: 11, message: '长度为11个字符', trigger: 'blur' }
        ],
        email: [{ required: true, message: '请输入邮箱地址', trigger: 'blur' }],
        six: [{ required: true, message: '请选择性别', trigger: 'change' }]
      },
      pwdForm: {
        userName: '',
        oldPass: '',
        newPass: '',
        checkPass: ''
      },
      pwdRules: {
        oldPass: [{ required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '长度必须大于6个字符', trigger: 'blur' }],
        newPass: [
          { validator: validatePass, trigger: 'blur' },
          { min: 6, message: '长度必须大于6个字符', trigger: 'blur' }
        ],
        checkPass: [
          { validator: validatePass2, trigger: 'blur' }
        ]
      },
      activeName: 'first',
      UserInfo: null,
      queryParams: {
        userName: 'admin'
      }
    }
  },
  created() {
    this.getUserData()
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
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    submitPwdForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          alert('submit!')
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetPwdForm(formName) {
      this.$refs[formName].resetFields()
    },
    getUserData() {
      this.listLoading = true
      listUser().then(response => {
        const respData = response.data
        console.log(respData)
        this.UserInfo = respData
        this.ruleForm.name = this.UserInfo.name
        this.listLoading = false
      })
    },
    changPwd(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          const user = this.pwdForm
          user.userName = this.UserInfo[0].userName
          changPass(user)
            .then(response => {
              if (response.code) {
                this.$message.success('用户密码已修改')
              }
            })
            .catch(err => {
              console.log(err)
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style scoped>
.userinfolist {
  border-top: 1px solid #e7eaec;
  list-style: none;
  padding: 11px 0;
  font-size: 16px;
  border-bottom: 1px solid #e7eaec;
  margin-bottom: -1px;
}
</style>

