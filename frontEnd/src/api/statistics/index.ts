import request from "@/utils/request";

enum API {
    BOOKING_STATISTICS = "/statistics/bookings"
}

// 获取预订统计数据
export const reqBookingStatistics = () => 
    request.get<any, any>(API.BOOKING_STATISTICS);