// vue.config.js

module.exports = {
		publicPath: '',
    // options
    outputDir: '../undyingkingdoms/templates/dist',

    assetsDir: '../../static/dist',

    pages: {
				economy: {
						entry: 'src/economy/main.js',
						template: 'public/index.html',
			      filename: 'economy.html'
				}
		},
    runtimeCompiler: undefined,
    productionSourceMap: undefined,
    parallel: undefined,
    css: undefined
}
