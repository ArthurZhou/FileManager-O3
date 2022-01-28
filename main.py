# !/usr/bin/python
# -*- coding: UTF-8 -*-

"""
 filemanager 2.0
 By Arthur Zhou
"""

# import block
import _thread
import _tkinter
import os
import socket
import sys
import time
import uuid
import tkinter as tk
from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import askopenfilename

# help
# is this the first time you use this system

true = str(os.path.exists('./config.txt'))
if true == 'False':
    # first time
    from setup import setup
    setup()
else:
    pass


def reset():
    print('There are something wrong with your configurations \nNow you can:\n a.re-setup\n b.quit')
    ch = input('I want:')
    if ch == 'a':
        tc = str(os.path.exists('config.txt'))
        if tc == 'True':
            os.remove('config.txt')
        ts = str(os.path.exists('config.txt'))
        if ts == 'True':
            os.remove('sign.')
        from setup import setup
        setup()
    if ch == 'b':
        sys.exit(0)


# setup
print('\nLoading...\nSetting up')
global version
version = 'FileManager O3(Alpha-0.10.0)'
conFig = './config.txt'
# get configurations
try:
    with open(conFig, 'r') as f:
        line = f.readlines()
        # get server ip
        ipaddr = line[0].replace('\n', '')
        port = line[1].replace('\n', '')
    f.close()
except:
    reset()


# def function
def listFile():
    global inCld
    # file list
    # send a message to the server to get file list
    s.send('>getfilelist<'.encode('utf-8'))
    filelist.delete(0, 'end')
    wa.delete(0, 'end')

    # print location
    global w
    w = s.recv(1024).decode('utf-8')
    print(w)
    tk.Label(root, text='Path:', font=('', 15)).grid(row=0, column=0)
    wa.insert('end', w)
    # refresh recv
    time.sleep(0.1)
    # get file list and turn it into list
    inCld = s.recv(1024).decode('utf-8')
    inCld = inCld.replace('[', '').replace(']', '').replace(',', '').replace("'", '')
    inCld = inCld.split()
    # print
    for items in inCld:
        filelist.insert('end', items)


def openF():
    global f
    try:
        opFl = filelist.curselection()
        opFl = str(opFl).replace('(', '').replace(')', '').replace(',', '')
        opFl = filelist.get(opFl)
        if opFl == '':
            pass
        else:
            # send command to server
            s.send('>open<'.encode('utf-8'))
            time.sleep(0.3)
            # send name to server
            s.send(opFl.encode('utf-8'))
            time.sleep(0.1)
            # receive another T-or-F message
            # is 'opFl' a file or a folder?
            fof = s.recv(1024).decode('utf-8')
            if str(fof) == 'file':
                inc = s.recv(1024).decode('utf-8')
                fileWin = tk.Tk()
                fileWin.title(w)
                fileWin.geometry('800x600')
                s1 = Scrollbar(fileWin)
                s1.pack(side=RIGHT, fill=Y)
                s2 = Scrollbar(fileWin, orient=HORIZONTAL)
                s2.pack(side=BOTTOM, fill=X)
                path = tk.Label(fileWin, text='Preview of:' + opFl)
                path.pack()
                look = tk.Text(fileWin)
                look.insert('insert', inc)
                look.pack()
                s1.config(command=look.yview)
                s2.config(command=look.xview)
                fileWin.mainloop()
            if str(fof) == 'fold':
                time.sleep(0.2)
                listFile()
    except _tkinter.TclError:
        pass


def back():
    s.send('>back<'.encode('utf-8'))
    listFile()


def delete():
    deFl = filelist.curselection()
    deFl = str(deFl).replace('(', '').replace(')', '').replace(',', '')
    deFl = filelist.get(deFl)
    s.send('>delt<'.encode('utf-8'))
    time.sleep(0.1)
    s.send(deFl.encode('utf-8'))
    listFile()


def create():
    global way
    cho = input(' a.file \n b.folder:')
    if cho == 'a':
        fled = input('File name:')
        file = open(os.getcwd() + '/' + fled, 'w')
        file.write('New file...')
        file.close()
        print('Success!')
    if cho == 'b':
        fled = input('Folder name:')
        os.mkdir(fled)
        print('Success!')
    main()


