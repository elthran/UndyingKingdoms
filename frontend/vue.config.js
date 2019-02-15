// vue.config.js

module.exports = {
		// options
	outputDir: "../undyingkingdoms/templates/dist",
	assetsDir: "../../static/dist",
	pages: {
		economy: {
			entry: 'src/economy/main.js',
			template: 'public/index.html',
      filename: 'economy.html'
		}
	}
}
