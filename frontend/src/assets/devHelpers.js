/* eslint-disable */
import axios from 'axios';

function baseURL () {
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost:5000'
  } else {
    return ''
  }
}

async function login () {
  const { default: $ } = await import(/* webpackChunkName: "jquery" */ 'jquery')
  var loginUrl = 'http://localhost:5000/login/'
  var csrfToken;

  await $.ajax({
    type: "GET",
    url: loginUrl,
    xhrFields: {
      withCredentials: true
    },
    success: async (response, status) => {
      // console.log('GET login successful');
      // console.log(response);
      csrfToken = $('#csrf_token', response);
      // console.log(csrfToken.val());
      if (csrfToken.val() === undefined) {
        // console.log("You are already logged in!")
        return "You are already logged in."
      } else {
        return await $.ajax({
          type: "POST",
          url: loginUrl,
          data: $.param({
            email: "haldon@gmail.com",
            password: "brunner"
          }),
          xhrFields: {
            withCredentials: true
          },
          headers: {"X-CSRF-TOKEN": csrfToken.val()},
          success: (response, status) => {
            // console.log("POST login successful")
            // console.log(response);
            return "POST login successful."
          },
          error: (error) => {
            console.log('POST login failed');
            console.log(error);
            return false
          }
        });
      }
    },
    error: (error) => {
      console.log("login get request failed")
      console.log(error);
      return false
    }
  });
}

// This function auto executes.
export const devLogin = function () {
  if (process.env.NODE_ENV === 'development') {
    return login()
    .then(() => {
      return true
    })
    .catch(() => {
      console.log("Login failed, try reloading the page a few times ....")
      return false
    })
  } else {
    return null
  }
}();

export const customAxios = axios.create({
  baseURL: baseURL(),
  withCredentials: true,
});
