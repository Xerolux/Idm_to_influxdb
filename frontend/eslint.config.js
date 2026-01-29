// Xerolux 2026
import eslintPluginVue from 'eslint-plugin-vue'
import vueParser from 'vue-eslint-parser'

export default [
  {
    name: 'app/files-to-lint',
    files: ['**/*.{js,mjs,jsx,vue}'],
  },

  {
    name: 'app/vue-files',
    files: ['**/*.vue'],
    languageOptions: {
      parser: vueParser,
      ecmaVersion: 'latest',
      sourceType: 'module',
    },
    plugins: {
      vue: eslintPluginVue,
    },
    processor: eslintPluginVue.processors['.vue'],
    rules: {
      ...eslintPluginVue.configs['flat/essential'].rules,
      'vue/multi-word-component-names': 'off',
    },
  },

  {
    name: 'app/javascript-files',
    files: ['**/*.{js,mjs}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        window: 'readonly',
        document: 'readonly',
        console: 'readonly',
        setTimeout: 'readonly',
        clearTimeout: 'readonly',
        URL: 'readonly',
      },
    },
  },

  {
    name: 'app/all-files',
    files: ['**/*.{js,mjs,jsx,vue}'],
    rules: {
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      'no-undef': 'off', // Disabled since we use browser globals
    },
  },
]
