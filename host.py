import _thread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
from socket import *

# Global variables
conn = None
host = "127.0.0.1"  # Use localhost for testing
port = 25612  # Ensure this matches the client

# Socket initialization
s = socket(AF_INET, SOCK_STREAM)
try:
    s.bind((host, port))
    s.listen(1)
except OSError as e:
    print(f"Error binding socket: {e}")
    exit(1)

chatOb = None

class Chat(BoxLayout):
    def __init__(self, **kwargs):
        super(Chat, self).__init__(**kwargs)

    def clickAction(self):
        global conn
        textMsg = self.ids['EntryBox'].text

        if textMsg != '':
            self.update_chat_box(f"\nYou: {textMsg}")
            self.ids['EntryBox'].text = ""
            if conn:
                try:
                    conn.sendall(textMsg.encode())
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

def getHostConnected():
    global conn, chatOb
    import time
    time.sleep(1)  # Ensure the UI is ready

    chatOb.update_chat_box("Waiting for Connection")
    try:
        conn, addr = s.accept()
        chatOb.update_chat_box(f"Connected with: {str(addr)}")

        while True:
            try:
                data = conn.recv(1024)
                if data:
                    chatOb.update_chat_box(f"\nOther: {data.decode()}")
                else:
                    chatOb.update_chat_box("Connection closed by peer.")
                    break
            except Exception as e:
                chatOb.update_chat_box(f"\nError receiving message: {e}")
                break
    finally:
        if conn:
            conn.close()
        s.close()

if __name__ == "__main__":
    _thread.start_new_thread(getHostConnected, ())
    ChatAppInterface().run()
