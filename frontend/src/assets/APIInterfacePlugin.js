var APIInterface = {}

APIInterface.install = function (Vue, options) {
  Vue.prototype.$getData = function (url, callback) {
    this.axios.get(url)
    .then((response) => {
      if (response.data.status === 'success') {
        delete response.data.status
        delete response.data.message
        callback(this, response.data)
      } else if (!(response.data.hasOwnProperty('status'))) {
        console.log('You need to add as "status" attribute to the api "' + url + '" return jsonify.')
        console.log('You should probably add a "message" attribute as well for debugging purposes.')
      } else {
        this.errors = response
      }
    })
    .catch((error) => {
      this.errors = error.response
    })
  }

  Vue.prototype.$deployData = async function (self, articles) {
    const { default: _ } = await import(/* webpackChunkName: "lodash" */ 'lodash')
    _.forEach(articles, function (article, key) {
      if (self.hasOwnProperty(key)) {
        self[key] = article
      } else {
        console.log('You need to add "' + key + '" to this vue component.')
        console.log('Its value is: ', article)
      }
    })
  }

  Vue.prototype.$sendForm = async function (form, callback) {
    const { default: $ } = await import(/* webpackChunkName: "jquery" */ 'jquery')
    if (!(form instanceof $)) {
      form = $(form)
    }
    this.axios({
      url: form.attr("action"),
      method: 'POST',
      // need to verify csrf id, I might be wrong.
      headers: { 'X-CSRF-TOKEN': $('#csrf_token').val() },
      data: form.serialize(),
      dataType: 'json' // type of data returned, not type sent.
    })
    .then((response) => {
      if (response.data.status === 'success') {
        delete response.data.status
        delete response.data.message
        callback(this, response.data)
      } else if (!(response.data.hasOwnProperty('status'))) {
        console.log('You need to add as "success" attribute to the api "' + url + '" return jsonify.')
        console.log('You should probably add a "message" attribute as well for debugging purposes.')
      } else {
        console.log(response)
      }
    })
    .catch((error) => {
      console.log(error.response)
    })
  }

  Vue.prototype.$sendData = function (data, callback) {
    var formData = new FormData();
    for ( var prop in data ) {
      if (data.hasOwnProperty(prop)) {
        formData.append(prop, data[prop]);
      }
    }
    var CSRFToken = formData.get('csrf_token') || formData.get('CSRFToken') || formData.get('csrfToken')
    this.axios({
      url: formData.get('_action'),
      method: 'POST',
      headers: {'X-CSRF-TOKEN': CSRFToken},
      data: formData,
      dataType: 'json'  // type of datareturned, not type sent
    })
    .then((response) => {
      if (response.data.status === 'success') {
        delete response.data.status
        delete response.data.message
        callback(this, response.data)
      } else if (!(response.data.hasOwnProperty('status'))) {
        console.log('You need to add as "success" attribute to the api "' + url + '" return jsonify.')
        console.log('You should probably add a "message" attribute as well for debugging purposes.')
      } else {
        console.log(response)
      }
    })
    .catch((error) => {
      console.log(error.response)
    })
  }
}

export const APIInterfacePlugin = APIInterface;
