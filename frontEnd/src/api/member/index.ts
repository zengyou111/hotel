import request from "@/utils/request";

enum API {
    MEMBER_LIST = "/members/",
    MEMBER_DETAIL = "/members/",
    AVAILABLE_USERS = "/members/available-users",
    USER_BY_PHONE = "/members/user/"
}

// 获取会员列表
export const reqMemberList = (params?: any) => 
    request.get<any, any>(API.MEMBER_LIST, { params });

// 获取会员详情
export const reqMemberDetail = (id: number) => 
    request.get<any, any>(API.MEMBER_DETAIL + id);

// 创建会员
export const reqCreateMember = (data: any) => 
    request.post<any, any>(API.MEMBER_LIST, data);

// 更新会员
export const reqUpdateMember = (id: number, data: any) => 
    request.put<any, any>(API.MEMBER_DETAIL + id, data);

// 删除会员
export const reqDeleteMember = (id: number) => 
    request.delete<any, any>(API.MEMBER_DETAIL + id);

// 获取可用用户列表（没有关联会员的用户）
export const reqAvailableUsers = (params?: any) =>
    request.get<any, any>(API.AVAILABLE_USERS, { params });

// 通过手机号查找用户
export const reqUserByPhone = (phone: string) =>
    request.get<any, any>(API.USER_BY_PHONE + phone);