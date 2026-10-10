import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Em desenvolvimento, /api vai para o Flask. Assim front e back ficam no
    // mesmo endereço e o cookie de sessão funciona sem CORS.
    proxy: {
      '/api': 'http://127.0.0.1:5000',
    },
  },
})
