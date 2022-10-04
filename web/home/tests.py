# from django.test import TestCase
from ocr import *
import unittest
import numpy as np
import os
import json
import cv2
import sys

TESTING_DIR = os.path.dirname(os.path.realpath(__file__)) + '\\testing'
BBOXES1 = json.load(open(os.path.join(TESTING_DIR, 'boundingBoxes.json')))
BBOXES2 = json.load(open(os.path.join(TESTING_DIR, 'boundingBoxes2.json')))
BBOXES3 = json.load(open(os.path.join(TESTING_DIR, 'boundingBoxes3.json')))
BBOXES4 = json.load(open(os.path.join(TESTING_DIR, 'boundingBoxes4.json')))

class InvoiceTestCase1(unittest.TestCase):

    def testAlignedInvoice(self):
        img_path = os.path.join(TESTING_DIR, 'invoice1.png') 

        with open(img_path, 'rb') as f:
            binary_image = f.read()
            np_image = np.frombuffer(binary_image, np.uint8)

            aligned, _ = image_alignment.align_document(np_image, np_image)
            _, _, data = ocr_scanner.extract_data(aligned, BBOXES1)

            keys = ['client_name', 'address', 'country', 'zip_code', 'invoice_total', 'item1', 'item2', 'item3', 'item4', 'item_price1', 'item_price2', 'item_price3', 'item_price4', 'item_amount1', 'item_amount2', 'item_amount3', 'item_amount4', 'subtotal', 'tax', 'total']
            self.assertEqual(keys, list(data.keys()))

            self.assertEqual(data['client_name'][0], 'Client Name')
            self.assertEqual(data['address'][0], '1 Client Address')
            self.assertEqual(data['country'][0], 'City, State, Country')
            self.assertEqual(data['item1'][0], 'Your item Name')
            self.assertEqual(data['total'][0], '$4520.00')
            self.assertEqual(data['tax'][0], '$520.00')

    def testMisalignedInvoice(self):
        template_path = os.path.join(TESTING_DIR, 'invoice1.png') 
        img_path = os.path.join(TESTING_DIR, 'invoice1_photo1.png') 

        with open(img_path, 'rb') as f:
            with open(template_path, 'rb') as f2:
                template_binary_image = f2.read()
                binary_image = f.read()
                np_template = np.frombuffer(template_binary_image, np.uint8)
                np_image = np.frombuffer(binary_image, np.uint8)

                aligned, _ = image_alignment.align_document(np_image, np_template)
                _, _, data = ocr_scanner.extract_data(aligned, BBOXES1)

                keys = ['client_name', 'address', 'country', 'zip_code', 'invoice_total', 'item1', 'item2', 'item3', 'item4', 'item_price1', 'item_price2', 'item_price3', 'item_price4', 'item_amount1', 'item_amount2', 'item_amount3', 'item_amount4', 'subtotal', 'tax', 'total']
                self.assertEqual(list(data.keys()), keys)

                self.assertEqual(data['client_name'][0], 'Client Name')
                self.assertEqual(data['address'][0], '1 Client Address')
                self.assertEqual(data['country'][0], 'City, State, Country')
                self.assertEqual(data['item1'][0], 'Your item Name')
                self.assertEqual(data['total'][0], '$4520.00')
                self.assertEqual(data['tax'][0], '$520.00')

    def testMisalignedInvoice1photo2(self):
        template_path = os.path.join(TESTING_DIR, 'invoice1.png') 
        img_path = os.path.join(TESTING_DIR, 'invoice1_photo2.png') 

        with open(img_path, 'rb') as f:
            with open(template_path, 'rb') as f2:
                template_binary_image = f2.read()
                binary_image = f.read()
                np_template = np.frombuffer(template_binary_image, np.uint8)
                np_image = np.frombuffer(binary_image, np.uint8)

                aligned, _ = image_alignment.align_document(np_image, np_template)
                _, _, data = ocr_scanner.extract_data(aligned, BBOXES1)

                keys = ['client_name', 'address', 'country', 'zip_code', 'invoice_total', 'item1', 'item2', 'item3', 'item4', 'item_price1', 'item_price2', 'item_price3', 'item_price4', 'item_amount1', 'item_amount2', 'item_amount3', 'item_amount4', 'subtotal', 'tax', 'total']
                self.assertEqual(list(data.keys()), keys)

                self.assertEqual(data['client_name'][0], 'Client Name')
                self.assertEqual(data['address'][0], '1 Client Address')
                self.assertEqual(data['country'][0], 'City, State, Country')
                self.assertEqual(data['item1'][0], 'Your item Name')
                self.assertEqual(data['total'][0], '$4520.00')
                self.assertEqual(data['tax'][0], '$520.00')

