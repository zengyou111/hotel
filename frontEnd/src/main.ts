import { createApp } from 'vue'

//引入清除默认样式
// @ts-ignore
import '@/style/reset.scss'
import './index.css'

//引入 vue-router 核心插件并安装
// @ts-ignore
import router from '@/router';
//引入 element-plus 插件
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
//引入 element-plus 国际化文件
//@ts-ignore,ts 不支持 zh-cn.mjs，所以这里要忽略 ts 校验，否则会有警告线提示
//@ts-ignore
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
//引入 pinia 仓库
// @ts-ignore
import pinia from '@/store'




// @ts-ignore
import App from './App.vue';
// @ts-ignore
import Top from '../src/components/top/index.vue';
// @ts-ignore
import Bottom from '../src/components/bottom/index.vue';



const app=createApp(App)
app.use(router);




app.use(ElementPlus,{
    locale:zhCn
});


app.component('Top',Top);
app.component('Bottom',Bottom);

app.use(pinia);
app.mount('#app')
