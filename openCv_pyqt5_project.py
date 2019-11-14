from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import cv2
import numpy as np 
import os 
import os.path





class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 420, 380)
        self.setWindowTitle("Take a picture of video!")
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Press 'Q' to quit and stop video")
        self.label.move(25, 25)
        self.update()

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Start video!")
        self.b1.move(30, 50)
        self.b1.clicked.connect(self.clicked)
        
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Press 'Esc' to escape from picture")
        self.label.move(150, 200)
        self.update()
        
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Press 'Space' to take a picture")
        self.label.move(150, 225)
        self.update()
        
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Snap pic!")
        self.b1.move(250, 250)
        self.b1.clicked.connect(self.snapPic)   

    def clicked(self):
        # self.label.setText("you clicked the button!")
        # self.update()
        self.showWebcam()
    
    def snapPic(self):
        self.takePicture()
        
    def takePicture(self):
        self.cam = cv2.VideoCapture(0)
        self.directory = "opencv_images"
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        cv2.namedWindow("Picture Time!")

        self.img_counter = 0

        while True:
            self.ret, self.frame = self.cam.read()
            cv2.imshow("Picture Time!", self.frame)
            if not self.ret:
                break
            self.k = cv2.waitKey(1)

            if self.k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif self.k%256 == 32:
                # SPACE pressed
                self.img_name = "opencv_images/opencv_image_{}.png".format(self.img_counter)
                cv2.imwrite(self.img_name, self.frame)
                print("{} written!".format(self.img_name))
                self.img_counter += 1

        self.cam.release()

        cv2.destroyAllWindows()
        
        
    def showWebcam(self):
        self.directory = "opencv_videos"
        self.file = "webcam.avi"
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            
        if not os.path.isfile(self.file):
            self.file = "1{}".format(self.file)
            print(self.file)
        
        self.cap = cv2.VideoCapture(0)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter("{}/{}".format((self.directory), (self.file)), self.fourcc, 20.0, (640, 480))
        while True:
            self.ret, self.frame = self.cap.read()
            
            ## self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            self.out.write(self.frame)
            cv2.imshow("window", self.frame)
            ## cv2.imshow("gray", self.gray)
            
            self.key = cv2.waitKey(1)
            if self.key == ord('q'):
                break
        
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

    def update(self):
        self.label.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = MyWindow()

    win.show()
    sys.exit(app.exec_())


window()
