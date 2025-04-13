<template>
    <div class="member-container">
        <el-card class="box-card">
            <template #header>
                <div class="card-header">
                    <span>会员管理</span>
                    <el-button type="primary" @click="showAddMemberDialog">添加会员</el-button>
                </div>
            </template>

            <!-- 会员列表 -->
            <el-table :data="memberList" style="width: 100%" v-loading="loading">
                <el-table-column prop="id" label="ID" width="80" />
                <el-table-column prop="name" label="姓名" width="120" />
                <el-table-column prop="phone" label="手机号" width="150" />
                <el-table-column prop="level" label="会员等级" width="120">
                    <template #default="{ row }">
                        <el-tag :type="getMemberLevelTag(row.level)">
                            {{ getMemberLevelText(row.level) }}
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

        <!-- 添加会员对话框 -->
        <el-dialog v-model="addDialogVisible" title="添加会员" width="500px">
            <el-form :model="memberForm" label-width="100px" ref="memberFormRef">
                <!-- 用户查找部分 -->
                <el-form-item label="用户手机号">
                    <div class="search-container">
                        <el-input
                            v-model="memberForm.searchPhone"
                            placeholder="请输入用户手机号"
                            :disabled="!!selectedUser"
                        >
                            <template #append>
                                <el-button @click="searchUser" :disabled="!!selectedUser">
                                    查找用户
                                </el-button>
                            </template>
                        </el-input>
                    </div>
                </el-form-item>

                <!-- 显示查找到的用户信息 -->
                <el-form-item v-if="selectedUser" label="用户信息">
                    <div class="user-info">
                        <span>手机号: {{ selectedUser.phone }}</span>
                        <el-button type="text" @click="clearSelectedUser">重新选择</el-button>
                    </div>
                </el-form-item>

                <!-- 会员信息部分 -->
                <el-form-item label="会员姓名">
                    <el-input v-model="memberForm.name" placeholder="请输入会员姓名" />
                </el-form-item>

                <el-form-item label="会员等级">
                    <el-select v-model="memberForm.level" placeholder="请选择会员等级">
                        <el-option label="普通会员" :value="1" />
                        <el-option label="银卡会员" :value="2" />
                        <el-option label="金卡会员" :value="3" />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
        <span class="dialog-footer">
          <el-button @click="addDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
            </template>
        </el-dialog>

        <!-- 编辑会员对话框 -->
        <el-dialog v-model="editDialogVisible" title="编辑会员" width="500px">
            <el-form :model="editForm" label-width="100px" ref="editFormRef">
                <el-form-item label="会员姓名">
                    <el-input v-model="editForm.name" placeholder="请输入会员姓名" />
                </el-form-item>

                <el-form-item label="会员等级">
                    <el-select v-model="editForm.level" placeholder="请选择会员等级">
                        <el-option label="普通会员" :value="1" />
                        <el-option label="银卡会员" :value="2" />
                        <el-option label="金卡会员" :value="3" />
                    </el-select>
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
    reqMemberList,
    reqCreateMember,
    reqUpdateMember,
    reqDeleteMember,
    reqUserByPhone
} from '@/api/member'

// 会员列表数据
const memberList = ref([])
const loading = ref(false)

// 添加会员表单
const addDialogVisible = ref(false)
const memberFormRef = ref()
const selectedUser = ref(null)
const memberForm = reactive({
    searchPhone: '',
    name: '',
    level: 1,
})

// 编辑会员表单
const editDialogVisible = ref(false)
const editFormRef = ref()
const editForm = reactive({
    id: '',
    name: '',
    level: 1,
})

// 获取会员列表
const getMemberList = async () => {
    try {
        loading.value = true
        const res = await reqMemberList()
        memberList.value = res.data
    } catch (error) {
        console.error('获取会员列表失败:', error)
        ElMessage.error('获取会员列表失败')
    } finally {
        loading.value = false
    }
}

// 查找用户
const searchUser = async () => {
    if (!memberForm.searchPhone) {
        ElMessage.warning('请输入手机号')
        return
    }
    try {
        const res = await reqUserByPhone(memberForm.searchPhone)
        if (res.data) {
            selectedUser.value = res.data
            ElMessage.success('找到用户')
        }
    } catch (error) {
        console.error('查找用户失败:', error)
        ElMessage.error('未找到用户')
    }
}

// 清除选中的用户
const clearSelectedUser = () => {
    selectedUser.value = null
    memberForm.searchPhone = ''
}

// 显示添加会员对话框
const showAddMemberDialog = () => {
    addDialogVisible.value = true
    memberForm.searchPhone = ''
    memberForm.name = ''
    memberForm.level = 1
    selectedUser.value = null
}

// 提交添加会员表单
const submitForm = async () => {
    if (!selectedUser.value || !memberForm.name) {
        ElMessage.warning('请填写完整信息')
        return
    }

    try {
        const memberData = {
            name: memberForm.name,
            phone: selectedUser.value.phone,
            level: memberForm.level,
            user_id: selectedUser.value.id
        }

        await reqCreateMember(memberData)
        ElMessage.success('添加会员成功')
        addDialogVisible.value = false
        getMemberList()
    } catch (error) {
        console.error('添加会员失败:', error)
        ElMessage.error('添加会员失败')
    }
}

// 编辑会员
const handleEdit = (row: any) => {
    editForm.id = row.id
    editForm.name = row.name
    editForm.level = row.level
    editDialogVisible.value = true
}

// 提交编辑表单
const submitEditForm = async () => {
    if (!editForm.name) {
        ElMessage.warning('请输入会员姓名')
        return
    }

    try {
        await reqUpdateMember(editForm.id, {
            name: editForm.name,
            level: editForm.level
        })
        ElMessage.success('更新会员成功')
        editDialogVisible.value = false
        getMemberList()
    } catch (error) {
        console.error('更新会员失败:', error)
        ElMessage.error('更新会员失败')
    }
}

// 删除会员
const handleDelete = (row: any) => {
    ElMessageBox.confirm('确定要删除该会员吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(async () => {
        try {
            await reqDeleteMember(row.id)
            ElMessage.success('删除成功')
            getMemberList()
        } catch (error) {
            console.error('删除会员失败:', error)
            ElMessage.error('删除失败')
        }
    }).catch(() => {})
}

// 会员等级显示
const getMemberLevelText = (level: number) => {
    const levelMap = {
        1: '普通会员',
        2: '银卡会员',
        3: '金卡会员'
    }
    return levelMap[level] || '未知等级'
}

const getMemberLevelTag = (level: number) => {
    const levelMap = {
        1: '',
        2: 'success',
        3: 'warning'
    }
    return levelMap[level] || 'info'
}

// 初始化
onMounted(() => {
    getMemberList()
})
</script>

<style scoped lang="scss">
.member-container {
    padding: 20px;

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .search-container {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .user-info {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px;
        background-color: #f5f7fa;
        border-radius: 4px;
    }
}
</style>