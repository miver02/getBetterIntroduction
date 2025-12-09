import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()], // 自动导入 Element Plus 相关函数
    }),
    Components({
      resolvers: [ElementPlusResolver()], // 自动导入 Element Plus 组件
    }),
  ],
  server: {
    proxy: {
      '/api': {
        target: 'http://0.0.0.0:6666',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
