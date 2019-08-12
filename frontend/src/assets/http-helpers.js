/* eslint-disable */
import axios from 'axios'


function baseURL () {
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost:5000'
  } else {
    return ''
  }
}

const defaultConfig = {
  baseURL: baseURL(),
  withCredentials: true,
  xsrfCookieName: 'CSRF-Token',
  xsrfHeaderName: 'X-CSRF-Token',
}

const http = axios.create(defaultConfig)

// csrf header should be auto injected so I don't need a
// request interceptor function for that.
http.interceptors.request.use(function (config) {
    // Do something before request is sent
    return config;
  }, function (error) {
    // Do something with request error
    return Promise.reject(error);
  });


function handleUnauthorized (status) {
  if (status === 401) {
    // redirect to login
    return http.get('/api/routing/login')
    .then((response) => {
      // allow redirection back to this url
      window.location.href = `${response.data.URL}?q=${window.location.href}`
      return null
    })
  }
  return Promise.reject(null)
}


// Add a response interceptor
http.interceptors.response.use(function (response) {
  const headers = response.headers

  let csrfToken = ''
  if (headers['x-csrf-token']) { // token name gets lower-cased by axios
    csrfToken = headers['x-csrf-token'] || 'you should have sent a csrf token'
  } else if (headers["content-type"] == 'document') {
    const data = response.data
    const csrfElement = data.getElementById('csrf_token')
    csrfToken = csrfElement.value || "document doesn't contains a csrf token"
  }

  if (csrfToken != '') {
    document.cookie = `CSRF-Token=${csrfToken}`
  }
  return response
}, function (error) {
  // console.log('intercepting response error', error)
  // This should be chainable?
  // Each handleFoo should return a resolve or reject.
  // resolve is succesfull and would return that instead?
  // reject would be handled by next handleFoo?
  // eg, reject means handle method did nothing.
  const response = handleUnauthorized(error.response.status)
  // console.log('response handler produced:', response)
  return response
    .then((response) => {
      return Promise.resolve(response)
    })
    .catch(() => {
      return Promise.reject(error)
    })
})

export default http
