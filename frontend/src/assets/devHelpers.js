/* eslint-disable */
import $ from "jquery";
import axios from 'axios';

function baseURL () {
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost:5000';
  } else {
    return '';
  }
}

function login () {
  var loginUrl = 'http://localhost:5000/login/'
  var csrfToken;

  $.ajax({
    async: false,
    type: "GET",
    url: loginUrl,
    xhrFields: {
      withCredentials: true
    },
    success: (response, status) => {
      // console.log('GET login successful');
      // console.log(response);
      csrfToken = $('#csrf_token', response);
      // console.log(csrfToken.val());
      if (csrfToken.val() === undefined) {
        // console.log("You are already logged in!")
      } else {
        $.ajax({
          async: false,
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
          },
          error: (error) => {
            console.log('POST login failed');
            console.log(error);
          }
        });
      }
    },
    error: (error) => {
      console.log("login get request failed")
      console.log(error);
    }
  });
}

// This function auto executes.
export const devLogin = function () {
  if (process.env.NODE_ENV === 'development') {
    return login();
  } else {
    return {};
  }
}();

export const customAxios = axios.create({
  baseURL: baseURL(),
  withCredentials: true
});
