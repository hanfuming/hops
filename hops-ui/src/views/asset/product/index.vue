<template>
  <div class="app-container">
    <el-form :inline="true" :model="formInline" class="demo-form-inline">
      <el-form-item label="项目名称">
        <el-input v-model="formInline.user" size="small" placeholder="项目名称" />
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="formInline.region" size="small" placeholder="状态">
          <el-option label="测试中" value="testing" />
          <el-option label="已上线" value="online" />
          <el-option label="已下线" value="offling" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="small" @click="onSubmit">查询</el-button>
        <el-button
          type="primary"
          icon="el-icon-plus"
          size="small"
          @click="handleAdd"
        >新增</el-button>
      </el-form-item>
    </el-form>
    <el-table
      v-loading="listLoading"
      element-loading-text="数据加载中"
      class="table-expand"
      :data="deptOptions"
      style="width: 100%;margin-bottom: 20px;"
      row-key="proId"
      :default-expand-all="true"
      :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
    >
      <el-table-column prop="proName" label="项目名称" width="180" />
      <el-table-column prop="status" label="状态">
        <template slot-scope="scope">
          <span>{{ scope.row.status == '0' ? '已上线' : '测试中' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button type="text" icon="el-icon-view" size="small" @click="handleView(scope.row)">详细</el-button>
          <el-button
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row);title = '修改项目'"
            size="small"
          >编辑</el-button>
          <el-button
            type="text"
            icon="el-icon-delete"
            @click="deleteProduct(scope.row.id)"
            size="small"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!--添加或修改项目对话框-->
    <el-dialog :title="title" :visible.sync="dialogFormVisible">
      <el-form
        ref="ruleForm"
        :model="ruleForm"
        :rules="rules"
        label-width="100px"
        class="demo-ruleForm"
        size="small"
      >
        <el-form-item label="项目名称" prop="proName">
          <el-input v-model="ruleForm.proName" />
        </el-form-item>
        <el-form-item label="父项目" prop="parentId">
          <el-select v-model="ruleForm.parentId" filterable placeholder="请选择父项目">
            <el-option label="无" value="0"></el-option>
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.proName"
              :value="item.proId"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="项目负责人" prop="leader">
          <el-input v-model="ruleForm.leader" />
        </el-form-item>
        <el-form-item label="负责人电话" prop="phone">
          <el-input v-model.number="ruleForm.phone" />
        </el-form-item>
        <el-form-item label="负责人邮箱" prop="email">
          <el-input v-model="ruleForm.email" />
        </el-form-item>
        <el-form-item label="项目状态" prop="status">
          <el-radio-group v-model="ruleForm.status">
            <el-radio label="0">已上线</el-radio>
            <el-radio label="1">测试中</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="desc">
          <el-input v-model="ruleForm.desc" type="textarea" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm(ruleForm)">提交</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
    <!--添加项目对话框end-->
    <!--项目详细-->
    <el-dialog title="项目详细" :visible.sync="open" width="600px">
      <el-form ref="form" :model="form" label-width="100px" size="mini">
        <el-row>
          <el-col :span="12">
            <el-form-item label="项目名称：">{{ form.proName }}</el-form-item>
            <el-form-item label="项目负责人：">{{ form.leader }}</el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="负责人电话：">{{ form.phone }}</el-form-item>
            <el-form-item label="负责人邮箱：">{{ form.email }}</el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="创建人：">{{ form.createBy }}</el-form-item>
            <el-form-item label="创建时间：">{{ form.createTime }}</el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="项目状态：">
              <div v-if="form.status == 0">已上线</div>
              <div v-else-if="form.status == 1">已下线</div>
              <div v-else-if="form.status == 2">测试中</div>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="open = false">关 闭</el-button>
      </div>
    </el-dialog>
    <!--项目详细end-->
  </div>
</template>

<script>
import { getProductList, productAdd, productDel, productUpdate } from '@/api/assets/product'

export default {
  data() {
    return {
      formInline: {
        user: '',
        region: ''
      },
      deptOptions: null,
      listLoading: true,
      dialogFormVisible: false,
      options: [],
      // 是否显示弹出层
      open: false,
      // 弹出层标题
      title: "",
      ruleForm: {},
      rules: {
        proName: [
          { required: true, message: '请输入项目名称', trigger: 'blur' },
          { max: 25, message: '长度不超过25个字符', trigger: 'blur' }
        ],
        parentId: [
          { required: true, message: '请选择父项目', trigger: 'change' }
        ],
        leader: [
          { required: true, message: '请输入项目负责人', trigger: 'blur' },
          { max: 10, message: '长度不超过10个字符', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入项目负责人电话', trigger: 'blur' },
          { type: 'number', message: '电话必须为数字' }
        ],
        email: [
          { required: true, message: '请输入项目负责人邮箱', trigger: 'blur' },
          { max: 50, message: '长度不超过50个字符', trigger: 'blur' }
        ],
        status: [{ required: true, message: '请选项目状态', trigger: 'change' }]
      },
      form: {},
    }
  },
  created() {
    this.productData()
  },
  methods: {
    // 表单重置
    reset() {
      this.ruleForm = {
        proId: undefined,
        parentId: 0,
        proName: undefined,
        leader: undefined,
        phone: undefined,
        email: undefined,
        status: '0',
        createBy: undefined,
        createTime: undefined
      };
    },
    convertToTreeData(data, pid) {
      const result = []
      let temp = []
      for (let i = 0; i < data.length; i++) {
        if (data[i].parentId === pid) {
          const obj = {
            proName: data[i].proName,
            proId: data[i].proId,
            parentId: data[i].parentId,
            status: data[i].status,
            leader: data[i].leader,
            phone: data[i].phone,
            email: data[i].email,
            createBy: data[i].createBy,
            createTime: data[i].createTime
          }
          temp = this.convertToTreeData(data, data[i].proId)
          if (temp.length > 0) {
            obj.children = temp
          }
          result.push(obj)
        }
      }
      return result
    },
    productData() {
      this.listLoading = true
      getProductList().then(response => {
        const respData = response.data.items
        this.options = respData
        const treeData = this.convertToTreeData(respData, 0)
        this.deptOptions = treeData
        this.listLoading = false
      })
    },
    submitForm: function() {
      this.$refs["ruleForm"].validate(valid => {
        if (valid){
          if (this.ruleForm.proId != undefined){
            productUpdate(this.ruleForm).then(response => {
            if (response.code) {
              this.$message.success('项目已更新')
              this.productData()
              this.dialogFormVisible= false
            }
            });
          } else {
            productAdd(this.ruleForm).then(response => {
            if (response.code) {
              this.$message.success('项目已添加')
              this.productData()
              this.dialogFormVisible= false
            }
            })
            .catch(err => {
              console.log(err)
            })
          }
        }
      })  
    },
    deleteProduct(productId) {
      const proId = { proId: productId }
      this.$confirm('此操作将永久删除该项目, 是否继续?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          productDel(proId)
            .then(response => {
              if (response.code) {
                this.$message.success('项目已删除')
                this.productData()
              }
            })
            .catch(err => {
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
    /** 新增按钮操作 */
    handleAdd(row) {
      this.reset();
      if (row != null) {
        this.ruleForm.parentId = row.proId;
      }
      this.dialogFormVisible = true;
      this.title = "添加菜单";
    },
    /** 详细按钮操作 */
    handleView(row) {
      console.log(row)
      this.open = true;
      this.form = row;
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      this.dialogFormVisible = true;
      this.ruleForm = row;

    },
    onSubmit() {
      console.log('submit!')
    },
    handleClick(row) {
      console.log(row)
    }
  }
}
</script>

