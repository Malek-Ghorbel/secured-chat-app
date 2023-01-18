import hashlib
import socket
import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

from client import Client


def login_page():
    signup_window.destroy()
    import login


def connect_database():
    if usernameEntry.get() == '' or passwordEntry.get() == '' or confirmpasswordEntry.get() == '':
        messagebox.showerror('Error', 'All Fields Are Required')
    elif passwordEntry.get() != confirmpasswordEntry.get():
        messagebox.showerror('Error', 'Password Mismatch')
    else:
        try:
            conn = sqlite3.connect("userdata.db")
            mycursor = conn.cursor()
        except:
            messagebox.showerror(
                'Error', 'Database connectivity issue , Please try again')
            return
        password = hashlib.sha256(
            passwordEntry.get().encode()).hexdigest()
        username = usernameEntry.get()
        userExist = mycursor.execute(
            "SELECT * FROM userdata WHERE username=?", (username,)).fetchall()
        if userExist:
            messagebox.showerror(
                'Error', 'User already exist')
            return
        else:
            mycursor.execute("INSERT INTO userdata (username,password) VALUES(?,?)",
                             (usernameEntry.get(), password))
        conn.commit()
        conn.close()
        messagebox.showinfo('Success', 'Registration successful')
        client = Client(socket.gethostbyname(
            socket.gethostname()), 9090, usernameEntry.get())
        signup_window.destroy()


def hide1():
    openeye1.config(file='./img/closeye.png')
    passwordEntry.config(show='*')
    eyeButton1.config(command=show1)


def show1():
    openeye1.config(file='./img/openeye.png')
    passwordEntry.config(show='')
    eyeButton1.config(command=hide1)


def hide2():
    openeye2.config(file='./img/closeye.png')
    confirmpasswordEntry.config(show='*')
    eyeButton2.config(command=show2)


def show2():
    openeye2.config(file='./img/openeye.png')
    confirmpasswordEntry.config(show='')
    eyeButton2.config(command=hide2)


signup_window = Tk()
signup_window.title('Signup Page')
signup_window.resizable(False, False)

background = ImageTk.PhotoImage(file='./img/bg.jpg')

bgLabel = Label(signup_window, image=background)
bgLabel.grid()

frame = Frame(signup_window, bg='white')
frame.place(x=554, y=100)


heading = Label(frame, text='CREATE AN ACCOUNT', font=(
    'Microsoft Yahei UI Light', 18, 'bold'), bg='white', fg='#000064')
heading.grid(row=0, column=0, padx=10, pady=10)

openeye1 = PhotoImage(file='./img/closeye.png')
eyeButton1 = Button(signup_window, image=openeye1, bd=0,
                    bg='white', activebackground='white', cursor="hand2", command=show1)
eyeButton1.place(x=760, y=250)

openeye2 = PhotoImage(file='./img/closeye.png')
eyeButton2 = Button(signup_window, image=openeye2, bd=0,
                    bg='white', activebackground='white', cursor="hand2", command=show2)
eyeButton2.place(x=760, y=308)

usernameLabel = Label(frame, text='Username', font=(
    'Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='#000064')
usernameLabel.grid(row=1, column=0, sticky='w', padx=25,)

usernameEntry = Entry(frame, width=25, font=(
    'Microsoft Yahei UI Light', 10, 'bold'), fg='white', bg='#000064')
usernameEntry.grid(row=2, column=0, sticky='w', padx=25, pady=(10, 0))

passwordLabel = Label(frame, text='Password', font=(
    'Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='#000064')
passwordLabel.grid(row=3, column=0, sticky='w', padx=25, pady=(10, 0))

passwordEntry = Entry(frame, width=25, show="*", font=(
    'Microsoft Yahei UI Light', 10, 'bold'), fg='white', bg='#000064')
passwordEntry.grid(row=4, column=0, sticky='w', padx=25)

confirmpasswordLabel = Label(frame, text='Confirmpassword', font=(
    'Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='#000064')
confirmpasswordLabel.grid(row=5, column=0, sticky='w', padx=25, pady=(10, 0))

confirmpasswordEntry = Entry(frame, width=25, show="*", font=(
    'Microsoft Yahei UI Light', 10, 'bold'), fg='white', bg='#000064')
confirmpasswordEntry.grid(row=6, column=0, sticky='w', padx=25)

signupButton = Button(frame, text='Signup', font=(
    'Open Sans', 16, 'bold'), bd=0, bg='#000064', fg='white', activebackground='#000064', activeforeground='white', width=17, command=connect_database)
signupButton.grid(row=10, column=0, pady=50)

alreadyaccount = Label(frame, text='Already have an account :', font=(
    'Open Sans', '9', 'bold'), bg='white', fg='#000064')
alreadyaccount.grid(row=11, column=0, sticky='w', padx=25, pady=10)

loginButton = Button(frame, text='Log in', font=(
    'Open Sans', '9', 'bold underline'), bd=0, cursor='hand2', bg='white', fg='blue',
    activebackground='white', activeforeground='blue', command=login_page)
loginButton.place(x=173, y=378)


signup_window.mainloop()
