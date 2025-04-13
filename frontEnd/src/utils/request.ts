import axios from "axios";
import { ElMessage } from "element-plus";

// 创建axios实例
const request = axios.create({
    baseURL: "/api",
    timeout: 5000
});

// 请求拦截器
request.interceptors.request.use(
    (config) => {
        // 从localStorage获取token
        const token = localStorage.getItem("token");
        if (token) {
            // 设置token到请求头
            config.headers["Authorization"] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 响应拦截器
request.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        // 处理错误响应
        let message = "";
        const status = error.response?.status;
        switch (status) {
            case 401:
                message = "未授权，请重新登录";
                // 可以在这里清除token并跳转到登录页
                localStorage.removeItem("token");
                window.location.href = "/login";
                break;
            case 403:
                message = "拒绝访问";
                break;
            case 404:
                message = "请求地址错误";
                break;
            case 500:
                message = "服务器内部错误";
                break;
            default:
                message = "网络连接异常";
        }
        ElMessage({
            type: "error",
            message
        });
        return Promise.reject(error);
    }
);

export default request;