import request from "@/utils/request";

enum API {
    BRANCH_LIST = "/branches/",
    BRANCH_DETAIL = "/branches/"
}

// 获取分店列表
export const reqBranchList = (params?: any) => 
    request.get<any, any>(API.BRANCH_LIST, { params });

// 获取分店详情
export const reqBranchDetail = (id: number) => 
    request.get<any, any>(API.BRANCH_DETAIL + id);

// 创建分店
export const reqCreateBranch = (data: any) => 
    request.post<any, any>(API.BRANCH_LIST, data);

// 更新分店
export const reqUpdateBranch = (id: number, data: any) => 
    request.put<any, any>(API.BRANCH_DETAIL + id, data);

// 删除分店
export const reqDeleteBranch = (id: number) => 
    request.delete<any, any>(API.BRANCH_DETAIL + id);