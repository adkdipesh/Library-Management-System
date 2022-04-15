from asyncio.windows_events import NULL
from django.shortcuts import render, redirect
from django.contrib.auth import logout
#from django.contrib.auth.decorators import login_required
from librarian.models import ISBN, Student, Transaction
# To save image using decoded string
import base64, re
from PIL import Image
from io import BytesIO
from base64 import b64decode
# For both QR scan and face scan/recognize
import cv2                   # pip install openCV-python  #pip install cv2
# For face scan and recognize
import numpy as np
# For QR scan
import imutils
from imutils.video import VideoStream
from pyzbar import pyzbar  # pip install pybazar 
import argparse
import datetime
import time
# For Audio
from gtts import gTTS      # pip install gTTS
import os
import playsound       # pip install playsound

def sound(text):
    sound_file=gTTS(text=text,lang='en',slow=True)
    sound_file.save("notification.mp3")
    os.system("notification.mp3")

def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)


def recognize():
    cam=cv2.VideoCapture(0)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    while(True):
        ret, im=cam.read()
       # im=cv2.imread('static/image.jpg')
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            print(conf)
            if(conf < 40): 
                print(Id)
                if(Id == 1):
                    id = 15
                    print(Id)
                    cam.release()
                    cv2.destroyAllWindows()
                    return id
                else:
                    return 0

def slogin(request):
    if request.method == "POST":
        image_str = request.POST.get("uname")        
        # imgdata = decode_base64(img_str[24:])
        imagestr = image_str
        im = Image.open(BytesIO(b64decode(imagestr.split(',')[1])))
        im.save("static/image.jpg")
        std_id=recognize()
        if(std_id==15):
            obj = Student.objects.get(id = std_id)
            transactions = Transaction.objects.filter(student = obj)
            # return redirect(home, xyz={'student':obj})
            return render(request, 'studenttemplate/index.html', {'student':obj,'transactions':transactions})
        else:
            return render(request, 'studenttemplate/slogin.html', {'msg':'Unauthenticate Person detected.'})
    return render(request, 'studenttemplate/slogin.html', {})



def slogout(request):
    logout(request)
    return redirect('slogin-page')


def home(request):
    student = Student.objects.get(id = 15)
    transactions = Transaction.objects.filter(student = student)
    # transaction_data = []
    # for transaction in transactions:
    # isbn = ISBN.objects.get(id=transaction.isbn)
    # barcode = isbn.barcode 
    # for transaction in transactions:     
    # print(transaction.isbn.edition.which_edition)
    # print(transaction.isbn.edition.title.name)        
    return render(request, 'studenttemplate/index.html', {"student":student,'transactions':transactions})




def qrscan():
    # construct the argument parser and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-o", "--output", type=str, default="barcodes.csv",help="path to output CSV file containing barcodes")
    # args = vars(ap.parse_args())

    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    #vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
    # open the output CSV file for writing and initialize the set of
    # barcodes found thus far
    # csv = open(args["output"], "w")
    found = set()

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)

        # loop over the detected barcodes
        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            vs.stop()
            cv2.destroyAllWindows()
            print(text)
            return text
            # if the barcode text is currently not in our CSV file, write
            # the timestamp + barcode to disk and update the set
            # if barcodeData not in found:
                # csv.write("{},{}\n".format(datetime.datetime.now(),
                #     barcodeData))
                # csv.flush()
                # found.add(barcodeData)

                    # show the output frame
        cv2.imshow("Barcode Scanner", frame)
    
    

        # # if the `q` key was pressed, break from the loop
        # if key == ord("q"):
        #     break   
    # close the output CSV file do a bit of cleanup
    # print("[INFO] cleaning up...")
    # csv.close()
    # cv2.destroyAllWindows()
    # vs.stop()

def borrowbook(request):
    if(request.GET.get("camera")):
        barcode = qrscan()
        obj = Transaction()
        obj.isbn = ISBN.objects.get(barcode = barcode)
        obj.student = Student.objects.get(id = 15)
        sts = Transaction.objects.filter(isbn = obj.isbn, returned_status = False).count()
        print(sts)       
        count1 = obj.student.issued_count
        fine = obj.student.fine_status      
        print(count1, fine)       
        if count1<2 and fine == False and sts == 0:
        #if obj.student.issued_count <= 2:
            obj.student.issued_count += 1
            obj.student.save()
            obj.save()
            sound("book issued successfully")
            return render(request, 'studenttemplate/borrowbook.html',{'obj':obj})
        else:
            sound("book issue Failed, Either you have already meet book limit of 2 or yet to clear fine")
            return render(request, 'studenttemplate/borrowbook.html',{'msg':'Book Issue Failed'})
    return render(request, 'studenttemplate/borrowbook.html',{'msg':'Scan First'})

def returnbook(request):
    if(request.GET.get("camera")):
        barcode = qrscan()
        isbnflt = ISBN.objects.get(barcode=barcode)
        student = Student.objects.get(id = 15)
        obj = Transaction.objects.get(isbn = isbnflt, student=student)
        if obj != NULL :
            obj.student.issued_count -= 1
            obj.student.save()
            obj.delete()
            sound("book returned successfully")
            return render(request, 'studenttemplate/returnbook.html',{'barcode':barcode, 'msg':' is returned successfully.'})
        else:
            sound("Book return Failed. This book wasn't issued to you.")
            return render(request, 'studenttemplate/returnbook.html',{'msg':'Failed to return'})
    return render(request, 'studenttemplate/returnbook.html',{})