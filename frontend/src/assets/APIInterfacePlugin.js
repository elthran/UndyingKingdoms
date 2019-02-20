var APIInterface = {};

APIInterface.install = function (Vue, options) {
  Vue.prototype.$getData = function (url, callback) {
    this.axios.get(url)
    .then((response) => {
      if (response.data.status === 'success') {
        delete response.data.status
        delete response.data.message
        callback(this, response.data)
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