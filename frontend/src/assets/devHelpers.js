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

  axios.get(loginUrl, {withCredentials: true})
  .then( (response, status) => {
    console.log('GET login successful');
    // console.log(response);
    csrfToken = $('#csrf_token', response.data);
    if (status === 200 && csrfToken.val() !== undefined) {
      console.log(csrfToken.val());
      axios.post(loginUrl, 
        $.param({
          email: "haldon@gmail.com",
          password: "brunner"
        }), {
        headers: {"X-CSRF-TOKEN": csrfToken.val()},
        withCredentials: true
      })
      .always(function (response, status) {
        if (status === "success") {
          console.log("POST login successful")
          callback(response);
        } else {
          console.log(response);
          console.log(response.responseText);
        }
      });
    } else {
      console.log("You are already logged in!")
    }
  }).catch( (error) => {
    console.log("login get request failed")
    console.log(error);
  });
}

login();

export const HTTP = axios.create({
  baseURL: baseURL(),
  withCredentials: true
});
