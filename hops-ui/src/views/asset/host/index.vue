<template>
  <div class="app-container">
    <el-row :gutter="20">
      <!--项目树数据-->
      <el-col :span="4" :xs="24">
        <div class="head-container">
          <el-input
            v-model="filterText"
            placeholder="输入关键字进行过滤"
            size="small"
            prefix-icon="el-icon-search"
            style="margin-bottom: 20px"
          />
        </div>
        <div class="head-container">
          <el-tree
            ref="tree"
            :data="deptOptions"
            :props="defaultProps"
            :expand-on-click-node="false"
            :default-expand-all="true"
            :filter-node-method="filterNode"
            @node-click="handleNodeClick"
          />
        </div>
      </el-col>
      <!--用户数据-->
      <el-col :span="20" :xs="24">
        <el-form :inline="true" :model="formInline" class="demo-form-inline">
          <el-form-item label="内网IP">
            <el-input v-model="formInline.innerIP" size="small" placeholder="内网IP" />
          </el-form-item>
          <el-form-item label="外网IP">
            <el-input v-model="formInline.outerIP" size="small" placeholder="外网IP" />
          </el-form-item>
          <el-form-item label="所属云">
            <el-select v-model="formInline.cloud" size="small" placeholder="所属云">
              <el-option label="腾讯云" value="tencent" />
              <el-option label="华为云" value="huawei" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              icon="el-icon-search"
              size="small"
              @click="searchSubmit(formInline)"
            >查询</el-button>
          </el-form-item>
        </el-form>
        <el-row :gutter="10" class="mb8">
          <el-col :span="1.5">
            <el-button type="primary" icon="el-icon-plus" size="small" @click="handleAdd">新增</el-button>
          </el-col>
          <el-col :span="1.5">
            <el-button
              type="success"
              icon="el-icon-edit"
              size="small"
              :disabled="single"
              @click="handleUpdate"
            >修改</el-button>
          </el-col>
          <el-col :span="1.5">
            <el-button
              type="danger"
              icon="el-icon-delete"
              size="small"
              :disabled="multiple"
              @click="handleDelete"
            >删除</el-button>
          </el-col>
          <el-col :span="1.5">
            <el-button
              type="info"
              icon="el-icon-upload2"
              size="small"
              @click="dialogVisible = true"
            >导入</el-button>
          </el-col>
          <el-col :span="1.5">
            <el-button type="warning" icon="el-icon-download" size="small" @click="handleExport">导出</el-button>
          </el-col>
        </el-row>
        <el-table
          v-loading="listLoading"
          :data="tableData"
          type="index"
          style="width: 100%"
          element-loading-text="数据加载中"
        >
          <el-table-column type="selection" width="50" />
          <el-table-column label="ID/名称">
            <template slot-scope="scope">
              <el-tooltip placement="top">
                <div slot="content">
                  id:{{ scope.row.hId }}&nbsp;
                  <i
                    class="el-icon-copy-document"
                    @click="doCopy(scope.row.hId)"
                  />
                </div>
                <span>{{ scope.row.hostName }}</span>
              </el-tooltip>
              <el-tooltip placement="top">
                <div slot="content">{{ scope.row.hostOs }}</div>
                <i class="iconfont" :class="scope.row.hostOs | osFilter" />
              </el-tooltip>
              <!-- <el-popover v-model="scope.row.hId" placement="bottom" width="160"> -->
              <el-popover v-model="scope.row.HostId" placement="bottom" width="160">
                <el-input v-model="input" placeholder="请输入内容" size="mini" />
                <div style="text-align: right; margin-top: 10px;">
                  <el-button size="mini" type="text" @click="scope.row.HostId = false">取消</el-button>
                  <el-button
                    type="primary"
                    size="mini"
                    @click="scope.row.HostId = false;confirmEdit(scope.row.hostName, scope.row.hId, input, scope.$index)"
                  >保存</el-button>
                </div>
                <i slot="reference" class="el-icon-edit" @click="handleEdit(scope.row.hostName)" />
              </el-popover>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态">
            <template slot-scope="scope">
              <el-link
                :type="scope.row.status | statusFilter"
                :underline="false"
              >{{ scope.row.status == '0' ? "运行中": "异常" }}</el-link>
            </template>
          </el-table-column>
          <el-table-column label="配置">
            <template slot-scope="scope">
              {{ scope.row.hardwareId__CPU }}核
              {{ scope.row.hardwareId__memory }}G
              {{ scope.row.disk }}G
            </template>
          </el-table-column>
          <el-table-column label="IP地址" width="180px">
            <template slot-scope="scope">
              内网:{{ scope.row.innerIP }}&nbsp;
              <i
                class="el-icon-copy-document copybutton"
                @click="doCopy(scope.row.innerIP)"
              />
              <br>
              外网:{{ scope.row.outerIP }}&nbsp;
              <i
                class="el-icon-copy-document copybutton"
                @click="doCopy(scope.row.outerIP)"
              />
            </template>
          </el-table-column>
          <el-table-column prop="proId__proName" label="所属项目" />
          <el-table-column prop="cloud" label="所属云" />
          <el-table-column prop="region" label="所属区域" />
          <el-table-column prop="createTime" label="创建时间" />
        </el-table>
        <div style="right: 0;float:right; margin-top: 20px;">
          <el-pagination
            background
            layout="total, sizes, prev, pager, next"
            :total="total"
            :page-size.sync="queryParams.pageSize"
            :current-page.sync="queryParams.pageNum"
            :page-sizes="[10, 20, 30, 50, 100]"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-col>
    </el-row>
    <!-- 导入对话框 -->
    <el-dialog title="导入" :visible.sync="dialogVisible" width="30%" :before-close="handleClose">
      <el-upload
        class="upload-demo"
        drag
        action="https://jsonplaceholder.typicode.com/posts/"
        multiple
      >
        <i class="el-icon-upload" />
        <div class="el-upload__text">
          将文件拖到此处，或
          <em>点击上传</em>
        </div>
        <div slot="tip" class="el-upload__tip" style="color:red">
          提示：仅允许导入“xls”或“xlsx”格式文件！
          <el-link type="info" style="font-size:12px" @click="importTemplate">下载模板</el-link>
        </div>
      </el-upload>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
      </span>
    </el-dialog>
    <!-- end导入对话框 -->
  </div>
