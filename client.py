import _thread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
from socket import *

# Global variables
s = socket(AF_INET, SOCK_STREAM)
host = "127.0.0.1"  # Should match the server's IP
port = 25612  # Ensure this matches the server

chatOb = None

class Chat(BoxLayout):
    def __init__(self, **kwargs):
        super(Chat, self).__init__(**kwargs)

    def clickAction(self):
        global s
        textMsg = self.ids['EntryBox'].text

        if textMsg != '':
            self.update_chat_box(f"\nYou: {textMsg}")
            self.ids['EntryBox'].text = ""
            try:
                s.sendall(textMsg.encode())
            except Exception as e:
                self.update_chat_box(f"\nError sending message: {e}")

    def update_chat_box(self, message):
        def update(dt):
            self.ids['ChatBox'].text += message
        Clock.schedule_once(update)

class ChatAppInterface(App):
    def build(self):
        global chatOb
        chatOb = Chat()
        Window.size = (400, 500)
        return chatOb

def getClientConnected():
    global chatOb
    import time
    time.sleep(1)  # Ensure the UI is ready

    try:
        s.connect((host, port))
        chatOb.update_chat_box("Successfully connected")
    except Exception as e:
        chatOb.update_chat_box(f"Unable to connect: {e}")
        return

    while True:
        try:
            data = s.recv(1024)
            if data:
                chatOb.update_chat_box(f"\nOther: {data.decode()}")
            else:
                chatOb.update_chat_box("Connection closed by peer.")
                break
        except Exception as e:
            chatOb.update_chat_box(f"\nError receiving message: {e}")
            break

    s.close()

if __name__ == "__main__":
    _thread.start_new_thread(getClientConnected, ())
    ChatAppInterface().run()
