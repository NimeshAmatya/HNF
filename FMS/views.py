from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from keras.models import load_model
from keras.preprocessing import image
import json
from tensorflow import Graph
import tensorflow as tf
import cv2
import numpy as np
import os
from .models import Forms
import csv
from django.http import HttpResponseRedirect, JsonResponse
import json
from django.db.models import Q
from .forms import Image_form

model_graph = Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        model=load_model('D:\\Year III\\FYP\\HRF\\models\\model_hand.h5')
# Create your views here.
def index(request):
    if request.method == "POST":
        form = Image_form(request.POST or None,request.files or None)
        if form.is_valid():
            form.save()
    else:
        form = Image_form()
    context = {
        'a':1, 
        'form':form,
        }
    return render(request, 'index.html', context)

def predict(request):
    if request.method == "POST":
        form = Image_form(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
    else:
        form = Image_form()

    word_dict = {
    0:'A',
    1:'B',
    2:'C',
    3:'D',
    4:'E',
    5:'F',
    6:'G',
    7:'H',
    8:'I',
    9:'J',
    10:'K',
    11:'L',
    12:'M',
    13:'N',
    14:'O',
    15:'P',
    16:'Q',
    17:'R',
    18:'S',
    19:'T',
    20:'U',
    21:'V',
    22:'W',
    23:'X',
    24:'Y',
    25:'Z'
    }

    per = 25

    roi = [[(232, 549), (319, 624), 'text', 'FirstName'], 
        [(339, 549), (427, 624), 'text', 'FirstName'], 
        [(439, 549), (527, 624), 'text', 'FirstName'], 
        [(539, 552), (619, 627), 'text', 'FirstName'], 
        [(637, 552), (717, 622), 'text', 'FirstName'], 
        [(729, 552), (817, 624), 'text', 'FirstName'], 
        [(834, 549), (929, 624), 'text', 'FirstName'], 
        [(944, 552), (1027, 622), 'text', 'FirstName'], 
        [(239, 769), (327, 847), 'text', 'LastName'], 
        [(344, 774), (429, 847), 'text', 'LastName'], 
        [(444, 777), (529, 844), 'text', 'LastName'], 
        [(542, 767), (627, 847), 'text', 'LastName'], 
        [(639, 769), (719, 847), 'text', 'LastName'], 
        [(737, 772), (822, 842), 'text', 'LastName'], 
        [(839, 772), (934, 847), 'text', 'LastName'], 
        [(947, 772), (1034, 847), 'text', 'LastName'], 
        [(242, 999), (329, 1077), 'text', 'Address'], 
        [(339, 997), (424, 1077), 'text', 'Address'], 
        [(444, 1004), (529, 1077), 'text', 'Address'], 
        [(549, 999), (624, 1077), 'text', 'Address'], 
        [(639, 999), (719, 1074), 'text', 'Address'], 
        [(737, 1002), (819, 1074), 'text', 'Address'], 
        [(842, 1002), (932, 1077), 'text', 'Address'], 
        [(947, 997), (1039, 1082), 'text', 'Address'], 
        [(244, 1209), (337, 1287), 'text', 'Gender'], 
        [(354, 1212), (442, 1284), 'text', 'Gender'], 
        [(449, 1212), (542, 1284), 'text', 'Gender'], 
        [(557, 1219), (637, 1279), 'text', 'Gender'], 
        [(657, 1217), (729, 1284), 'text', 'Gender'], 
        [(754, 1212), (829, 1284), 'text', 'Gender'], 
        [(242, 1422), (329, 1494), 'text', 'Field'], 
        [(349, 1427), (442, 1499), 'text', 'Gender'], 
        [(459, 1424), (539, 1499), 'text', 'Gender']]

    imgQ = cv2.imread('D:\\Year III\\FYP\\Form.png')

    orb = cv2.ORB_create(1500)
    kp1, des1 = orb.detectAndCompute(imgQ, None)
    imgKp1 = cv2.drawKeypoints(imgQ, kp1, None)

    #path = 'D:\\Year III\\FYP\\Forms'
    path = 'media/Forms/pdfs'
    myPicList = os.listdir(path)
    print(myPicList)
    # fileObj = request.FILES['filePath']
    # fs = FileSystemStorage()
    # filePathName = fs.save(fileObj.name, fileObj)
    # filePathName = fs.url(filePathName)
    # test_image = '.'+filePathName
    for j,y in enumerate(myPicList):
        # fileObj = request.FILES['filePath']
        # fs = FileSystemStorage()
        # filePathName = fs.save(fileObj.name, fileObj)
        # filePathName = fs.url(filePathName)
        # test_image = '.'+filePathName
        
        img = cv2.imread(path + "/" + y)
        #img = cv2.imread(test_image)
        #img = cv2.resize(img, (w//2, h//2))
        #cv2.imshow("y",img)
        kp2, des2 = orb.detectAndCompute(img, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.match(des2, des1)
        matches.sort(key = lambda x:x.distance)
        good = matches[:int(len(matches)*(per/100))]
        imgMatch = cv2.drawMatches(img, kp2, imgQ, kp1, good[:70], None, flags=2)
        #imgMatch = cv2.resize(imgMatch, (w//2, h//2))
        #cv2.imshow(y, imgMatch)

        srcPoints = np.float32([kp2[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        dstPoints = np.float32([kp1[m.trainIdx].pt for m in good]).reshape(-1,1,2)

        M, _ = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.0)
        h,w = imgQ.shape[:2]
        imgScan = cv2.warpPerspective(img, M, (w,h))
        #imgScan = cv2.resize(imgScan, (w//2, h//2 ))
        #cv2.imshow(y, imgScan) 

        imgShow = img.copy()
        imgMask = np.zeros_like(imgShow)

        myData = []
    
        for x, r in enumerate(roi):
        #Highlight the fields
            cv2.rectangle(imgMask,(r[0][0], r[0][1]), (r[1][0], r[1][1]),(255,0,0), cv2.FILLED)
            imgShow = cv2.addWeighted(imgShow, 0.99, imgMask, 0.1,0)
        
        #Cropping the characters
            imgCrop = imgScan[r[0][1]:r[1][1],r[0][0]:r[1][0]]
        #cv2.imshow(str(x),imgCrop)
        
        
        
            if r[2] == 'text':

                img = cv2.imread('imgCrop')
                img_copy = imgCrop.copy()
                #cv2.imshow("img_copy", img_copy)
                img = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2RGB)
                img = cv2.resize(imgCrop, (400,440))

                img_copy = cv2.GaussianBlur(img_copy, (7,7), 0)
                img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
                #cv2.imshow("ImgGray",img_gray)
                _, img_thresh = cv2.threshold(img_gray, 180, 255, cv2.THRESH_BINARY_INV)
                #cv2.imshow("ImTHresh",img_thresh)
    
                img_final = cv2.resize(img_thresh, (28,28))
                #cv2.imshow("Img",img_final)
                img_final1 = np.reshape(img_final, (1,28,28,1))

                with model_graph.as_default():
                    with tf_session.as_default():
                        print(f'{r[3]}:{word_dict[np.argmax(model.predict(img_final1))]}')
                        myData.append(word_dict[np.argmax(model.predict(img_final1))]) 

            cv2.putText(imgShow, str(myData[x]),(r[0][0],r[0][1]),
             cv2.FONT_HERSHEY_PLAIN,2.5,(0,0,255),4)

        with open('D:\Year III\FYP\HRF\FMS\DataOutput.csv','a+') as f:
            for data in myData:
                f.write((str(data)))
            f.write('\n')       
        imgShow = cv2.resize(imgShow,(w//2, h//2))

        # with open('D:\Year III\FYP\HRF\FMS\DataOutput.csv') as f:
        #     reader = csv.reader(f)
        #     for row in reader:
        #         _, created = Forms.objects.get_or_create(
        #             FirstName =[myData[0:8]],     
        #             LastName = [myData[8:16]],
        #             Address = [myData[16:24]],
        #             Gender = [myData[24:30]],
        #             Field = [myData[30:33]],

        #         )
        
        #cv2.imshow(y, imgShow)
        #cv2.imshow("KeyPoints",imgKp1) 
        #cv2.imshow("Output",imgQ)
    cv2.waitKey(0)

    fn = ''.join(myData[0:8]) 
    ln = ''.join(myData[8:16])
    ad = ''.join(myData[16:24])
    gen = ''.join(myData[24:30])
    fie = ''.join(myData[30:33])

    context ={
        'fn':fn, #firstname
        'ln':ln, #lastname
        'ad':ad, #address
        'gen':gen, #gender
        'fie':fie, #field

        'form':form,
    }


    return render (request,'form.html',context)

def upload_form(request):
    FirstName = request.POST.get('FirstName')
    LastName = request.POST.get('LastName')
    Address = request.POST.get('Address')
    Gender = request.POST.get('Gender')
    Field = request.POST.get('Field')

    try:
        newForm = Forms(FirstName=FirstName,LastName=LastName, Address=Address, Gender=Gender, Field=Field)
        newForm.save()
        return redirect('FMS:form')

    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def form_list(request):
    form = Forms.objects.all()

    query = ""
    if request.GET:
        query = request.GET['q']

        book = get_data_queryset(str(query))

    return render(request, "form_list.html",{"forms":form})

def delete_form(request,pk):
    form = Forms.objects.get(pk=pk)
    form.delete()
    return redirect('/form')

def get_data_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        forms = Forms.objects.filter(
            Q(location__icontains=q)
        ).distinct()

    for form in forms:
        queryset.append(form)
    return list(set(queryset))

def show_all_data(request):
    form = Forms.objects.all()
    print(type(form))
    dict_type = {"forms":list(form.values("FirstName","LastName","Address","Gender","Field"))}

    return JsonResponse(dict_type)


