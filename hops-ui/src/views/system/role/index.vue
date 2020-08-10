<template>
  <div class="app-container">
    <el-form :inline="true" :model="searchForm" class="demo-form-inline">
      <el-form-item label="角色名称">
        <el-input v-model="searchForm.name" size="small" placeholder="角色名称" />
      </el-form-item>
      <el-form-item label="字符权限">
        <el-input v-model="searchForm.phone" size="small" placeholder="字符权限" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="small" @click="onSubmit">查询</el-button>
      </el-form-item>
    </el-form>
    <el-button v-hasPermi="['system:role:add']" type="primary" icon="el-icon-plus" size="mini" @click="handleAdd">新增</el-button>
    <el-table :data="roleData" style="width: 100%">
      <el-table-column prop="id" label="角色编号" />
      <el-table-column prop="roleName" label="角色名称" />
      <el-table-column prop="roleKey" label="权限字符" />
      <el-table-column prop="status" label="状态">
        <template slot-scope="scope">
          <span>{{ scope.row.status == '0' ? '启用' : '停用' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="300px;">
        <template slot-scope="scope">
          <el-button v-if="scope.row.roleKey !== 'admin'" v-hasPermi="['system:role:edit']" type="text" size="small" icon="el-icon-edit" @click="handleUpdate(scope.row)">编辑</el-button>
          <el-button v-if="scope.row.roleKey !== 'admin'" v-hasPermi="['system:role:remove']" type="text" size="small" icon="el-icon-delete" @click="deleteRole(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!--添加角色对话框-->
    <el-dialog :title="title" :visible.sync="open" width="50%" :before-close="handleClose">
      <el-form
        ref="addRoleForm"
        :model="addRoleForm"
        label-width="100px"
      >
        <el-form-item label="角色名称" prop="roleName">
          <el-input v-model="addRoleForm.roleName" />
        </el-form-item>
        <el-form-item label="权限字符" prop="roleKey">
          <el-input v-model="addRoleForm.roleKey" />
        </el-form-item>
        <el-form-item label="菜单权限">
          <el-tree
            ref="menu"
            :data="menuOptions"
            show-checkbox
            node-key="id"
            empty-text="加载中，请稍后"
            :props="defaultProps"
          />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="addRoleForm.remark" type="textarea" placeholder="请输入内容" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="open = false">取 消</el-button>
        <el-button type="primary" @click="open = false;submitForm(addRoleForm)">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>

import { listRole, getRole, addRole, updateRole, delRole } from '@/api/system/role'
import { treeselect, roleMenuTreeselect } from '@/api/system/menu'
export default {
  data() {
    return {
      searchForm: {
        name: '',
        phone: '',
        email: ''
      },
      // 菜单列表
      menuOptions: [],
      addRoleForm: {},
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      dialogVisible: false,
      roleData: null,
      listLoading: true,
      // 是否显示弹出层
      open: false
    }
  },
  created() {
    this.getRoleData()
  },
  methods: {
    getRoleData() {
      this.listLoading = true
      listRole().then(response => {
        this.roleData = response.data.items
        this.listLoading = false
      })
    },
    /** 查询菜单树结构 */
    getMenuTreeselect() {
      treeselect().then(response => {
        this.menuOptions = response.data
      })
    },
    /** 根据角色ID查询菜单树结构 */
    getRoleMenuTreeselect(roleId) {
      roleMenuTreeselect(roleId).then(response => {
        this.menuOptions = response.data
        this.$refs.menu.setCheckedKeys(response.checkedKeys)
      })
    },
    // 所有菜单节点数据
    getMenuAllCheckedKeys() {
      // 目前被选中的菜单节点
      const checkedKeys = this.$refs.menu.getHalfCheckedKeys()
      // 半选中的菜单节点
      const halfCheckedKeys = this.$refs.menu.getCheckedKeys()
      checkedKeys.unshift.apply(checkedKeys, halfCheckedKeys)
      return checkedKeys
    },
    // 表单重置
    reset() {
      if (this.$refs.menu !== undefined) {
        this.$refs.menu.setCheckedKeys([])
      }
      this.addRoleForm = {
        roleId: undefined,
        roleName: undefined,
        roleKey: undefined,
        menuIds: [],
        remark: undefined
      }
      // this.$refs.addRoleForm.resetFields()
    },
    /** 新增按钮操作 */
    handleAdd() {
      // this.reset();
      this.getMenuTreeselect()
      this.open = true
      this.title = '添加角色'
    },
    onSubmit() {
      console.log('submit!')
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset()
      const roleId = row.id || this.ids
      this.$nextTick(() => {
        this.getRoleMenuTreeselect(roleId)
      })
      getRole(roleId).then(response => {
        this.form = response.data
        this.open = true
        this.title = '修改角色'
      })
    },
    /** 提交按钮 */
    submitForm: function() {
      this.$refs['addRoleForm'].validate(valid => {
        if (valid) {
          if (this.addRoleForm.roleId !== undefined) {
            this.addRoleForm.menuIds = this.getMenuAllCheckedKeys()
            updateRole(this.addRoleForm).then(response => {
              if (response.code === 200) {
                this.msgSuccess('修改成功')
                this.getList()
                this.open = false
              } else {
                this.msgError(response.msg)
              }
            })
          } else {
            this.addRoleForm.menuIds = this.getMenuAllCheckedKeys()
            addRole(this.addRoleForm).then(response => {
              if (response.code) {
                this.$message.success('新增成功')
                this.getRoleData()
                this.open = false
              } else {
                this.msgError(response.msg)
              }
            })
          }
        }
      })
    },
    deleteRole(roleId) {
      const rId = { roleId: roleId }
      this.$confirm('此操作将永久删除该角色, 是否继续?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          delRole(rId)
            .then(response => {
              if (response.code) {
                this.$message.success('角色已删除')
                this.getRoleData()
              }
            })
            .catch(err => {
              this.$message.info('此角色不能被删除', err)
              console.log(err)
            })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    }
    // handleClick(row) {
    //   console.log(row)
    // }
  }
}
</script>

