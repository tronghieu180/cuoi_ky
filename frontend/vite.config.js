import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  server: {
    proxy: {
      '/db/search': 'http://localhost:8080',
    },
    watch: {
      usePolling: true
    }
  },
  plugins: [react()]
})
