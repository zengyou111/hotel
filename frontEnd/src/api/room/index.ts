import request from "@/utils/request";

enum API {
    ROOM_LIST = "/rooms/",
    ROOM_DETAIL = "/rooms/"
}

// 获取客房列表
export const reqRoomList = (params?: any) => 
    request.get<any, any>(API.ROOM_LIST, { params });

// 获取客房详情
export const reqRoomDetail = (id: number) => 
    request.get<any, any>(API.ROOM_DETAIL + id);

// 创建客房
export const reqCreateRoom = (data: any) => 
    request.post<any, any>(API.ROOM_LIST, data);

// 更新客房
export const reqUpdateRoom = (id: number, data: any) => 
    request.put<any, any>(API.ROOM_DETAIL + id, data);

// 删除客房
export const reqDeleteRoom = (id: number) => 
    request.delete<any, any>(API.ROOM_DETAIL + id);