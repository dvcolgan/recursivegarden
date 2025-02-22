import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'url'
import fs from 'fs'
import path from 'path'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// Automatically discover all widget entries
function getWidgetEntries() {
  const widgetsDir = './frontend/widgets'
  const entries: Record<string, string> = {
    styles: './frontend/styles.css',
  }

  // Read all widget directories
  fs.readdirSync(widgetsDir, { withFileTypes: true })
    .filter((dirent) => dirent.isDirectory())
    .forEach((dirent) => {
      const widgetName = dirent.name
      const mainPath = path.join(widgetsDir, widgetName, 'main.ts')

      // Only add entry if main.ts exists
      if (fs.existsSync(mainPath)) {
        entries[widgetName] = mainPath
      }
    })

  return entries
}

// https://vite.dev/config/
export default defineConfig({
  root: '.',
  base: '/static/',
  build: {
    manifest: 'manifest.json',
    outDir: './backend/static',
    emptyOutDir: true,
    rollupOptions: {
      input: getWidgetEntries(),
    },
  },
  plugins: [
    vue({
      include: [/\.vue$/],
    }),
    tailwindcss(),
  ],
  server: {
    cors: true,
    allowedHosts: [
      '.optimism.buri-frog.ts.net',
      '.optimism',
      '.entropy.buri-frog.ts.net',
      '.entropy',
    ],
    port: 3333,
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./frontend', import.meta.url)),
    },
    extensions: ['.html', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue', '.md'],
  },
})
