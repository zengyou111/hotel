// @ts-ignore
import { createRouter, createWebHistory } from "vue-router";
import useUserStore from "@/store/modules/user";

//createRouter 方法，用于创建路由器实例，可以管理多个路由
export default createRouter({
    //路由的模式设置
    history: createWebHistory(),
    //管理路由
    routes: [
        {
            path:'/login',
            component:()=>import('@/pages/login/index.vue'),
            meta:{requireTopAndFooter:false}
        },
        {
            path:'/',
            redirect: '/login',
            meta:{requireTopAndFooter:false}
        },
        // 管理员路由
        {
            path:'/admin',
            component:()=>import('@/pages/admin/index.vue'),
            meta:{requireTopAndFooter:true, requireAdmin:true},
            redirect: '/admin/dashboard',
            children: [
                {
                    path:'dashboard',
                    component:()=>import('@/pages/admin/dashboard/index.vue'),
                    meta:{title:'管理员首页', requireTopAndFooter:true, requireAdmin:true}
                },
                {
                    path:'member',
                    component:()=>import('@/pages/admin/member/index.vue'),
                    meta:{title:'会员管理', requireTopAndFooter:true, requireAdmin:true}
                },
                {
                    path:'branch',
                    component:()=>import('@/pages/admin/branch/index.vue'),
                    meta:{title:'分店管理', requireTopAndFooter:true, requireAdmin:true}
                },
                {
                    path:'room',
                    component:()=>import('@/pages/admin/room/index.vue'),
                    meta:{title:'客房管理', requireTopAndFooter:true, requireAdmin:true}
                },
                {
                    path:'booking',
                    component:()=>import('@/pages/admin/booking/index.vue'),
                    meta:{title:'预订管理', requireTopAndFooter:true, requireAdmin:true}
                },
                {
                    path:'statistics',
                    component:()=>import('@/pages/admin/statistics/index.vue'),
                    meta:{title:'数据统计', requireTopAndFooter:true, requireAdmin:true}
                }
            ]
        },
        // 普通用户路由
        {
            path:'/user',
            component:()=>import('@/pages/user/booking/index.vue'),
            meta:{requireTopAndFooter:true},
            redirect: '/user/home',
            children: [
                {
                    path:'home',
                    component:()=>import('@/pages/user/home/index.vue'),
                    meta:{title:'用户首页', requireTopAndFooter:true}
                },
                {
                    path:'profile',
                    component:()=>import('@/pages/user/profile/index.vue'),
                    meta:{title:'个人信息', requireTopAndFooter:true}
                },
                {
                    path:'booking',
                    component:()=>import('@/pages/user/booking/index.vue'),
                    meta:{title:'我的预订', requireTopAndFooter:true}
                },
                {
                    path:'hotels',
                    component:()=>import('@/pages/user/hotels/index.vue'),
                    meta:{title:'酒店列表', requireTopAndFooter:true}
                }
            ]
        },
        // 404页面
        {
            path: '/:pathMatch(.*)*',
            component: () => import('@/pages/404/index.vue'),
            meta: { requireTopAndFooter: false }
        }
    ],
    //滚动行为：控制滚动条的位置
    //切换路由时，页面跳转到最上方
    scrollBehavior() {
        return {
            left: 0,
            top: 0
        }
    }
});