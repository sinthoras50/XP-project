import json
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from matplotlib.font_manager import json_load
import numpy as np
from .ocr import *
import base64
import cv2

# Create your views here.
def home(request):
    return render(request, 'home/home.html')


@csrf_exempt
def upload(request):

    if request.method == 'POST':
        template_json = None
        template = np_template = None

        if 'fileJson' in request.FILES:
            template_json = json.loads(request.FILES['fileJson'].read())

        if 'fileTemplate' in request.FILES:
            template = request.FILES['fileTemplate'].read()
            np_template = np.fromstring(template, np.uint8)

        save_locations = request.POST['saveLocations']
        if save_locations == 'true':
            f = open('boundingBoxes.json', 'w')
            json.dump(template_json, f)
            f.close()

        invoice = request.FILES['fileInvoice'].read()
        np_invoice = np.fromstring(invoice, np.uint8)

        
        if template == None:
            aligned = cv2.imdecode(np_invoice, cv2.IMREAD_UNCHANGED)
        else:
            aligned, preview = image_alignment.align_document(np_invoice, np_template)

        result, result_preview, data = ocr_scanner.extract_data(aligned, template_json)

        retval, frame_buffer = cv2.imencode('.png', result_preview)
        frame_b64 = base64.b64encode(frame_buffer)

        ret = {
            'img': str(frame_b64)[2:-1],
            'data': data
        }

        return HttpResponse(json.dumps(ret))
