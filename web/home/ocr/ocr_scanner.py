from collections import namedtuple
import pytesseract
import argparse
import imutils
import cv2

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'

OCRLocation = namedtuple('OCRLocation', ['id', 'bbox',
	'filter_keywords'])

# define the locations of each area of the document we wish to OCR
# TODO let user select field locations
OCR_LOCATIONS = [
	OCRLocation('client_name', (52,299,233,30), []),
	OCRLocation('address', (52,337,233,30), []),
	OCRLocation('country', (52,355,233,30), []),
	OCRLocation('zip_code', (52,385,233,30), []),
    OCRLocation('invoice_total', (714,304,253,56), []),
    OCRLocation('item1', (55,563,360,60), ['Item', 'description', 'goes', 'here']),
    OCRLocation('item2', (55,642,360,60), ['Item', 'description', 'goes', 'here']),
    OCRLocation('item3', (55,717,360,60), ['Item', 'description', 'goes', 'here']),
    OCRLocation('item4', (55,799,360,60), ['Item', 'description', 'goes', 'here']),
]

def cleanup_text(text):
	# strip out non-ASCII text so we can draw the text on the image
	# using OpenCV
	return ''.join([c if ord(c) < 128 else '' for c in text]).strip()

def extract_data(image, ocr_locations=OCR_LOCATIONS):
    parsingResults = []

    # loop over the locations of the document we are going to OCR
    for loc in ocr_locations:
        # extract the OCR ROI from the aligned image
        (x, y, w, h) = loc.bbox
        roi = image[y:y + h, x:x + w]

        # OCR the ROI using Tesseract
        rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(rgb)

        # break the text into lines and loop over them
        for line in text.split('\n'):
            # if the line is empty, ignore it
            if len(line) == 0:
                continue

            # convert the line to lowercase and then check to see if the
            # line contains any of the filter keywords (these keywords
            # are part of the *form itself* and should be ignored)
            lower = line.lower()
            count = sum([lower.count(x) for x in loc.filter_keywords])

            # if the count is zero then we know we are *not* examining a
            # text field that is part of the document itself (ex., info,
            # on the field, an example, help text, etc.)
            if count == 0:
                # update our parsing results dictionary with the OCR'd
                # text if the line is *not* empty
                parsingResults.append((loc, line))

    # initialize a dictionary to store our final OCR results
    results = {}

    # loop over the results of parsing the document
    for (loc, line) in parsingResults:

        # grab any existing OCR result for the current ID of the document
        r = results.get(loc.id, None)

        # if the result is None, initialize it using the text and location
        # namedtuple (converting it to a dictionary as namedtuples are not
        # hashable)
        if r is None:
            results[loc.id] = (line, loc._asdict())

        # otherwise, there exists an OCR result for the current area of the
        # document, so we should append our existing line
        else:
            # unpack the existing OCR result and append the line to the
            # existing text
            (existingText, loc) = r
            text = '{}\n{}'.format(existingText, line)

            # update our results dictionary
            results[loc['id']] = (text, loc)

    # loop over the results
    for (locID, result) in results.items():
        # unpack the result tuple
        (text, loc) = result

        # display the OCR result to our terminal
        print(loc['id'])
        print('=' * len(loc['id']))
        print('{}\n\n'.format(text))

        # extract the bounding box coordinates of the OCR location and
        # then strip out non-ASCII text so we can draw the text on the
        # output image using OpenCV
        (x, y, w, h) = loc['bbox']
        clean = cleanup_text(text)

        # draw a bounding box around the text
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # loop over all lines in the text
        for (i, line) in enumerate(text.split('\n')):
            # draw the line on the output image
            startY = y + (i * 70) + 40
            cv2.putText(image, line, (x, startY),
                cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 255), 5)


    preview = imutils.resize(image, 400)

    return image, preview, results
