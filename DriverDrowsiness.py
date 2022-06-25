'''In this code we have created a system which will take image as an input from the camera,
after taking the input we will detect the face and eyes from the image and then feed it to the classifier
where classifier will categorize this images as open or closed and will alert the driver depending upon the result '''

# importing all the necessary modules
import cv2
import os
# from keras.models import load_model
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
from mail import SendMail
import sys
win= Tk()
# Set the size of the tkinter window
win.geometry("1280x720")
frame = Frame(win, width=1280, height=720)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open("GUI.png"))

# Create a Label Widget to display the text or Image
label = Label(frame, image = img)
label.pack()
btn2=ttk.Button(win,text="STOP DETECTING",command= lambda:win.destroy())
btn2.place(x=600, y=400)

from tensorflow.keras.models import load_model
import numpy as np
from pygame import mixer
import tensorflow as tf
import smtplib



def Drowsiness():
    # Starting the mixer
    mixer.init()
    sound = mixer.Sound('alarm.wav')
    # these xml files are used to detect the faces
    face = cv2.CascadeClassifier('haar cascade files\haarcascade_frontalface_alt.xml')
    leye = cv2.CascadeClassifier('haar cascade files\haarcascade_lefteye_2splits.xml')
    reye = cv2.CascadeClassifier('haar cascade files\haarcascade_righteye_2splits.xml')
    print(tf.__version__)
    lbl = ['Closed', 'Open']
    # load the model we have created
    model = load_model('models/eyes_detection1.h5')
    path = os.getcwd()
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    # declaring the variables
    count =0
    score =0
    thicc =2
    rpred =[99]
    lpred =[99]
    # creating an infinite loop
    while (True):
        ret, frame = cap.read()
        height, width = frame.shape[:2]
        # convert the captured images to grayscale images:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.1, minSize=(25, 25))
        left_eye = leye.detectMultiScale(gray)
        right_eye = reye.detectMultiScale(gray)

        cv2.rectangle(frame, (0, height - 50), (200, height), (0, 0, 0), thickness=cv2.FILLED)
        # Iterating over faces:
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 1)
        # Iterating over right eye:
        for (x, y, w, h) in right_eye:
            r_eye = frame[y:y + h, x:x + w]
            count = count + 1
            r_eye = cv2.cvtColor(r_eye, cv2.COLOR_BGR2GRAY)
            r_eye = cv2.resize(r_eye, (24, 24))
            r_eye = r_eye / 255
            r_eye = r_eye.reshape(24, 24, -1)
            r_eye = np.expand_dims(r_eye, axis=0)
            rpred = model.predict_classes(r_eye)
            if (rpred[0] == 1):
                lbl = 'Open'
            if (rpred[0] == 0):
                lbl = 'Closed'
            break
        # Iterating over left eye:
        for (x, y, w, h) in left_eye:
            l_eye = frame[y:y + h, x:x + w]
            count = count + 1
            l_eye = cv2.cvtColor(l_eye, cv2.COLOR_BGR2GRAY)
            l_eye = cv2.resize(l_eye, (24, 24))
            l_eye = l_eye / 255
            l_eye = l_eye.reshape(24, 24, -1)
            l_eye = np.expand_dims(l_eye, axis=0)
            lpred = model.predict_classes(l_eye)
            if (lpred[0] == 1):
                lbl = 'Open'
            if (lpred[0] == 0):
                lbl = 'Closed'
            break

        if (rpred[0] == 0 and lpred[0] == 0):
            score = score + 1
            cv2.putText(frame,"Closed", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        else:
            score = score - 1
            cv2.putText(frame,"Open", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

        if (score < 0):
            score = 0
        cv2.putText(frame, 'Score:' + str(score), (100, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        if (score > 10):
            # person is feeling sleepy so we beep the alarm

            cv2.imwrite(os.path.join(path, 'image.jpg'), frame)
            try:
                sound.play()
                SendMail()

            except:  # displaying = False
                pass
            if (thicc < 16):
                thicc = thicc + 2
            else:
                thicc = thicc - 2
                if (thicc < 2):
                    thicc = 2
            cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), thicc)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def Exit():
    win.destroy()


# Add an optional Label widget
Label(win, font= ('Aerial 17 bold italic'))

# Create a Button to display the message
btn1=ttk.Button(win, text= "START DETECTING", command=Drowsiness)
btn1.place(x=600, y=350)
btn2=ttk.Button(win,text="STOP DETECTING",command=Exit)
btn2.place(x=600, y=400)
win.mainloop()

