<template>
    <div class="booking-container">
        <!-- 我的预订 -->
        <el-card class="box-card">
            <template #header>
                <div class="card-header">
                    <span>我的预订</span>
                    <el-button type="primary" @click="showNewBookingDialog">新增预订</el-button>
                </div>
            </template>

            <!-- 筛选条件 -->
            <div class="filter-container">
                <el-select
                    v-model="filterStatus"
                    placeholder="预订状态"
                    clearable
                    @change="getMyBookings"
                    style="width: 150px;"
                >
                    <el-option label="全部" :value="null" />
                    <el-option label="待确认" value="pending" />
                    <el-option label="已确认" value="confirmed" />
                    <el-option label="已取消" value="cancelled" />
                    <el-option label="已完成" value="completed" />
                </el-select>
            </div>

            <!-- 预订列表 -->
            <el-table :data="bookingList" style="width: 100%" v-loading="loading">
                <el-table-column prop="id" label="预订号" width="80" />
                <el-table-column label="分店" width="150">
                    <template #default="{ row }">
                        {{ getBranchName(row.room.branch_id) }}
                    </template>
                </el-table-column>
                <!--<el-table-column label="分店" width="150">-->
                <!--    <template #default="{ row }">-->
                <!--        {{row.room.name}}-->
                <!--        &lt;!&ndash;{{ row.room && row.room.branch ? row.room.branch.name : '未知分店' }}&ndash;&gt;-->
                <!--        &lt;!&ndash;{{ row.branch.name }}&ndash;&gt;-->
                <!--    </template>-->
                <!--</el-table-column>-->
                <el-table-column label="房间" width="150">
                    <template #default="{ row }">
                        {{ row.room.room_number }} ({{ row.room.room_type }})
                    </template>
                </el-table-column>
                <el-table-column label="入住日期" width="120">
                    <template #default="{ row }">
                        {{ formatDate(row.check_in_date) }}
                    </template>
                </el-table-column>
                <el-table-column label="退房日期" width="120">
                    <template #default="{ row }">
                        {{ formatDate(row.check_out_date) }}
                    </template>
                </el-table-column>
                <el-table-column prop="total_price" label="总价" width="100">
                    <template #default="{ row }">
                        ¥{{ row.total_price }}
                    </template>
                </el-table-column>
                <el-table-column prop="status" label="状态" width="100">
                    <template #default="{ row }">
                        <el-tag :type="getStatusType(row.status)">
                            {{ getStatusText(row.status) }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="created_at" label="预订时间" width="180" />
                <el-table-column label="操作" width="150">
                    <template #default="{ row }">
                        <el-button
                            type="danger"
                            size="small"
                            @click="handleCancel(row)"
                            :disabled="!canCancel(row.status)"
                        >
                            取消预订
                        </el-button>
                        <el-button
                            type="primary"
                            size="small"
                            @click="handleViewDetail(row)"
                        >
                            详情
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页 -->
            <div class="pagination-container" v-if="bookingList.length > 0">
                <el-pagination
                    background
                    layout="prev, pager, next"
                    :total="total"
                    :page-size="pageSize"
                    :current-page="currentPage"
                    @current-change="handlePageChange"
                />
            </div>
        </el-card>

        <!-- 新增预订对话框 -->
        <el-dialog v-model="newBookingDialogVisible" title="新增预订" width="700px">
            <div class="booking-form">
                <!-- 步骤条 -->
                <el-steps :active="activeStep" finish-status="success" simple>
                    <el-step title="选择分店" />
                    <el-step title="选择日期" />
                    <el-step title="选择房间" />
                    <el-step title="确认预订" />
                </el-steps>

                <!-- 步骤1：选择分店 -->
                <div v-if="activeStep === 0" class="step-content">
                    <h3>请选择分店</h3>
                    <el-select v-model="bookingForm.branch_id" placeholder="请选择分店" style="width: 100%">
                        <el-option
                            v-for="branch in branchList"
                            :key="branch.id"
                            :label="branch.name"
                            :value="branch.id"
                        />
                    </el-select>

                    <div class="step-actions">
                        <el-button type="primary" @click="nextStep" :disabled="!bookingForm.branch_id">下一步</el-button>
                    </div>
                </div>

                <!-- 步骤2：选择日期 -->
                <div v-if="activeStep === 1" class="step-content">
                    <h3>请选择入住和退房日期</h3>
                    <el-date-picker
                        v-model="dateRange"
                        type="daterange"
                        range-separator="至"
                        start-placeholder="入住日期"
                        end-placeholder="退房日期"
                        :disabled-date="disablePastDates"
                        style="width: 100%"
                    />

                    <div class="step-actions">
                        <el-button @click="prevStep">上一步</el-button>
                        <el-button type="primary" @click="handleDateSelected" :disabled="!dateRange || !dateRange[0] || !dateRange[1]">下一步</el-button>
                    </div>
                </div>

                <!-- 步骤3：选择房间 -->
                <div v-if="activeStep === 2" class="step-content">
                    <h3>请选择房间</h3>

                    <!-- 房间筛选 -->
                    <div class="room-filters">
                        <el-select
                            v-model="roomFilter.type"
                            placeholder="房间类型"
                            clearable
                            @change="searchAvailableRooms"
                            style="width: 150px; margin-right: 15px;"
                        >
                            <el-option label="全部" :value="null" />
                            <el-option label="标准间" value="标准间" />
                            <el-option label="豪华间" value="豪华间" />
                            <el-option label="套房" value="套房" />
                        </el-select>

                        <el-select
                            v-model="roomFilter.capacity"
                            placeholder="容纳人数"
                            clearable
                            @change="searchAvailableRooms"
                            style="width: 150px;"
                        >
                            <el-option label="全部" :value="null" />
                            <el-option label="1人" :value="1" />
                            <el-option label="2人" :value="2" />
                            <el-option label="3人" :value="3" />
                            <el-option label="4人及以上" :value="4" />
                        </el-select>
                    </div>

                    <!-- 可用房间列表 -->
                    <el-table
                        :data="availableRooms"
                        style="width: 100%"
                        v-loading="roomsLoading"
                        @row-click="selectRoom"
                        highlight-current-row
                    >
                        <el-table-column prop="room_number" label="房间号" width="100" />
                        <el-table-column prop="room_type" label="房间类型" width="120" />
                        <el-table-column prop="floor" label="楼层" width="80" />
                        <el-table-column prop="capacity" label="容纳人数" width="100" />
                        <el-table-column prop="price" label="价格/晚" width="100">
                            <template #default="{ row }">
                                ¥{{ row.price }}
                            </template>
                        </el-table-column>
                        <el-table-column prop="description" label="描述" min-width="150" />
                    </el-table>

                    <div v-if="availableRooms.length === 0 && !roomsLoading" class="no-rooms-tip">
                        所选日期没有可用房间，请尝试其他日期或分店
                    </div>

                    <div class="step-actions">
                        <el-button @click="prevStep">上一步</el-button>
                        <el-button type="primary" @click="nextStep" :disabled="!bookingForm.room_id">下一步</el-button>
                    </div>
                </div>

                <!-- 步骤4：确认预订 -->
                <div v-if="activeStep === 3" class="step-content">
                    <h3>确认预订信息</h3>

                    <div class="booking-summary">
                        <el-descriptions title="预订详情" :column="1" border>
                            <el-descriptions-item label="分店">
                                {{ getBranchName(bookingForm.branch_id) }}
                            </el-descriptions-item>
                            <el-descriptions-item label="房间">
                                {{ selectedRoomInfo.room_number }} ({{ selectedRoomInfo.room_type }})
                            </el-descriptions-item>
                            <el-descriptions-item label="入住日期">
                                {{ formatDate(bookingForm.check_in_date) }}
                            </el-descriptions-item>
                            <el-descriptions-item label="退房日期">
                                {{ formatDate(bookingForm.check_out_date) }}
                            </el-descriptions-item>
                            <el-descriptions-item label="住宿天数">
                                {{ calculateDays() }} 晚
                            </el-descriptions-item>
                            <el-descriptions-item label="房间价格">
                                ¥{{ selectedRoomInfo.price }} / 晚
                            </el-descriptions-item>
                            <el-descriptions-item label="总价">
                                <span class="total-price">¥{{ calculateTotalPrice() }}</span>
                            </el-descriptions-item>
                        </el-descriptions>

                        <el-form :model="bookingForm" label-width="100px">
                            <el-form-item label="特殊要求">
                                <el-input
                                    v-model="bookingForm.special_requests"
                                    type="textarea"
                                    :rows="3"
                                    placeholder="如有特殊要求，请在此说明"
                                />
                            </el-form-item>
                        </el-form>
                    </div>

                    <div class="step-actions">
                        <el-button @click="prevStep">上一步</el-button>
                        <el-button type="primary" @click="submitBooking">提交预订</el-button>
                    </div>
                </div>
            </div>
        </el-dialog>

        <!-- 预订详情对话框 -->
        <el-dialog v-model="detailDialogVisible" title="预订详情" width="600px">
            <div v-if="selectedBooking" class="booking-detail">
                <el-descriptions title="预订信息" :column="1" border>
                    <el-descriptions-item label="预订号">{{ selectedBooking.id }}</el-descriptions-item>
                    <el-descriptions-item label="分店">
                        {{ selectedBooking ? getBranchName(selectedBooking.room.branch_id) : '' }}
                    </el-descriptions-item>
                    <el-descriptions-item label="地址">
                        {{ selectedBooking ? getBranchAddress(selectedBooking.room.branch_id) : '' }}
                    </el-descriptions-item>
                    <!--<el-descriptions-item label="分店">{{ selectedBooking.branch.name }}</el-descriptions-item>-->
                    <!--<el-descriptions-item label="地址">{{ selectedBooking.branch.address }}</el-descriptions-item>-->
                    <el-descriptions-item label="房间号">{{ selectedBooking.room.room_number }}</el-descriptions-item>
                    <el-descriptions-item label="房间类型">{{ selectedBooking.room.room_type }}</el-descriptions-item>
                    <el-descriptions-item label="入住日期">{{ formatDate(selectedBooking.check_in_date) }}</el-descriptions-item>
                    <el-descriptions-item label="退房日期">{{ formatDate(selectedBooking.check_out_date) }}</el-descriptions-item>
                    <el-descriptions-item label="总价">¥{{ selectedBooking.total_price }}</el-descriptions-item>
                    <el-descriptions-item label="状态">
                        <el-tag :type="getStatusType(selectedBooking.status)">
                            {{ getStatusText(selectedBooking.status) }}
                        </el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="预订时间">{{ selectedBooking.created_at }}</el-descriptions-item>
                    <el-descriptions-item label="特殊要求" v-if="selectedBooking.special_requests">
                        {{ selectedBooking.special_requests }}
                    </el-descriptions-item>
                </el-descriptions>

                <div class="detail-actions" v-if="canCancel(selectedBooking.status)">
                    <el-button type="danger" @click="handleCancelFromDetail">取消预订</el-button>
                </div>
            </div>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { reqMyBookings, reqCreateBooking, reqCancelBooking, reqAvailableRooms } from '@/api/booking'
import { reqBranchList } from '@/api/branch'

const formatDate = (date: string | Date): string => {
    if (!date) return '';

    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');

    return `${year}-${month}-${day}`;
};


// 状态变量
const loading = ref(false)
const roomsLoading = ref(false)
const bookingList = ref([])
const branchList = ref([])
const availableRooms = ref([])
const filterStatus = ref(null)
const selectedBooking = ref(null)

// 分页相关
const total = ref(0)
const pageSize = ref(10)
const currentPage = ref(1)

// 对话框控制
const newBookingDialogVisible = ref(false)
const detailDialogVisible = ref(false)

// 预订表单步骤
const activeStep = ref(0)
const dateRange = ref(null)
const roomFilter = reactive({
    type: null,
    capacity: null
})

// 预订表单数据
const bookingForm = reactive({
    branch_id: null,
    room_id: null,
    check_in_date: null,
    check_out_date: null,
    special_requests: ''
})

// 选中的房间信息
const selectedRoomInfo = reactive({
    room_number: '',
    room_type: '',
    price: 0
})


// 添加获取分店名称和地址的方法
// const getBranchName = (branchId) => {
//     if (!branchId || !branchList.value) return '未知分店';
//     const branch = branchList.value.find(b => b.id === branchId);
//     return branch ? branch.name : '未知分店';
// }

const getBranchAddress = (branchId) => {
    if (!branchId || !branchList.value) return '未知地址';
    const branch = branchList.value.find(b => b.id === branchId);
    return branch ? branch.address : '未知地址';
}



// 获取我的预订列表
const getMyBookings = async () => {
    loading.value = true
    try {
        const params = {
            skip: (currentPage.value - 1) * pageSize.value,
            limit: pageSize.value
        }

        if (filterStatus.value) {
            params.status = filterStatus.value
        }

        const res = await reqMyBookings(params)
        bookingList.value = res.data || []
        console.log('bookings',bookingList.value)
        total.value = res.total || bookingList.value.length
    } catch (error) {
        console.error('获取预订列表失败:', error)
        ElMessage.error('获取预订列表失败')
    } finally {
        loading.value = false
    }
}

// 处理分页变化
const handlePageChange = (page) => {
    currentPage.value = page
    getMyBookings()
}

// 获取分店列表
const getBranchList = async () => {
    try {
        const res = await reqBranchList({ is_active: true })
        console.log('branchList',res.data)
        branchList.value = res.data || []
    } catch (error) {
        console.error('获取分店列表失败:', error)
        ElMessage.error('获取分店列表失败')
    }
}

// 获取分店名称
const getBranchName = (branchId) => {
    const branch = branchList.value.find(b => b.id === branchId)
    return branch ? branch.name : ''
}

// 搜索可用房间
const searchAvailableRooms = async () => {
    if (!bookingForm.branch_id || !bookingForm.check_in_date || !bookingForm.check_out_date) {
        return
    }

    roomsLoading.value = true
    try {
        const params = {
            branch_id: bookingForm.branch_id,
            check_in_date: formatDate(bookingForm.check_in_date),
            check_out_date: formatDate(bookingForm.check_out_date)
        }

        if (roomFilter.type) {
            params.room_type = roomFilter.type
        }

        if (roomFilter.capacity) {
            params.capacity = roomFilter.capacity
        }

        const res = await reqAvailableRooms(params)
        availableRooms.value = res.data || []
    } catch (error) {
        console.error('获取可用房间失败:', error)
        ElMessage.error('获取可用房间失败')
    } finally {
        roomsLoading.value = false
    }
}

// 禁用过去的日期
const disablePastDates = (date) => {
    return date < new Date(new Date().setHours(0, 0, 0, 0))
}

// 显示新增预订对话框
const showNewBookingDialog = () => {
    // 重置表单和步骤
    activeStep.value = 0
    dateRange.value = null
    bookingForm.branch_id = null
    bookingForm.room_id = null
    bookingForm.check_in_date = null
    bookingForm.check_out_date = null
    bookingForm.special_requests = ''
    roomFilter.type = null
    roomFilter.capacity = null
    availableRooms.value = []

    newBookingDialogVisible.value = true
}

// 下一步
const nextStep = () => {
    activeStep.value++
}

// 上一步
const prevStep = () => {
    activeStep.value--
}

// 处理日期选择
const handleDateSelected = () => {
    if (!dateRange.value || !dateRange.value[0] || !dateRange.value[1]) {
        ElMessage.warning('请选择入住和退房日期')
        return
    }

    bookingForm.check_in_date = dateRange.value[0]
    bookingForm.check_out_date = dateRange.value[1]

    // 进入下一步前搜索可用房间
    searchAvailableRooms()
    nextStep()
}

// 选择房间
const selectRoom = (row) => {
    bookingForm.room_id = row.id
    selectedRoomInfo.room_number = row.room_number
    selectedRoomInfo.room_type = row.room_type
    selectedRoomInfo.price = row.price
}

// 计算住宿天数
const calculateDays = () => {
    if (!bookingForm.check_in_date || !bookingForm.check_out_date) {
        return 0
    }

    const checkIn = new Date(bookingForm.check_in_date)
    const checkOut = new Date(bookingForm.check_out_date)
    const diffTime = Math.abs(checkOut - checkIn)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    return diffDays
}

// 计算总价
const calculateTotalPrice = () => {
    const days = calculateDays()
    return (days * selectedRoomInfo.price).toFixed(2)
}

// 提交预订
const submitBooking = async () => {
    try {
        await reqCreateBooking({
            room_id: bookingForm.room_id,
            check_in_date: formatDate(bookingForm.check_in_date),
            check_out_date: formatDate(bookingForm.check_out_date),
            special_requests: bookingForm.special_requests
        })

        ElMessage.success('预订成功')
        newBookingDialogVisible.value = false
        getMyBookings()
    } catch (error) {
        console.error('预订失败:', error)
        ElMessage.error('预订失败，请稍后重试')
    }
}

// 取消预订
const handleCancel = (row) => {
    ElMessageBox.confirm('确定要取消该预订吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(async () => {
        try {
            await reqCancelBooking(row.id)
            ElMessage.success('取消预订成功')
            getMyBookings()
        } catch (error) {
            console.error('取消预订失败:', error)
            ElMessage.error('取消预订失败')
        }
    }).catch(() => {})
}

