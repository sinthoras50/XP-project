import json
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from matplotlib.font_manager import json_load
import numpy as np
from .ocr.image_alignment import align_document
from .ocr.ocr_scanner import extract_data
import base64
import cv2

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

@csrf_exempt
def upload(request):

    if request.method == 'POST':


        # print(request.FILES['fileInvoice'].file.getvalue().decode("utf-8"))
        # print(request.FILES['fileTemplate'].file.getvalue().decode("utf-8"))

        template = request.FILES['fileTemplate'].read()
        invoice = request.FILES['fileInvoice'].read()
        np_template = np.fromstring(template, np.uint8)
        np_invoice = np.fromstring(invoice, np.uint8)

        aligned, preview = align_document(np_invoice, np_template)
        result, result_preview, data = extract_data(aligned)

        retval, frame_buffer = cv2.imencode('.png', result_preview)
        frame_b64 = base64.b64encode(frame_buffer)

        ret = {
            'img': str(frame_b64)[2:-1],
            'data': data
        }

        # return render(request, 'home/home.html', {'img': frame_b64})
        return HttpResponse(json.dumps(ret))
