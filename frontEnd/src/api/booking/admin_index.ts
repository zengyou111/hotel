import request from "@/utils/request";

enum API {
    ADMIN_BOOKING_LIST = "/bookings/admin",
    ADMIN_BOOKING_COUNT = "/bookings/admin/count",
    BOOKING_DETAIL = "/bookings/",
    BOOKING_STATUS = "/bookings/"
}

// 获取所有预订列表（管理员）
export const reqAdminBookings = (params?: any) => 
    request.get<any, any>(API.ADMIN_BOOKING_LIST, { params });

// 获取预订总数（管理员）
export const reqAdminBookingCount = (params?: any) => 
    request.get<any, any>(API.ADMIN_BOOKING_COUNT, { params });

// 获取预订详情
export const reqBookingDetail = (id: number) => 
    request.get<any, any>(API.BOOKING_DETAIL + id);

// 更新预订状态
export const reqUpdateBookingStatus = (id: number, status: string) => 
    request.put<any, any>(`${API.BOOKING_STATUS}${id}/status`, { status });