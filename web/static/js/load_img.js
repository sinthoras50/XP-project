


const CanvasModule = (() => {
  // const scalingFactor = 0.6;
  const desiredWidth = 580;
  const rectLineColor1 = "red";
  const rectLineColor2 = "blue";
  const rectLineWidth = 2;
  const boundingBoxes = {};
  const bbNames = [];

  let scalingFactor = 1;
  let canvasOffsetX = 0;
  let canvasOffsetY = 0;
  let dragging = false;
  let imgWidthNew = 0;
  let imgHeightNew = 0;

  let img = null;
  let ctx = null;
  let canvas = null;
  
  let rectangles = [];
  let rectanglesOutput = [];
  let rectX = 0;
  let rectY = 0;

  let cursorX = 0;
  let cursorY = 0;

  function displayButtons() {
		document.getElementById("upload-wrap").hidden = true;
		
		const ids = ["undo", "add", "keyName", "download", "keyNameLabel", "filteredWords", "filteredWordsLabel", "about"];
		ids.forEach(id => document.getElementById(id).hidden = false); 
    
    const elements = Array.from(document.getElementsByClassName("input-container"));
    elements.forEach(el => {
      el.style.padding = "0px 30px 0px 30px";
    });

    document.getElementById("keyName").addEventListener("keydown", e => {
      if (e.key == 'Enter') {
        add();
      }
    });

  }

  function init() {
    document.querySelector("#image_input").addEventListener("change", function () {
      const reader = new FileReader();
    
      reader.addEventListener("load", () => {
        console.log(reader.result);
        displayButtons();
    
        canvas = document.getElementById("canvas");
        img = new Image();

        if (isPdf) {

        } else {
          img.src = reader.result;  
        }
    
        img.onload = () => {
          scalingFactor = desiredWidth / img.width;

          imgWidthNew = img.width * scalingFactor;
          imgHeightNew = img.height * scalingFactor;
    
          canvas.width = imgWidthNew;
          canvas.height = imgHeightNew;
          canvas.hidden = false;
    
          ctx = canvas.getContext("2d");
    
          ctx.drawImage(img, 0, 0, imgWidthNew, imgHeightNew);
    
          ctx.strokeStyle = rectLineColor1;
          ctx.lineWidth = rectLineWidth;
    
          ctx.textAlign = "center";
          ctx.fillStyle = "#2f990f";
          ctx.font = "20px sans-serif";
    
          const canvasOffset = canvas.getBoundingClientRect();
          canvasOffsetX = canvasOffset.left;
          canvasOffsetY = canvasOffset.top;
    
          canvas.addEventListener("mousedown", e => mouseDown(e) );
          canvas.addEventListener("mousemove", e => mouseMove(e) );
          canvas.addEventListener("mouseup", e => mouseUp(e) );
          canvas.addEventListener("mouseout", e => mouseOut(e) );
          canvas.addEventListener("keydown", e => handleKeypress(e));
        };
      });
      
      const file = this.files[0];
      let isPdf = false;

      if (file.type == "application/pdf") {
        alert("Not implemented yet.");
        isPdf = true;
      } else {
        reader.readAsDataURL(file);
      }
    });
  }

  function handleKeypress(e) {
    e.preventDefault();
    e.stopPropagation();

    currRectWidth = parseInt(cursorX - canvasOffsetX) - rectX;
    currRectHeight = parseInt(cursorY - canvasOffsetY) - rectY;

    const key = e.key;
    console.log(key);
    switch(key) {
      case "ArrowUp":
        rectY -= 2;
        cursorY -= 2;
        break;
      case "ArrowDown":
        rectY += 2;
        cursorY += 2;
        break;
      case "ArrowLeft":
        rectX -= 2;
        cursorX -= 2;
        break;
      case "ArrowRight":
        rectX += 2;
        cursorX += 2;
        break;
      case "8":
        rectY -= 2;
        currRectHeight = parseInt(cursorY - canvasOffsetY) - rectY;
        break;
      case "2":
        rectY += 2;
        currRectHeight = parseInt(cursorY - canvasOffsetY) - rectY;
        break;
      case "4":
        rectX -= 2;
        currRectWidth = parseInt(cursorX - canvasOffsetX) - rectX;
        break;
      case "6":
        rectX += 2;
        currRectWidth = parseInt(cursorX - canvasOffsetX) - rectX;
        break;
      case "p":
        const previousName = bbNames.slice(-1);
        console.log(previousName);
  
        if (previousName.length != 0) {
          const [x, y, w, h] = boundingBoxes[previousName[0]]["absolute"];
          [cursorX, cursorY] = boundingBoxes[previousName[0]]["cursor"];
          rectX = x;
          rectY = y;

          reDraw();

          console.log(`prev rect ${x}, ${y}, ${w}, ${h} cursor ${cursorX} ${cursorY}`);
          ctx.strokeRect(x, y, w, h);
          return true;
        }
    }

    console.log("before redraw");
    console.log(`${rectX}, ${rectY}, ${currRectWidth}, ${currRectHeight}`);
    reDraw();
    ctx.strokeRect(rectX, rectY, currRectWidth, currRectHeight);

    return true;
  }

  function mouseDown(e) {
    e.preventDefault();
    e.stopPropagation();
    canvas.focus();
  
    rectX = parseInt(e.clientX - canvasOffsetX);
    rectY = parseInt(e.clientY - canvasOffsetY);
  
    dragging = true;
    return true;
  }
  
  function mouseUp(e) {
    e.preventDefault();
    e.stopPropagation();

    cursorX = e.clientX;
    cursorY = e.clientY;
  
    dragging = false;
  
    rectangles.push([rectX, rectY, currRectWidth, currRectHeight]);
    rectanglesOutput.push([rectX * (1/scalingFactor), rectY * (1/scalingFactor), currRectWidth * (1/scalingFactor), currRectHeight * (1/scalingFactor)]);
    return true;
  }
  
  function mouseOut(e) {
    e.preventDefault();
    e.stopPropagation();
  
    dragging = false;
    return true;
  }
  
  function mouseMove(e) {
    e.preventDefault();
    e.stopPropagation();
  
    if (!dragging) {
      return true;
    }
  
    reDraw();
  
    currRectWidth = parseInt(e.clientX - canvasOffsetX) - rectX;
    currRectHeight = parseInt(e.clientY - canvasOffsetY) - rectY;
  
    ctx.strokeRect(rectX, rectY, currRectWidth, currRectHeight);
    return true;
  }
  
  function reDraw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0, imgWidthNew, imgHeightNew);
  

    ctx.strokeStyle = rectLineColor2;
    for (const [key, obj] of Object.entries(boundingBoxes)) {
      const [x, y, w, h] = obj["absolute"];
      ctx.strokeRect(x, y, w, h);
      ctx.fillText(key, x + w/2, y + h/2 + 5);
  
    }

    ctx.strokeStyle = rectLineColor1;
  
  }
  
  function add() {
    const key = document.getElementById("keyName").value;
    const filteredWords = document.getElementById("filteredWords").value.split(/\s+/);
  
    if (filteredWords.length == 1 && filteredWords[0] == "") filteredWords.pop();
  
    document.getElementById("keyName").value = "";
    document.getElementById("filteredWords").value = "";
  
    if (key.trim() == "") {
      alert("Key name cannot be empty!");
      return;
    }
    if (key in boundingBoxes) {
      alert("Key names have to be unique!");
      return;
    }
  
  
    // draw text
  
    ctx.fillText(key, rectX + currRectWidth/2, rectY + currRectHeight/2 + 5);
  
    bbNames.push(key);
  
    const scaled = [rectX * (1/scalingFactor), rectY * (1/scalingFactor), currRectWidth * (1/scalingFactor), currRectHeight * (1/scalingFactor)].map(x => Math.round(x));
    boundingBoxes[key] = {
      "absolute":  [rectX, rectY, currRectWidth, currRectHeight],
      "scaled": scaled,
      "filteredWords": filteredWords,
      "cursor": [cursorX, cursorY]
    };
  
    // boundingBoxes[key] = [rectX * (1/scalingFactor), rectY * (1/scalingFactor), currRectWidth * (1/scalingFactor), currRectHeight * (1/scalingFactor)];
    previousBB = key;
    console.log(boundingBoxes);

    document.getElementById("canvas").focus();

  }
  
  function undo() {
    rectangles.pop();
    rectanglesOutput.pop();
  
    const previousName = bbNames.pop();
  
    if (typeof previousName != "undefined") {
      delete boundingBoxes[previousName];
    }
  
    reDraw();
  }
  
  function download(content, fileName, contentType) {
    const a = document.createElement("a");
    const file = new Blob([content], { type: contentType });
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
  }
   
  function onDownload(){
    download(JSON.stringify(boundingBoxes), "boundingBoxes.json", "text/plain");
  }

  return {
    add,
    undo,
    onDownload,
    init
  }
  
})();

CanvasModule.init();
