from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk

import encrypter as enc

class Client:
    def __init__(self):
        self.encoder = enc.Encrypter()

        self.command_list = ["clear", "help", "setkey"]

        self.key = [0,0,0,0,0]
        self.keyList = self.key

        self.host = 0
        self.port = 0

        # TKinter GUI

        self.window = tk.Tk()
        self.window.title("Ligma Chatter")

        #self.window.geometry()
        #self.window.propagate(0)

        self.setup_window = tk.Toplevel()
        self.setup_window.title("Setup")

        self.ip_var = tk.StringVar()
        self.ip_var.set("0.0.0.0")

        self.port_var = tk.StringVar()

        self.ip_entry = tk.Entry(self.setup_window, textvariable=self.ip_var)
        self.ip_entry.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S)

        self.host_entry = tk.Entry(self.setup_window, textvariable=self.port_var)
        self.host_entry.grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S)

        self.ip_label = tk.Label(self.setup_window, text="Host")
        self.ip_label.grid(row=0, column=0, sticky=tk.W)

        self.port_label = tk.Label(self.setup_window, text="Port")
        self.port_label.grid(row=1, column=0, sticky=tk.W)

        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(self.setup_window, textvariable=self.name_var)
        self.name_entry.grid(row=2, column=1, sticky=tk.W+tk.E+tk.N+tk.S)

        self.name_label = tk.Label(self.setup_window, text="Name" )
        self.name_label.grid(row=2, column=0, sticky=tk.W)

        self.connect_button = tk.Button(self.setup_window, text="Connect", command=self.connect)
        self.connect_button.grid(row=3, columnspan=2)

        self.msg_frame = tk.Frame(self.window)

        self.tk_msg = tk.StringVar()
        self.tk_msg.set("Type your messages here.")

        self.key_var = tk.StringVar()
        self.scrollbar = tk.Scrollbar(self.msg_frame)

        self.msg_list = tk.Listbox(self.msg_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)

        self.scrollbar.grid(row=0, column=0)
        self.msg_list.grid(row=0, column=0)
        self.msg_frame.grid(row=0, columnspan=3)

        self.entry_field = tk.Entry(self.window, textvariable=self.tk_msg)
        self.entry_field.bind("<Return>", self.sendMsg)
        self.entry_field.grid(row=1, column=1)

        self.send_button = tk.Button(self.window, text="Send", command=self.sendMsg)
        self.send_button.grid(row=1, column=2)

        self.key_entry = tk.Entry(self.window, textvariable=self.key_var, width=10)
        self.key_entry.grid(row=1, column=0)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)


    def recieveMsg(self):
        while True:
            try:
                name = ""
                prefix = ""
                msgDecode = ""
                self.keySet(self.key_var.get())

                msg = self.client_socket.recv(1024).decode("utf8")
                isMsg = False
                for letter in msg:
                    if letter != ":" and not isMsg:
                        name += letter
                    elif letter == ":" and not isMsg:
                        prefix = ":"
                        isMsg = True
                    elif isMsg:
                        msgDecode += letter
                print("name: %s, prefix: %s, msgtodecode: %s" %(name, prefix, msgDecode))
                if prefix != ":":
                    self.msg_list.insert(tk.END, msg, )
                else:
                    self.msg_list.insert(tk.END, name+prefix+ " " + self.encoder.msgDecode(self.key, msgDecode))
            except OSError:
                break

    def check_commands(self, msg):
        pass
        """prefix1 = ""
        prefix2 = ""
        command = ""
        for letter in msg:
            if (prefix1 == "" and prefix2 == "") and (letter == "-"):
                prefix1 = "-"
            elif (prefix1 == "-" and prefix2 == "") and (letter == "-"):
                prefix2 = "-"
            elif (prefix1 == "-" and prefix2 == "-") and (letter != "-"):
                command += letter
        
        if command in self.command_list:
            if command == "help":
                self.client_socket()"""


    def keySet(self, keyString):
        i = 0
        for char in keyString:
            self.key[i] = int(char)
            i += 1
        self.keylist = self.key

    def sendMsg(self, event=None):
        msg = self.tk_msg.get()
        self.tk_msg.set("")
        self.keySet(self.key_var.get())
        #self.msg_list.insert(tk.END, self.encoder.msgEncode(self.key, msg))

        self.client_socket.send(bytes(self.encoder.msgEncode(self.key, msg), "utf8"))
        if msg == "{quit}":
            self.client_socket.close()
            self.window.quit()

        print("encoded message: " + self.encoder.msgEncode(self.key, msg))
    
    def connect(self):
        self.setup_window.destroy()

        addr = (str(self.ip_var.get()), int(self.port_var.get()))

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(addr)

        self.client_socket.send(bytes(self.name_var.get(), "utf8"))
        print(self.name_var.get())

        recieve_thread = Thread(target=self.recieveMsg)
        recieve_thread.start()

    def on_closing(self, event=None):
        self.tk_msg.set("{quit}")
        self.sendMsg()
    

client = Client()
tk.mainloop()



    