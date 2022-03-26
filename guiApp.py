from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
    
root = Tk()

frame1 = ttk.Frame(root)
frame2 = ttk.Frame(root)
frame1.grid(row=0,column=0)
frame2.grid(row=0,column=1)

# when we actually add our elements, we'll have to use either grid or place down below.
# pack absolutely tosses these dimensions out the window
frame1.config(height = 420, width = 320)
frame1.config(relief = RIDGE)
frame2.config(height = 420, width = 320)
frame2.config(relief = RIDGE)

label_title = ttk.Label(frame1, text = "Desired Job Title")
label_city = ttk.Label(frame1, text = "City")
label_prov = ttk.Label(frame1, text = "Province")
label_key = ttk.Label(frame1, text = "Keywords")

label_title.config(font = ('Playfair Display', 18, 'bold')) # font name, size, and style
label_city.config(font = ('Playfair Display', 18, 'bold')) # font name, size, and style
label_prov.config(font = ('Playfair Display', 18, 'bold')) # font name, size, and style
label_key.config(font = ('Playfair Display', 18, 'bold')) # font name, size, and style

entry_title = ttk.Entry(frame1, width = 30)
entry_city = ttk.Entry(frame1, width = 30)
entry_key = ttk.Entry(frame1, width = 30)

province = StringVar()
combobox_prov = ttk.Combobox(frame1, textvariable = province)
combobox_prov.config(values = ('Alberta','British Columbia','Manitoba','New Brunswick','Newfoundland and Labrador',
                                   'Northwest Territories','Nova Scotia','Nunavut','Ontario','Prince Edward Island',
                                   'Quebec','Saskatchewan','Yukon'))
combobox_prov.state(['readonly']) # prevents user from typing in combobox
province.set('Alberta')

logo = Image.open('C:/Users/Owner/Desktop/python-icom3010/career-beacon.png')
logo = logo.resize((305,72), Image.ANTIALIAS)
logoPI = ImageTk.PhotoImage(logo)
logoLabel = ttk.Label(frame1, image = logoPI)
logoLabel.image = logoPI

btn_submit = ttk.Button(frame1, text = "Submit")

logoLabel.pack()

label_title.pack()
entry_title.pack()
label_city.pack()
entry_city.pack()
label_prov.pack()
combobox_prov.pack()
label_key.pack()
entry_key.pack()

btn_submit.pack(pady=(10,10))

job_notebook = ttk.Notebook(frame2)
job_notebook.pack()

tab1 = ttk.Frame(job_notebook)
tab2 = ttk.Frame(job_notebook)
tab3 = ttk.Frame(job_notebook)
job_notebook.add(tab1, text = 'Favourites')
job_notebook.add(tab2, text = 'Results')
job_notebook.add(tab3, text = 'Featured')
job_notebook.select(0)

root.mainloop()