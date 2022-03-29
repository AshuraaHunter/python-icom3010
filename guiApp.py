from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import mainScrape

arr = []
    
root = Tk()
root.option_add("*TCombobox*Listbox*Font",('Circular Std Medium',10)) # the dropdown list of the combobox needs to have its styles defined separately
root.resizable(False,False)

style = ttk.Style()
style.configure('TNotebook.Tab',font=('Circular Std Medium',10)) # since the tabs are not a different widget type, we can set up a style for them

frame1 = ttk.Frame(root)
frame2 = ttk.Frame(root)
frame1.grid(row=0,column=0)
frame2.grid(row=0,column=1)

# when we actually add our elements, we'll have to use either grid or place down below.
# pack absolutely tosses these dimensions out the window
frame1.config(relief=FLAT)
frame2.config(relief=FLAT)

label_title = ttk.Label(frame1,text="Desired Job Title")
label_city = ttk.Label(frame1,text="City")
label_prov = ttk.Label(frame1,text="Province")
label_key = ttk.Label(frame1,text="Keywords")

label_title.config(font=('Circular Std Medium',18,'bold')) # font name, size, and style
label_city.config(font=('Circular Std Medium',18,'bold'))
label_prov.config(font=('Circular Std Medium',18,'bold'))
label_key.config(font=('Circular Std Medium',18,'bold'))

entry_title = ttk.Entry(frame1,font=('Circular Std Medium',10),width=30)
entry_city = ttk.Entry(frame1,font=('Circular Std Medium',10),width=30)
entry_key = ttk.Entry(frame1,font=('Circular Std Medium',10),width=30)

province = StringVar()
combobox_prov = ttk.Combobox(frame1,font=('Circular Std Medium',10),textvariable=province,width=27) # 3 less since the arrow icon takes up added space
combobox_prov.config(values=('Alberta','British Columbia','Manitoba','New Brunswick','Newfoundland and Labrador',
                                   'Northwest Territories','Nova Scotia','Nunavut','Ontario','Prince Edward Island',
                                   'Quebec','Saskatchewan','Yukon'))
combobox_prov.state(['readonly']) # prevents user from typing in combobox
province.set('Alberta')

# source: https://www.activestate.com/resources/quick-reads/how-to-add-images-in-tkinter/
logo = Image.open('C:/Users/Owner/Desktop/python-icom3010/career-beacon.png')
logo = logo.resize((305,72),Image.ANTIALIAS)
logoPI = ImageTk.PhotoImage(logo)
logoLabel = ttk.Label(frame1,image=logoPI)
logoLabel.image = logoPI

btn_submit = ttk.Button(frame1,text="Submit",command=lambda:scrape())

logoLabel.grid(row=0,column=0)

label_title.grid(row=1,column=0,padx=(10,10),sticky='w')
entry_title.grid(row=2,column=0)
label_city.grid(row=3,column=0,padx=(10,10),sticky='w')
entry_city.grid(row=4,column=0)
label_prov.grid(row=5,column=0,padx=(10,10),sticky='w')
combobox_prov.grid(row=6,column=0)
label_key.grid(row=7,column=0,padx=(10,10),sticky='w')
entry_key.grid(row=8,column=0)

btn_submit.grid(row=9,column=0,padx=(10,10),pady=(10,10),sticky='e')

job_notebook = ttk.Notebook(frame2)
job_notebook.grid(row=0,column=0)

# initialization function, which we call to set up each notebook tab
# we give the canvas its scrollbar, setup the scrollbar's dimensions and canvas' position,
# then the scrollbar's position, and ensure the canvas is actually created with the frame we specified.
def tab_init(canvas,frame,scrollbar):
    canvas.config(yscrollcommand=scrollbar.set)
    scrollbar.config(orient=VERTICAL,command=canvas.yview)
    canvas.grid(row=1,column=0)
    scrollbar.grid(row=1,column=1,sticky='ns')
    canvas.create_window(0,0,window=frame)
    

# update function, which we will call upon inserting a new entry from our searches / queries
# update_idletasks() lets us process any pending events WITHOUT inadvertently triggering callbacks
# and we update the canvas' scrollregion to fit the frame's new contents (coords() gets its dimensions)
def tab_upd(canvas,frame):
    canvas.update_idletasks()
    canvas.config(scrollregion=frame.coords())


# each tab needs its own frame
# each of these frames has a canvas that allows for scrollbar attachment, and which contains a frame that houses the items we'll be storing within it
tab_fav = ttk.Frame(job_notebook)
fav_canvas = Canvas(tab_fav)
fav_frame = ttk.Frame(fav_canvas)
fav_scrollbar = ttk.Scrollbar(tab_fav)

tab_res = ttk.Frame(job_notebook)
res_canvas = Canvas(tab_res)
res_frame = ttk.Frame(res_canvas)
res_scrollbar = ttk.Scrollbar(tab_res)

tab_feat = ttk.Frame(job_notebook)
feat_canvas = Canvas(tab_feat)
feat_frame = ttk.Frame(feat_canvas)
feat_scrollbar = ttk.Scrollbar(tab_feat)

tab_init(fav_canvas,fav_frame,fav_scrollbar)
tab_init(res_canvas,res_frame,res_scrollbar)
tab_init(feat_canvas,feat_frame,feat_scrollbar)

job_notebook.add(tab_fav,text='Favourites')
job_notebook.add(tab_res,text='Results')
job_notebook.add(tab_feat,text='Featured')
job_notebook.select(0)

def scrape():
    arr = mainScrape.basic_scrape(entry_title.get(),entry_city.get(),combobox_prov.get())
    
    for listing in arr:
        pass
    

root.mainloop()