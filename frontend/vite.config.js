import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // 只要你在 Vue 里请求以 /api 开头的地址
      // 比如 axios.get('/api/users/')
      // Vite 就会自动帮你转发到 Django 的 8000 端口
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        // 后端实际路由从 /course/... 开始，这里去掉 /api 前缀后再转发给 Django。
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
