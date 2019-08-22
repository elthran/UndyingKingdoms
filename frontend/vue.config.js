// vue.config.js

// const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')

module.exports = {
  // using dev public path of "/" fixes async components.
  publicPath: '/static/dist',
  // process.env.NODE_ENV === 'production'
  //   ? '/static/dist'
  //   : '/',
  // options
  outputDir: '../app/static/dist',
  indexPath: '../../templates/dist/index.html',

//  pages: {
//    economy: {
//      entry: 'src/economy/main.js',
//      template: 'public/index.html',
//      filename: 'economy.html'
//    },
//    infrastructure: {
//      entry: 'src/infrastructure/main.js',
//      template: 'public/index.html',
//      filename: 'infrastructure.html'
//    },
//    overview: {
//      entry: 'scr/overview/main.js',
//      template: 'public/index.html',
//      filename: 'overview.html'
//    }
//  },
  configureWebpack: {
    module: {
      rules: [
        { test: /\.js$/, exclude: /node_modules/, loader: "babel-loader" },
        { test: /\.pug$/, loader: 'pug-plain-loader' },
      ],
    },
    plugins: [
      // new analyzer.BundleAnalyzerPlugin()
    ],
  },
}
