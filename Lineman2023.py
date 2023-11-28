import customtkinter as ctk
import tkinter as tk
import couchdb




##CouchDB parameters for connecting to the database
couchdb_server_url = 'Your CouchDB server URL'
username = 'Username'  
password = 'Password!'


##Connect to the CouchDB server
server = couchdb.Server(couchdb_server_url)
server.resource.credentials = (username, password)


##Access the data base INSERT THE NAME HERE for the lineman data
db = server['lineman_info']


##The interface for the lineman
root = ctk.CTk()
root.geometry("1400x800")
root.title("Power Outage Dispatch - 5th Ave Electric")




##Entries for verifying the lineman
FirstName = ctk.CTkEntry(master=root, placeholder_text="First Name", width=275)
LastName = ctk.CTkEntry(master=root, placeholder_text="Last Name", width=275)
Lineman_ID = ctk.CTkEntry(master=root, placeholder_text="Lineman ID", width=275)


##Placing the boxes for the lineman to enter their information
FirstName.grid(row=1, column=0, pady=20, padx=10)
LastName.grid(row=1, column=1, pady=12, padx=10)
Lineman_ID.grid(row=1, column=2, pady=12, padx=10)

##Declare lineman_choice as a StringVar
lineman_choice = ctk.StringVar()





##Function to handle lineman status
def lineman_status(status):
    lineman_window = ctk.CTk()
    lineman_window.geometry("1400x800")

    ##Set the value of lineman_choice
    lineman_choice.set(status)

    ##Dropdown box for the lineman to update their status
    combobox = ctk.CTkOptionMenu(master=lineman_window, values=["available", "not available", "working", "heading to location", "leaving location"], variable=lineman_choice)
    combobox.grid(row=0, column=0, pady=12, padx=10)


    ##Function to update lineman status in CouchDB
    def update_status():
        ##Get the values entered by the lineman
        first_name = FirstName.get().strip()
        last_name = LastName.get().strip()
        lineman_id = Lineman_ID.get().strip()
        selected_status = lineman_choice.get()


        ##Retrieve the existing document from CouchDB
        try:
            doc = db[lineman_id]
        except couchdb.ResourceNotFound:
            print(f"Lineman ID {lineman_id} not found in CouchDB")
            return


        ##Update the relevant fields in the document
        doc['first_name'] = first_name
        doc['last_name'] = last_name
        doc['status'] = selected_status


        ##Save the updated document back to CouchDB
        db[lineman_id] = doc
        print(f"Updated document for Lineman ID: {lineman_id}")
        lineman_window.destroy()


    ##Button to update the status of the lineman
    update_status_button = ctk.CTkButton(master=lineman_window, text="Update", command=update_status)
    update_status_button.grid(row=8, column=0, pady=12, padx=10)




##Button to log in the lineman
start_button = ctk.CTkButton(master=root, text="Update Status", command=lambda: lineman_status("Status"))
start_button.grid(row=8, column=0, pady=12, padx=10)


##Run the interface
root.mainloop()