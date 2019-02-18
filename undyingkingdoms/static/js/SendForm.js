function sendForm (form, callback, args) {
  var url;
  if (args === undefined) {
    url = form.attr("action")
  } else {
    url = form.attr("action") + "?" + args
  }
  $.ajax({
    url: url,
    method: "POST",
    // need to verify csrf id, I might be wrong.
    headers: {"X-CSRF-TOKEN": $("#csrf_token").val()},
    data: form.serialize(),
    dataType: "json",  // type of data returned, not type sent.
  })
  .always(function (data, status) {
    if (status === 'success') {
      console.log('the request succeeded');
      callback(data);
    } else {
      console.log('The request was not sucessful.')
      console.log(data);
    }
  });
}
