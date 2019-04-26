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
//      console.log("$hydrate response", response)
      return this.$deployData(response.data)
    })
    .catch((error) => {
//      console.log("$hydrate error", error)
      // console.log("status", error.response.status)
      if (error.response.status === 401) {
        // redirect to login
        return this.axios.get('/api/routing/login')
        .then((response) => {
          window.location.href = response.data.url
          return Promise.resolve(null)
        })
      }
      // this.$router.push('/login/')
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

  Vue.prototype.$sendForm = async function (form) {
    // FormData will only use input fields that use the name attribute.
    var formData = new FormData(form)
    if (!formData.has('csrf_token')) {
      formData.set('csrf_token', formData.get('CSRFToken') || formData.get('csrfToken'))
    }
    // console.log("form", form, form.getAttribute('action'))
    return this.axios({
      url: form.getAttribute('action'),
      method: 'POST',
      headers: { 'X-CSRF-TOKEN': formData.get('csrf_token') },
      data: formData,
      dataType: 'json' // type of data returned, not type sent.
    })
    .then((response) => {
      return response.data
    })
    .catch((error) => {
      console.log("$sendForm error:", error.response)
      return Promise.reject(error.response.data)
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
      headers: {'X-CSRF-TOKEN': formData.get('csrf_token') },
      data: formData,
      dataType: 'json'  // type of data returned, not type sent
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
