import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  base: '/static/kindlewick/',
  plugins: [react()],
  build: {
    outDir: path.resolve(__dirname, '../../static/kindlewick'),
    emptyOutDir: false,
    rollupOptions: {
      output: {
        entryFileNames: 'app.js',
        assetFileNames: (assetInfo) => {
          // place CSS and other assets under assets/
          return assetInfo.name && assetInfo.name.endsWith('.css')
            ? 'assets/style.css'
            : 'assets/[name][extname]'
        },
      },
    },
  },
})
