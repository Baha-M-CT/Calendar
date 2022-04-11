from tkinter import *
from tkcalendar import *
import datetime
from Database import Database
from MyCalendar import MyCalendar
from PIL import ImageTk, Image
#=======================================================================================#
read = Database()
# Create a main window
root=Tk()
root.title("Calendar and Events")
root.resizable(0,0)
#=======================================================================================#
# GLOBAL variables
date=datetime.datetime.now()
y=date.year
m=date.month
d=date.day
wd=date.strftime("%A")
eventtext=""
photo=ImageTk.PhotoImage(Image.open("wood.jpg"))
lab = Label(root, image=photo).pack()
sel_date=date
sel_hour=0
sel_min=0
#=======================================================================================#
# Function for new window - Create Event
def openNewWindow():
    global current_day, sel_date
    hour_string = StringVar()
    min_string = StringVar()
    query_status = StringVar()
    f = ('Times', 10)
    newWindow = Toplevel(root)
    newWindow.title("New Window")
    newWindow.geometry("320x320")
    newWindow.resizable(0, 0)
    Label(newWindow, text="Enter Event Details").grid(row=0, column=1,padx=10, pady=10)
    newWindow.grab_set()
    # get selected Date
    def get_sel_date(e):
        global sel_date
        sel_date=event_date.get_date()

    # get selected Time
    def get_sel_time():
        global sel_hour, sel_min
        sel_hour=hour_sb.get()
        sel_min = min_sb.get()

    # submit request to add new event in the DB
    def submit():
        event_status.config(fg='black')
        searchdate3 = sel_date.strftime("%Y-%m-%d")
        lastid = read.addevent(event_title.get(), event_notes.get(), searchdate3, sel_hour, sel_min)
        if lastid > 0:
            # clear the text boxes
            event_title.delete(0, END)
            event_notes.delete(0, END)
            #event_date.delete(0, END)
            hour_string.set("0")
            min_string.set("0")
            query_status.set("Event Succesfully Created")
        elif lastid == -1:
            # sql error
            event_status.config(fg='red')
            query_status.set("Data too long for 'Event Title'")
        elif lastid == -2:
            # sql error
            event_status.config(fg='red')
            query_status.set("Data too long for 'Event Notes")

    #create text box fields
    event_title = Entry(newWindow, width=30)
    event_title.grid(row=1, column=1)
    event_notes = Entry(newWindow, width=30)
    event_notes.grid(row=2, column=1, ipady=10)
    current_day = datetime.datetime.strptime(current_day, '%d/%m/%Y').strftime('%m-%d-%Y')
    event_date = DateEntry(newWindow, width=25, background='darkblue', foreground='white', borderwidth=2)
    event_date.set_date(current_day)
    sel_date = event_date.get_date()
    event_date.bind("<<DateEntrySelected>>", get_sel_date)
    event_date.grid(row=3, column=1)
    hour_sb = Spinbox(newWindow,from_=0,to=23,wrap=True,textvariable=hour_string,width=2,state="readonly",font=f,justify=CENTER)
    hour_sb.grid(row=4, column=1, sticky = 'W')
    min_sb = Spinbox(newWindow,from_=0,to=59,wrap=True,textvariable=min_string,width=2,state="readonly",font=f,justify=CENTER)
    min_sb.grid(row=4, column=1)

    # create text box labels
    event_title_label = Label(newWindow, text="Event Title")
    event_title_label.grid(row=1, column=0,padx=10, pady=10)
    event_notes_label = Label(newWindow, text="Event Notes")
    event_notes_label.grid(row=2, column=0,padx=10, pady=10)
    event_date_label = Label(newWindow, text="Event Date")
    event_date_label.grid(row=3, column=0,padx=10, pady=10)
    event_time_label = Label(newWindow, text="Event Time")
    event_time_label.grid(row=4, column=0,padx=10, pady=10)
    event_time_text = Label(newWindow, text="Hour          Minute", font=("Arial", 10))
    event_time_text.grid(row=5, column=1,sticky = 'W')

    #DB operations status label
    event_status = Label(newWindow, textvariable=query_status)
    event_status.grid(row=8, column=1)

    #Submit button
    submit_btn = Button(newWindow, text = "Add Event", command=lambda:[get_sel_time(), submit()])
    submit_btn.grid(row = 6, column = 0, columnspan=2,padx=30, pady=10)

#=======================================================================================#
#Functin to get selected value from Events list - will be used for Event editing
def CurSelect(event):
    value=str((list.get(list.curselection())))
    print("selected value: ", value)
#=======================================================================================#

calendar= MyCalendar(root, selectmode="day", date_pattern="dd/mm/yyyy", year =y, month=m,
                  day=d, background="#042f80", foreground="white", selectbackground="#f5b907",
                  selectforeground="black", weekendbackground="#f74040", weekendforeground="black",
                  font="Arial 13 bold")
calendar.place(x=20, y=20)
date=calendar.get_date()
now = datetime.datetime.now()

# 'Create event' button
event_button = Button(root, text="Create event",height=2, width=14, font=("Arial", 12, 'bold'), command=openNewWindow)
event_button.place(x=370, y=60)

#create window for the list of events under the calendar
frame = Frame(root,bg = "#dcedc1")
frame.place(x=20, y=250)
list = Listbox(frame, width=32, height=6, bg = "#dcedc1", activestyle = 'dotbox', selectmode="single", font='consolas')
list.bind('<<ListboxSelect>>', CurSelect)
list.pack(side="left", fill="y", pady=5)

# for scrolling vertically
scrollbar = Scrollbar(frame, orient="vertical")
scrollbar.config(command=list.yview)
scrollbar.pack(side="right", fill="y")
list.config(yscrollcommand=scrollbar.set)

#function runs when we click on date
def on_change_day(event):
    global current_day
    #clear events list
    list.delete('0', 'end')
    current_day = calendar.get_date()
    searchdate2 = datetime.datetime.strptime(current_day, '%d/%m/%Y').strftime('%Y-%m-%d')
    # read from DB - events for selected day
    myresults = read.fetch(searchdate2)
    for each_event in myresults:
        date_txt = (datetime.datetime.strftime(each_event[2], '%b %d'))
        eventtime = (str(each_event[3])[0:5])
        list.insert(END, (date_txt +", " + eventtime +" - "  + each_event[1]))

#Function to highligh days with events
def display_current_month_events():
    #clear events list
    list.delete('0', 'end')
    month, year = calendar.get_displayed_month_year()
    year1 = str(year)
    month1 = str(month)
    # highlight days having events
    myresults = read.fetchmonth(month1, year1)
    eventtext = ""
    for row in myresults:
        marker_day = row[2]
        calendar.calevent_create(marker_day, 'meeting', 'meeting')
        #calendar.tag_config('meeting', background='red', foreground='yellow')

#Function is called when the Month is changed
def on_change_month(event):
    # remove previously displayed events
    calendar.calevent_remove('all')
    year, month = calendar.get_displayed_month_year()
    # display current month events
    display_current_month_events()

#here I call both functions when program starts
on_change_month('<<CalendarMonthChanged>>')
on_change_day('<<CalendarSelected>>')

#waiting for the user to select Month or Date
calendar.bind('<<CalendarMonthChanged>>', on_change_month)
calendar.bind('<<CalendarSelected>>', on_change_day)

root.mainloop()