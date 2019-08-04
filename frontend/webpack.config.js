const webpack = require('webpack')
// const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')

module.exports = {
  module: {
    rules: [
      { test: /\.js$/, exclude: /node_modules/, loader: "babel-loader" },
      { test: /\.pug$/, loader: 'pug-plain-loader' },
    ],
  },
  plugins: [
    // new analyzer.BundleAnalyzerPlugin()
  ],
}
