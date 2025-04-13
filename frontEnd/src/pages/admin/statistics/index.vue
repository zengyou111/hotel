<template>
    <div class="statistics-container">
        <h2>数据统计</h2>

        <div v-loading="loading">
            <!-- 数据概览卡片 -->
            <el-row :gutter="20" class="data-overview">
                <el-col :span="6">
                    <el-card shadow="hover" class="data-card">
                        <template #header>
                            <div class="card-header">
                                <span>总预订数</span>
                            </div>
                        </template>
                        <div class="card-value">{{ statistics.total_bookings || 0 }}</div>
                    </el-card>
                </el-col>

                <el-col :span="6">
                    <el-card shadow="hover" class="data-card">
                        <template #header>
                            <div class="card-header">
                                <span>总收入</span>
                            </div>
                        </template>
                        <div class="card-value">¥{{ formatPrice(statistics.total_revenue) }}</div>
                    </el-card>
                </el-col>

                <el-col :span="6">
                    <el-card shadow="hover" class="data-card">
                        <template #header>
                            <div class="card-header">
                                <span>总用户数</span>
                            </div>
                        </template>
                        <div class="card-value">{{ statistics.user_statistics?.total_users || 0 }}</div>
                    </el-card>
                </el-col>

                <el-col :span="6">
                    <el-card shadow="hover" class="data-card">
                        <template #header>
                            <div class="card-header">
                                <span>有预订记录用户</span>
                            </div>
                        </template>
                        <div class="card-value">{{ statistics.user_statistics?.users_with_bookings || 0 }}</div>
                    </el-card>
                </el-col>
            </el-row>

            <!-- 预订状态统计 -->
            <el-row :gutter="20" class="chart-row">
                <el-col :span="12">
                    <el-card shadow="hover" class="chart-card">
                        <template #header>
                            <div class="card-header">
                                <span>预订状态分布</span>
                            </div>
                        </template>
                        <div id="status-chart" class="chart"></div>
                    </el-card>
                </el-col>

                <el-col :span="12">
                    <el-card shadow="hover" class="chart-card">
                        <template #header>
                            <div class="card-header">
                                <span>最近7天预订趋势</span>
                            </div>
                        </template>
                        <div id="daily-chart" class="chart"></div>
                    </el-card>
                </el-col>
            </el-row>

            <!-- 分店和房型统计 -->
            <el-row :gutter="20" class="chart-row">
                <el-col :span="12">
                    <el-card shadow="hover" class="chart-card">
                        <template #header>
                            <div class="card-header">
                                <span>分店预订分布</span>
                            </div>
                        </template>
                        <div id="branch-chart" class="chart"></div>
                    </el-card>
                </el-col>

                <el-col :span="12">
                    <el-card shadow="hover" class="chart-card">
                        <template #header>
                            <div class="card-header">
                                <span>房型受欢迎程度</span>
                            </div>
                        </template>
                        <div id="room-type-chart" class="chart"></div>
                    </el-card>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { reqBookingStatistics } from '@/api/statistics/index';
import { ElMessage } from 'element-plus';
import * as echarts from 'echarts';

const loading = ref(true);
const statistics = ref<any>({});
let statusChart: any = null;
let dailyChart: any = null;
let branchChart: any = null;
let roomTypeChart: any = null;

// 获取统计数据
const fetchStatistics = async () => {
    loading.value = true;
    try {
        const res = await reqBookingStatistics();
        statistics.value = res.data;
        renderCharts();
    } catch (error) {
        console.error('获取统计数据失败:', error);
        ElMessage.error('获取统计数据失败');
    } finally {
        loading.value = false;
    }
};

// 渲染所有图表
const renderCharts = () => {
    renderStatusChart();
    renderDailyChart();
    renderBranchChart();
    renderRoomTypeChart();
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

    const data = Object.entries(statusStats).map(([status, count]) => ({
        name: statusMap[status] || status,
        value: count
    }));

    const option = {
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 10,
            data: data.map(item => item.name)
        },
        series: [
            {
                name: '预订状态',
                type: 'pie',
                radius: ['50%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
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

// 渲染每日预订趋势图
const renderDailyChart = () => {
    const dailyStats = statistics.value.daily_statistics || {};
    const chartDom = document.getElementById('daily-chart');
    if (!chartDom) return;

    dailyChart = echarts.init(chartDom);

    const dates = Object.keys(dailyStats).sort();
    const counts = dates.map(date => dailyStats[date]);

    // 格式化日期显示
    const formattedDates = dates.map(date => {
        const d = new Date(date);
        return `${d.getMonth() + 1}/${d.getDate()}`;
    });

    const option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        xAxis: {
            type: 'category',
            data: formattedDates,
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
                data: counts,
                type: 'line',
                smooth: true,
                symbol: 'circle',
                symbolSize: 8,
                lineStyle: {
                    width: 3
                },
                itemStyle: {
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
                                color: 'rgba(64, 158, 255, 0.5)'
                            },
                            {
                                offset: 1,
                                color: 'rgba(64, 158, 255, 0.1)'
                            }
                        ]
                    }
                }
            }
        ]
    };

    dailyChart.setOption(option);
};

// 渲染分店预订分布图
const renderBranchChart = () => {
    const branchStats = statistics.value.branch_statistics || {};
    const chartDom = document.getElementById('branch-chart');
    if (!chartDom) return;

    branchChart = echarts.init(chartDom);

    const data = Object.entries(branchStats).map(([name, count]) => ({
        name,
        value: count
    }));

    const option = {
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 10,
            data: data.map(item => item.name)
        },
        series: [
            {
                name: '分店预订',
                type: 'pie',
                radius: '55%',
                center: ['50%', '60%'],
                data: data,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    branchChart.setOption(option);
};

// 渲染房型受欢迎程度图
const renderRoomTypeChart = () => {
    const roomTypeStats = statistics.value.room_type_popularity || {};
    const chartDom = document.getElementById('room-type-chart');
    if (!chartDom) return;

    roomTypeChart = echarts.init(chartDom);

    const roomTypes = Object.keys(roomTypeStats);
    const counts = roomTypes.map(type => roomTypeStats[type]);

    const option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        xAxis: {
            type: 'category',
            data: roomTypes,
            axisLabel: {
                interval: 0,
                rotate: 30
            }
        },
        yAxis: {
            type: 'value',
            minInterval: 1
        },
        series: [
            {
                data: counts,
                type: 'bar',
                barWidth: '60%',
                itemStyle: {
                    color: '#67C23A'
                }
            }
        ]
    };

    roomTypeChart.setOption(option);
};

// 格式化价格显示
const formatPrice = (price) => {
    if (price === undefined || price === null) return '0.00';
    return parseFloat(price).toFixed(2);
};

// 窗口大小变化时重新调整图表大小
const handleResize = () => {
    statusChart?.resize();
    dailyChart?.resize();
    branchChart?.resize();
    roomTypeChart?.resize();
};

onMounted(() => {
    fetchStatistics();
    window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
    window.removeEventListener('resize', handleResize);
    statusChart?.dispose();
    dailyChart?.dispose();
    branchChart?.dispose();
    roomTypeChart?.dispose();
});
</script>

<style scoped>
.statistics-container {
    padding: 20px;
}

.data-overview {
    margin-bottom: 20px;
}

.data-card {
    height: 150px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-value {
    font-size: 36px;
    font-weight: bold;
    color: #409EFF;
    text-align: center;
    margin-top: 20px;
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
</style>