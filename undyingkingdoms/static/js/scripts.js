// Function to communicate with Python via asynchronous POST request.
// if you don't want to pass a parameter pass null instead
// e.g. getJSONFromPython("/handle_ajax_request", "{{ csrf_token() }}", localCallback, null, event);
// url -> an app.route to interact with
// CSRFToken -> a CSRF token that you need because you are using that ...
// callback -> a function that will be executed after Python returns a response
// dataToSend -> a JSON object that you are sending to Python
// event -> an event that you can suppress ... or probably ignore;
//
// Minimal usage looks like:
//     getJSONFromPython("/handle_ajax_request", "{{ csrf_token() }}");

// url is the app route that python runs
// CSRFToken is always the same. Just passes in the token.
// Callback is the JS function which handles the returned Python data (which is a JSON object, similar to a dictionary
// DataToSend is the data being sent to Python as a dictionary
// event is only needed if you want to pass a form in and suppress event bubbling
function getJSONViaPOST (url, CSRFToken, callback, dataToSend, event) {
    "use strict";

    if (url === undefined || CSRFToken === undefined) {
        throw "You must always pass in a url and a CSRFToken!";
    }

    var JSONdata;
    var xhttp;

    if (dataToSend) {
        JSONdata = JSON.stringify(dataToSend);
    }

    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        // console.log(xhttp);
        if (xhttp.readyState === 4 && xhttp.status === 200 && callback) {
            if (xhttp.getResponseHeader("Content-Type") === "application/json") {
                var response = JSON.parse(xhttp.responseText);
                callback(response);
            } else {
                throw "Did not return valid JSON data from python";
            }
        }
    };

    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("X-CSRFToken", CSRFToken);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSONdata);

    if (event) {
        // For normal event suppression.
        event.preventDefault();
        // Extra event suppression
        event.stopPropagation();
        // For form submit suppression
        return false;
    }
}
