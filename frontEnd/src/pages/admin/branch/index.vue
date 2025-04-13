<template>
    <div class="branch-container">
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span>分店管理</span>
            <el-button type="primary" @click="showAddBranchDialog">添加分店</el-button>
          </div>
        </template>
        
        <!-- 筛选条件 -->
        <div class="filter-container">
          <el-select v-model="filterStatus" placeholder="分店状态" clearable @change="getBranchList">
            <el-option label="全部" :value="null" />
            <el-option label="活跃" :value="true" />
            <el-option label="停用" :value="false" />
          </el-select>
        </div>
        
        <!-- 分店列表 -->
        <el-table :data="branchList" style="width: 100%" v-loading="loading">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="分店名称" width="150" />
          <el-table-column prop="address" label="地址" min-width="200" />
          <el-table-column prop="phone" label="联系电话" width="150" />
          <el-table-column prop="is_active" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.is_active ? 'success' : 'danger'">
                {{ row.is_active ? '活跃' : '停用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column label="操作" width="200">
            <template #default="{ row }">
              <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
              <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
      
      <!-- 添加分店对话框 -->
      <el-dialog v-model="addDialogVisible" title="添加分店" width="500px">
        <el-form :model="branchForm" label-width="100px" ref="branchFormRef">
          <el-form-item label="分店名称">
            <el-input v-model="branchForm.name" placeholder="请输入分店名称" />
          </el-form-item>
          
          <el-form-item label="地址">
            <el-input v-model="branchForm.address" placeholder="请输入分店地址" />
          </el-form-item>
          
          <el-form-item label="联系电话">
            <el-input v-model="branchForm.phone" placeholder="请输入联系电话" />
          </el-form-item>
          
          <el-form-item label="描述">
            <el-input 
              v-model="branchForm.description" 
              type="textarea" 
              :rows="3" 
              placeholder="请输入分店描述" 
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="addDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitForm">确定</el-button>
          </span>
        </template>
      </el-dialog>
  
      <!-- 编辑分店对话框 -->
      <el-dialog v-model="editDialogVisible" title="编辑分店" width="500px">
        <el-form :model="editForm" label-width="100px" ref="editFormRef">
          <el-form-item label="分店名称">
            <el-input v-model="editForm.name" placeholder="请输入分店名称" />
          </el-form-item>
          
          <el-form-item label="地址">
            <el-input v-model="editForm.address" placeholder="请输入分店地址" />
          </el-form-item>
          
          <el-form-item label="联系电话">
            <el-input v-model="editForm.phone" placeholder="请输入联系电话" />
          </el-form-item>
          
          <el-form-item label="描述">
            <el-input 
              v-model="editForm.description" 
              type="textarea" 
              :rows="3" 
              placeholder="请输入分店描述" 
            />
          </el-form-item>
          
          <el-form-item label="状态">
            <el-switch
              v-model="editForm.is_active"
              :active-value="true"
              :inactive-value="false"
              active-text="活跃"
              inactive-text="停用"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="editDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitEditForm">确定</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, reactive, onMounted } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import { 
    reqBranchList, 
    reqCreateBranch, 
    reqUpdateBranch, 
    reqDeleteBranch 
  } from '@/api/branch'
  
  // 分店列表数据
  const branchList = ref([])
  const loading = ref(false)
  const filterStatus = ref(null)
  
  // 添加分店表单
  const addDialogVisible = ref(false)
  const branchFormRef = ref()
  const branchForm = reactive({
    name: '',
    address: '',
    phone: '',
    description: ''
  })
  
  // 编辑分店表单
  const editDialogVisible = ref(false)
  const editFormRef = ref()
  const editForm = reactive({
    id: '',
    name: '',
    address: '',
    phone: '',
    description: '',
    is_active: true
  })
  
  // 获取分店列表
  const getBranchList = async () => {
    try {
      loading.value = true
      const params = filterStatus.value !== null ? { is_active: filterStatus.value } : {}
      const res = await reqBranchList(params)
      branchList.value = res.data
    } catch (error) {
      console.error('获取分店列表失败:', error)
      ElMessage.error('获取分店列表失败')
    } finally {
      loading.value = false
    }
  }
  
  // 显示添加分店对话框
  const showAddBranchDialog = () => {
    addDialogVisible.value = true
    branchForm.name = ''
    branchForm.address = ''
    branchForm.phone = ''
    branchForm.description = ''
  }
  
  // 提交添加分店表单
  const submitForm = async () => {
    if (!branchForm.name || !branchForm.address || !branchForm.phone) {
      ElMessage.warning('请填写必要信息')
      return
    }
    
    try {
      await reqCreateBranch(branchForm)
      ElMessage.success('添加分店成功')
      addDialogVisible.value = false
      getBranchList()
    } catch (error) {
      console.error('添加分店失败:', error)
      ElMessage.error('添加分店失败，可能是分店名称已存在')
    }
  }
  
  // 编辑分店
  const handleEdit = (row: any) => {
    editForm.id = row.id
    editForm.name = row.name
    editForm.address = row.address
    editForm.phone = row.phone
    editForm.description = row.description || ''
    editForm.is_active = row.is_active
    editDialogVisible.value = true
  }
  
  // 提交编辑表单
  const submitEditForm = async () => {
    if (!editForm.name || !editForm.address || !editForm.phone) {
      ElMessage.warning('请填写必要信息')
      return
    }
    
    try {
      await reqUpdateBranch(editForm.id, editForm)
      ElMessage.success('更新分店成功')
      editDialogVisible.value = false
      getBranchList()
    } catch (error) {
      console.error('更新分店失败:', error)
      ElMessage.error('更新分店失败，可能是分店名称已存在')
    }
  }
  
  // 删除分店
  const handleDelete = (row: any) => {
    ElMessageBox.confirm('确定要删除该分店吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      try {
        await reqDeleteBranch(row.id)
        ElMessage.success('删除成功')
        getBranchList()
      } catch (error) {
        console.error('删除分店失败:', error)
        ElMessage.error('删除失败')
      }
    }).catch(() => {})
  }
  
  // 初始化
  onMounted(() => {
    getBranchList()
  })
  </script>
  
  <style scoped lang="scss">
  .branch-container {
    padding: 20px;
  
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  
    .filter-container {
      margin-bottom: 20px;
    }
  }
  </style>