export default {
	name: 'helpers',
	methods: {
		envDependentUrl (url) {
			if (process.env.NODE_ENV === 'development') {
				return 'http://localhost:5000' + url;
			} else {
				return url
			}
		}
	}
}