</template>

<script>
import { getHostList } from '@/api/assets/host'
import { getProductList } from '@/api/assets/product'
import { changeHostName } from '@/api/assets/host'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        0: 'success',
        1: 'warning',
        2: 'danger'
      }
      return statusMap[status]
    },
    osFilter(os) {
      const osMap = {
        CentOS: 'iconcentos',
        Ubuntu: 'iconubuntu',
        Windows: 'iconuntitled'
      }
      return osMap[os]
    }
  },

  data() {
    return {
      formInline: {
        innerIP: '',
        outerIP: '',
        cloud: ''
      },
      copyValue: '',
      input: '',
      show: null,
      filterText: '',
      deptOptions: null,
      dialogVisible: false,
      tableData: null,
      total: null,
      listLoading: true,
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        innerIP: undefined,
        outerIP: undefined,
        cloud: undefined,
        proId: undefined
      }
    }
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val)
    }
  },
  created() {
    this.fetchData()
    this.productData()
  },

  methods: {
    convertToTreeData(data, pid) {
      const result = []
      let temp = []
      for (let i = 0; i < data.length; i++) {
        if (data[i].parentId === pid) {
          const obj = {
            label: data[i].proName,
            id: data[i].proId,
            status: data[i].status
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
    // 筛选节点
    filterNode(value, data) {
      if (!value) return true
      return data.label.indexOf(value) !== -1
    },
    fetchData() {
      this.listLoading = true
      getHostList(this.queryParams).then(response => {
        this.tableData = response.data.items
        this.total = response.data.total
        this.listLoading = false
      })
    },
    productData() {
      getProductList().then(response => {
        const respData = response.data.items
        const treeData = this.convertToTreeData(respData, 0)
        this.deptOptions = treeData
      })
    },
    // 节点单击事件
    handleNodeClick(data) {
      this.queryParams.innerIP = undefined
      this.queryParams.outerIP = undefined
      this.queryParams.proId = data.id
      this.queryParams.pageNum = 1
      this.fetchData()
    },
    searchSubmit(formInline) {
      this.queryParams.innerIP = formInline.innerIP
      this.fetchData()
      console.log(formInline.innerIP)
    },
    handleEdit: function(row) {
      this.input = Object.assign(row)
    },
    confirmEdit(row, rID, rename, index) {
      const newName = { hId: rID, hostName: rename }
      changeHostName(newName)
        .then(response => {
          if (response.code) {
            this.$message({
              message: '名称修改成功',
              type: 'success'
            })
            this.$set(this.tableData[index], 'hostName', rename)
          }
        })
        .catch(err => {
          console.log(err)
        })
    },
    handleSizeChange(val) {
      this.queryParams.pageNum = 1
      this.queryParams.pageSize = val
      this.fetchData()
      console.log(`每页 ${val} 条`)
    },
    handleCurrentChange(val) {
      this.queryParams.pageNum = val
      this.fetchData()
      console.log(`当前页: ${val}`)
    },
    /** 导入按钮操作 */
    handleImport() {
      console.log(123)
    },
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
        })
        .catch(_ => {})
    },
    doCopy: function(val) {
      var that = this
      this.copyValue = val
      this.$copyText(this.copyValue).then(
        function(e) {
          that.$message.success('已复制')
        },
        function(e) {
          that.$message.error('复制失败')
        }
      )
    }
  }
}
</script>

<style lang="scss" scoped>
.copybutton {
  display: none;
}
/* .test:hover {
  display:inline-block;
  background-color: red;
} */
.el-table__body tr td:hover {
  .copybutton {
    display: inline;
  }
}
</style>
