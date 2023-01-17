import hashlib
import socket
import sqlite3
from tkinter import *
from PIL import ImageTk
from tkinter import messagebox

from client import Client

# Functionality Part


def connect_database():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'All Fields Are Required')
    else:
        try:
            conn = sqlite3.connect("userdata.db")
            mycursor = conn.cursor()
        except:
            messagebox.showerror(
                'Error', 'Database connectivity issue , Please try again')
            return
        password2 = hashlib.sha256(
            passwordEntry.get().encode()).hexdigest()
        query = 'select * from userdata where username=? and password=?'
        mycursor.execute(query, (usernameEntry.get(), password2))
        row = mycursor.fetchone()
        if row == None:
            messagebox.showerror('Error', 'Invalid username or password')
        else:
            messagebox.showinfo('Success', 'Login is successful !')
            client = Client(socket.gethostbyname(
                socket.gethostname()), 9090, usernameEntry.get())
            login_window.destroy()


def username_enter(event):
    if usernameEntry.get() == 'UserName':
        usernameEntry.delete(0, END)


def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)


def hide():
    openeye.config(file='./img/closeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)


def show():
    openeye.config(file='./img/openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)


def signup_page():
    login_window.destroy()
    import signup


# GUI Part
login_window = Tk()
login_window.geometry('990x660+50+50')
login_window.resizable(0, 0)
login_window.title('Login Page')
bgImage = ImageTk.PhotoImage(file='./img/bg.jpg')

bgLabel = Label(login_window, image=bgImage)
bgLabel.place(x=0, y=0)

heading = Label(login_window, text='USER LOGIN', font=(
    'Microsoft Yahei UI Light', 23, 'bold'), bg='white', fg='#000064')
heading.place(x=605, y=120)

usernameLabel = Label(text='Username', font=(
    'Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='#000064')
usernameLabel.place(x=580, y=180)
usernameEntry = Entry(login_window, width=25, font=(
    'Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='#000064')
usernameEntry.place(x=580, y=200)
usernameEntry.bind('<FocusIn>', username_enter)

frame1 = Frame(login_window, width=250, height=2, bg='#000064')
frame1.place(x=580, y=222)

passwordLabel = Label(text='Password', font=(
    'Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='#000064')
passwordLabel.place(x=580, y=230)

passwordEntry = Entry(login_window, width=25, show="*", font=(
    'Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='#000064')
passwordEntry.place(x=580, y=260)
passwordEntry.bind('<FocusIn>', password_enter)

frame2 = Frame(login_window, width=250, height=2, bg='#000064')
frame2.place(x=580, y=282)
openeye = PhotoImage(file='./img/closeye.png')
eyeButton = Button(login_window, image=openeye, bd=0,
                   bg='white', activebackground='white', cursor="hand2", command=show)
eyeButton.place(x=800, y=254)

loginButton = Button(login_window, text='Login', font=(
    'Open Sans', 16, 'bold'), fg='white', bg='#000064', activeforeground='#000064', activebackground='#000064', cursor='hand2', bd=0, width=19, command=connect_database)
loginButton.place(x=578, y=350)

signupLabel = Label(login_window, text='Dont have an account ? ', font=(
    'Open Sans', 9, 'bold'), fg='#000064', bg='white')
signupLabel.place(x=590, y=500)

newaccountButton = Button(login_window, text='Create new account', font=(
    'Open Sans', 9, 'bold underline'), fg='blue', bg='white', activeforeground='blue', activebackground='white', cursor='hand2', bd=0, command=signup_page)
newaccountButton.place(x=727, y=500)

login_window.mainloop()
