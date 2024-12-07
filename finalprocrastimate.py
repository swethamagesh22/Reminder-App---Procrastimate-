from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import datetime, time
import os, subprocess
from tkcalendar import DateEntry
import mysql.connector
from tkinter import ttk
import platform

def main():
    # Connecting MySQL database to Python
    while True:
        global mydb, mycursor
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='Swetha@22', database='procrastimate')
        mycursor = mydb.cursor()
        if mydb.is_connected():
            print('Database successfully connected')    #Confirming the connection
        break

    # The following function gets executed when clicked on the "Today's Reminders" menu option
    def today_rem():
        t_sql = tk.Toplevel(master)
        t_sql.geometry('1000x300')
        t_sql.configure(background='yellow')
        Label(t_sql, text="Today's reminders").pack()
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        query = f"SELECT * FROM allreminders WHERE Date = '{current_date}'"
        mycursor.execute(query)
        t_output = mycursor.fetchall()

        # Creating a table to display reminders in a tabular format
        tree = ttk.Treeview(t_sql, columns=('Reminder','Description', 'Date', 'Hours', 'Minutes'), show='headings')
        tree.pack(side=TOP, padx=10, pady=10)

        tree.heading('Reminder', text='Reminder')
        tree.heading('Date', text='Date')
        tree.heading('Hours', text='Hours')
        tree.heading('Minutes', text='Minutes')
        tree.heading('Description', text='Description')

        for reminder in t_output:
            tree.insert('', 'end', values=(reminder[0], reminder[1], reminder[2], reminder[3], reminder[4]))
            #tree.insert('', 'end', values=reminder)
        
        # Create an exit button
        exit_button = Button(t_sql, text="Exit", command=t_sql.destroy)
        exit_button.pack()

    # The following function gets executed when clicked on the "Scheduled Reminders" menu option
    def sch_rem():
        sc_sql = tk.Toplevel(master)
        sc_sql.geometry('1000x300')
        sc_sql.configure(background='blue')
        Label(sc_sql, text='Scheduled reminders').pack()
        # Get the current date
        current_date = datetime.datetime.now().date()

        # Retrieve upcoming scheduled reminders from the database
        query = f"SELECT * FROM scheduled WHERE Date > '{current_date}';"
        mycursor.execute(query)
        sc_output = mycursor.fetchall()

        # Creating a table to display reminders in a tabular format
        tree = ttk.Treeview(sc_sql, columns=('Reminder','Description', 'Date', 'Hours', 'Minutes'), show='headings')
        tree.pack(side=TOP, padx=10, pady=10)

        tree.heading('Reminder', text='Reminder')
        tree.heading('Description', text='Description')
        tree.heading('Date', text='Date')
        tree.heading('Hours', text='Hours')
        tree.heading('Minutes', text='Minutes')
        #tree.heading('Description', text='Description')

        for reminder in sc_output:
            tree.insert('', 'end', values=(reminder[0], reminder[1], reminder[2], reminder[3], reminder[4]))
            #tree.insert('', 'end', values=reminder)

        # Create an exit button
        exit_button = Button(sc_sql, text="Exit", command=sc_sql.destroy)
        exit_button.pack()

    # The following function gets executed when clicked on the "All Reminders" menu option
    def all_rem():
        all_sql = tk.Toplevel(master)
        all_sql.geometry('1000x300')
        all_sql.configure(background='cyan')
        Label(all_sql, text='All reminders').pack()
        query = f"SELECT * FROM allreminders ORDER BY Date, hours, mins;"
        mycursor.execute(query)
        all_output = mycursor.fetchall()
        
        # Creating a table to display reminders in a tabular format
        tree = ttk.Treeview(all_sql, columns=('Reminder','Description', 'Date', 'Hours', 'Minutes'), show='headings')
        tree.pack(side=TOP, padx=10, pady=10)

        tree.heading('Reminder', text='Reminder')
        tree.heading('Date', text='Date')
        tree.heading('Hours', text='Hours')
        tree.heading('Minutes', text='Minutes')
        tree.heading('Description', text='Description')

        for reminder in all_output:
            tree.insert('', 'end', values=(reminder[0], reminder[4], reminder[1], reminder[2], reminder[3]))
            #tree.insert('', 'end', values=reminder)
        
        # Create an exit button
        exit_button = Button(all_sql, text="Exit", command=all_sql.destroy)
        exit_button.pack()

     #creation of the menu driven tkinter window 
    global master, path, img, panel
    master = tk.Tk()        #the text box title
    master.title(string='Procrasti-mate')
    path=Image.open("/Users/swetha/Documents/python/Procrasti-mate.jpeg")
    img = ImageTk.PhotoImage(path)
    panel = tk.Label(image = img)
    
    panel.image=img         #image attached to the tkinter box
    frame1=Frame(master)
    frame1.pack(side=TOP,fill=X)
    frame2=Frame(master)
    frame2.pack(side=TOP,fill=X)
    panel.pack(side = "left", fill = "both", expand = "yes")
  
    #the following functions gets executed when clicked on 'create a new reminder' menu option
    def new():

        #displays the user inputed values when pressed on show
        def display():
            print("Reminder: %s\nDate: %s\nHours: %s\nMinutes: %s\nDescription: %s" % (e1.get(),e2,hour_scale.get(),minute_scale.get(),e5.get()))
            #print("Reminder: %s\nDate: %s\nHours: %s\nMinutes: %s\nDescription: %s" % (e1.get(),e2,e3.get(),e4.get(),e5.get()))
        
        final=tk.Toplevel(master)
        final.geometry("750x280")
        final.configure(background='orange')
        
        #labelling the rows
        tk.Label(final,text='Reminder').grid(row=4,column=0,sticky=E)
        tk.Label(final,text='Date (DD-MM-YYYY)').grid(row=5,column=0,sticky=E)
        tk.Label(final,text='Hours').grid(row=6,column=0,sticky=E)
        tk.Label(final,text='Minutes').grid(row=6,column=2,sticky=E)
        tk.Label(final,text='Description').grid(row=7,column=0,sticky=E)
        #tk.label(frame2,text='location').grid(row=8,column=0,sticky=E)
        
        #to create a calendar derived date effect
        def date_entry():
            def storedate():
                global e2
                e2=cal.get_date()
                date_label.config(text = "Selected Date is: " + str(e2))
                top.destroy()

            top = tk.Toplevel(master)
            tk.Label(top, text='Choose date').pack(padx=10, pady=10)
            cal = DateEntry(top, width=20, background='darkblue', foreground='white', borderwidth=2)
            cal.pack(padx=10, pady=10)
            date_label = Label(final, text="")
            date_label.grid(row=5, column=2, sticky=W, pady=9)
            tk.Button(top, text="ok", command=storedate).pack()
        
        #the creation widgets in the new reminder option
        #global e1, e2, e3, e4, e5
        global e1, e2, e5
        e1=tk.Entry(final)         #to enter values
        e2=tk.Entry(frame2)
        #e3=tk.Spinbox(final, from_=0, to=23)
        #e4=tk.Spinbox(final, from_=0, to=59)
        e5=tk.Entry(final)
        #e6=tk.Entry(frame2) #-> if we need location
        e1.grid(row=4,column=1)       #to display a seperate textbox and grid
        e2.grid(row=5,column=1)
        #e3.grid(row=6,column=1)
        #e4.grid(row=6,column=3)
        e5.grid(row=7,column=1)
        #e6.grid(row=8,column=1) #-> if we need location

        # Scroll timer for selecting hours
        hour_scale = tk.Scale(final, from_=0, to=23, orient=tk.HORIZONTAL)
        hour_scale.grid(row=6, column=1, sticky=tk.W, pady=9)


        # Scroll timer for selecting minutes
        minute_scale = tk.Scale(final, from_=0, to=59, orient=tk.HORIZONTAL)
        minute_scale.grid(row=6, column=3, sticky=tk.W, pady=9)
        
        # Exit button
        exit_btn = Button(final, text="Exit", command=final.destroy)
        exit_btn.grid(row=8, column=3, sticky=tk.W, pady=9)
        
        #variable validation
        def validation():
            #if e1=='' or e2=='' or e3=='' or e4==''and type(e3)!=int and type(e4)!=int:
            if e1=='' or e2=='':
                empty=tk.Toplevel(master)
                empty.geometry("250x200")
                w = Label(empty, text ='ALERT!!!', font = "80")  
                w.pack()
                msg = Message(empty, text = "All entries except description are required and the hour and mins value should be integrers only, to proceed further")   
                msg.pack() 
            
            else:
                success=tk.Toplevel(master)
                success.geometry("250x200")
                t=Label(success, text='SUCCESS', font='80')
                t.pack()
                msg=Message(success, text='You reminder has been set. You can now close this window')
                msg.pack()
        
        #desktop voiceover (text to speech) - voices the reminder out loud
        #also notifies the user with a notification
        #for macOS operating system
        def os_notifier():
            #voice notification
            os.system('say "your reminder"')
            os.system('say "is due now"')

            #Desktop notification
            title = "Reminder"
            message = "is due now!"

            if platform.system() == "Darwin":    #macOS
                command = f'osascript -e \'display notification "{rem} {message}" with title "{title}"\''
                subprocess.call(command, shell=True)
            
        
        #the following is the backend of the whole program
        #only applicable for new reminders
        def backend():
            #backend storing
            validation()
            global rem, x, hours, mins, date, desc
            rem=e1.get()
            #date = e2
            s_e2=str(e2)
            x=s_e2.split('-')
            #hours=int(e2.get())
            #mins=int(e5.get())
            hours = hour_scale.get()
            mins = minute_scale.get()
            date=datetime.datetime(int(x[0]),int(x[1]),int(x[2]),hours,mins)
            desc=e5.get()

            # Calculate time difference
            global currenttime
            currenttime=datetime.datetime.now()
            #time_difference = (date - currenttime).total_seconds()

            # Wait for the reminder time
            #if time_difference > 0:
             #   time.sleep(time_difference)
            
             # Check if the reminder time has been reached
            #while datetime.datetime.now() < date:
             #   time.sleep(1)  # Wait for 1 second before checking again

            # Trigger the reminder
            os_notifier()
            #master.destroy()

            #backend processing
            def check_reminder():
                if currenttime>=date:
                    os_notifier()
                else:
                   master.after(1000,check_reminder)
            master.after(int((date - datetime.datetime.now()).total_seconds() * 1000), check_reminder)
            # Check the reminder at the scheduled time
            check_reminder()
            
            #storing of reminders accordingly to the tables - all, today and scheduled
            mycursor.execute('INSERT INTO allreminders VALUES (%s, %s, %s, %s, %s)', (rem, e2, hours, mins, desc))
            if currenttime.strftime('%m') < date.strftime('%m') and currenttime.strftime('%d') < date.strftime('%d'):
                mycursor.execute('INSERT INTO scheduled VALUES (%s, %s, %s, %s, %s)', (rem, desc, e2, hours, mins))
            elif currenttime.strftime('%m') == date.strftime('%m') and currenttime.strftime('%d') == date.strftime('%d'):
                mycursor.execute('INSERT INTO today VALUES (%s, %s, %s, %s, %s)', (rem, desc, e2, hours, mins))
            mydb.commit()

            # Destroy the reminder window
            #master.destroy()
            
        #buttons for new reminder fn      #check if sticky,pady is needed
        tk.Button(final,text='choose date',command=date_entry).grid(row=5,column=1,sticky=tk.W,pady=9)
        tk.Button(final,text='Save',command=backend).grid(row=8,column=0,sticky=tk.W,pady=9)
        tk.Button(final,text='Show',command=display).grid(row=8,column=1,sticky=tk.W,pady=9)
        #tk.Button(final,text='Go back to menu',command=main).grid(row=9,column=3,sticky=tk.W,pady=9)
        
    #heading for the master window    
    label = Label(master, text ="**Choose your desired action to be performed from the options given below**")
    master.configure(background='pink')
    label.pack(pady = 10)
    
    # new window on button click
    btn = Button(master, text ="Create a new reminder",command = new)
    btn.pack(pady = 10)
    btn = Button(master, text ="Scheduled Reminders", command = sch_rem)
    btn.pack(pady = 11)
    btn = Button(master, text ="Reminders for Today", command = today_rem)
    btn.pack(pady = 12)
    btn = Button(master, text ="All Reminders", command = all_rem)
    btn.pack(pady = 13)
    btn = Button(master, text ="Exit", command = master.destroy)
    btn.pack(pady = 14)
        
    master.mainloop()       #looping the above process 
    
    master.quit()       #once the process is done, it quits


if __name__ == "__main__":
    main()
