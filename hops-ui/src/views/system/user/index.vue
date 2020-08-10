<template>
  <div class="app-container">
    <el-form :inline="true" :model="searchForm" class="demo-form-inline">
      <el-form-item label="用户名称">
        <el-input v-model="searchForm.name" size="small" placeholder="用户名称" />
      </el-form-item>
      <el-form-item label="手机号码">
        <el-input v-model="searchForm.phone" size="small" placeholder="手机号码" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="small" @click="onSubmit">查询</el-button>
      </el-form-item>
    </el-form>
    <el-button v-hasPermi="['system:user:add']" type="primary" size="small" @click="dialogVisible = true">添加用户</el-button>
    <el-table
      v-loading="listLoading"
      :data="UserList"
      element-loading-text="数据加载中"
      style="width: 100%"
    >
      <el-table-column prop="username" label="用户名称" />
      <el-table-column prop="nickName" label="用户昵称" />
      <el-table-column prop="roles__roleName" label="用户角色" />
      <el-table-column prop="mobile" label="手机号码" />
      <el-table-column prop="status" label="状态">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.status"
            active-value="0"
            inactive-value="1"
            @change="handleStatusChange(scope.row)"
          />
        </template>
      </el-table-column>
      <el-table-column prop="createTime" label="创建时间" width="180">
        <template slot-scope="scope">
          <span>{{ $moment(scope.row.createTime).format('YYYY-MM-DD hh:mm') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="300px;">
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="editDialogVisible = true;handleEdit(scope.row)">编辑</el-button>
          <el-button type="text" size="small" @click="deleteUser(scope.row.username)">删除</el-button>
          <el-button type="text" size="small" @click="resetPwd(scope.row.username)">重置密码</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <el-dialog title="添加用户" :visible.sync="dialogVisible" width="50%" :before-close="handleClose">
      <el-form
        ref="addForm"
        :model="addForm"
        :rules="addRules"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="addForm.username" />
        </el-form-item>
        <el-form-item label="用户角色" prop="roleId">
          <el-select v-model="addForm.roles_id" placeholder="请选择用户角色">
            <el-option
              v-for="item in roleList"
              :key="item.value"
              :label="item.roleName"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogVisible = false;submitForm('addForm')">确 定</el-button>
      </span>
    </el-dialog>
    <!--编辑用户框-->
    <el-dialog title="用户编辑" :visible.sync="editDialogVisible" width="50%" :before-close="handleClose">
      <el-form ref="editUser" :model="editUser" label-width="80px">
        <el-form-item label="用户名称">
          <el-input v-model="editUser.username" />
        </el-form-item>
        <el-form-item label="用户昵称">
          <el-input v-model="editUser.nickName" />
        </el-form-item>
        <el-form-item label="用户角色">
          <el-input v-model="editUser.role" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="editUser.phone" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="editUser.email" />
        </el-form-item>
        <el-form-item label="用户状态" prop="status">
          <el-select v-model="editUser.status" placeholder="请选择用户状态">
            <el-option label="启用" value="0" />
            <el-option label="停用" value="1" />
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editDialogVisible = false">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { adduser } from '@/api/adduser'
import { listUser } from '@/api/system/user'
import { delUser } from '@/api/adduser'
import { resetpasswd } from '@/api/adduser'
import { changUser } from '@/api/adduser'
import { listRole } from '@/api/system/role'

export default {
  data() {
    return {
      searchForm: {
        name: '',
        phone: ''
      },
      editUser: {
        username: '',
        nickName: '',
        role: '',
        phone: '',
        email: '',
        status: ''
      },
      listLoading: true,
      dialogVisible: false,
      editDialogVisible: false,
      UserList: null,
      roleList: [],
      addForm: {
        username: '',
        roles_id: ''
      },
      addRules: {
        username: [
          { required: true, message: '请输入用户名称', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.getUserData()
    // this.roleData()
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
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          adduser(this.addForm)
            .then(response => {
              if (response.code) {
                this.$message.success('用户已添加')
                this.getUserData()
              }
            })
            .catch(err => {
              console.log(err)
            })
          this.$router.push({ path: '/userManage/userList' })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },

    onSubmit() {
      console.log('submit!')
    },

    handleStatusChange(row) {
      const text = row.status === '0' ? '启用' : '停用'
      const that = this
      this.$confirm('确认要' + text + '' + row.username + '用户吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          // return changeUserStatus(row.userId, row.status)
          const user = { userid: row.id, status: row.status }
          changUser(user)
            .then(response => {
              if (response.code) {
                that.$message.success('用户已' + text)
              }
            })
            .catch(err => {
              console.log(err)
            })
        })
        .catch(() => {
          row.status = row.status === '0' ? '1' : '0'
        })
    },
    getUserData() {
      this.listLoading = true
      listUser().then(response => {
        const respData = response.data.items
        this.UserList = respData
        this.listLoading = false
      })
    },
    roleData() {
      listRole().then(response => {
        const respData = response.data.items
        this.roleList = respData
      })
    },
    deleteUser(username) {
      const user = { username: username }
      this.$confirm('此操作将永久删除该用户, 是否继续?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          delUser(user)
            .then(response => {
              if (response.code) {
                this.$message.success('用户已删除')
                this.getUserData()
              }
            })
            .catch(err => {
              this.$message.info('此用户不能被删除', err)
              console.log(err)
            })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    resetPwd(username) {
      const user = { username: username }
      this.$confirm('此操作将重置用户密码, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          resetpasswd(user)
            .then(response => {
              if (response.code) {
                this.$message.success('用户密码已重置')
              }
            })
            .catch(err => {
              this.$message.info('此用户不能重置密码', err)
              console.log(err)
            })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消重置'
          })
        })
    },
    handleEdit: function(row) {
      this.editUser.username = Object.assign(row.username)
      this.editUser.nickName = Object.assign(row.nickName)
      this.editUser.role = Object.assign(row.role)
      this.editUser.phone = Object.assign(row.phone)
      this.editUser.email = Object.assign(row.email)
      this.editUser.status = row.status
    },
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
        })
        .catch(_ => {})
    }
  }
  // handleClick(row) {
  //   console.log(row)
  // }
}
</script>

