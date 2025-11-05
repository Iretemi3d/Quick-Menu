import sys,os
from PySide6.QtCore import Qt, QUrl, QTimer, QObject, Signal
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QWidget,QGridLayout
from qframelesswindow import FramelessWindow, StandardTitleBar
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition, FluentBackgroundTheme, FluentTranslator, TransparentPushButton)
from qfluentwidgets import FluentIcon as FIF
import keyboard
import threading


class HotkeySignal(QObject):
    toggle_requested = Signal()

class Window(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        empty_title_bar = QWidget(self)
        empty_title_bar.setFixedHeight(0)
        self.setTitleBar(empty_title_bar)
        
        self.resize(800, 400)

        self.setWindowTitle('Quick')

        screen = QApplication.primaryScreen().availableGeometry()
        w, h = screen.width(), screen.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        qss_path = "Main\demo.qss"
        with open(qss_path, encoding='utf-8') as f:
            self.setStyleSheet(f.read())

        #functs
        def soundset():
            os.system("start ms-settings:apps-volume")


        self.transparentPushButton1 = TransparentPushButton('Sound settings', self)
        self.transparentPushButton1.setMinimumHeight(20)
        self.transparentPushButton1.clicked.connect(soundset)




        self.gridLayout = QGridLayout(self)
        self.gridLayout.addWidget(self.transparentPushButton1,0 , 1)





        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key.Key_S:
            os.system("start ms-settings:apps-volume")
            
            

        # elif blah blah blah

        super().keyPressEvent(event)



            

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    setTheme(Theme.DARK)
    w = Window()
    
    w.setWindowFlags(w.windowFlags() | Qt.WindowType.Tool)
    w.show()  
    app.processEvents()
    w.hide()  

    hotkey_signal = HotkeySignal()


    def toggle_window():
        app.processEvents()

        if w.isHidden():
            w.show()
            app.processEvents()
            
            if w.windowState() & Qt.WindowState.WindowMinimized:
                w.setWindowState(Qt.WindowState.WindowNoState)
                app.processEvents()
            w.raise_()
            app.processEvents()
            
            w.activateWindow() 
            app.processEvents()

            w.setFocus()
            app.processEvents()
            
            w.raise_()
            app.processEvents()

          
        else:
            w.hide()
    

    hotkey_signal.toggle_requested.connect(toggle_window)

    def hotkey_listener():
        def hotkey_callback():
            hotkey_signal.toggle_requested.emit()
        
        keyboard.add_hotkey('shift+esc', hotkey_callback)
        keyboard.wait() 

        
            
    threading.Thread(target=hotkey_listener, daemon=True).start()
    app.exec()

    
    