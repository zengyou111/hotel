<template>
    <!--顶部-->
    <div class="top" :class="{ 'top-collapsed': isCollapsed }">
        <!--内容部分-->
        <div class="content">
            <!--左侧-->
            <div class="left">
                <img src="../../assets/images/logo.png" @click="goHome" class="logo">
                <p>酒店预订系统</p>
            </div>
            <!--右侧-->
            <div class="right">
                <p class="help">帮助中心</p>
                <p class="login" v-if="!userStore.getToken" @click="goLogin">注册登录</p>
                <el-dropdown v-else @command="handleCommand">
                    <span class="user-info">
                        <img class="avatar" src="../../assets/images/avatar.jpg">
                        <span class="username">{{ userStore.getPhone }}</span>
                    </span>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </div>
        </div>
        <!--收缩按钮（始终固定在底部）-->
        <div class="collapse-button" @click="toggleCollapse">
            <el-icon :class="{ 'rotate-icon': isCollapsed }">
                <arrow-up></arrow-up>
            </el-icon>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from "vue-router";
import { ArrowUp } from '@element-plus/icons-vue';
import { ElMessageBox } from 'element-plus';
import useUserStore from "@/store/modules/user";

let $router = useRouter();
let userStore = useUserStore();

// 控制顶部组件收缩状态
const isCollapsed = ref<boolean>(false);

const goLogin = () => {
    $router.push({ path: '/login' });
};

// 切换顶部组件收缩状态
const toggleCollapse = () => {
    isCollapsed.value = !isCollapsed.value;
};

// 处理下拉菜单命令
const handleCommand = (command: string) => {
    if (command === 'profile') {
        // 根据用户角色跳转到不同的个人信息页面
        if (userStore.isAdmin) {
            $router.push({ path: '/admin/dashboard' });
        } else {
            $router.push({ path: '/user/profile' });
        }
    } else if (command === 'logout') {
        // 退出登录确认
        ElMessageBox.confirm(
            '确定要退出登录吗?',
            '提示',
            {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            }
        ).then(() => {
            // 清除用户信息
            userStore.clearUserInfo();
            // 跳转到登录页
            $router.push('/login');
        }).catch(() => {
            // 取消退出
        });
    }
};

// 切换回主页
const goHome = () => {
    // 根据用户角色跳转到不同的首页
    if (!userStore.getToken) {
        $router.push({ path: '/login' });
    } else if (userStore.isAdmin) {
        $router.push({ path: '/admin/dashboard' });
    } else {
        $router.push({ path: '/user/home' });
    }
};
</script>

<style scoped lang="scss">
.top {
    z-index: 999;
    width: 100%;
    height: 10vh; /* 初始高度 */
    background: linear-gradient(180deg, #ffffff, #f0f7f4); /* 白色到浅绿色渐变 */
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    transition: height 0.3s ease;
    position: relative;

    /* 收缩状态 */
    &.top-collapsed {
        height: 30px;
    }

    /* 内容部分 */
    .content {
        width: 100%;
        flex: 1;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: opacity 0.3s ease;
        padding: 0 20px;

        /* 收缩时隐藏内容 */
        .top-collapsed & {
            opacity: 0;
            pointer-events: none;
        }

        /* 左侧内容 */
        .left {
            display: flex;
            align-items: center;
            .logo {
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                cursor: pointer;
                &:hover {
                    transform: scale(1.1);
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                }
            }
            img {
                width: 50px;
                height: 50px;
            }
            p {
                font-size: 24px; /* 字体稍大，突出品牌 */
                color: #409EFF; /* 酒店蓝色 */
                margin-left: 12px;
                font-weight: 600; /* 加粗，简约大气 */
                font-family: 'Helvetica Neue', sans-serif; /* 大厂常用字体 */
            }
        }

        /* 右侧内容 */
        .right {
            display: flex;
            align-items: center;
            font-size: 14px;
            color: #666; /* 深灰色，简洁 */
            .help {
                margin-right: 20px;
                cursor: pointer;
                &:hover {
                    color: #409EFF; /* 悬停时变蓝 */
                }
            }
            .login {
                cursor: pointer;
                color: #409EFF; /* 蓝色突出注册登录 */
                font-weight: 500;
                &:hover {
                    color: #337ecc; /* 深蓝色悬停效果 */
                }
            }
            .user-info {
                display: flex;
                align-items: center;
                cursor: pointer;
            }
            .username {
                margin-left: 8px;
                color: #333;
            }
            .avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                cursor: pointer;
                border: 2px solid #e6f0f9; /* 浅蓝色边框 */
            }
        }
    }

    /* 收缩按钮 */
    .collapse-button {
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        cursor: pointer;
        background-color: #ffffff;
        border: 1px solid #e0e0e0; /* 浅灰边框 */
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* 更轻的阴影 */
        transition: all 0.3s ease;

        &:hover {
            background-color: #f7f9fa; /* 浅蓝色悬停背景 */
            border-color: #409EFF;
        }

        .el-icon {
            color: #409EFF; /* 蓝色箭头 */
            transition: transform 0.3s ease;
            &.rotate-icon {
                transform: rotate(180deg);
            }
        }
    }
}
</style>