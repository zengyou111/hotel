// 本地存储用户信息
export const SET_TOKEN = (userInfo: string) => {
    localStorage.setItem("USERINFO", userInfo);
};

// 获取本地用户信息字符串
export const GET_TOKEN = () => {
    return localStorage.getItem("USERINFO");
};

// 获取解析后的用户信息对象
export const GET_USER_INFO = () => {
    const userInfo = localStorage.getItem("USERINFO");
    if (userInfo) {
        try {
            return JSON.parse(userInfo);
        } catch (e) {
            // 兼容旧版本，只存储了token的情况
            return { access_token: userInfo };
        }
    }
    return null;
};

// 清除本地用户数据
export const REMOVE_TOKEN = () => {
    localStorage.removeItem("USERINFO");
};