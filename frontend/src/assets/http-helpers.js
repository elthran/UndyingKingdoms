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
  xsrfCookieName: 'CSRFToken',
  xsrfHeaderName: 'X-CSRFToken',
}

const http = axios.create(defaultConfig)
document.cookie = `CSRFToken=`

// Add a response interceptor
http.interceptors.response.use(function (response) {
  // if (response type is document) {
  if (true) {
    const data = response.data
    const csrfElement = data.getElementById('csrf_token')
    const csrfToken = csrfElement.value
  } else {
    const headers = response.headers
    const csrfToken = headers['X-CSRFToken']
  }
  document.cookie = `CSRFToken=${csrfToken}`
  return response
}, function (error) {
  // Do something with response error
  return Promise.reject(error)
})

export default axios
