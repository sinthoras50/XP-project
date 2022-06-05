from pdf2image import convert_from_bytes


def pdf_to_image(pdf):
    images = convert_from_bytes(pdf)

    return images[0]