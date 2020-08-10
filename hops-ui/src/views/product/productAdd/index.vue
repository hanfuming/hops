<template>
  <div class="app-container">
    <el-card class="box-card">
      <div style="margin:30px 200px 30px 50px; min-width:500px; max-width:800px;">
        <el-form
          ref="ruleForm"
          :model="ruleForm"
          :rules="rules"
          label-width="100px"
          class="demo-ruleForm"
        >
          <el-form-item label="项目名称" prop="proName">
            <el-input v-model="ruleForm.proName" />
          </el-form-item>
          <el-form-item label="父项目" prop="parentId">
            <el-select v-model="ruleForm.parentId" placeholder="请选择父项目">
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
            <el-button type="primary" @click="submitForm(ruleForm)">申请</el-button>
            <el-button @click="resetForm('ruleForm')">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>
<script>
import { getProductParent } from '@/api/assets/productadd'
import { ProductAdd } from '@/api/assets/productadd'

export default {
  data() {
    return {
      options: [],
      ruleForm: {
        proName: '',
        parentId: '',
        leader: '',
        phone: '',
        email: '',
        status: ''
      },
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
      }
    }
  },
  created() {
    this.productData()
  },
  methods: {
    submitForm(formName) {
      ProductAdd(formName)
        .then(response => {
          if (response.code) {
            this.$message.success('申请已提交')
          }
        })
        .catch(err => {
          console.log(err)
        })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    productData() {
      getProductParent().then(response => {
        const respData = response.data.items
        this.options = respData
      })
    }
  }
}
</script>
