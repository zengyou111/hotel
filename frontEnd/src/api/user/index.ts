// api/user/index.ts
import request from "@/utils/request";

enum API {
    REGISTER = "/auth/register",
    LOGIN = "/auth/login",
    USER_INFO = "/users/me"  // 添加获取当前用户信息的API
}

// 注册接口
export const reqRegister = (phone: string, password: string, is_admin: boolean = false) =>
    request.post<any, any>(API.REGISTER, {
        phone,
        password,
        is_admin
    });

// 登录接口（使用手机号+密码）
export const reqLogin = (phone: string, password: string) => {
    // 使用URLSearchParams对象
    const params = new URLSearchParams();
    params.append('username', phone);
    params.append('password', password);

    return request.post<any, any>(API.LOGIN, params, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    });
};

// 获取当前登录用户信息
export const reqUserInfo = () => request.get<any, any>(API.USER_INFO);