from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import mainScrape
import webbrowser # handles links

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
combobox_prov = ttk.Combobox(frame1,font=('Circular Std Medium',10),textvariable=province,width=28) # 2 less since the arrow icon takes up added space
combobox_prov.config(values=('Alberta','British Columbia','Manitoba','New Brunswick','Newfoundland and Labrador',
                                   'Northwest Territories','Nova Scotia','Nunavut','Ontario','Prince Edward Island',
                                   'Quebec','Saskatchewan','Yukon'))
combobox_prov.state(['readonly']) # prevents user from typing in combobox
province.set('Alberta')

# source: https://www.activestate.com/resources/quick-reads/how-to-add-images-in-tkinter/
logo = Image.open('C:/Users/Owner/Desktop/python-icom3010/career-beacon.png')
logo = logo.resize((305,72),Image.ANTIALIAS)
logo_pi = ImageTk.PhotoImage(logo)
logo_label = ttk.Label(frame1,image=logo_pi)
logo_label.image = logo_pi

small_logo = Image.open('C:/Users/Owner/Desktop/python-icom3010/cb_small.png')
small_logo = small_logo.resize((60,60),Image.ANTIALIAS)
small_logo_pi = ImageTk.PhotoImage(small_logo)

btn_submit = ttk.Button(frame1,text="Submit",command=lambda:scrape())

logo_label.grid(row=0,column=0)

label_title.grid(row=1,column=0,padx=(10,10),sticky='w')
entry_title.grid(row=2,column=0)
label_city.grid(row=3,column=0,padx=(10,10),sticky='w')
entry_city.grid(row=4,column=0)
label_prov.grid(row=5,column=0,padx=(10,10),sticky='w')
combobox_prov.grid(row=6,column=0)
label_key.grid(row=7,column=0,padx=(10,10),sticky='w')
entry_key.grid(row=8,column=0)

btn_submit.grid(row=9,column=0,padx=(10,10),pady=(10,10),sticky='e')

job_notebook = ttk.Notebook(frame2,height=480,width=376)
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
# and we update the canvas' scrollregion to fit the new contents (bbox() gets its dimensions)
def tab_upd(canvas):
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(0.0)


# each tab needs its own frame
# each of these frames has a canvas that allows for scrollbar attachment, and which contains a frame that houses the items we'll be storing within it
tab_fav = ttk.Frame(job_notebook)
fav_canvas = Canvas(tab_fav,highlightthickness=0,height=480,width=360)
fav_canvas.pack()
fav_frame = ttk.Frame(fav_canvas)
fav_frame.pack()
fav_scrollbar = ttk.Scrollbar(tab_fav)

tab_res = ttk.Frame(job_notebook)
res_canvas = Canvas(tab_res,highlightthickness=0,height=480,width=360)
res_canvas.pack()
res_frame = ttk.Frame(res_canvas)
res_frame.pack()
res_scrollbar = ttk.Scrollbar(tab_res)

tab_feat = ttk.Frame(job_notebook)
feat_canvas = Canvas(tab_feat,highlightthickness=0,height=480,width=360)
feat_canvas.pack()
feat_frame = ttk.Frame(feat_canvas)
feat_frame.pack()
feat_scrollbar = ttk.Scrollbar(tab_feat)

tab_init(fav_canvas,fav_frame,fav_scrollbar)
tab_init(res_canvas,res_frame,res_scrollbar)
tab_init(feat_canvas,feat_frame,feat_scrollbar)

job_notebook.add(tab_fav,text='Favourites')
job_notebook.add(tab_res,text='Results')
job_notebook.add(tab_feat,text='Featured')
job_notebook.select(0)

def scrape():
    job_notebook.select(1)
    arr = mainScrape.basic_scrape(entry_title.get(),entry_city.get(),combobox_prov.get())
    cnt = 0
    
    if not isinstance(arr,list):
        print(type(arr))
        return
    
    for listing in arr:
        listing_frame = ttk.Frame(res_frame)
        listing_frame.grid_propagate(0) # keeps our frames a consistent size
        listing_frame.config(width=360,height=128,
                             relief=RIDGE,padding=(5,5))
        
        icon_label = ttk.Label(listing_frame,image=small_logo_pi)
        icon_label.image = small_logo_pi
        
        listing_title = Message(listing_frame,text=listing.title)
        listing_title.config(font=('Circular Std Medium',10,'bold'),width=240)
        
        listing_company = Message(listing_frame,text=listing.company)
        listing_company.config(font=('Circular Std Medium',10,'normal'),width=180)
        
        listing_location = ttk.Label(listing_frame,text=listing.location)
        listing_location.config(font=('Circular Std Medium',10,'normal'))
        
        listing_date = ttk.Label(listing_frame,text=f"Posted on {listing.date}")
        listing_date.config(font=('Circular Std Medium',10,'normal'))
        
        listing_button = ttk.Button(listing_frame)
        listing_button.config(width=10,text="Apply",command=lambda listing=listing: webbrowser.open(listing.link)) # stores the listing properties; otherwise this points to the very last link element
        
        icon_label.grid(row=0,column=0,rowspan=2)
        listing_title.grid(row=0,column=1)
        listing_company.grid(row=1,column=1)
        listing_location.grid(row=2,column=1)
        listing_date.grid(row=3,column=1)
        listing_button.place(relx=0.8,rely=0.8)
        
        listing_frame.grid_columnconfigure(1,weight=1)
        
        listing_frame.grid(row=cnt,column=1)
        tab_upd(res_canvas)
        cnt += 1
    

root.mainloop()