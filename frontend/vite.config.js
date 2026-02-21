import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
    base: '/static/',
    root: path.resolve(__dirname),

    build: {
        // Папка, куда Vite положит собранные файлы (на уровень выше, рядом с backend)
        outDir: path.resolve(__dirname, '../static_vite/'),
        manifest: true,
        emptyOutDir: true,
        rollupOptions: {
            input: {
                // --- VENDOR JS (Берем из вашей папки app/libs/) ---
                jquery_js: path.resolve(__dirname, 'app/libs/jquery/dist/jquery.min.js'),
                jquery_ui_js: path.resolve(__dirname, 'app/libs/jquery/dist/jquery-ui-1.10.4.custom.min.js'),
                count_to_js: path.resolve(__dirname, 'app/libs/count/jquery.countTo.js'),
                swiper_js: path.resolve(__dirname, 'app/libs/swiper/dist/js/swiper.min.js'),
                simple_lightbox_js: path.resolve(__dirname, 'app/libs/gallery/simple-lightbox.min.js'),
                scrollax_js: path.resolve(__dirname, 'app/libs/parallax/scrollax.min.js'),
                picturefill_js: path.resolve(__dirname, 'app/libs/picturefill/picturefill.min.js'),
                stickyfill_js: path.resolve(__dirname, 'app/libs/sticky-sidebar/stickyfill.min.js'),
                m_custom_scrollbar_js: path.resolve(__dirname, 'app/libs/scroll/jquery.mCustomScrollbar.js'),
                basictable_js: path.resolve(__dirname, 'app/libs/table/jquery.basictable.min.js'),
                tooltipser_js: path.resolve(__dirname, 'app/libs/tooltip/dist/js/tooltipster.bundle.min.js'),
                select2_js: path.resolve(__dirname, 'app/libs/select2/dist/js/select2.min.js'),

                // --- ВАШИ СКРИПТЫ ---
                common_js: path.resolve(__dirname, 'app/js/common.js'),
                registration_js: path.resolve(__dirname, 'app/js/registration.js'),

                // --- СТИЛИ ---
                styles: path.resolve(__dirname, 'app/sass/main.sass'),
            },
        },
    },

    server: {
        host: '0.0.0.0', // Для докера
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
