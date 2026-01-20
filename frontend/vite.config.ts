import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // Local dev convenience: Vue devserver -> ASP.NET API
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      // Result images served by the API (wwwroot/results/*)
      '/results': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      // Optional static assets served by the API (wwwroot/assets/*)
      '/assets': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
})
