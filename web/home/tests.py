# from django.test import TestCase
from ocr import *
import unittest
import numpy as np
import os

TESTING_DIR = os.path.dirname(os.path.realpath(__file__)) + '\\testing'

class InvoiceTestCase(unittest.TestCase):

    def testAlignedInvoice1(self):
        img_path = os.path.join(TESTING_DIR, 'invoice1.png') 

        with open(img_path, 'rb') as f:
            binary_image = f.read()
            np_image = np.frombuffer(binary_image, np.uint8)

            aligned, _ = image_alignment.align_document(np_image, np_image)
            _, _, data = ocr_scanner.extract_data(aligned)

            keys = ['client_name', 'address', 'country', 'zip_code', 'invoice_total', 'item1', 'item2', 'item3', 'item4', 'item_price1', 'item_price2', 'item_price3', 'item_price4', 'item_amount1', 'item_amount2', 'item_amount3', 'item_amount4', 'subtotal', 'tax', 'total']
            self.assertEqual(list(data.keys()), keys)

            self.assertEqual(data['client_name'][0], 'Client Name')
            self.assertEqual(data['address'][0], '1 Client Address')
            self.assertEqual(data['country'][0], 'City, State, Country')
            self.assertEqual(data['item1'][0], 'Your item Name')
            self.assertEqual(data['total'][0], '$4520.00')
            self.assertEqual(data['tax'][0], '$520.00')

    def testMisalignedInvoice1(self):
        template_path = os.path.join(TESTING_DIR, 'invoice1.png') 
        img_path = os.path.join(TESTING_DIR, 'invoice1_photo1.png') 

        with open(img_path, 'rb') as f:
            with open(template_path, 'rb') as f2:
                template_binary_image = f2.read()
                binary_image = f.read()
                np_template = np.frombuffer(template_binary_image, np.uint8)
                np_image = np.frombuffer(binary_image, np.uint8)

                aligned, _ = image_alignment.align_document(np_image, np_template)
                _, _, data = ocr_scanner.extract_data(aligned)

                keys = ['client_name', 'address', 'country', 'zip_code', 'invoice_total', 'item1', 'item2', 'item3', 'item4', 'item_price1', 'item_price2', 'item_price3', 'item_price4', 'item_amount1', 'item_amount2', 'item_amount3', 'item_amount4', 'subtotal', 'tax', 'total']
                self.assertEqual(list(data.keys()), keys)

                self.assertEqual(data['client_name'][0], 'Client Name')
                self.assertEqual(data['address'][0], '1 Client Address')
                self.assertEqual(data['country'][0], 'City, State, Country')
                self.assertEqual(data['item1'][0], 'Your item Name')
                self.assertEqual(data['total'][0], '$4520.00')
                self.assertEqual(data['tax'][0], '$520.00')

    def testMisalignedInvoice1(self):
        template_path = os.path.join(TESTING_DIR, 'invoice1.png') 
        img_path = os.path.join(TESTING_DIR, 'invoice1_photo2.png') 

        with open(img_path, 'rb') as f:
            with open(template_path, 'rb') as f2:
                template_binary_image = f2.read()
                binary_image = f.read()
                np_template = np.frombuffer(template_binary_image, np.uint8)
                np_image = np.frombuffer(binary_image, np.uint8)

                aligned, _ = image_alignment.align_document(np_image, np_template)
                _, _, data = ocr_scanner.extract_data(aligned)

                keys = ['client_name', 'address', 'country', 'zip_code', 'invoice_total', 'item1', 'item2', 'item3', 'item4', 'item_price1', 'item_price2', 'item_price3', 'item_price4', 'item_amount1', 'item_amount2', 'item_amount3', 'item_amount4', 'subtotal', 'tax', 'total']
                self.assertEqual(list(data.keys()), keys)

                self.assertEqual(data['client_name'][0], 'Client Name')
                self.assertEqual(data['address'][0], '1 Client Address')
                self.assertEqual(data['country'][0], 'City, State, Country')
                self.assertEqual(data['item1'][0], 'Your item Name')
                self.assertEqual(data['total'][0], '$4520.00')
                self.assertEqual(data['tax'][0], '$520.00')

if __name__ == '__main__':
    unittest.main()