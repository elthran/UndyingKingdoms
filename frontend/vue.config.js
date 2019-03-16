// vue.config.js

const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin

module.exports = {
  publicPath: '/static/dist',
  // options
  outputDir: '../undyingkingdoms/static/dist',

  // assetsDir: '../../static/dist',

  pages: {
//    economy: {
//      entry: 'src/economy/main.js',
//      template: 'public/index.html',
//      filename: 'economy.html'
//    },
    infrastructure: {
      entry: 'src/infrastructure/main.js',
      template: 'public/index.html',
      filename: 'infrastructure.html'
    }
  },
  configureWebpack: {
    plugins: [
      // new BundleAnalyzerPlugin()
    ]
  }
}
