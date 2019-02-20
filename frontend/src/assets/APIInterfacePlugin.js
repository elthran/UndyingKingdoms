var APIInterface = {};

APIInterface.install = function (Vue, options) {
  Vue.prototype.$getData = function (url, callback) {
    this.axios.get(url)
    .then((response) => {
      if (response.data.status === 'success') {
        delete response.data.status
        delete response.data.message
        callback(this, response.data)
      } else if (!(response.data.hasOwnProperty('status'))) {
        console.log('You need to add as "success" attribute to the api return jsonify.')
        console.log('You should probably add a "message" attribute as well for debugging purposes.')
      } else {
        this.errors = response
      }
    })
    .catch((error) => {
      this.errors = error.response
    })
  }
  
  Vue.prototype.$deployData = function (self, articles) {
    _.forEach(articles, function (article, key) {
      if (self.hasOwnProperty(key)) {
        self[key] = article
      } else {
        console.log('You need to add "' + key + '" to this vue component.')
        console.log('Its value is: ', article)
      }
    })
  }
}

export const APIInterfacePlugin = APIInterface;