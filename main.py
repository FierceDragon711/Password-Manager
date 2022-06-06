from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for char in range(nr_letters)]
    password_symbols = [random.choice(symbols) for char in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for char in range(nr_numbers)]
    password_list = password_numbers + password_letters + password_symbols
    random.shuffle(password_list)

    password = "".join(password_list)

    entry_password.delete(0, END)
    entry_password.insert(0,password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = entry_website.get()
    email = entry_username.get()
    password = entry_password.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Empty Field Detected", message="Please Fil All Fields")
    else:
        try:
            with open("Saved Passwords.json", mode="r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("Saved Passwords.json", mode="w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("Saved Passwords.json", mode="w") as file:
                json.dump(data, file, indent=4)
        finally:
            messagebox.showinfo(title=entry_website.get(), message="Password Saved")
            entry_website.delete(0, END)
            entry_password.delete(0, END)


# ---------------------------- Find Password ------------------------------- #


def find_password():
    website = entry_website.get()
    try:
        with open("Saved Passwords.json", mode="r") as file:
            content = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Missing File", message="No Data File Found")
    else:
        if website in content:
            email = content[website]["email"]
            password = content[website]["password"]
            messagebox.showinfo(title="Password in file", message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Generator")
window.config(padx=50, pady=50, bg="white")

canvas = Canvas(width=200, height=200, highlightthickness=0, bg="white")
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)

label_website = Label(text="Website:", font=("Helvetica", 12, "normal"), bg="white")
label_username = Label(text="Email/Username:", font=("Helvetica", 12, "normal"), bg="white")
label_password = Label(text="Password", font=("Helvetica", 12, "normal"), bg="white")

entry_website = Entry(width=35)
entry_username = Entry(width=35)
entry_password = Entry(width=35)

button_generate = Button(text="Generate Password", width=14, command=generate_password)
button_add = Button(text="Add", width=30, highlightthickness=0, command=save)
button_search = Button(text="Search", width=14, command=find_password)

canvas.grid(row=0, column=1)
label_website.grid(row=1, column=0)
button_search.grid(row=1, column =2)
label_username.grid(row=2, column=0)
label_password.grid(row=3, column=0)
entry_website.grid(row=1, column=1)
entry_website.focus()
entry_username.grid(row=2, column=1)
entry_username.insert(0, "email@email.com")
entry_password.grid(row=3, column=1)
button_generate.grid(row=3, column=2)
button_add.grid(row=4, column=1)

window.mainloop()
