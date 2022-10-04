

const MainModule = (() => {
  let result = {};

  function upload() {
    xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
      if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
        const data = JSON.parse(xmlHttp.responseText).data;
        const image = JSON.parse(xmlHttp.responseText).img;
  
        result = {}
        processData(data);
    
        document.getElementById(
          "result-image"
        ).src = `data:image/png;base64, ${image}`;
  
        setTimeout(() => {
          document.querySelector("#result-image").scrollIntoView({
            behaviour: "smooth",
            block: "start",
            inline: "nearest"
          });        
        }, 500);
    
        console.log(data);
      }    
    }
  
    let url = "http://localhost:8000/upload";
    xmlHttp.open("POST", url);
  
    let csrfToken = "{{ csrf_token }}";
    xmlHttp.setRequestHeader("X-CSRFToken", csrfToken);
  
    const fileJson = document.getElementById("fileJson").files[0];
    const fileInvoice = document.getElementById("fileInvoice").files[0];
    const fileTemplate = document.getElementById("fileTemplate").files[0];
  
    if (typeof fileInvoice == "undefined") {
      alert("No invoice to be uploaded!");
      return;    
    }
  
    document.getElementById("result-image").hidden = false;
  
    // console.log(fileInvoice);
    // console.log(fileTemplate);
  
    const formData = new FormData();
    formData.append("fileInvoice", fileInvoice);
    formData.append("fileTemplate", fileTemplate);
  
    if (typeof fileJson != "undefined") {
      formData.append("fileJson", fileJson);
    }
  
    formData.append("saveLocations", document.getElementById("saveLocationsSwitch").checked);
    xmlHttp.send(formData);
  
  }
  
  function processData(data) {
    for (const [key, obj] of Object.entries(data)) {
      result[key] = data[key][0];
    }
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
  
    const file = document.getElementById("fileInvoice").value;
    let extension;
  
    if (file.includes(".png")) {
      extension = ".png";
    } else if (file.includes(".jpg")) {
      extension = ".jpg";
    } else {
      alert("Only .png and .jpg extensions are supported!");
      return;
    }
  
    const fileName = file.split(/\\+/).pop().split(extension)[0] + ".json";
    download(JSON.stringify(result), fileName, "text/plain");
  }
  
  function init() {
    const fileJson = document.getElementById("fileJson");
    
    fileJson.addEventListener("change", event => {
      const json = document.getElementById("fileJson").files[0];
      const checkbox = document.getElementById("saveLocationsSwitch");
  
      if (typeof json != "undefined") {
        checkbox.disabled = false;
      } else {
        checkbox.disabled = true;
        checkbox.checked = false;
      }
  
      return true;
    });  
  
    const collapsible = document.getElementsByClassName("collapsible");
  
    Array.from(collapsible).forEach(element => {
      element.addEventListener("click", function() {
        this.classList.toggle("active");
        const content = this.nextElementSibling;
  
        if (content.style.maxHeight) {
          content.style.maxHeight = null;
        } else {
          content.style.maxHeight = content.scrollHeight + "px";
        }
      })
  
      return true;
    });
  }

  return {
    init,
    upload,
    onDownload
  }
})();

MainModule.init();

