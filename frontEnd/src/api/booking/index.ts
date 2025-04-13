import request from "@/utils/request";

enum API {
    BOOKING_LIST = "/bookings/my-bookings",
    BOOKING_DETAIL = "/bookings/",
    BOOKING_CREATE = "/bookings/",
    BOOKING_CANCEL = "/bookings/",
    AVAILABLE_ROOMS = "/bookings/available-rooms"
}

// 获取当前用户的预订列表
export const reqMyBookings = (params?: any) => 
    request.get<any, any>(API.BOOKING_LIST, { params });

// 获取预订详情
export const reqBookingDetail = (id: number) => 
    request.get<any, any>(API.BOOKING_DETAIL + id);

// 创建预订
export const reqCreateBooking = (data: any) => 
    request.post<any, any>(API.BOOKING_CREATE, data);

// 取消预订
export const reqCancelBooking = (id: number) => 
    request.put<any, any>(`${API.BOOKING_CANCEL}${id}/cancel`);

// 获取可用房间
export const reqAvailableRooms = (params: any) => 
    request.get<any, any>(API.AVAILABLE_ROOMS, { params });