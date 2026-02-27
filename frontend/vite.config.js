import { defineConfig } from 'vite';
import path from 'path';
import fs from 'fs';

function getFilesFromDir(dir, fileList = []) {
    if (!fs.existsSync(dir)) return fileList;
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const absolutePath = path.join(dir, file);
        if (fs.statSync(absolutePath).isDirectory()) {
            getFilesFromDir(absolutePath, fileList);
        } else {
            fileList.push(absolutePath);
        }
    }
    return fileList;
}


const imgDir = path.resolve(__dirname, 'app/img');
const imageFiles = getFilesFromDir(imgDir);

const imageInputs = {};
imageFiles.forEach((file) => {
    const relativePath = path.relative(__dirname, file).replace(/\\/g, '/');
    imageInputs[relativePath] = file;
});

export default defineConfig({
    base: '/static/',
    root: path.resolve(__dirname),

    build: {
        outDir: path.resolve(__dirname, '../static_vite/'),
        manifest: 'manifest.json',
        emptyOutDir: true,
        rollupOptions: {
            input: {
                'app/js/common.js': path.resolve(__dirname, 'app/js/common.js'),
                'app/js/registration.js': path.resolve(__dirname, 'app/js/registration.js'),
                'app/sass/main.sass': path.resolve(__dirname, 'app/sass/main.sass'),
                ...imageInputs
            },
        },
    },

    server: {
        host: '0.0.0.0',
        port: 5173,
        origin: 'http://localhost:5173',
        watch: {
            usePolling: true,
        }
    },

    css: {
        preprocessorOptions: {
            sass: { silenceDeprecations: ['import', 'global-builtin', 'color-functions', 'slash-div'] },
            scss: { silenceDeprecations: ['import', 'global-builtin', 'color-functions', 'slash-div'] }
        }
    }
});
