var APIInterface = {}

APIInterface.install = function (Vue, options) {
  Vue.prototype.$getData = function (url) {
    return this.axios.get(url)
    .then((response) => {
      return response.data
    })
    .catch((error) => {
      // console.log("$getData errors are:", error, error.response)
      return Promise.reject(error)
    })
  }

  Vue.prototype.$hydrate = function (url) {
    // console.log('hydrating')
    return this.axios.get(url)
    .then((response) => {
      // if (!(response.data.hasOwnProperty('debugMessage'))) {
      //   console.log('You need to add as "debugMessage" attribute to the api "' + url + '" return jsonify.')
      // }
      // delete response.data.debugMessage
      return this.$deployData(response.data)
    })
    .catch((error) => {
      console.log("$hydrate errors are:", error, error.response)
      return Promise.reject(error)
    })
  }

  Vue.prototype.$deployData = function (data) {
    // console.log("Deploying data")
    // console.log(data)
    for ( var prop in data ) {
      // console.log(prop, data[prop])
      if (data.hasOwnProperty(prop)) {
        this.$data[prop] = data[prop]
      }
      if (!(this.$data.hasOwnProperty(prop))) {
        console.log('You need to add "' + prop + '" to this vue component.')
        console.log('Its value is: ', data[prop])
      }
    }
    return data
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
      return response.data
    })
    .catch((error) => {
      return Promise.reject(error)
    })
  }

  Vue.prototype.$sendData = async function (data) {
    // console.log("running $sendData")
    var formData = new FormData();
    for ( var prop in data ) {
      if (data.hasOwnProperty(prop)) {
        formData.append(prop, data[prop]);
      }
    }
    if (!formData.has('csrf_token')) {
      formData.set('csrf_token', formData.get('CSRFToken') || formData.get('csrfToken'))
    }
    return this.axios({
      url: formData.get('action'),
      method: 'POST',
      headers: {'X-CSRF-TOKEN': formData.get('csrf_token')},
      data: formData,
      dataType: 'json'  // type of datareturned, not type sent
    })
    .then((response) => {
      return response.data
    })
    .catch((error) => {
      // console.log("$sendData errors are:", error, error.response)
      return Promise.reject(error)
    })
  }
}

export const APIInterfacePlugin = APIInterface;