class InvoiceTestCase2(unittest.TestCase):
    def testAlignedInvoice(self):
        img_path = os.path.join(TESTING_DIR, 'invoice2.png') 

        with open(img_path, 'rb') as f:
            binary_image = f.read()
            np_invoice = np.frombuffer(binary_image, np.uint8)
            invoice = cv2.imdecode(np_invoice, cv2.IMREAD_UNCHANGED)

            _, _, data = ocr_scanner.extract_data(invoice, BBOXES2)

            keys = [
                'billing_name', 'billing_address', 'billing_address_2', 'invoice_num', 'date', 'po_box', 'due_date', 'item1', 'item2', 'item3', 'price1', 'price2', 'price3', 
                'amount1', 'amount2', 'amount3', 'amount_total' ]

            self.assertEqual(list(data.keys()), keys)
            self.assertIn('John Smith', data['billing_name'][0])
            self.assertIn('2 Court Square', data['billing_address'][0])
            self.assertIn('New York, NY 12210', data['billing_address_2'][0])
            self.assertIn('Front and rear brake cables', data['item1'][0])
            self.assertIn('New set of pedal arms', data['item2'][0])
            self.assertIn('100', data['amount1'][0])

class InvoiceTestCase3(unittest.TestCase):
    def testAlignedInvoice(self):
        img_path = os.path.join(TESTING_DIR, 'invoice3.png') 

        with open(img_path, 'rb') as f:
            binary_image = f.read()
            np_invoice = np.frombuffer(binary_image, np.uint8)
            invoice = cv2.imdecode(np_invoice, cv2.IMREAD_UNCHANGED)

            _, _, data = ocr_scanner.extract_data(invoice, BBOXES3)

            keys = [
                'name', 'address1', 'address2', 'invoice_num', 'invoice_date', 'po_box', 'due_date', 'item1', 'item2', 'item3', 'price1', 'price2', 'price3', 'price_total'
            ]

            self.assertEqual(list(data.keys()), keys)
            self.assertIn('John Smith', data['name'][0])
            self.assertIn('2 Court Square', data['address1'][0])
            self.assertIn('New York, NY 12210', data['address2'][0])
            self.assertIn('Front and rear brake cables', data['item1'][0])
            self.assertIn('New set of pedal arms', data['item2'][0])
            self.assertIn('100', data['price1'][0])
            self.assertIn('30', data['price2'][0])
            self.assertIn('15', data['price3'][0])
            self.assertIn('154.06', data['price_total'][0])

class InvoiceTestCase4(unittest.TestCase):
    def testAlignedInvoice(self):
        img_path = os.path.join(TESTING_DIR, 'invoice4.png') 

        with open(img_path, 'rb') as f:
            binary_image = f.read()
            np_invoice = np.frombuffer(binary_image, np.uint8)
            invoice = cv2.imdecode(np_invoice, cv2.IMREAD_UNCHANGED)

            _, _, data = ocr_scanner.extract_data(invoice, BBOXES4)

            keys = [
                'invoice_num', 'date', 'due_date', 'bill_to', 'address', 'city', 'country', 'postal', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'total',
                'amount1', 'amount2', 'amount3', 'amount4', 'amount5', 'amount6', 'company_name'
            ]

            self.assertEqual(list(data.keys()), keys)
            self.assertIn('0000001', data['invoice_num'][0])
            self.assertIn('12/31/20', data['date'][0])
            self.assertIn('12/31/20', data['due_date'][0])
            self.assertIn('Company Name', data['bill_to'][0])
            self.assertIn('Address', data['address'][0])
            self.assertIn('Item 1', data['item1'][0])
            self.assertIn('Item 1', data['item2'][0])
            self.assertIn('Item 1', data['item3'][0])
            self.assertIn('$00000.00', data['total'][0])



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=3).run(suite)