def upload():
    global f, backL, true, root
    path = ''

    def selectPath():
        global path
        input.delete(0, 'end')
        path = askopenfilename(parent=root)
        input.insert('end', path)

    def canc():
        wa.grid(row=0, column=1)
        op.grid(row=1, column=2)
        de.grid(row=2, column=2)
        bk.grid(row=3, column=2)
        do.grid(row=4, column=2)
        up.grid(row=1, column=3)
        bt.grid_forget()
        cn.grid_forget()
        tit.grid_forget()
        input.grid_forget()
        check.grid_forget()
        s.send('>œ<'.encode('utf-8'))

    def send():
        upFl = input.get()
        true = str(os.path.exists(upFl))
        if true == 'False':
            s.send('>œ<'.encode('utf-8'))
            tkinter.messagebox.showinfo(version + '-Error',
                                        'No such file or directory!\nPress "OK" to continue...', parent=root)
        if true == 'True':
            dof = os.path.isdir(upFl)
            fod = os.path.isfile(upFl)
            time.sleep(0.2)
            if str(fod == 'True') and str(dof == 'False'):
                try:
                    s.send('file'.encode('utf-8'))
                    nm = os.path.basename(upFl)
                    s.send(nm.encode('utf-8'))
                    root.title('Uploading file...')
                    with open(upFl, 'r') as f:
                        copy = f.read()
                        time.sleep(0.2)
                        s.send(copy.encode('utf-8'))
                        f.close()
                    root.title('Finish!')
                    time.sleep(1)
                    root.title(version)

                except OSError:
                    pass

        '''
            if str(dof == 'True') and str(fod == 'False'):
        
                try:
                    nameD = os.path.basename(upFl)
                    os.mkdir(os.getcwd() + '/' + nameD)
                    for root, dirs, files in os.walk(upFl):
                        for items in range(len(files)):
                            backF = files[items]
                            Dir = root
                            Way = str(Dir + '/' + backF)
        
                            with open(Way, 'rb') as f:
                                copy = f.read().decode('utf-8')
                                file = open(os.getcwd() + '/' + nameD + '/' + backF, 'w')
                                file.write(str(copy))
                                file.close()
                        print('Successful uploaded!')
                except OSError:
                    pass
        '''
        tit.grid_forget()
        input.grid_forget()
        check.grid_forget()
        wa.grid(row=0, column=1)
        op.grid(row=1, column=2)
        de.grid(row=2, column=2)
        bk.grid(row=3, column=2)
        do.grid(row=4, column=2)
        up.grid(row=1, column=3)
        bt.grid_forget()
        cn.grid_forget()
        listFile()

    s.send('>up<'.encode('utf-8'))
    wa.grid_forget()
    op.grid_forget()
    de.grid_forget()
    bk.grid_forget()
    do.grid_forget()
    up.grid_forget()
    time.sleep(0.1)
    tit = tk.Label(root, text='Path:')
    input = tk.Entry(root)
    bt = tk.Button(root, text="select", command=selectPath)
    check = tk.Button(root, text='upload', command=send)
    cn = tk.Button(root, text='cancel', command=canc, width=35)
    tit.grid(row=6, column=0)
    input.grid(row=6, column=1)
    check.grid(row=6, column=2)
    bt.grid(row=6, column=3)
    cn.grid(row=7, column=0, columnspan=4)


def download():
    global s, msg
    s.send('>down<'.encode('utf-8'))
    doFl = filelist.curselection()
    doFl = str(doFl).replace('(', '').replace(')', '').replace(',', '')
    doFl = filelist.get(doFl)
    time.sleep(0.1)
    s.send(doFl.encode('utf-8'))
    fod = s.recv(1024).decode('utf-8')
    if fod == 'file':
        time.sleep(0.1)
        root.title('Downloading file...')
        f = open(doFl, 'w')
        remsg = s.recv(1024)
        root.title('Finish!')
        f.write(remsg.decode('utf-8'))
        f.close()
        time.sleep(1)
        root.title(version)

        '''
        if str(dof == 'True') and str(fod == 'False'):

            try:
                nameD = os.path.basename(fileSource)
                os.mkdir(fileTarget + '/' + nameD)
                for root, dirs, files in os.walk(fileSource):
                    for items in range(len(files)):
                        backF = files[items]
                        Dir = root
                        Way = str(Dir + '/' + backF)

                        with open(Way, 'rb') as f:
                            copy = f.read().decode('utf-8')
                            file = open(fileTarget + '/' + nameD + '/' + backF, 'w')
                            file.write(str(copy))
                            file.close()
                    print('Successful uploaded!')

            except OSError:
                pass
        '''
        listFile()


def stop():
    s.send('>quit<'.encode('utf-8'))
    s.close()
    sys.exit(0)


