function callReset() {
    sendRequest("/admin/reset");
}
function callRefresh() {
    sendRequest("/admin/refresh");
}

function sendRequest(url) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("response").innerHTML = xhttp.response;
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
}
