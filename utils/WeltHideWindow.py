# from utils.Notification import NotificationWindow
from utils.Notification import NotificationIcon
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QRect, Qt, QRectF
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QMenu, QWidget, QListWidget, QVBoxLayout, QPushButton, QApplication, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPainterPath, \
    QColor



class WeltHideWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(WeltHideWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.resize(300, 100)
        self.capture_staut = 0
       #self.viewport().setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        #self.setWindowOpacity(0.9)

        self.initMenu()
        self.initAnimation()

    def close_windows(self):
        self.close()
        #QApplication.instance().aboutQt()

    def initAnimation(self):
        # 按钮动画
        self._animation = QPropertyAnimation(self._contextMenu,
                                             b'geometry',
                                             self,
                                             easingCurve=QEasingCurve.Linear,
                                             duration=100)
        # easingCurve 修改该变量可以实现不同的效果

    def paintEvent(self, event):
        # 圆角以及背景色
        super(WeltHideWindow, self).paintEvent(event)
        painter = QPainter(self)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        painter.fillPath(path, Qt.white)

    #右键菜单关闭
    def initMenu(self):
        self._contextMenu = QMenu(self)
        self._contextMenu.addAction('Close', self.close_windows)

    def mousePressEvent(self, event):
        '''鼠标按下事件，需要记录下坐标self._pos 和 是否可移动self._canMove'''
        super(WeltHideWindow, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._pos = event.globalPos() - self.pos()
            # 当窗口最大化或者全屏时不可移动
            self._canMove = not self.isMaximized() or not self.isFullScreen()

    def mouseMoveEvent(self, event):
        '''鼠标移动事件，动态调整窗口位置'''
        super(WeltHideWindow, self).mouseMoveEvent(event)
        if event.buttons() == Qt.LeftButton and self._canMove:
            self.move(event.globalPos() - self._pos)

    def mouseReleaseEvent(self, event):
        '''鼠标弹起事件，这个时候需要判断窗口的左边是否符合贴到左边，顶部，右边一半'''
        super(WeltHideWindow, self).mouseReleaseEvent(event)
        self._canMove = False
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        if x < 0:
            # 隐藏到左边
            return self.move(1 - self.width(), y)
        if y < 0:
            # 隐藏到顶部
            return self.move(x, 1 - self.height())
        if x > self._width - self.width() / 2:  # 窗口进入右边一半距离
            # 隐藏到右边
            return self.move(self._width - 1, y)

    def enterEvent(self, event):
        '''鼠标进入窗口事件，用于弹出显示窗口'''
        super(WeltHideWindow, self).enterEvent(event)
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        if x < 0:
            return self.move(0, y)
        if y < 0:
            return self.move(x, 0)
        if x > self._width - self.width() / 2:
            return self.move(self._width - self.width(), y)

    def leaveEvent(self, event):
        '''鼠标离开事件，如果原先窗口已经隐藏，并暂时显示，此时离开后需要再次隐藏'''
        super(WeltHideWindow, self).leaveEvent(event)
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        if x == 0:
            return self.move(1 - self.width(), y)
        if y == 0:
            return self.move(x, 1 - self.height())
        if x == self._width - self.width():
            return self.move(self._width - 1, y)

    def contextMenuEvent(self, event):
        pos = event.globalPos()
        size = self._contextMenu.sizeHint()
        x, y, w, h = pos.x(), pos.y(), size.width(), size.height()
        self._animation.stop()
        self._animation.setStartValue(QRect(x, y, 0, 0))
        self._animation.setEndValue(QRect(x, y, w, h))
        self._animation.start()
        self._contextMenu.exec_(event.globalPos())

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = WeltHideWindow()
    w.show()
    sys.exit(app.exec_())
