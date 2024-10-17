import sqlite3
from tkinter import *
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
import tkinter.ttk as ttk
import os

# Designing window for registration
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")
    
    global username
    global password
    global username_entry
    global password_entry
    
    username = StringVar()
    password = StringVar()
    
    Label(register_screen, text="Please enter details below", bg="blue").pack()
    Label(register_screen, text="").pack()
    
    Label(register_screen, text="Username * ").pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    
    Label(register_screen, text="Password * ").pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command=register_user).pack()

# Designing window for login
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    
    global username_verify
    global password_verify
    global username_login_entry
    global password_login_entry
    
    username_verify = StringVar()
    password_verify = StringVar()
    
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()
    
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    
    Label(login_screen, text="").pack()
    
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command=login_verify).pack()

# Implementing event on register button
def register_user():
    username_info = username.get()
    password_info = password.get()
    
    with open(username_info, "w") as file:
        file.write(username_info + "\n")
        file.write(password_info)
    
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()

# Implementing event on login button
def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    
    list_of_files = os.listdir()
    
    if username1 in list_of_files:
        with open(username1, "r") as file:
            verify = file.read().splitlines()
        
        if password1 in verify:
            login_success()
        else:
            password_not_recognised()
    else:
        user_not_found()

# Designing popup for login success
def login_success():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()

# Designing popup for login invalid password
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Error")
    password_not_recog_screen.geometry("150x100")
    
    Label(password_not_recog_screen, text="Invalid Password").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()

# Designing popup for user not found
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Error")
    user_not_found_screen.geometry("150x100")
    
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

# Deleting popups
def delete_login_success():
    login_success_screen.destroy()

def delete_password_not_recognised():
    password_not_recog_screen.destroy()

def delete_user_not_found_screen():
    user_not_found_screen.destroy()

# Designing Main (first) window
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    
    Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    
    Button(text="Login", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()
    
    main_screen.mainloop()

# Connecting to Database
connector = sqlite3.connect('library.db')
cursor = connector.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Library (BK_NAME TEXT, BK_ID TEXT PRIMARY KEY NOT NULL, AUTHOR_NAME TEXT, BK_STATUS TEXT, CARD_ID TEXT)')

def issuer_card():
    cid = sd.askstring('Issuer Card ID', 'What is the Issuer’s Card ID?')
    if not cid:
        mb.showerror('Issuer ID cannot be zero!', 'Can’t keep Issuer ID empty, it must have a value')
    else:
        return cid

def display_records():
    global tree
    tree.delete(*tree.get_children())
    curr = connector.execute('SELECT * FROM Library')
    data = curr.fetchall()
    for record in data:
        tree.insert('', END, values=record)

def clear_fields():
    global bk_status, bk_id, bk_name, author_name, card_id
    bk_status.set('Available')
    for i in ['bk_id', 'bk_name', 'author_name', 'card_id']:
        exec(f"{i}.set('')")
    bk_id_entry.config(state='normal')
    try:
        tree.selection_remove(tree.selection()[0])
    except:
        pass

def clear_and_display():
    clear_fields()
    display_records()

def view_record():
    global bk_name, bk_id, bk_status, author_name, card_id
    if not tree.focus():
        mb.showerror('Select a row!', 'To view a record, you must select it in the table. Please do so before continuing.')
        return
    current_item_selected = tree.focus()
    values_in_selected_item = tree.item(current_item_selected)
    selection = values_in_selected_item['values']
    bk_name.set(selection[0])
    bk_id.set(selection[1])
    bk_status.set(selection[3])
    author_name.set(selection[2])

def add_record():
    global connector
    global bk_name, bk_id, author_name, bk_status
    if bk_status.get() == 'Issued':
        card_id.set(issuer_card())
    else:
        card_id.set('N/A')
    surety = mb.askyesno('Are you sure?', 'Are you sure this is the data you want to enter?\nPlease note that Book ID cannot be changed in the future')
    if surety:
        try:
            connector.execute('INSERT INTO Library (BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID) VALUES (?, ?, ?, ?, ?)',
                               (bk_name.get(), bk_id.get(), author_name.get(), bk_status.get(), card_id.get()))
            connector.commit()
            clear_and_display()
            mb.showinfo('Record added', 'The new record was successfully added to your database')
        except sqlite3.IntegrityError:
            mb.showerror('Book ID already in use!', 'The Book ID you are trying to enter is already in the Database, please alter that book’s record or check any discrepancies on your side')

def update_record():
    def update():
        global bk_status, bk_name, bk_id, author_name, card_id
        if bk_status.get() == 'Issued':
            card_id.set(issuer_card())
        else:
            card_id.set('N/A')
        cursor.execute('UPDATE Library SET BK_NAME=?, BK_STATUS=?, AUTHOR_NAME=?, CARD_ID=? WHERE BK_ID=?',
                       (bk_name.get(), bk_status.get(), author_name.get(), card_id.get(), bk_id.get()))
        connector.commit()
        clear_and_display()
        edit.destroy()
        bk_id_entry.config(state='normal')
        clear.config(state='normal')
        view_record()
        bk_id_entry.config(state='disable')
        clear.config(state='disable')
    
    edit = Button(left_frame, text='Update Record', font=btn_font, bg=btn_hlb_bg, width=20, command=update)
    edit.place(x=50, y=375)

def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
        return
    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]
    cursor.execute('DELETE FROM Library WHERE BK_ID=?', (selection[1],))
    connector.commit()
    tree.delete(current_item)
    mb.showinfo('Done', 'The record you wanted to delete has been removed.')

# Call the main screen function to start the application
main_account_screen()