def starter():

    def tryconn():
        try:
            global s
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ipaddr, int(port)))
        except ConnectionError or TimeoutError or ConnectionRefusedError or ConnectionResetError:
            if ConnectionError:
                cause = 'Bad connection.(Try again later)'
            if TimeoutError:
                cause = 'Connection time out.(May be the server is offline)'
            if ConnectionRefusedError:
                cause = 'Connection refused.(This may caused by your and the server-side`s firewalls.)'
            if ConnectionResetError:
                cause = 'The server reset your connection.' \
                        '(This may caused by bad connections or connecting to a stopped server.)'
            ret = tkinter.messagebox.askretrycancel(version + '-Error',
                                                    'Can`t connect to {0}:{1}!\n{2}'.format(ipaddr, port, cause),
                                                    parent=login)
            print(ret)
            if str(ret) == 'True':
                tryconn()
            else:
                sys.exit(1)

    def check():
        uida = uuid.uuid5(uuid.NAMESPACE_DNS, nm.get() + psw.get())
        s.send(str(uida).encode('utf-8'))
        time.sleep(0.1)
        tf = s.recv(1024).decode('utf-8')
        print(tf)
        if tf == 'True':
            print('Welcome\n')
            # correct password, run main()
            tkinter.messagebox.showinfo(version + '-Message',
                                        'Connected to {0}:{1}. Logged in as {2}\n'
                                        'Press "OK" to continue...'.format(ipaddr, 8080, nm.get()),
                                        parent=login)
            main()
        else:
            # wrong password
            tkinter.messagebox.showwarning(version + '-Warning',
                                           'Wrong username or password.(Try to restart)', parent=login)

    tryconn()
    login = tk.Tk()
    login.title('Login')
    screenwidth = login.winfo_screenwidth()
    screenheight = login.winfo_screenheight()
    size = '%dx%d+%d+%d' % (280, 200, (screenwidth - 280) / 2, (screenheight - 200) / 2)
    login.geometry(size)
    login.resizable(0, 0)  # set window to NO-resizable
    tk.Label(login, text='FileManager Login', font=('', 20)).grid(row=0, column=0, columnspan=2)
    tk.Label(login, text='Username:', font=('', 15)).grid(row=1, column=0)
    nm = tk.Entry(login)
    nm.grid(row=1, column=1)
    tk.Label(login, text='Password:', font=('', 15)).grid(row=2, column=0)
    psw = tk.Entry(login, show='*')
    psw.grid(row=2, column=1)
    tk.Button(login, text='Login', font=('', 15), command=check).grid(row=3, column=0, columnspan=2)
    login.mainloop()


# def main
def main():
    global way, folderP, filelist, root, wa, op, de, bk, do, up
    root = tk.Tk()
    root.title(version)
    root.protocol('WM_DELETE_WINDOW', stop)
    filelist = tk.Listbox(root, width=20, heigh=20, font=('', 15))
    filelist.grid(row=1, column=0, columnspan=2, rowspan=5)
    wa = tk.Entry(root)
    wa.grid(row=0, column=1)
    listFile()
    # function buttons
    op = tk.Button(root, text='open', width=10, heigh=2, font=('', 15), bg='grey',
                   command=openF)
    op.grid(row=1, column=2)
    de = tk.Button(root, text='delete', width=10, heigh=2, font=('', 15), bg='grey',
                   command=delete)
    de.grid(row=2, column=2)
    bk = tk.Button(root, text='back', width=10, heigh=2, font=('', 15), bg='grey',
                   command=back)
    bk.grid(row=3, column=2)
    do = tk.Button(root, text='download', width=10, heigh=2, font=('', 15), bg='grey',
                   command=download)
    do.grid(row=4, column=2)
    up = tk.Button(root, text='upload', width=10, heigh=2, font=('', 15), bg='grey',
                   command=upload)
    up.grid(row=1, column=3)

    # print and choose function block
    '''

        if fInput == "?":
            helP()

        if fInput == "settings":
            print('a.change username and password\nb.change default directory')
            cup = input('Choose function:')
            if cup == 'a':
                chance = 5
                while True:
                    if chance > 0:
                        nm = input('Username:')
                        psw = input('Password:')
                        if str(nm) == str(username) and str(psw) == str(password):
                            from setting import changeUP
                            changeUP()
                        else:
                            print('Wrong username or password\n')
                            chance = chance - 1
                            print('You have ', chance, 'times left.')
                            continue
                    else:
                        sys.exit(0)

            if cup == 'b':
                from setting import changeDir
                changeDir()
        '''
    root.mainloop()


# start
if __name__ == '__main__':
    # try:
    starter()
    _thread.start_new_thread(main, ())
# except:
# show a message if server closed
# if BrokenPipeError:
# print('Disconnect from the server...')
# pass
