from pdf2image import convert_from_path
pages = convert_from_path('file.pdf', 500)
pages = convert_from_path('file.pdf', 500, single_file=True)
pages[0].save('file.jpg', 'JPEG')