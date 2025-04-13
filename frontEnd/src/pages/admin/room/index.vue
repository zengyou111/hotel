<template>
    <div class="room-container">
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span>客房管理</span>
            <el-button type="primary" @click="showAddRoomDialog" :disabled="!selectedBranch">添加客房</el-button>
          </div>
        </template>
        
        <!-- 分店选择 -->
        <div class="filter-container">
          <el-select 
            v-model="selectedBranch" 
            placeholder="请选择分店" 
            @change="handleBranchChange"
            style="width: 200px; margin-right: 15px;"
          >
            <el-option 
              v-for="branch in branchList" 
              :key="branch.id" 
              :label="branch.name" 
              :value="branch.id" 
            />
          </el-select>
          
          <el-select 
            v-model="filterStatus" 
            placeholder="客房状态" 
            clearable 
            @change="getRoomList"
            style="width: 150px; margin-right: 15px;"
          >
            <el-option label="全部" :value="null" />
            <el-option label="可用" :value="true" />
            <el-option label="不可用" :value="false" />
          </el-select>
          
          <el-select 
            v-model="filterType" 
            placeholder="房间类型" 
            clearable 
            @change="getRoomList"
            style="width: 150px;"
          >
            <el-option label="全部" :value="null" />
            <el-option label="标准间" :value="标准间" />
            <el-option label="豪华间" :value="豪华间" />
            <el-option label="套房" :value="套房" />
          </el-select>
        </div>
        
        <!-- 提示信息 -->
        <div v-if="!selectedBranch" class="empty-tip">
          请先选择一个分店
        </div>
        
        <!-- 客房列表 -->
        <el-table 
          v-else 
          :data="roomList" 
          style="width: 100%" 
          v-loading="loading"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="room_number" label="房间号" width="120" />
          <el-table-column prop="room_type" label="房间类型" width="120" />
          <el-table-column prop="floor" label="楼层" width="80" />
          <el-table-column prop="price" label="价格" width="100">
            <template #default="{ row }">
              ¥{{ row.price }}
            </template>
          </el-table-column>
          <el-table-column prop="capacity" label="容纳人数" width="100" />
          <el-table-column prop="is_available" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.is_available ? 'success' : 'danger'">
                {{ row.is_available ? '可用' : '不可用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" min-width="150" />
          <el-table-column label="操作" width="200">
            <template #default="{ row }">
              <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
              <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
      
      <!-- 添加客房对话框 -->
      <el-dialog v-model="addDialogVisible" title="添加客房" width="500px">
        <el-form :model="roomForm" label-width="100px" ref="roomFormRef">
          <el-form-item label="分店">
            <el-input :value="getBranchName(selectedBranch)" disabled />
          </el-form-item>
          
          <el-form-item label="房间号">
            <el-input v-model="roomForm.room_number" placeholder="请输入房间号" />
          </el-form-item>
          
          <el-form-item label="房间类型">
            <el-select v-model="roomForm.room_type" placeholder="请选择房间类型" style="width: 100%">
              <el-option label="标准间" value="标准间" />
              <el-option label="豪华间" value="豪华间" />
              <el-option label="套房" value="套房" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="楼层">
            <el-input-number v-model="roomForm.floor" :min="1" :max="99" />
          </el-form-item>
          
          <el-form-item label="价格">
            <el-input-number 
              v-model="roomForm.price" 
              :min="0" 
              :precision="2" 
              :step="10" 
              style="width: 100%"
            />
          </el-form-item>
          
          <el-form-item label="容纳人数">
            <el-input-number v-model="roomForm.capacity" :min="1" :max="10" />
          </el-form-item>
          
          <el-form-item label="描述">
            <el-input 
              v-model="roomForm.description" 
              type="textarea" 
              :rows="3" 
              placeholder="请输入客房描述" 
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
  
      <!-- 编辑客房对话框 -->
      <el-dialog v-model="editDialogVisible" title="编辑客房" width="500px">
        <el-form :model="editForm" label-width="100px" ref="editFormRef">
          <el-form-item label="分店">
            <el-input :value="getBranchName(editForm.branch_id)" disabled />
          </el-form-item>
          
          <el-form-item label="房间号">
            <el-input v-model="editForm.room_number" placeholder="请输入房间号" />
          </el-form-item>
          
          <el-form-item label="房间类型">
            <el-select v-model="editForm.room_type" placeholder="请选择房间类型" style="width: 100%">
              <el-option label="标准间" value="标准间" />
              <el-option label="豪华间" value="豪华间" />
              <el-option label="套房" value="套房" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="楼层">
            <el-input-number v-model="editForm.floor" :min="1" :max="99" />
          </el-form-item>
          
          <el-form-item label="价格">
            <el-input-number 
              v-model="editForm.price" 
              :min="0" 
              :precision="2" 
              :step="10" 
              style="width: 100%"
            />
          </el-form-item>
          
          <el-form-item label="容纳人数">
            <el-input-number v-model="editForm.capacity" :min="1" :max="10" />
          </el-form-item>
          
          <el-form-item label="描述">
            <el-input 
              v-model="editForm.description" 
              type="textarea" 
              :rows="3" 
              placeholder="请输入客房描述" 
            />
          </el-form-item>
          
          <el-form-item label="状态">
            <el-switch
              v-model="editForm.is_available"
              :active-value="true"
              :inactive-value="false"
              active-text="可用"
              inactive-text="不可用"
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
    reqRoomList, 
    reqCreateRoom, 
    reqUpdateRoom, 
    reqDeleteRoom 
  } from '@/api/room'
  import { reqBranchList } from '@/api/branch'
  
  // 分店列表数据
  const branchList = ref([])
  const selectedBranch = ref(null)
  
  // 客房列表数据
  const roomList = ref([])
  const loading = ref(false)
  const filterStatus = ref(null)
  const filterType = ref(null)
  
  // 添加客房表单
  const addDialogVisible = ref(false)
  const roomFormRef = ref()
  const roomForm = reactive({
    room_number: '',
    room_type: '标准间',
    floor: 1,
    price: 199,
    capacity: 2,
    description: ''
  })
  
  // 编辑客房表单
  const editDialogVisible = ref(false)
  const editFormRef = ref()
  const editForm = reactive({
    id: '',
    room_number: '',
    room_type: '',
    floor: 1,
    price: 0,
    capacity: 2,
    description: '',
    is_available: true,
    branch_id: null
  })
  
  // 获取分店列表
  const getBranchList = async () => {
    try {
      const res = await reqBranchList()
      branchList.value = res.data
      // 如果有分店，默认选择第一个
      if (branchList.value.length > 0) {
        selectedBranch.value = branchList.value[0].id
        getRoomList()
      }
    } catch (error) {
      console.error('获取分店列表失败:', error)
      ElMessage.error('获取分店列表失败')
    }
  }
  
  // 获取客房列表
  const getRoomList = async () => {
    if (!selectedBranch.value) return
    
    try {
      loading.value = true
      const params = {
        branch_id: selectedBranch.value
      }
      
      if (filterStatus.value !== null) {
        params.is_available = filterStatus.value
      }
      
      if (filterType.value) {
        params.room_type = filterType.value
      }
      
      const res = await reqRoomList(params)
      roomList.value = res.data
    } catch (error) {
      console.error('获取客房列表失败:', error)
      ElMessage.error('获取客房列表失败')
    } finally {
      loading.value = false
    }
  }
  
  // 处理分店变更
  const handleBranchChange = () => {
    getRoomList()
  }
  
  // 获取分店名称
  const getBranchName = (branchId) => {
    const branch = branchList.value.find(item => item.id === branchId)
    return branch ? branch.name : ''
  }
  
  // 显示添加客房对话框
  const showAddRoomDialog = () => {
    if (!selectedBranch.value) {
      ElMessage.warning('请先选择分店')
      return
    }
    
    addDialogVisible.value = true
    roomForm.room_number = ''
    roomForm.room_type = '标准间'
    roomForm.floor = 1
    roomForm.price = 199
    roomForm.capacity = 2
    roomForm.description = ''
  }
  
  // 提交添加客房表单
  const submitForm = async () => {
    if (!roomForm.room_number) {
      ElMessage.warning('请输入房间号')
      return
    }
    
    try {
      const roomData = {
        ...roomForm,
        branch_id: selectedBranch.value
      }
      
      await reqCreateRoom(roomData)
      ElMessage.success('添加客房成功')
      addDialogVisible.value = false
      getRoomList()
    } catch (error) {
      console.error('添加客房失败:', error)
      ElMessage.error('添加客房失败，可能是房间号已存在')
    }
  }
  
  // 编辑客房
  const handleEdit = (row: any) => {
    editForm.id = row.id
    editForm.room_number = row.room_number
    editForm.room_type = row.room_type
    editForm.floor = row.floor
    editForm.price = row.price
    editForm.capacity = row.capacity
    editForm.description = row.description || ''
    editForm.is_available = row.is_available
    editForm.branch_id = row.branch_id
    editDialogVisible.value = true
  }
  
  // 提交编辑表单
  const submitEditForm = async () => {
    if (!editForm.room_number) {
      ElMessage.warning('请输入房间号')
      return
    }
    
    try {
      await reqUpdateRoom(editForm.id, {
        room_number: editForm.room_number,
        room_type: editForm.room_type,
        floor: editForm.floor,
        price: editForm.price,
        capacity: editForm.capacity,
        description: editForm.description,
        is_available: editForm.is_available
      })
      ElMessage.success('更新客房成功')
      editDialogVisible.value = false
      getRoomList()
    } catch (error) {
      console.error('更新客房失败:', error)
      ElMessage.error('更新客房失败，可能是房间号已存在')
    }
  }
  
  // 删除客房
  const handleDelete = (row: any) => {
    ElMessageBox.confirm('确定要删除该客房吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      try {
        await reqDeleteRoom(row.id)
        ElMessage.success('删除成功')
        getRoomList()
      } catch (error) {
        console.error('删除客房失败:', error)
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
  .room-container {
    padding: 20px;
  
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  
    .filter-container {
      margin-bottom: 20px;
      display: flex;
      align-items: center;
    }
    
    .empty-tip {
      text-align: center;
      padding: 40px 0;
      color: #909399;
      font-size: 16px;
    }
  }
  </style>