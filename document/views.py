from rest_framework import viewsets
from rest_framework import permissions
from django.http import HttpResponse, JsonResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from shutil import copyfile, rmtree
from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader
import uuid
import os
import base64
from django.conf import settings


BASE_PATH_DOCUMENT_FILES_FOLDER = os.path.join(settings.BASE_DIR, 'document_files')


@csrf_exempt
def generate_document(request):
    if request.method == 'POST':

        # print(request.POST)
        document_name = request.POST['document_name'][1:-1]
        
        font_file_content64 = request.POST['font_file_content64'][1:-1]
        font_file_content64 = font_file_content64.replace("\\n", "")
        
        font_size = request.POST['font_size'][1:-1]
        font_ink_color = request.POST['font_ink_color'][1:-1]
        paper_margin = request.POST['paper_margin'][1:-1]
        paper_lines = request.POST['paper_lines'][1:-1]
        
        text_file_content64 = request.POST['text_file_content64'][1:-1]
        text_file_content64 = text_file_content64.replace("\\n", "\n")

        unique_foldername = str(uuid.uuid4())
        # print(unique_foldername)
        folder_path = os.path.join(BASE_PATH_DOCUMENT_FILES_FOLDER, unique_foldername)
        try:
            os.mkdir(folder_path)
        except OSError as error:
            print(error)

        with default_storage.open('document_files/' + unique_foldername + '/' + unique_foldername + '.ttf', "wb") as fh:
            fh.write(base64.b64decode(font_file_content64))
            
        with default_storage.open('document_files/' + unique_foldername + '/' + unique_foldername + '.txt', "w+") as fh:
            # fh.write(base64.b64decode(text_file_content64))
            fh.write(text_file_content64)
        
        pdf = PDF('P', 'mm', 'A4')
        pdf.add_font('MyCustomFont', '', BASE_PATH_DOCUMENT_FILES_FOLDER + '/' + unique_foldername + '/' + unique_foldername + '.ttf', uni=True)
        pdf.set_font('MyCustomFont', '', int(font_size))
        
        if font_ink_color == 'Blue':
            pdf.set_text_color(0, 15, 85)  # blue
        elif font_ink_color == 'Black':
            pdf.set_text_color(51, 51, 51) # black
        elif font_ink_color == 'Red':
            pdf.set_text_color(247, 2, 15) # red
            
        if paper_margin == 'true':
            pdf.set_left_margin(29.0)
            pdf.set_top_margin(29.0)
        
        
        pdf.print_content_to_pdf(BASE_PATH_DOCUMENT_FILES_FOLDER + '/' + unique_foldername + '/' + unique_foldername + '.txt')
        pdf.output(BASE_PATH_DOCUMENT_FILES_FOLDER + '/' + unique_foldername + '/' + unique_foldername + '.pdf', 'F')
        
        watermark_filename = ''
        if paper_margin == 'true' and paper_lines == 'true':
            watermark_filename = 'watermark_paper_margin_lines.pdf'
        elif paper_margin == 'true':
            watermark_filename = 'watermark_paper_margin.pdf'
        elif paper_lines == 'true':
            watermark_filename = 'watermark_paper_lines.pdf'
                
        if watermark_filename != '':
            create_watermark(input_pdf=BASE_PATH_DOCUMENT_FILES_FOLDER + '/' + unique_foldername + '/' + unique_foldername + '.pdf', output=BASE_PATH_DOCUMENT_FILES_FOLDER + '/' + unique_foldername + '/' + unique_foldername + '.pdf', watermark=BASE_PATH_DOCUMENT_FILES_FOLDER + '/' + watermark_filename)
        
        
        with open(BASE_PATH_DOCUMENT_FILES_FOLDER + '/' + unique_foldername + '/' + unique_foldername + '.pdf', 'rb') as binary_file:
            binary_file_data = binary_file.read()
            base64_encoded_data = base64.b64encode(binary_file_data)
            base64_message = base64_encoded_data.decode('utf-8')
        
        # rmtree(BASE_PATH_DOCUMENT_FILES_FOLDER + '/' + unique_foldername + '/')
        
        return JsonResponse({  
            
            "document_name" : document_name + ".pdf",
            "content64" : base64_message
        })
        
        # my_data = {'received': 'yes'}
        # response = HttpResponse(my_data, content_type='application/json')

        # return JsonResponse(my_data)
    else:
        return HttpResponse("Invalid Request")
        
        
class PDF(FPDF):

    '''def __init__(self, paper_margin, paper_lines, orientation = 'P', unit = 'mm', format = 'A4'):
        FPDF.__init__(self, orientation, unit, format)
        self.paper_margin = paper_margin
        self.paper_lines = paper_lines
        

    def footer(self):
        if self.paper_margin == 'true':
            pdf.set_draw_color(255, 192, 203)
            pdf.set_line_width(0.4)
            pdf.line(0, 25, 210, 25)
            pdf.line(25, 0, 25, 297)
            
        if self.paper_lines == 'true':
            if self.paper_margin == 'true':
                self.add_lines_to_page(33)
            else:
                self.add_lines_to_page(0)
        
    def add_lines_to_page(self, y):
        pdf.set_draw_color(174, 181, 176)
        
        while y < 297:
            pdf.set_line_width(0.2)
            pdf.line(0, y, 210, y)
            y += 8
    '''
    
    def print_content_to_pdf(self, name):
        self.add_page()
        
        # Read text file
        with open(name, 'rb') as fh:
            txt = fh.read().decode('latin-1')
        # Output justified text
        self.multi_cell(0, 8, txt)
        # Line break
        self.ln()
        
        
def create_watermark(input_pdf, output, watermark):
    watermark_obj = PdfFileReader(watermark)
    watermark_page = watermark_obj.getPage(0)

    pdf_reader = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()

    # Watermark all the pages
    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)

    with open(output, 'wb') as out:
        pdf_writer.write(out)
       
