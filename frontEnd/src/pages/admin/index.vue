<template>
    <div class="admin-container">
      <el-container>
        <el-aside width="200px">
          <el-menu
            :default-active="activeMenu"
            class="el-menu-vertical"
            background-color="#304156"
            text-color="#bfcbd9"
            active-text-color="#409EFF"
            router
          >
            <el-menu-item index="/admin/dashboard">
              <el-icon><DataLine /></el-icon>
              <span>管理员首页</span>
            </el-menu-item>
            <el-menu-item index="/admin/member">
              <el-icon><User /></el-icon>
              <span>会员管理</span>
            </el-menu-item>
            <el-menu-item index="/admin/branch">
              <el-icon><House /></el-icon>
              <span>分店管理</span>
            </el-menu-item>
            <el-menu-item index="/admin/room">
              <el-icon><Key /></el-icon>
              <span>客房管理</span>
            </el-menu-item>
            <el-menu-item index="/admin/booking">
              <el-icon><Calendar /></el-icon>
              <span>预订管理</span>
            </el-menu-item>
            <el-menu-item index="/admin/statistics">
              <el-icon><PieChart /></el-icon>
              <span>数据统计</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-container>
          <el-main>
            <router-view></router-view>
          </el-main>
        </el-container>
      </el-container>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed } from 'vue';
  import { useRoute } from 'vue-router';
  import { DataLine, User, House, Key, Calendar, PieChart } from '@element-plus/icons-vue';
  
  const route = useRoute();
  
  // 计算当前激活的菜单项
  const activeMenu = computed(() => {
    return route.path;
  });
  </script>
  
  <style scoped>
  .admin-container {
    height: calc(100vh - 10vh); /* 减去顶部高度 */
    display: flex;
  }
  
  .el-container {
    width: 100%;
    height: 100%;
  }
  
  .el-aside {
    background-color: #304156;
    color: #bfcbd9;
    height: 100%;
  }
  
  .el-menu {
    border-right: none;
    height: 100%;
  }
  
  .el-main {
    padding: 20px;
    overflow-y: auto;
  }
  </style>