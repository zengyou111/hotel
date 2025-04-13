// @ts-ignore
import { defineConfig } from 'vite'
// @ts-ignore
import vue from '@vitejs/plugin-vue'
//引入 node 提供内置模块 path,可以获取绝对路径
import path from 'path';
// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  //src文件夹配置别名
  resolve: {
    alias: {
      "@": path.resolve(__dirname, 'src')
    }
  },
  //配置代理跨域
  server:{
    proxy:{
      '/api':{
        target:'http://localhost:8000',//本地ip
        changeOrigin:true,
      }
    }
  }
})