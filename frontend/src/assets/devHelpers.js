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
    // console.log(csrfToken.val());
    if (csrfToken.val() === undefined) {
      console.log("You are already logged in!")
    } else {
      console.log("Should get here")
      axios.post(loginUrl, 
        $.param({
          email: "haldon@gmail.com",
          password: "brunner"
        }), {
        headers: {"X-CSRF-TOKEN": csrfToken.val()},
        withCredentials: true
      })
      .then(function (response, status) {
        console.log("POST login successful")
        console.log(response);
      }).catch( (error) => {
        console.log('POST login failed');
        console.log(error);
      });
    }
  }).catch( (error) => {
    console.log("login get request failed")
    console.log(error);
  });
}

login();

export const devAxios = axios.create({
  baseURL: baseURL(),
  withCredentials: true
});
