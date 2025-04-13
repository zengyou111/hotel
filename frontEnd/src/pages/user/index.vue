<template>
    <div class="user-container">
      <el-container>
        <el-header class="user-header">
          <el-menu
            :default-active="activeMenu"
            mode="horizontal"
            router
            background-color="#fff"
            text-color="#333"
            active-text-color="#409EFF"
          >
            <el-menu-item index="/user/booking">首页</el-menu-item>
            <!--<el-menu-item index="/user/hotels">酒店列表</el-menu-item>-->
            <el-menu-item index="/user/booking">我的预订</el-menu-item>
            <!--<el-menu-item index="/user/profile">个人信息</el-menu-item>-->
          </el-menu>
        </el-header>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed } from 'vue';
  import { useRoute } from 'vue-router';
  
  const route = useRoute();
  
  // 计算当前激活的菜单项
  const activeMenu = computed(() => {
    return route.path;
  });
  </script>
  
  <style scoped>
  .user-container {
    min-height: calc(100vh - 10vh); /* 减去顶部高度 */
  }
  
  .user-header {
    background-color: #fff;
    border-bottom: 1px solid #e6e6e6;
    padding: 0;
  }
  
  .el-menu.el-menu--horizontal {
    border-bottom: none;
  }
  
  .el-main {
    padding: 20px;
    background-color: #f5f7fa;
  }
  </style>