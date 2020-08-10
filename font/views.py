from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse, JsonResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from PIL import Image
from .get_ttx_file import generate_ttx_file
from fontTools import ttx
from shutil import copyfile, rmtree 
import uuid
import os
import base64
from django.conf import settings


# Web Automation Imports
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from time import sleep
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# import time
# from selenium.webdriver.common.action_chains import ActionChains
# import requests
# from selenium.webdriver.chrome.options import Options



characters = {1 : ["x22", "x25", "x26", "x27", "x28", "x29", "x2c", "x2d", "x2e", "x2f", "x30", "x31", "x32", "x33", "x34", "x35", "x36", "x37", "x38", "x39", "x3a", "x3d", "x3f", "x41", "x42", "x43", "x44", "x45", "x46", "x47", "x48", "x49", "x4a", "x4b", "x4c", "x4d", "x4e", "x4f", "x50", "x51", "x52", "x53", "x54", "x55", "x56", "x57", "x58", "x59", "x5a", "x61", "x62", "x63", "x64", "x65", "x66", "x67", "x68", "x69", "x6a", "x6b"], 2 : ["x6c", "x6d", "x6e", "x6f", "x70", "x71", "x72", "x73", "x74", "x75", "x76", "x77", "x78", "x79", "x7a"], 3 : ["x21", "x23", "x24", "x2a", "x2b", "x3b", "x3c", "x3e", "x40", "x5b", "x5c", "x5d", "x5e", "x5f", "x60", "x7b", "x7c", "x7d", "x7e", "x2191"]}

templates_char_count = {1: 60, 2: 15, 3: 20}

#characters_list_1 = ["x22", "x25", "x26", "x27", "x28", "x29", "x2c", "x2d", "x2e", "x2f", "x30", "x31", "x32", "x33", "x34", "x35", "x36", "x37", "x38", "x39", "x3a", "x3d", "x3f", "x41", "x42", "x43", "x44", "x45", "x46", "x47", "x48", "x49", "x4a", "x4b", "x4c", "x4d", "x4e", "x4f", "x50", "x51", "x52", "x53", "x54", "x55", "x56", "x57", "x58", "x59", "x5a", "x61", "x62", "x63", "x64", "x65", "x66", "x67", "x68", "x69", "x6a", "x6b"]

#characters_list_2 = ["x6c", "x6d", "x6e", "x6f", "x70", "x71", "x72", "x73", "x74", "x75", "x76", "x77", "x78", "x79", "x7a"]

#characters_list_3 = ["x21", "x23", "x24", "x2a", "x2b", "x3b", "x3c", "x3e", "x40", "x5b", "x5c", "x5d", "x5e", "x5f", "x60", "x7b", "x7c", "x7d", "x7e"]

BASE_PATH_IMAGE_FOLDER = os.path.join(settings.BASE_DIR, 'images')
BASE_PATH_TTF_FILES_FOLDER = os.path.join(settings.BASE_DIR, 'ttf_files')
# BASE_FINAL_TEMPLATE_FOLDER_PATH = '/home/harshit/Desktop/handwritten_font/final_templates'
# CHROME_DRIVER_EXECUTABLE_PATH = '/home/harshit/Desktop/handwritten_font/chromedriver_linux64/chromedriver'


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@csrf_exempt
def generate_font(request):
    if request.method == 'POST':

        # print(request.headers)
        # print(request.POST)
        # file = request.POST.get('file')
        # filename = str(file)
        # print(request.FILES)
        # print(request.POST['testing'])

        # print(request.FILES.getlist('images[]')[0])
        # print(request.FILES.getlist('images[]')[1])

        unique_foldername = str(uuid.uuid4())
        # print(unique_foldername)
        folder_path = os.path.join(BASE_PATH_IMAGE_FOLDER, unique_foldername)
        try:
            os.mkdir(folder_path)
        except OSError as error:
            print(error)

        images_names = {}
        #print(request.FILES)
        for file_ptr in request.FILES.getlist('images[]'):
            filename = str(file_ptr)
            images_names.update({filename : 1})

            with default_storage.open('images/' + unique_foldername + '/' + filename, 'wb+') as destination:
                for chunk in file_ptr.chunks():
                    destination.write(chunk)
        
        font_name = request.POST['font_name'][1:-1]
        lowercase, uppercase, numbers, symbols = generate_ttx_file(folder_path, font_name)
        lowercase = ''.join(sorted(lowercase))
        uppercase = ''.join(sorted(uppercase))
        numbers = ''.join(sorted(numbers))

        ttx.main(['-d', folder_path, folder_path + '/' + font_name + '.ttx'])
        font_file_save_name = unique_foldername
        
        copyfile(folder_path + '/' + font_name + '.ttf', BASE_PATH_TTF_FILES_FOLDER + '/' + font_file_save_name + '.ttf')
        
        with open(folder_path + '/' + font_name + '.ttf', 'rb') as binary_file:
            binary_file_data = binary_file.read()
            base64_encoded_data = base64.b64encode(binary_file_data)
            base64_message = base64_encoded_data.decode('utf-8')
        
        rmtree(folder_path + '/')  
        
        return JsonResponse({  
            
            "name" : font_name + ".ttf",
            "content64" : base64_message,
            "lowercase" : lowercase,
            "uppercase" : uppercase,
            "numbers" : numbers,
            "symbols" : symbols
        })
        

        # templates = {1: 0, 2: 0, 3: 0}

        # for key in templates:
        #     paste_images_to_template(key, images_names, templates, path)

        # total_user_char_count = len(images_names)

        # # Two dimensional list and each element of the list (i.e. each row) holds a list having template numbers that are to be send in one go as there is total character count is less than 75
        # template_combinations = []
        # char_count = 0
        # combination = []
        # for key in templates:
        #     if templates[key] != 0:
        #         if char_count + templates[key] <= 75:
        #             combination.append(key)
        #         else:
        #             template_combinations.append(combination)
        #             combination = []
        #             combination.append(key)
        #             char_count = templates[key]

        # if len(combination) > 0:
        #     template_combinations.append(combination)

        # my_data = {'received': 'yes'}
        # response = HttpResponse(my_data, content_type='application/json')

        # return JsonResponse(my_data)
    else:
        return HttpResponse("Invalid Request")


def paste_images_to_template(template_no, image_names, templates, user_char_images_folder_path):

    char_count = templates_char_count[template_no]
    template_image = Image.open(BASE_FINAL_TEMPLATE_FOLDER_PATH + '/' + str(template_no) + '.png')
    template_copy = template_image.copy()

    left = 33
    top = 129
    right = 233
    bottom = 389
    count = 0

    for char in characters[template_no]:
        char += '.png'
        count += 1
        if image_names.has_key(char):
            templates[template_no] += 1
            user_char_image_path = user_char_images_folder_path + '/' + char
            user_char_img = Image.open(user_char_image_path)
            template_copy.paste(user_char_img, (left_1, top_1, right_1, bottom_1))

        left += 200
        right += 200

        if count == 6 or count == 12 or count == 20 or count == 28 or count == 36 or count == 44 or count == 52 or count == 60:
            left = 33
            right = 233
            top += 260
            bottom += 260

    template_copy.save(user_char_images_folder_path + '/' + template_no + '.png')

