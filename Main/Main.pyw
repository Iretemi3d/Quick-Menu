import sys,os
from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtWidgets import QApplication, QWidget,QGridLayout
from qframelesswindow import FramelessWindow
from qfluentwidgets import (setTheme, Theme, PrimaryPushButton, LineEdit, setThemeColor)
from qfluentwidgets import FluentIcon as FIF
import keyboard
import threading
import subprocess
import webbrowser


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
        self.setStyleSheet("Window { background-color: rgba(40, 40, 40, 0.85); border: 2px solid red; border-radius: 9px;}")
        #functs
        global user
        user = os.environ['USERNAME']
        

        def soundset():
            os.system("start ms-settings:apps-volume")

        global codeset
        def codeset():
            
            try:
                vspath = fr"C:\Users\{user}\AppData\Local\Programs\Microsoft VS Code\Code.exe"
                gitpath = fr"C:\Users\{user}\AppData\Local\GitHubDesktop\GitHubDesktop.exe"

                subprocess.Popen([gitpath], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.Popen([vspath], creationflags=subprocess.CREATE_NO_WINDOW)

            except Exception as e:
                with open("log.txt","w") as f:
                    f.writelines("Error occured: " + str(e))


        def sigint():
            try:
                binNin = fr"C:\Users\{user}\AppData\Local\Programs\Vector35\BinaryNinja\binaryninja.exe"
                webbrowser.open('https://pwn.college')
                webbrowser.open('https://x64.syscall.sh')
                webbrowser.open('https://pwnable.sigint.mx/challenges')

                subprocess.Popen([binNin], creationflags=subprocess.CREATE_NO_WINDOW)

            except Exception as e:
                with open("log.txt","w") as f:
                    f.writelines("Error occured: " + str(e))






                

        self.transparentPushButton1 = PrimaryPushButton('Sound settings', self)
        self.transparentPushButton1.setMinimumHeight(40)
        self.transparentPushButton1.clicked.connect(soundset)

        self.transparentPushButton2 = PrimaryPushButton('Code Start', self)
        self.transparentPushButton2.setMinimumHeight(40)
        self.transparentPushButton2.clicked.connect(codeset)
        
        self.transparentPushButton3 = PrimaryPushButton('SIGINT', self)
        self.transparentPushButton3.setMinimumHeight(40)
        self.transparentPushButton3.clicked.connect(sigint)



        self.txtLine = LineEdit(self)
        self.txtLine.setClearButtonEnabled(True)
        self.txtLine.setMinimumHeight(35)
        self.txtLine.returnPressed.connect(self.readtxt)
        
        
       
        qss = """
            PrimaryPushButton {
                border: 2px solid black;
                border-radius: 4px;
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
            }
            PrimaryPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
                border-color: #ff5555;
            }
            PrimaryPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
                border-color: #ff3333;
            }
        """

        qsstxtline = """
            LineEdit {
                border: 2px solid black;
                border-radius: 4px;
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                }
                """
        
#style sheet
        self.transparentPushButton1.setStyleSheet(qss)
        self.transparentPushButton2.setStyleSheet(qss)
        self.transparentPushButton3.setStyleSheet(qss)
        self.txtLine.setStyleSheet(qsstxtline)





        self.gridLayout = QGridLayout(self)
        self.gridLayout.addWidget(self.transparentPushButton1,0 , 1)
        self.gridLayout.addWidget(self.transparentPushButton2,1 , 1)
        self.gridLayout.addWidget(self.transparentPushButton3,2 , 1)
        self.gridLayout.addWidget(self.txtLine,4,1)



        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)


    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key.Key_S:
            os.system("start ms-settings:apps-volume")
        elif key == Qt.Key.Key_C:
            codeset()
        elif key == Qt.Key.Key_Backspace:
            QApplication.instance().quit()
        


        super().keyPressEvent(event)


    def readtxt(self):
            inp = self.txtLine.text()
            if inp[0:3] == "cmd:":
                print("commands")
            else:
                url = "http://www.google.com/search?q="
                search = url+inp.replace(" ","+")
                webbrowser.open(search)
            
            self.txtLine.clear()

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    setTheme(Theme.DARK)
    setThemeColor('#FF0000')
    w = Window()
    
    w.setWindowFlags(w.windowFlags() | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
    w.show()  
    app.processEvents()
    w.hide()  

    hotkey_signal = HotkeySignal()


    def toggle_window():
        app.processEvents()

        if w.isHidden():
            w.show()
            app.processEvents()

            w.raise_()
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


