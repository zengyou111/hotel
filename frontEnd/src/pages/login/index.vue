<template>
    <div class="login_container">
        <el-row>
            <el-col :span="12" :xs="0"></el-col>
            <el-col :span="12" :xs="24">
                <div class="content">
                    <h1>Hello</h1>
                    <h2>欢迎来到 酒店平台</h2>
                    <!-- 密码登录 -->
                    <div v-if="flag === 1" class="login_form_password">
                        <el-form :model="loginForm">
                            <el-form-item>
                                <el-input :prefix-icon="Iphone" v-model="loginForm.phone" placeholder="请输入手机号"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input :prefix-icon="Lock" type="password" v-model="loginForm.password" placeholder="请输入密码"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-button @click="Login" style="border-radius: 20px; margin: 10px 50px; width: 90%" type="primary" size="large">登录</el-button>
                            </el-form-item>
                        </el-form>
                        <div style="display: flex; align-items: center; justify-content: center;">
                            <span style="font-size: 15px">没有注册?</span>
                            <span style="color: #55fe9e; font-size: 15px; margin-left: 5px" @click="switchStatus(2)">点击注册</span>
                        </div>
                    </div>
                    <!-- 注册 -->
                    <div v-else-if="flag === 2" class="register_form">
                        <el-form :model="registerForm">
                            <el-form-item>
                                <el-input :prefix-icon="Iphone" v-model="registerForm.phone" placeholder="请输入手机号"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input :prefix-icon="Lock" type="password" v-model="registerForm.password" placeholder="请输入密码"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-checkbox v-model="registerForm.is_admin">注册为管理员</el-checkbox>
                            </el-form-item>
                            <el-form-item>
                                <el-button @click="Register" style="border-radius: 20px; margin: 10px 50px; width: 90%" type="primary" size="large">注册</el-button>
                            </el-form-item>
                            <h1 style="font-size: 15px; text-align: center" @click="switchStatus(1)">返回登录</h1>
                        </el-form>
                    </div>
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script setup lang="ts" name="Login">
import { ref, reactive } from "vue";
import { Iphone, Lock } from "@element-plus/icons-vue";
import { reqRegister, reqLogin, reqUserInfo } from "@/api/user";
import { ElMessage } from "element-plus";
import useUserStore from "@/store/modules/user";
import { useRouter } from "vue-router";

let userStore = useUserStore();
let $router = useRouter();
let flag = ref<number>(1); // 1: 密码登录, 2: 注册

// 登录表单数据
let loginForm = reactive({
    phone: "",
    password: ""
});

// 注册表单数据
let registerForm = reactive({
    phone: "",
    password: "",
    is_admin: false
});

// 切换状态
const switchStatus = (status: number) => {
    flag.value = status;
};

// 注册
const Register = async () => {
    try {
        if (!registerForm.phone || !registerForm.password) {
            ElMessage({ type: "warning", message: "请输入手机号和密码" });
            return;
        }

        console.log("注册信息:", {
            phone: registerForm.phone,
            password: registerForm.password,
            is_admin: registerForm.is_admin
        });

        let res = await reqRegister(
            registerForm.phone,
            registerForm.password,
            registerForm.is_admin
        );

        if (res.data && res.data.access_token) {
            ElMessage({ type: "success", message: "注册成功，请登录" });

            // 保存注册时使用的手机号和密码
            const registeredPhone = registerForm.phone;
            const registeredPassword = registerForm.password;
            const isAdmin = registerForm.is_admin;

            // 清空注册表单
            registerForm.phone = "";
            registerForm.password = "";
            registerForm.is_admin = false;

            // 自动填充登录表单
            loginForm.phone = registeredPhone;
            loginForm.password = registeredPassword;

            switchStatus(1); // 注册成功后切换到登录页面
        } else {
            ElMessage({ type: "error", message: "注册失败，请稍后重试" });
        }
    } catch (error) {
        ElMessage({ type: "error", message: "注册失败，可能是手机号已被注册" });
    }
};

// 登录（手机号+密码）
const Login = async () => {
    try {
        if (!loginForm.phone || !loginForm.password) {
            ElMessage({ type: "warning", message: "请输入手机号和密码" });
            return;
        }

        console.log("登录信息:", {
            phone: loginForm.phone,
            password: loginForm.password
        });

        let res = await reqLogin(loginForm.phone, loginForm.password);
        if (res.data && res.data.access_token) {
            // 获取用户信息
            try {
                // 先存储token，以便后续请求使用
                const token = res.data.access_token;
                localStorage.setItem('token', token);

                // 获取用户详细信息
                const userInfoRes = await reqUserInfo();
                console.log("用户详细信息:", userInfoRes.data);

                if (userInfoRes.data) {
                    // 构建完整的用户信息
                    const userInfo = {
                        access_token: token,
                        token_type: res.data.token_type,
                        phone: loginForm.phone,
                        is_admin: userInfoRes.data.is_admin
                    };

                    console.log("完整用户信息:", userInfo);

                    // 存储用户信息
                    userStore.setUserInfo(userInfo);

                    // 根据用户类型跳转不同页面
                    if (userInfo.is_admin) {
                        console.log("管理员登录，跳转到管理员页面");
                        await $router.push({ path: "/admin/dashboard" });
                        ElMessage({ type: "success", message: "管理员登录成功" });
                    } else {
                        console.log("普通用户登录，跳转到用户页面");
                        await $router.push({ path: "/user/home" });
                        ElMessage({ type: "success", message: "用户登录成功" });
                    }
                } else {
                    ElMessage({ type: "error", message: "获取用户信息失败" });
                }
            } catch (error) {
                console.error("获取用户信息失败:", error);
                ElMessage({ type: "error", message: "获取用户信息失败" });
            }
        } else {
            ElMessage({ type: "error", message: "登录失败，请检查手机号和密码" });
        }
    } catch (error) {
        console.error("登录失败:", error);
        ElMessage({ type: "error", message: "登录失败，请稍后重试" });
    }
};
</script>

<style scoped lang="scss">
.login_container {
    width: 100vw;
    height: 100vh;
    background: url("@/assets/images/hotel.png");
    background-size: cover;
    .content {
        position: relative;
        width: 60%;
        top: 30vh;
        background: url("@/assets/images/login_form.png") no-repeat;
        background-size: cover;
        padding: 40px;
        h1 {
            margin: 10px;
            color: white;
            font-size: 40px;
        }
        h2 {
            margin: 20px 10px;
            color: white;
            font-size: 20px;
        }
        .login_form_password,
        .register_form {
            margin: 20px 0;
            padding: 10px;
            width: 100%;
        }
    }
}
</style>