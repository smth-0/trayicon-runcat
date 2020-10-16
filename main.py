import sys, psutil, time
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QSystemTrayIcon, QStyle, QMenu, QAction, qApp
from PyQt5.QtCore import QRunnable, QThreadPool, QTimer

class Program(QWidget):
    def __init__(self):
        super().__init__()

        self.sleep_icon = QIcon('static/my-sleeping-symbolic.svg')
        self.run_icons = [QIcon('static/my-running-%d-symbolic.svg'%i) for i in range(0, 5)]
        self.counter = 0

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

        self.initUI()

    def initUI(self):
        self.hide()
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.sleep_icon)
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(self.onclose)
        tray_menu = QMenu()
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.load=0

        self.move(180, 100)
        self.setFixedSize(320, 1)
        self.setWindowTitle('run cat')

        self.status = 'working'

    def recurring_timer(self):
        self.load = (int(psutil.cpu_percent())+self.load)/2
        if self.load < 10:
            tmpicon = self.sleep_icon
        else:
            tmpicon = self.run_icons[self.counter]
            self.counter+=1
            if self.counter > 4:
                self.counter = 0
        # print(self.load)
        self.tray_icon.setIcon(tmpicon)

    def onclose(self):
        self.status = 'onclose' if quit else ''
        qApp.quit()

    def closeEvent(self, evnt):
        if self.status == 'onclose':
            super(Program, self).closeEvent(evnt)
        else:
            evnt.ignore()
            self.hide()


def isThereAnyOtherCopies():
    import subprocess

    cmd = 'WMIC PROCESS get Caption'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    final = []
    for line in proc.stdout:
        pre = line.decode().rstrip('\n')[:-2].rstrip()
        if pre:
            final.append(pre)
    print(final.count('main.exe'))
    print(final)
    return final.count(__name__.strip('_') + '.exe') > 3


# if isThereAnyOtherCopies():
#     sys.exit(0)

app = QApplication(sys.argv)
form = Program()
form.show()
sys.exit(app.exec())
