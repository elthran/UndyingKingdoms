/* eslint-disable */
import axios from 'axios';


function baseURL () {
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost:5000'
  } else {
    return ''
  }
}

const customAxios = axios.create({
  baseURL: baseURL(),
  withCredentials: true,
})

function login () {
  // const { default: $ } = await import(/* webpackChunkName: "jquery" */ 'jquery')
  const loginUrl = '/login/'

  const csrfToken = customAxios.get(loginUrl, {
      responseType: 'document'
    })
    .then((response) => {
      const data = response.data
      const csrfElement = data.getElementById('csrf_token')
      return csrfElement.value
    })
    .catch((error) => {
      console.log('axios get login error:', error)
      return null
    })

    const data = {
      email: "haldon@gmail.com",
      password: "brunner",
      csrf_token: csrfToken,
    }
    const formData = new FormData()
    for ( const prop in data ) {
      if (data.hasOwnProperty(prop)) {
        formData.append(prop, data[prop])
      }
    }
    return customAxios({
        url: loginUrl,
        method: 'POST',
        headers: {'X-CSRF-TOKEN': csrfToken },
        data: formData,
      })
      .then((response) => {
        console.log('login should have worked', response)
        return true
      })
      .catch((error) => {
        console.log('axios post to login error:', error);
        return false
      })


  // await $.ajax({
  //   type: "GET",
  //   url: loginUrl,
  //   xhrFields: {
  //     withCredentials: true
  //   },
  //   success: async (response, status) => {
  //     // console.log('GET login successful');
  //     // console.log(response);
  //     csrfToken = $('#csrf_token', response);
  //     // console.log(csrfToken.val());
  //     if (csrfToken.val() === undefined) {
  //       // console.log("You are already logged in!")
  //       return "You are already logged in."
  //     } else {
  //       return await $.ajax({
  //         type: "POST",
  //         url: loginUrl,
  //         data: $.param({
  //           email: "haldon@gmail.com",
  //           password: "brunner"
  //         }),
  //         xhrFields: {
  //           withCredentials: true
  //         },
  //         headers: {"X-CSRF-TOKEN": csrfToken.val()},
  //         success: (response, status) => {
  //           // console.log("POST login successful")
  //           // console.log(response);
  //           return "POST login successful."
  //         },
  //         error: (error) => {
  //           console.log('POST login failed');
  //           console.log(error);
  //           return Promise.resolve(false)
  //         }
  //       }).catch((error) => {
  //         console.log('devHelpers error', error)
  //       })
  //     }
  //   },
  //   error: (error) => {
  //     console.log("login get request failed")
  //     console.log(error);
  //     return false
  //   }
  // });
}

// This function auto executes.
export const devLogin = function () {
  if (process.env.NODE_ENV === 'development') {
    return login()
  } else {
    return null
  }
}()

export { customAxios }
