import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog


HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090
FORMAT = 'utf-8'
active_users = []


class Client:

    def __init__(self, host, port, username):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = username
        
        self.gui_done = False
        self.running = True
        
        gui_thred = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        
        gui_thred.start()
        receive_thread.start()
        
    def on_closing(self, event=None):
        self.sock.send("[exit]".encode(FORMAT))
        self.sock.close()
        self.win.quit()
        
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title("Chat Client")
        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.win.configure(bg="lightgray")
        
        #connected users:
        
        self.users_frame = tkinter.Frame(self.win)
        self.users_frame.configure(bg="lightgray")
        self.users_frame.pack()
        
        self.users_label = tkinter.Label(self.users_frame, text="Connected Users", bg="lightgrey")
        self.users_label.config(font=("Arial", 12))
        self.users_label.pack(padx= 20, pady= 5)
        
        self.users_listbox = tkinter.Listbox(self.users_frame, height=8)
        self.users_listbox.pack(padx= 20, pady= 5)
        
        #chatbox
        self.chat_label = tkinter.Label(self.win, text="Chat", bg="lightgrey")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx= 20, pady= 5)
        
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled", height=14)
        
        #message input
        self.msg_label = tkinter.Label(self.win, text="Message", bg="lightgrey")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx= 20, pady= 5)
        
        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx= 20, pady= 5)
        
        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx= 20, pady= 5)
        
        self.gui_done = True
        
        self.win.mainloop()
        self.win.protocol("wM_DELETE_WINDOW", self.stop)

    def update_active_users(self):
        if self.gui_done:
            self.users_listbox.config(state='normal')
            self.users_listbox.delete(0, tkinter.END)
            for user in self.active_users:
                if user != self.nickname :
                    self.users_listbox.insert(tkinter.END, user) 
        
    def write(self):
        message = f"{self.input_area.get('1.0', 'end')}"
        
        self.text_area.config(state='normal')
        self.text_area.insert('end', f"you : {message}")
        self.text_area.yview('end')
        self.text_area.config(state='disabled')
        
        self.sock.send(f"{self.nickname} :{message}".encode(FORMAT))
        self.input_area.delete('1.0', 'end')
    
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)
        
    
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode(FORMAT)
                if message == 'NICK':
                    self.sock.send(self.nickname.encode(FORMAT))
                elif message.startswith("[Active Users] "):
                    self.active_users = message.split(" ")[2:]
                    self.update_active_users()
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')     
            except ConnectionAbortedError:
                break
            except Exception as e:
                print(e)
                #self.sock.close()
                break
            

