function upload() {
  xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = showResult;

  let url = "http://localhost:8000/upload";
  xmlHttp.open("POST", url);

  let csrfToken = "{{ csrf_token }}";
  xmlHttp.setRequestHeader("X-CSRFToken", csrfToken);

  let fileInvoice = document.getElementById("fileInvoice").files[0];
  let fileTemplate = document.getElementById("fileTemplate").files[0];

  console.log(fileInvoice);
  console.log(fileTemplate);

  var formData = new FormData();
  formData.append("fileInvoice", fileInvoice);
  formData.append("fileTemplate", fileTemplate);

  xmlHttp.send(formData);
}

function showResult() {
  if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
    console.log("..data extracted..");
    data = JSON.parse(xmlHttp.responseText).data;
    image = JSON.parse(xmlHttp.responseText).img;
    document.getElementById(
      "result-image"
    ).src = `data:image/png;base64, ${image}`;

    console.log(data);
  }
}
