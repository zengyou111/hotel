<template>
    <div class="dashboard-container">
        <h2>仪表盘</h2>

        <div v-loading="loading">
            <!-- 数据概览卡片 -->
            <el-row :gutter="20" class="data-overview">
                <el-col :span="6">
                    <el-card shadow="hover" class="data-card">
                        <div class="card-content">
                            <div class="card-icon">
                                <el-icon><Calendar /></el-icon>
                            </div>
                            <div class="card-info">
                                <div class="card-title">总预订数</div>
                                <div class="card-value">{{ statistics.total_bookings || 0 }}</div>
                            </div>
                        </div>
                    </el-card>
                </el-col>

                <el-col :span="6">
                    <el-card shadow="hover" class="data-card">
                        <div class="card-content">
                            <div class="card-icon revenue">
                                <el-icon><Money /></el-icon>
                            </div>
                            <div class="card-info">
                                <div class="card-title">总收入</div>
                                <div class="card-value">¥{{ formatPrice(statistics.total_revenue) }}</div>
                            </div>
                        </div>
                    </el-card>
                </el-col>

                <el-col :span="6">
                    <el-card shadow="hover" class="data-card">
                        <div class="card-content">
                            <div class="card-icon users">
                                <el-icon><User /></el-icon>
                            </div>
                            <div class="card-info">
                                <div class="card-title">总用户数</div>
                                <div class="card-value">{{ statistics.user_statistics?.total_users || 0 }}</div>
                            </div>
                        </div>
                    </el-card>
                </el-col>

                <el-col :span="6">
                    <el-card shadow="hover" class="data-card">
                        <div class="card-content">
                            <div class="card-icon branches">
                                <el-icon><OfficeBuilding /></el-icon>
                            </div>
                            <div class="card-info">
                                <div class="card-title">分店数量</div>
                                <div class="card-value">{{ branchCount }}</div>
                            </div>
                        </div>
                    </el-card>
                </el-col>
            </el-row>

            <!-- 预订状态统计 -->
            <el-row :gutter="20" class="chart-row">
                <el-col :span="16">
                    <el-card shadow="hover" class="chart-card">
                        <template #header>
                            <div class="card-header">
                                <span>最近7天预订趋势</span>
                            </div>
                        </template>
                        <div id="daily-chart" class="chart"></div>
                    </el-card>
                </el-col>

                <el-col :span="8">
                    <el-card shadow="hover" class="chart-card">
                        <template #header>
                            <div class="card-header">
                                <span>预订状态分布</span>
                            </div>
                        </template>
                        <div id="status-chart" class="chart"></div>
                    </el-card>
                </el-col>
            </el-row>

            <!-- 最近预订和快捷操作 -->
            <el-row :gutter="20" class="bottom-row">
                <el-col :span="16">
                    <el-card shadow="hover" class="recent-bookings-card">
                        <template #header>
                            <div class="card-header">
                                <span>最近预订</span>
                                <el-button type="primary" size="small" @click="goToBookings">查看全部</el-button>
                            </div>
                        </template>
                        <el-table :data="recentBookings" style="width: 100%">
                            <el-table-column prop="id" label="预订号" width="80" />
                            <el-table-column label="房间" width="120">
                                <template #default="scope">
                                    {{ scope.row.room.room_number }} ({{ scope.row.room.room_type }})
                                </template>
                            </el-table-column>
                            <el-table-column label="入住日期" width="100">
                                <template #default="scope">
                                    {{ formatDate(scope.row.check_in_date) }}
                                </template>
                            </el-table-column>
                            <el-table-column label="退房日期" width="100">
                                <template #default="scope">
                                    {{ formatDate(scope.row.check_out_date) }}
                                </template>
                            </el-table-column>
                            <el-table-column prop="total_price" label="总价" width="80">
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

                        </el-table>
                    </el-card>
                </el-col>

                <el-col :span="8">
                    <el-card shadow="hover" class="quick-actions-card">
                        <template #header>
                            <div class="card-header">
                                <span>快捷操作</span>
                            </div>
                        </template>
                        <div class="quick-actions">
                            <el-button type="primary" @click="goToBookings">
                                <el-icon><Tickets /></el-icon>
                                预订管理
                            </el-button>
                            <el-button type="success" @click="goToRooms">
                                <el-icon><House /></el-icon>
                                房间管理
                            </el-button>
                            <el-button type="warning" @click="goToBranches">
                                <el-icon><OfficeBuilding /></el-icon>
                                分店管理
                            </el-button>
                            <el-button type="info" @click="goToUsers">
                                <el-icon><User /></el-icon>
                                用户管理
                            </el-button>
                            <el-button type="danger" @click="goToStatistics">
                                <el-icon><DataAnalysis /></el-icon>
                                数据统计
                            </el-button>
                        </div>
                    </el-card>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { reqBookingStatistics } from '@/api/statistics/index';
import { reqAdminBookings, reqUpdateBookingStatus } from '@/api/booking/admin_index';
import { reqBranchList } from '@/api/branch/index';
import { ElMessage, ElMessageBox } from 'element-plus';
import * as echarts from 'echarts';
import {
    Calendar, Money, User, OfficeBuilding,
    Tickets, House, DataAnalysis
} from '@element-plus/icons-vue';

const router = useRouter();
const loading = ref(true);
const statistics = ref<any>({});
const recentBookings = ref([]);
const branchCount = ref(0);
let dailyChart: any = null;
let statusChart: any = null;

// 获取统计数据
const fetchStatistics = async () => {
    try {
        const res = await reqBookingStatistics();
        statistics.value = res.data;
        renderCharts();
    } catch (error) {
        console.error('获取统计数据失败:', error);
        ElMessage.error('获取统计数据失败');
    }
};

