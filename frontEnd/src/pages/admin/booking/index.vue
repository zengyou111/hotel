<template>
    <div class="booking-admin-container">
        <div class="header">
            <h2>预订管理</h2>
            <div class="filter-container">
                <el-select v-model="statusFilter" placeholder="预订状态" clearable @change="handleFilter">
                    <el-option label="全部" value=""></el-option>
                    <el-option label="待确认" value="pending"></el-option>
                    <el-option label="已确认" value="confirmed"></el-option>
                    <el-option label="已取消" value="cancelled"></el-option>
                    <el-option label="已完成" value="completed"></el-option>
                </el-select>
                <el-select
                    v-model="branchFilter"
                    placeholder="选择分店"
                    clearable
                    @change="handleFilter"
                    style="margin-left: 10px; width: 180px;"
                >
                    <el-option label="全部分店" value=""></el-option>
                    <el-option
                        v-for="branch in branchList"
                        :key="branch.id"
                        :label="branch.name"
                        :value="branch.id"
                    ></el-option>
                </el-select>
                <el-button type="primary" @click="fetchBookings" style="margin-left: 10px;">刷新</el-button>
            </div>
        </div>

        <el-card class="booking-table">
            <el-table
                v-loading="loading"
                :data="bookings"
                border
                style="width: 100%"
            >
                <el-table-column prop="id" label="预订号" width="80" />
                <!--<el-table-column prop="user.phone" label="用户手机号" width="120" />-->
                <el-table-column label="分店" width="150">
                    <template #default="scope">
                        {{ getBranchName(scope.row.room.branch_id) }}
                    </template>
                </el-table-column>
                <el-table-column label="房间" width="150">
                    <template #default="scope">
                        {{ scope.row.room.room_number }} ({{ scope.row.room.room_type }})
                    </template>
                </el-table-column>
                <el-table-column label="入住日期" width="120">
                    <template #default="scope">
                        {{ formatDate(scope.row.check_in_date) }}
                    </template>
                </el-table-column>
                <el-table-column label="退房日期" width="120">
                    <template #default="scope">
                        {{ formatDate(scope.row.check_out_date) }}
                    </template>
                </el-table-column>
                <el-table-column prop="total_price" label="总价" width="100">
                    <template #default="scope">
                        ¥{{ scope.row.total_price }}
                    </template>
                </el-table-column>
                <el-table-column prop="status" label="状态" width="100">
                    <template #default="scope">
                        <el-tag :type="getStatusType(scope.row.status)">
                            {{ getStatusText(scope.row.status) }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="预订时间" width="180">
                    <template #default="scope">
                        {{ formatDateTime(scope.row.created_at) }}
                    </template>
                </el-table-column>
                <el-table-column label="操作" fixed="right" width="200">
                    <template #default="scope">
                        <el-button
                            v-if="scope.row.status === 'pending'"
                            type="success"
                            size="small"
                            @click="handleConfirm(scope.row)"
                        >
                            确认
                        </el-button>
                        <el-button
                            v-if="scope.row.status === 'confirmed'"
                            type="warning"
                            size="small"
                            @click="handleComplete(scope.row)"
                        >
                            完成
                        </el-button>
                        <el-button
                            v-if="['pending', 'confirmed'].includes(scope.row.status)"
                            type="danger"
                            size="small"
                            @click="handleCancel(scope.row)"
                        >
                            取消
                        </el-button>
                        <el-button
                            type="primary"
                            size="small"
                            @click="handleViewDetail(scope.row)"
                        >
                            详情
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <div class="pagination-container">
                <el-pagination
                    background
                    layout="prev, pager, next"
                    :total="total"
                    :page-size="limit"
                    :current-page="currentPage"
                    @current-change="handlePageChange"
                />
            </div>
        </el-card>

        <!-- 预订详情对话框 -->
        <el-dialog v-model="detailDialogVisible" title="预订详情" width="600px">
            <div v-if="currentBooking" class="booking-detail">
                <el-descriptions title="预订信息" :column="1" border>
                    <el-descriptions-item label="预订号">{{ currentBooking.id }}</el-descriptions-item>
                    <!--<el-descriptions-item label="用户手机号">{{ currentBooking.user.phone }}</el-descriptions-item>-->
                    <el-descriptions-item label="分店">
                        {{ getBranchName(currentBooking.room.branch_id) }}
                    </el-descriptions-item>
                    <el-descriptions-item label="地址">
                        {{ getBranchAddress(currentBooking.room.branch_id) }}
                    </el-descriptions-item>
                    <el-descriptions-item label="房间号">{{ currentBooking.room.room_number }}</el-descriptions-item>
                    <el-descriptions-item label="房间类型">{{ currentBooking.room.room_type }}</el-descriptions-item>
                    <el-descriptions-item label="入住日期">{{ formatDate(currentBooking.check_in_date) }}</el-descriptions-item>
                    <el-descriptions-item label="退房日期">{{ formatDate(currentBooking.check_out_date) }}</el-descriptions-item>
                    <el-descriptions-item label="住宿天数">{{ calculateDays(currentBooking) }} 晚</el-descriptions-item>
                    <el-descriptions-item label="房间价格">¥{{ currentBooking.room.price }} / 晚</el-descriptions-item>
                    <el-descriptions-item label="总价">¥{{ currentBooking.total_price }}</el-descriptions-item>
                    <el-descriptions-item label="状态">
                        <el-tag :type="getStatusType(currentBooking.status)">
                            {{ getStatusText(currentBooking.status) }}
                        </el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="预订时间">{{ currentBooking.created_at }}</el-descriptions-item>
                    <el-descriptions-item label="特殊要求" v-if="currentBooking.special_requests">
                        {{ currentBooking.special_requests }}
                    </el-descriptions-item>
                </el-descriptions>

                <div class="detail-actions" v-if="['pending', 'confirmed'].includes(currentBooking.status)">
                    <el-button
                        v-if="currentBooking.status === 'pending'"
                        type="success"
                        @click="handleConfirmFromDetail"
                    >
                        确认预订
                    </el-button>
                    <el-button
                        v-if="currentBooking.status === 'confirmed'"
                        type="warning"
                        @click="handleCompleteFromDetail"
                    >
                        完成预订
                    </el-button>
                    <el-button type="danger" @click="handleCancelFromDetail">取消预订</el-button>
                </div>
            </div>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { reqAdminBookings, reqAdminBookingCount, reqUpdateBookingStatus, reqBookingDetail } from '@/api/booking/admin_index';
import { reqBranchList } from '@/api/branch';

// 状态数据
const loading = ref(false);
const bookings = ref([]);
const total = ref(0);
const currentPage = ref(1);
const limit = ref(10);
const statusFilter = ref('');
const branchFilter = ref('');
const branchList = ref([]);
const detailDialogVisible = ref(false);
const currentBooking = ref(null);

// 获取预订列表
const fetchBookings = async () => {
    loading.value = true;
    try {
        const skip = (currentPage.value - 1) * limit.value;
        const params = {
            skip,
            limit: limit.value,
            status: statusFilter.value || undefined,
            branch_id: branchFilter.value || undefined
        };

        const [bookingsRes, countRes] = await Promise.all([
            reqAdminBookings(params),
            reqAdminBookingCount({
                status: statusFilter.value || undefined,
                branch_id: branchFilter.value || undefined
            })
        ]);

        bookings.value = bookingsRes.data;
        total.value = countRes.data.count;
    } catch (error) {
        console.error('获取预订列表失败:', error);
        ElMessage.error('获取预订列表失败');
    } finally {
        loading.value = false;
    }
};

// 获取分店列表
const getBranchList = async () => {
    try {
        const res = await reqBranchList();
        branchList.value = res.data || [];
    } catch (error) {
        console.error('获取分店列表失败:', error);
        ElMessage.error('获取分店列表失败');
    }
};

// 获取分店名称
const getBranchName = (branchId) => {
    if (!branchId || !branchList.value) return '未知分店';
    const branch = branchList.value.find(b => b.id === branchId);
    return branch ? branch.name : '未知分店';
};

// 获取分店地址
const getBranchAddress = (branchId) => {
    if (!branchId || !branchList.value) return '未知地址';
    const branch = branchList.value.find(b => b.id === branchId);
    return branch ? branch.address : '未知地址';
};

// 处理页码变化
const handlePageChange = (page) => {
    currentPage.value = page;
    fetchBookings();
};

// 处理筛选
const handleFilter = () => {
    currentPage.value = 1;
    fetchBookings();
};

// 确认预订
const handleConfirm = async (booking) => {
    try {
        await ElMessageBox.confirm('确认此预订?', '提示', {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning'
        });

        await reqUpdateBookingStatus(booking.id, 'confirmed');
        ElMessage.success('预订已确认');
        fetchBookings();
    } catch (error) {
        if (error !== 'cancel') {
            console.error('确认预订失败:', error);
            ElMessage.error('确认预订失败');
        }
    }
};

// 完成预订
const handleComplete = async (booking) => {
    try {
        await ElMessageBox.confirm('将此预订标记为已完成?', '提示', {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning'
        });

        await reqUpdateBookingStatus(booking.id, 'completed');
        ElMessage.success('预订已完成');
        fetchBookings();
    } catch (error) {
        if (error !== 'cancel') {
            console.error('完成预订失败:', error);
            ElMessage.error('完成预订失败');
        }
    }
};

// 取消预订
const handleCancel = async (booking) => {
    try {
        await ElMessageBox.confirm('确认取消此预订?', '提示', {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning'
        });

        await reqUpdateBookingStatus(booking.id, 'cancelled');
        ElMessage.success('预订已取消');
        fetchBookings();
    } catch (error) {
        if (error !== 'cancel') {
            console.error('取消预订失败:', error);
            ElMessage.error('取消预订失败');
        }
    }
};

// 查看预订详情
const handleViewDetail = async (booking) => {
    try {
        const res = await reqBookingDetail(booking.id);
        currentBooking.value = res.data;
        detailDialogVisible.value = true;
    } catch (error) {
        console.error('获取预订详情失败:', error);
        ElMessage.error('获取预订详情失败');
    }
};

// 从详情页确认预订
const handleConfirmFromDetail = async () => {
    if (!currentBooking.value) return;

    try {
        await ElMessageBox.confirm('确认此预订?', '提示', {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning'
        });

        await reqUpdateBookingStatus(currentBooking.value.id, 'confirmed');
        ElMessage.success('预订已确认');
        detailDialogVisible.value = false;
        fetchBookings();
    } catch (error) {
        if (error !== 'cancel') {
            console.error('确认预订失败:', error);
            ElMessage.error('确认预订失败');
        }
    }
};

// 从详情页完成预订
const handleCompleteFromDetail = async () => {
    if (!currentBooking.value) return;

    try {
        await ElMessageBox.confirm('将此预订标记为已完成?', '提示', {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning'
        });

        await reqUpdateBookingStatus(currentBooking.value.id, 'completed');
        ElMessage.success('预订已完成');
        detailDialogVisible.value = false;
        fetchBookings();
    } catch (error) {
        if (error !== 'cancel') {
            console.error('完成预订失败:', error);
            ElMessage.error('完成预订失败');
        }
    }
};

// 从详情页取消预订
const handleCancelFromDetail = async () => {
    if (!currentBooking.value) return;

    try {
        await ElMessageBox.confirm('确认取消此预订?', '提示', {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning'
        });

        await reqUpdateBookingStatus(currentBooking.value.id, 'cancelled');
        ElMessage.success('预订已取消');
        detailDialogVisible.value = false;
        fetchBookings();
    } catch (error) {
        if (error !== 'cancel') {
            console.error('取消预订失败:', error);
            ElMessage.error('取消预订失败');
        }
    }
};

// 格式化日期
const formatDate = (dateString) => {
    if (!dateString) return '';

    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');

    return `${year}-${month}-${day}`;
};

// 格式化日期时间
const formatDateTime = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return `${formatDate(dateString)} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
};

// 计算住宿天数
const calculateDays = (booking) => {
    if (!booking || !booking.check_in_date || !booking.check_out_date) {
        return 0;
    }

    const checkIn = new Date(booking.check_in_date);
    const checkOut = new Date(booking.check_out_date);
    const diffTime = Math.abs(checkOut - checkIn);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
};

// 获取状态文本
const getStatusText = (status) => {
    const statusMap = {
        'pending': '待确认',
        'confirmed': '已确认',
        'cancelled': '已取消',
        'completed': '已完成'
    };
    return statusMap[status] || status;
};

// 获取状态标签类型
const getStatusType = (status) => {
    const typeMap = {
        'pending': 'warning',
        'confirmed': 'primary',
        'cancelled': 'danger',
        'completed': 'success'
    };
    return typeMap[status] || 'info';
};

// 页面加载时获取数据
onMounted(() => {
    fetchBookings();
    getBranchList();
});
</script>

<style scoped>
.booking-admin-container {
    padding: 20px;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.filter-container {
    display: flex;
    gap: 10px;
}

.booking-table {
    margin-bottom: 20px;
}

.pagination-container {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
}

.booking-detail {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.detail-actions {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

.label {
    font-weight: bold;
    width: 100px;
}
</style>