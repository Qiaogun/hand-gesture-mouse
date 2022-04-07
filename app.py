import sys
from utils.CommonHelper import CommonHelper
from utils.Handmouse import Hand_mouse
from utils.WeltHideWindow import WeltHideWindow
from utils.LogicProcessor import LogicProcessor
from PyQt5.QtCore import QRect, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout

from utils.Notification import NotificationWindow


class WorkThread(QThread):
    print_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.capstut = False

    def run(self):
        self.capstut = True
        self.print_signal.emit("starting...wait")
        lp = LogicProcessor(self)
        hm = Hand_mouse(self)
        lp.main_loop(hm)


# class MyButton(QPushButton):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         #self.setGeometry(QRect(10, 240, 93, 28))
#         #self.setStyleSheet('opacity: 90; background-color: rgba(90,90,90,0.9);')
#         self.adjustSize()


class CloseButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximumWidth(20)
        self.setMaximumHeight(20)


class StartButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximumWidth(20)
        self.setMaximumHeight(20)


class StopButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximumWidth(20)
        self.setMaximumHeight(20)


class MainWindow(WeltHideWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumWidth(170)
        self.setMinimumHeight(40)
        self._thread = WorkThread()
        self._thread.print_signal.connect(self.print_info)
        self._thread.start()
        
        x = CloseButton('', self, clicked=self.closeEvent)
        st = StartButton('', self, clicked=self.star_captur)
        sp = StopButton('', self, clicked=self.stop_captur)

        layout = QHBoxLayout(self)
        self._width = QApplication.desktop().availableGeometry(self).width()
        # st = QPushButton('capture start',self, clicked=self.star_captur)
        # sp = QPushButton('capture stop',self, clicked=self.stop_captur)
        # st.setMaximumWidth(150)
        # sp.setMaximumWidth(150)
        
        layout.addWidget(x)
        layout.addWidget(st)
        layout.addWidget(sp)

        self.adjustSize()

    def closeEvent(self):
        sys.exit(app.exec_())

    def print_info(self, info=None):
        NotificationWindow.info('info', info, callback=None)

    def star_captur(self):
        self._thread.capstut = True

    def stop_captur(self):
        self._thread.capstut = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    styleFile = './style.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    w = MainWindow()
    w.setStyleSheet(qssStyle)
    w.show()
    sys.exit(app.exec_())