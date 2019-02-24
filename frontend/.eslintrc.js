module.exports = {
  extends: [
    // add more generic rulesets here, such as:
    // 'eslint:recommended',
    'plugin:vue/recommended'
  ],
  rules: {
    'vue/require-default-prop': 'off',
    'vue/no-v-html': 'off'
    //    'no-console': 'off'
    //    'vue/no-parsing-error': [2, {
    //        "invalid-first-character-of-tag-name": false
    //    }]
  },
  parser: "vue-eslint-parser",
  parserOptions: {
    parser: "babel-eslint",
    sourceType: "module",
    ecmaVersion: 8
  }
}
