let result = {};

function upload() {
  xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = showResult;

  let url = "http://localhost:8000/upload";
  xmlHttp.open("POST", url);

  let csrfToken = "{{ csrf_token }}";
  xmlHttp.setRequestHeader("X-CSRFToken", csrfToken);

  const fileJson = document.getElementById("fileJson").files[0];
  const fileInvoice = document.getElementById("fileInvoice").files[0];
  const fileTemplate = document.getElementById("fileTemplate").files[0];

  // const align = document.getElementById("alignCheckbox").checked;

  // console.log(`align: ${align}`);

  console.log(fileInvoice);
  console.log(fileTemplate);

  var formData = new FormData();
  formData.append("fileInvoice", fileInvoice);
  formData.append("fileTemplate", fileTemplate);

  if (typeof fileJson != 'undefined') {
    formData.append("fileJson", fileJson);
  }

  xmlHttp.send(formData);
}

function showResult() {
  if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
    console.log("..data extracted..");
    result = {}

    const data = JSON.parse(xmlHttp.responseText).data;
    const image = JSON.parse(xmlHttp.responseText).img;

    result = processData(data, result);

    document.getElementById(
      "result-image"
    ).src = `data:image/png;base64, ${image}`;

    console.log(data);
  }
}

function processData(data, result) {
  for (const [key, obj] of Object.entries(data)) {
    result[key] = data[key][0];
  }

  return result;
}

function download(content, fileName, contentType) {
  const a = document.createElement("a");
  const file = new Blob([content], { type: contentType });
  a.href = URL.createObjectURL(file);
  a.download = fileName;
  a.click();
}
 
function onDownload(){
  if (Object.keys(result).length == 0) {
    alert("No data to be saved!");
    return;
  }
  download(JSON.stringify(result), "invoice.json", "text/plain");
}
