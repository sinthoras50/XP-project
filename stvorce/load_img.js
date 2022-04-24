var canvasOffsetX = 0;
var canvasOffsetY = 0;

var dragging = false;

var rectX = 0;
var rectY = 0;

var currRectWidth = 0;
var currRectHeight = 0;

var imgWidthOrig = 0;
var imgHeightOrig = 0;
var imgWidthNew = 0;
var imgHeightNew = 0;

// TODO: make the image scale dynamically 
var scalingFactor = 0.5;

var rectLineColor = "red";
var rectLineWidth = 2; 

var img = null;

var ctx = null;

var canvas = null;

var rectangles = [];
var rectanglesOutput = []

document.querySelector("#image_input").addEventListener("change", function () {
  const reader = new FileReader();

  reader.addEventListener("load", () => {
    document.getElementById("upload-wrap").hidden = true;
    document.getElementById("undo").hidden = false;

    canvas = document.getElementById("canvas");

    img = new Image();
    img.src = reader.result;

    img.onload = () => {
      imgWidthNew = img.width * scalingFactor;
      imgHeightNew = img.height * scalingFactor;

      canvas.width = imgWidthNew;
      canvas.height = imgHeightNew;
      canvas.hidden = false;

      ctx = canvas.getContext("2d");

      ctx.drawImage(img, 0, 0, imgWidthNew, imgHeightNew);

      ctx.strokeStyle = rectLineColor;
      ctx.lineWidth = rectLineWidth;

      var canvasOffset = canvas.getBoundingClientRect();
      canvasOffsetX = canvasOffset.left;
      canvasOffsetY = canvasOffset.top;

      canvas.addEventListener("mousedown", function (e) { mouseDown(e); });
      canvas.addEventListener("mousemove", function (e) { mouseMove(e); });
      canvas.addEventListener("mouseup", function (e) { mouseUp(e); });
      canvas.addEventListener("mouseout", function (e) { mouseOut(e); });
    };
  });

  reader.readAsDataURL(this.files[0]);
});

function mouseDown(e) {
  e.preventDefault();
  e.stopPropagation();

  rectX = parseInt(e.clientX - canvasOffsetX);
  rectY = parseInt(e.clientY - canvasOffsetY);

  dragging = true;
}

function mouseUp(e) {
  e.preventDefault();
  e.stopPropagation();

  dragging = false;

  rectangles.push([rectX, rectY, currRectWidth, currRectHeight]);
  rectanglesOutput.push([rectX * (1/scalingFactor), rectY * (1/scalingFactor), currRectWidth * (1/scalingFactor), currRectHeight * (1/scalingFactor)]);
  console.log(rectangles);
  console.log(rectanglesOutput);
}

function mouseOut(e) {
  e.preventDefault();
  e.stopPropagation();

  dragging = false;
}

function mouseMove(e) {
  e.preventDefault();
  e.stopPropagation();

  if (!dragging) {
    return;
  }

  reDraw();

  currRectWidth = parseInt(e.clientX - canvasOffsetX) - rectX;
  currRectHeight = parseInt(e.clientY - canvasOffsetY) - rectY;

  ctx.strokeRect(rectX, rectY, currRectWidth, currRectHeight);
}

function reDraw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.drawImage(img, 0, 0, imgWidthNew, imgHeightNew);

  rectangles.forEach((rectangle) => {
    ctx.strokeRect(rectangle[0], rectangle[1], rectangle[2], rectangle[3]);
  });
}

function undo() {
  rectangles.pop();
  rectanglesOutput.pop();
  reDraw();
}
