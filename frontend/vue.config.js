// vue.config.js

const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin

module.exports = {
  publicPath: '/static/dist',
  // options
  outputDir: '../undyingkingdoms/static/dist',

  // assetsDir: '../../static/dist',

  pages: {
    economy: {
      entry: 'src/economy/main.js',
      template: 'public/index.html',
      filename: 'economy.html'
    },
    insfrastructure: {
      entry: 'src/insfrastructure/main.js',
      template: 'public/index.html',
      filename: 'insfrastructure.html'
    }
  },
  configureWebpack: {
    plugins: [
      // new BundleAnalyzerPlugin()
    ]
  }
}
