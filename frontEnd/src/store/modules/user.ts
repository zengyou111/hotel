import { defineStore } from 'pinia';

// 定义用户信息接口
interface UserInfo {
  access_token: string;
  token_type: string;
  phone: string;
  is_admin: boolean;
}

// 定义状态接口
interface UserState {
  token: string | null;
  userInfo: UserInfo | null;
}

// 创建用户store
const useUserStore = defineStore('user', {
  // 定义状态
  state: (): UserState => {
    return {
      token: localStorage.getItem('token'),
      userInfo: null
    };
  },
  // 定义getters
  getters: {
    getToken(): string | null {
      return this.token;
    },
    getPhone(): string {
      return this.userInfo?.phone || '';
    },
    isAdmin(): boolean {
      // 确保明确返回布尔值
      return this.userInfo?.is_admin === true;
    }
  },
  // 定义actions
  actions: {
    // 设置用户信息
    setUserInfo(userInfo: UserInfo) {
      this.userInfo = userInfo;
      this.token = userInfo.access_token;
      localStorage.setItem('token', userInfo.access_token);
      console.log("Store中设置的用户信息:", this.userInfo);
      console.log("是否管理员:", this.isAdmin);
    },
    // 清除用户信息
    clearUserInfo() {
      this.userInfo = null;
      this.token = null;
      localStorage.removeItem('token');
    },
    // 更新用户信息
    updateUserInfo(userInfo: Partial<UserInfo>) {
      if (this.userInfo) {
        this.userInfo = { ...this.userInfo, ...userInfo };
      }
    },
    // 退出登录
    logout() {
      this.clearUserInfo();
    }
  }
});

export default useUserStore;