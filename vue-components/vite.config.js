import vue from "@vitejs/plugin-vue";

export default {
  plugins: [vue()],
  base: "./",
  build: {
    emptyOutDir: true,
    lib: {
      entry: "./src/main.js",
      name: "trame_gwc",
      formats: ["umd"],
      fileName: "trame_gwc",
    },
    minify: false,
    sourceMap: true,
    rollupOptions: {
      external: ["vue"],
      output: {
        globals: {
          vue: "Vue",
        },
      },
    },
    outDir: "../src/trame_gwc/module/serve",
    assetsDir: ".",
  },
};