// 获取最近预订
const fetchRecentBookings = async () => {
    try {
        const res = await reqAdminBookings({ skip: 0, limit: 5 });
        recentBookings.value = res.data;
    } catch (error) {
        console.error('获取最近预订失败:', error);
        ElMessage.error('获取最近预订失败');
    }
};

// 获取分店数量
const fetchBranchCount = async () => {
    try {
        const res = await reqBranchList();
        branchCount.value = res.data.length;
    } catch (error) {
        console.error('获取分店数量失败:', error);
        ElMessage.error('获取分店数量失败');
    }
};

// 加载所有数据
const loadAllData = async () => {
    loading.value = true;
    try {
        await Promise.all([
            fetchStatistics(),
            fetchRecentBookings(),
            fetchBranchCount()
        ]);
    } catch (error) {
        console.error('加载数据失败:', error);
    } finally {
        loading.value = false;
    }
};

// 渲染图表
const renderCharts = () => {
    renderDailyChart();
    renderStatusChart();
};

// 渲染每日预订趋势图
const renderDailyChart = () => {
    const dailyStats = statistics.value.daily_statistics || {};
    const chartDom = document.getElementById('daily-chart');
    if (!chartDom) return;

    dailyChart = echarts.init(chartDom);

    const dates = Object.keys(dailyStats).sort();
    const counts = dates.map(date => dailyStats[date]);

    const option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: dates.map(date => {
                const d = new Date(date);
                return `${d.getMonth() + 1}/${d.getDate()}`;
            }),
            axisLabel: {
                interval: 0
            }
        },
        yAxis: {
            type: 'value',
            minInterval: 1
        },
        series: [
            {
                name: '预订数',
                data: counts,
                type: 'line',
                smooth: true,
                lineStyle: {
                    width: 3,
                    color: '#409EFF'
                },
                areaStyle: {
                    color: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [
                            {
                                offset: 0,
                                color: 'rgba(64, 158, 255, 0.7)'
                            },
                            {
                                offset: 1,
                                color: 'rgba(64, 158, 255, 0.1)'
                            }
                        ]
                    }
                },
                itemStyle: {
                    color: '#409EFF'
                }
            }
        ]
    };

    dailyChart.setOption(option);
};

// 渲染预订状态分布图
const renderStatusChart = () => {
    const statusStats = statistics.value.status_statistics || {};
    const chartDom = document.getElementById('status-chart');
    if (!chartDom) return;

    statusChart = echarts.init(chartDom);

    const statusMap = {
        'pending': '待确认',
        'confirmed': '已确认',
        'cancelled': '已取消',
        'completed': '已完成'
    };

    const colorMap = {
        'pending': '#E6A23C',
        'confirmed': '#409EFF',
        'cancelled': '#F56C6C',
        'completed': '#67C23A'
    };

    const data = Object.entries(statusStats).map(([status, count]) => ({
        name: statusMap[status] || status,
        value: count,
        itemStyle: {
            color: colorMap[status]
        }
    }));

    const option = {
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            right: 10,
            top: 'center',
            data: data.map(item => item.name)
        },
        series: [
            {
                type: 'pie',
                radius: ['50%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 16,
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: data
            }
        ]
    };

    statusChart.setOption(option);
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
        fetchRecentBookings();
        fetchStatistics();
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
        fetchRecentBookings();
        fetchStatistics();
    } catch (error) {
        if (error !== 'cancel') {
            console.error('完成预订失败:', error);
            ElMessage.error('完成预订失败');
        }
    }
};

// 格式化价格显示
const formatPrice = (price) => {
    if (price === undefined || price === null) return '0.00';
    return parseFloat(price).toFixed(2);
};

// 格式化日期
const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');

    return `${month}/${day}`;
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

// 导航函数
const goToBookings = () => router.push('/admin/booking');
const goToRooms = () => router.push('/admin/room');
const goToBranches = () => router.push('/admin/branch');
const goToUsers = () => router.push('/admin/member');
const goToStatistics = () => router.push('/admin/statistics');

// 窗口大小变化时重新调整图表大小
const handleResize = () => {
    dailyChart?.resize();
    statusChart?.resize();
};

onMounted(() => {
    loadAllData();
    window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
    window.removeEventListener('resize', handleResize);
    dailyChart?.dispose();
    statusChart?.dispose();
});
</script>

<style scoped>
.dashboard-container {
    padding: 20px;
}

.data-overview {
    margin-bottom: 20px;
}

.data-card {
    height: 120px;
}

.card-content {
    display: flex;
    align-items: center;
    height: 100%;
}

.card-icon {
    width: 64px;
    height: 64px;
    border-radius: 8px;
    background-color: #409EFF;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 16px;
}

.card-icon :deep(svg) {
    font-size: 32px;
    color: white;
}

.card-icon.revenue {
    background-color: #67C23A;
}

.card-icon.users {
    background-color: #E6A23C;
}

.card-icon.branches {
    background-color: #F56C6C;
}

.card-info {
    flex: 1;
}

.card-title {
    font-size: 16px;
    color: #606266;
    margin-bottom: 8px;
}

.card-value {
    font-size: 24px;
    font-weight: bold;
    color: #303133;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chart-row {
    margin-bottom: 20px;
}

.chart-card {
    height: 400px;
}

.chart {
    height: 320px;
}

.bottom-row {
    margin-bottom: 20px;
}

.recent-bookings-card {
    height: 400px;
}

.quick-actions-card {
    height: 400px;
}

.quick-actions {
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 16px 0;
}

.quick-actions .el-button {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    height: 50px;
    font-size: 16px;
}

.quick-actions .el-button :deep(svg) {
    margin-right: 8px;
    font-size: 20px;
}
</style>