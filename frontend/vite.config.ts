import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Vite config. base: './' keeps asset paths relative so the build
// also works when loaded from a file:// URL inside Electron.
export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: 'dist',
    target: 'es2020',
  },
});