// 从详情页取消预订
const handleCancelFromDetail = () => {
    if (!selectedBooking.value) return

    ElMessageBox.confirm('确定要取消该预订吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(async () => {
        try {
            await reqCancelBooking(selectedBooking.value.id)
            ElMessage.success('取消预订成功')
            detailDialogVisible.value = false
            getMyBookings()
        } catch (error) {
            console.error('取消预订失败:', error)
            ElMessage.error('取消预订失败')
        }
    }).catch(() => {})
}

// 查看预订详情
const handleViewDetail = (row) => {
    selectedBooking.value = row
    detailDialogVisible.value = true
}

// 获取状态文本
const getStatusText = (status) => {
    const statusMap = {
        'pending': '待确认',
        'confirmed': '已确认',
        'cancelled': '已取消',
        'completed': '已完成'
    }
    return statusMap[status] || status
}

// 获取状态标签类型
const getStatusType = (status) => {
    const typeMap = {
        'pending': 'warning',
        'confirmed': 'success',
        'cancelled': 'danger',
        'completed': 'info'
    }
    return typeMap[status] || ''
}

// 判断是否可以取消预订
const canCancel = (status) => {
    return ['pending', 'confirmed'].includes(status)
}

// 初始化
onMounted(() => {
    getMyBookings()
    getBranchList()
})
</script>

<style scoped lang="scss">
.booking-container {
    padding: 20px;

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .filter-container {
        margin-bottom: 20px;
    }

    .pagination-container {
        margin-top: 20px;
        display: flex;
        justify-content: center;
    }

    .booking-form {
        .step-content {
            margin-top: 30px;

            h3 {
                margin-bottom: 20px;
                font-weight: 500;
            }

            .room-filters {
                display: flex;
                margin-bottom: 15px;
            }

            .no-rooms-tip {
                text-align: center;
                padding: 20px 0;
                color: #f56c6c;
            }
        }

        .step-actions {
            margin-top: 30px;
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }

        .booking-summary {
            margin-bottom: 20px;

            .total-price {
                font-size: 18px;
                font-weight: bold;
                color: #f56c6c;
            }
        }
    }

    .booking-detail {
        .detail-actions {
            margin-top: 20px;
            display: flex;
            justify-content: flex-end;
        }
    }
}
</style>