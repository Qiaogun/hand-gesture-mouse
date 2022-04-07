import cx_Freeze
import sys
import matplotlib
import numpy
import cv2
import os
import PyQt5
import mediapipe
import csv
import copy
import argparse
import itertools
import base64
import tensorflow
import win32api, win32con
from collections import Counter
from PyQt5.QtCore import QThread, pyqtSignal, QEasingCurve, QPropertyAnimation, QRect
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout

from PyQt5.QtCore import Qt, QRectF, QSize, QTimer
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPainterPath, \
    QColor
from PyQt5.QtWidgets import QWidget, QLabel,QMenu, \
    QGridLayout, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect, \
    QListWidget, QListWidgetItem

base = None
if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("app.py", base=base, icon="tap.ico")]
#os.environ['TCL_LIBRARY'] = r'C:\Users\danial khan\AppData\Local\Programs\Python\Python35\tcl\tcl8.6'
#os.environ['TK_LIBRARY'] = r'C:\Users\danial khan\AppData\Local\Programs\Python\Python35\tcl\tk8.6'
cx_Freeze.setup(
    name="Hand Mouse",
    #options = {"build_exe": {"packages":["PyQt5.QtCore","PyQt5.QtGui", "PyQt5.QtWidgets","ctypes","timeit","matplotlib","numpy","cv2"], "include_files":[r"C:\Users\danial khan\AppData\Local\Programs\Python\Python35\Lib\site-packages\PyQt5\plugins\platforms\qwindows.dll",r"C:\Users\danial khan\AppData\Local\Programs\Python\Python35\DLLs\tcl86t.dll",r"C:\Users\danial khan\AppData\Local\Programs\Python\Python35\DLLs\tk86t.dll","tdic1.ico"]}},
    options = {"build_exe": {"packages":["PyQt5.QtCore","PyQt5.QtGui", "PyQt5.QtWidgets","ctypes","timeit","matplotlib","numpy","cv2","tensorflow","mediapipe"],"include_files":[r"C:\Users\Qiao\AppData\Local\Programs\Python\Python39\Lib\site-packages\PyQt5\Qt5\plugins\platforms\qwindows.dll",r"C:\Users\Qiao\AppData\Local\Programs\Python\Python39\DLLs\tcl86t.dll",r"C:\Users\Qiao\AppData\Local\Programs\Python\Python39\DLLs\tk86t.dll",r"C:\Users\Qiao\AppData\Local\Programs\Python\Python39\Lib\site-packages\PyQt5\Qt5\bin\Qt5Core.dll","tap.ico","style.qss"]}},
    version="0.1",
    author='Cai Cai',
    description="Hand Mouse",
    executables=executables)

