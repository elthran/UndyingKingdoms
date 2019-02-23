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
    }
  },
  configureWebpack: {
    plugins: [
      new BundleAnalyzerPlugin(
        // { analyzerMode: 'disable' }
      )
    ]
  }
}
