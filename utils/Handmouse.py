import win32api, win32con
from win32api import GetSystemMetrics
from utils.Gesture_Queue import *
#from utils.hover_window import *
import sys


class Hand_mouse(object):
    GQ = Gesture_queue()
    TC = Time_counters()
    TC2 = Time_counters()

    def __init__(self, object, mouse_x=0, mouse_y=0, hand_state=0):
        self.screen_width = GetSystemMetrics(0)
        self.screen_height = GetSystemMetrics(1)
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.hand_state = hand_state
        self.gesture_list = [[], []]
        self.mouse_leftbut = 0
        self.object = object

    # 移動
    def mouse_point_update(self, mouse_x, mouse_y):
        #スクリーン補償
        mouse_x = (self.screen_width / 960) * (mouse_x) * 1.5 - 960 * 0.3
        mouse_y = (self.screen_height / 540) * (mouse_y) * 1.5 - 540 * 0.3

        # 振動減少
        self.mouse_x = (mouse_x + self.mouse_x) / 2
        self.mouse_y = (mouse_y + self.mouse_y) / 2
        # マウス移動
        win32api.SetCursorPos((int(self.mouse_x), int(self.mouse_y)))

    def click(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 200, 200, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 200, 200, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 200, 200, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 200, 200, 0, 0)

    def mouse_leftdown(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 200, 200, 0, 0)

    def mouse_leftup(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 200, 200, 0, 0)

    def mouse_rightdown(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 200, 200, 0, 0)

    def mouse_rightup(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 200, 200, 0, 0)

    def check_hand_state(self, keypoint_classifier_labels,
                         point_history_classifier_labels, mean_x_point,
                         mean_y_point):

        self.gesture_list = [
            self.gesture_list[1], [keypoint_classifier_labels]
        ]
        if Hand_mouse.TC2.flag != 1:
            if self.gesture_list == [['Six'], ['Six']]:
                if self.hand_state == 0:
                    self.hand_state = 1
                else:
                    self.hand_state = 0
                Hand_mouse.TC2.flag = 1
                if self.hand_state == 0:
                    self.object.print_signal.emit('Stop')
                    #NotificationWindow.success('info', 'Stop')
                    #print("Stop")
                else:
                    self.object.print_signal.emit('Start')
                    #NotificationWindow.success('info', 'Start')
                    #print("Start")
        Hand_mouse.TC2.update()

        if self.hand_state == 1:
            self.mouse_point_update(mean_x_point, mean_y_point)
            Hand_mouse.GQ.enqueue(point_history_classifier_labels)
            Hand_mouse.GQ.get_max_queue()
            self.gesture_list = [
                self.gesture_list[1], [keypoint_classifier_labels]
            ]

            if self.gesture_list == [['Ok'], ['Ok']]:
                #print(self.mouse_leftbut)
                if self.mouse_leftbut == 0:
                    self.mouse_leftbut = 1
                    self.mouse_leftdown()
                    self.object.print_signal.emit('mouse leftdown')
                    #WorkThread.pop_tip.emit('mouse_leftup')
                    #NotificationWindow.info('info', 'mouse leftdown')
                    #print("mouse_leftdown")
                elif self.mouse_leftbut == 1:
                    pass
                    #print("mouse_leftdown pass")

            if self.mouse_leftbut == 1 and (self.gesture_list == [['Open'],
                                                                  ['Open']]):
                self.mouse_leftup()
                self.mouse_leftbut = 0
                #print("mouse_leftup")
                self.object.print_signal.emit('mouse leftup')
                #WorkThread.pop_tip.emit('mouse_leftup')
            #NotificationWindow.info('info', 'mouse leftup')

            if Hand_mouse.TC.flag != 1:
                if self.gesture_list == [['Pointer'], ['Pointer']]:
                    self.mouse_leftdown()
                    self.mouse_leftup()
                    Hand_mouse.TC.flag = 1
                    #print("L")
                    #time.sleep(100)
                elif self.gesture_list == [['Two'], ['Two']]:
                    self.mouse_rightdown()
                    self.mouse_rightup()
                    Hand_mouse.TC.flag = 1
                    #print("R")
            Hand_mouse.TC.update()

            if Hand_mouse.GQ.get_max_queue() == 'Counter Clockwise':
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -30)
                #print("down")
            if Hand_mouse.GQ.get_max_queue() == 'Clockwise':
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, 30)
                #print("up")

        else:
            pass
