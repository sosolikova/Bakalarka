import tkinter
from tkinter import ttk
from tkinter import messagebox

def enter_data():
    accepted = accept_var.get()

    if accepted=="Accepted":
      # user info
      firstname = fist_name_entry.get()
      lastname = last_name_label.get()
      if firstname and lastname:
        title =title_combobox.get()
        age = age_spinbox.get()
        nationality = nationality_combobox.get()

        # course info
        registration_status = reg_status_var.get()
        numcourses = numcourses_spinbox.get()
        numsemesters = numcourses_spinbox.get()


        print("First name: ", firstname, "Last name: ", lastname)
        print("Title: ", title, "Age: ", age, "Nationality: ", nationality)
        print("# Courses: ", numcourses, "# Semesters: ", numsemesters)
        print("Registration status", registration_status)
        print("----------------------------------------------------------")
      else:
         tkinter.messagebox.showwarning(title="Error", message="Fist and Last name are required")
    else:
        tkinter.messagebox.showwarning(title= "Error", message="You have not accepted terms")
        



window = tkinter.Tk()
window.title("Statistické vyhodnocení dat z odpadového hospodářství")

frame = tkinter.Frame(window)
frame.pack()

# Saving User Info
user_info_frame = tkinter.LabelFrame(frame, text = "User Information")
user_info_frame.grid(row = 0, column = 0, padx = 20, pady = 10)

fist_name_label = tkinter.Label(user_info_frame, text="First name")
fist_name_label.grid(row=0, column = 0)
last_name_label = tkinter.Label(user_info_frame,text="Last name")
last_name_label.grid(row = 0, column = 1)

fist_name_entry = tkinter.Entry(user_info_frame)
last_name_label = tkinter.Entry(user_info_frame)
fist_name_entry.grid(row=1, column = 0)
last_name_label.grid(row=1, column = 1)

title_lable = tkinter.Label(user_info_frame, text="Title")
title_combobox = ttk.Combobox(user_info_frame, values=["","Pan", "Paní"] )
title_lable.grid(row=0, column = 2)
title_combobox.grid(row=1, column = 2)

age_label = tkinter.Label(user_info_frame, text="Age")
age_spinbox = tkinter.Spinbox(user_info_frame, from_ = 18, to=110)
age_label.grid(row=2, column=0)
age_spinbox.grid(row=3,column=0)

nationality_label = tkinter.Label(user_info_frame, text="Nationality")
nationality_combobox = ttk.Combobox(user_info_frame,values=["Africa", "Antarktida","Evropa","Asie","Amerika"])
nationality_label.grid(row=2, column = 1)
nationality_combobox.grid(row = 3, column=1)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

#Saving Course Info
courses_frame = tkinter.LabelFrame(frame)
courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

registered_label = tkinter.Label(courses_frame, text="Currently Registered")
reg_status_var = tkinter.StringVar(value="Not Register")
registered_check = tkinter.Checkbutton(courses_frame, text = "Currently Registered",     variable=reg_status_var, onvalue="Registered", offvalue="Not registered")
registered_label.grid(row=0, column=0)
registered_check.grid(row=1, column=0)

numcourses_label = tkinter.Label(courses_frame, text = "# Completed courses")
numcourses_spinbox = tkinter.Spinbox(courses_frame, from_=0, to='infinity')
numcourses_label.grid(row=0, column=1)
numcourses_spinbox.grid(row=1, column=1)

numsemesters_label = tkinter.Label(courses_frame, text = "# Semesters")
numsemesters_spinbox = tkinter.Spinbox(courses_frame, from_=0, to='infinity')
numsemesters_label.grid(row=0, column=2)
numsemesters_spinbox.grid(row=1, column=2)

for widget in courses_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Accept terms
terms_frame = tkinter.LabelFrame(frame,text="Terms and Conditions")
terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

accept_var = tkinter.StringVar(value="Not Accepted")
terms_check = tkinter.Checkbutton(terms_frame, text="I accept the terms and conditions.", variable=accept_var, onvalue="Accepted", offvalue="Not accepted")
terms_check.grid(row=0, column=0)

# Button
button = tkinter.Button(frame, text = "Enter data", command=enter_data)
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

window.mainloop()