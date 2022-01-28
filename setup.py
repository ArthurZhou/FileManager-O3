import os, sys


def setup():
    import socket, uuid
    import tkinter as tk
    import tkinter.messagebox
    global gip, gpt, f

    def sip():
        try:
            global ts
            ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ts.connect((gip.get(), int(gpt.get())))
            f.write(gip.get() + '\n' + gpt.get())
            ts.send('>setup<'.encode('utf-8'))
            tkinter.messagebox.showinfo('Message', 'Success!')
            f.close()
            askip.pack_forget()
            gip.pack_forget()
            askpt.pack_forget()
            gpt.pack_forget()
            con.pack_forget()
            usrt.pack()
            usr2.pack()
            pswt.pack()
            psw2.pack()
            con2.pack()
        except:
            ret = tkinter.messagebox.askretrycancel('Warning', 'Can`t connect to this server!\n', parent=swin)
            print(ret)
            if str(ret) == 'True':
                sip()
            else:
                pass

    def wriUP():
        askyn = tkinter.messagebox.askokcancel('Yes or no',
                                               'username:{0}\npassword:{1}\nYou can never change it after you click '
                                               '"OK".'.format(usr2.get(), psw2.get()), parent=swin)
        if str(askyn) == 'True':
            ts.send(str(uuid.uuid5(uuid.NAMESPACE_DNS, usr2.get() + psw2.get())).encode('utf-8'))
            back = ts.recv(1024).decode('utf-8')
            if back == 'ready!':
                tkinter.messagebox.showinfo('Message', 'Your account is ready!Restart FileManager to use it!', parent=swin)
                sys.exit(0)
            elif back == 'ex!':
                tkinter.messagebox.showerror('Error', 'Your account is already used!', parent=swin)
        else:
            pass

    conFig = './config.txt'
    f = open(conFig, 'w')

    os.mkdir('file')

    swin = tk.Tk()
    swin.title('FileManager-Start')
    swin.geometry('500x500')

    usrt = tk.Label(swin, text='Set your username', font=('Arial', 20), width=25, height=2)
    pswt = tk.Label(swin, text='Set your password', font=('Arial', 20), width=25, height=2)
    con2 = tk.Button(swin, text='OK', font=('Arial', 20), bg='grey', width=25, height=2, command=wriUP)
    usr2 = tk.Entry(swin)
    psw2 = tk.Entry(swin)

    askip = tk.Label(swin, text='Set server ip', font=('Arial', 20), width=25, height=2)
    gip = tk.Entry(swin)
    askpt = tk.Label(swin, text='Set server port', font=('Arial', 20), width=25, height=2)
    gpt = tk.Entry(swin)
    con = tk.Button(swin, text='OK', font=('Arial', 20), bg='grey', width=25, height=2, command=sip)
    askip.pack()
    gip.pack()
    askpt.pack()
    gpt.pack()
    con.pack()
    swin.mainloop()
