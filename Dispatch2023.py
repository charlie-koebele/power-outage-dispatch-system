import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import psycopg2
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




##Connect to the database using the appropriate host, dbname, user, and password
conn = psycopg2.connect(
    host= "Hostname",
    dbname="DB_TEST",       
    user="postgres",       
    password="PASSWORD"
)


##The initial interface for the calltaker/dispatcher
root = ctk.CTk()
root.geometry("1400x800")
root.title("Power Outage Dispatch - 5th Ave Electric")


##Entries for searching up the consumers
FirstName = ctk.CTkEntry(master=root, placeholder_text="First Name", width= 275)
LastName = ctk.CTkEntry(master=root, placeholder_text="Last Name", width= 275)
Address = ctk.CTkEntry(master=root, placeholder_text="Address", width= 275)
PhoneNumber = ctk.CTkEntry(master=root, placeholder_text="Phone Number", width= 275)
result_label = ctk.CTkLabel(master=root, text="")


##Placment of the textboxes and label in 'root'
FirstName.grid(row=1, column=0, pady=20, padx=10)
LastName.grid(row=1, column=1, pady=12, padx=10)
Address.grid(row=1, column=2, pady=12, padx=10)
PhoneNumber.grid(row=1, column=3, pady=12, padx=10)
result_label.grid(row=25, column=0, pady=12, padx=10)



##Function that opens the dispatch window to look at the tickets
def dispatch():
    ##Create a cursor
    cur = conn.cursor()

    ##Creating the interface for tickets
    dispatch_window = ctk.CTk()
    dispatch_window.geometry("800x800")
    dispatch_window.title("Dispatch")


    ##Function for retrieving the tickets to be displayed in the table
    def show_tickets():
        retrieve_tickets(tree)


    ##Function that makes it so you can click on the row where the ticket is
    def on_row_click(event):
        selected_item = tree.selection()
        if selected_item:
            num_row = tree.index(selected_item)  # Get the index of the selected row
            open_new_window(selected_item, num_row)
            

    ##Function to open a new window to view the ticket opened by the dispatcher
    def open_new_window(selected_item, num_row):
        ##The interface that the ticket information will be in
        ticket_window = ctk.CTk()
        ticket_window.geometry("800x800")
        ticket_window.title("Ticket")

        ##The information that will be in the ticket window
        description_label = ctk.CTkLabel(master=ticket_window, text="")
        available_label = ctk.CTkLabel(master=ticket_window, text="")
        item_values = tree.item(selected_item, 'values')
        ticket_id = item_values[0]

        ##The query for retrieving the description from the SQL database
        description_query = "SELECT description FROM consumer_tickets WHERE TRUE"
        cur.execute(description_query, [ticket_id])
        results = cur.fetchall()
        result_text = "\n".join([str(row) for row in results[num_row]])
        description_label.configure(text=result_text)
        description_label.grid(row=1, column=0, pady=20, padx=10)

        ##Displaying the results in the ticket window
        update_description = ctk.CTkEntry(master=ticket_window, placeholder_text="Description", width=275, height=275)
        update_description.grid(row=5, column=0, pady=20, padx=20)


        ##Function so the dispatcher can add addtional information to the ticket
        def add_description():
            ##Query for updating the description column in the ticket database in SQL
            updated_ticket = update_description.get().strip()
            ticket_insertion_query = "UPDATE consumer_tickets SET description = CONCAT(description, %s) WHERE ticket_id = %s"
            cur.execute(ticket_insertion_query, (updated_ticket, ticket_id))
            conn.commit()
            cur.close()
            ticket_window.destroy()


        ##The botton to call the function add_description to update the ticket
        update_ticket_button = ctk.CTkButton(ticket_window, text="Update Ticket", command=add_description)
        update_ticket_button.grid(row=25, column=1, pady=12, padx=10)

        ##Mango query to find available linemen to be displayed in the ticket
        ##for the dispatcher to call out the lineman
        query = {
            "selector": {
                "status": "available",
                "doctype": "lineman"
            }
        }

        ##Perform the query in the CouchDB database for the lineman
        available_linemen_result = db.find(query)

        ##Create a list to store linemen information
        linemen_info_list = []

        ##Append linemen information to the list
        for doc in available_linemen_result:
            linemen_info_list.append(f"Lineman Name: {doc['name']}, Status: {doc['status']}, Phone: {doc['phone']}")

        ##Join the list into a single string
        available_linemen_text = "\n".join(linemen_info_list)

        ##Make and display the label for the lineman
        available_label.configure(text=available_linemen_text)
        available_label.grid(row=10, column=0, pady=20, padx=10)
                
    ##Button that calls the function 'show_tickets' to display the tickets in the table
    get_tickets = ctk.CTkButton(master=dispatch_window, text="Get Tickets", command=show_tickets, width=275)
    get_tickets.grid(row=1, column=0, pady=20, padx=10)


    ##Create a Treeview widget for displaying the tickets in the table
    tree = ttk.Treeview(dispatch_window, columns=("Ticket ID", "Consumer ID", "Creation Date", "Last Updated", "Ticket Status", "Priority", "Category"), show="headings")

    ##Define column headings for the table to display the tickets
    tree.heading("Ticket ID", text="Ticket ID")
    tree.heading("Consumer ID", text="Consumer ID")
    tree.heading("Ticket Status", text="Ticket Status")
    tree.heading("Creation Date", text="Creation Date")
    tree.heading("Last Updated", text="Last Updated")
    tree.heading("Priority", text="Priority")
    tree.heading("Category", text="Category")
    

    ##Set the width of each column in the table for the tickets
    column_width = 115
    for col in tree["columns"]:
        tree.column(col, width=column_width)
    ##Displaying the talbe in the ticket window
    tree.grid(row=2, column=0, pady=12, padx=10)

    ##Bind the click event to the on_row_click function so the dispatcher can open and update the ticket
    tree.bind("<ButtonRelease-1>", on_row_click)

    dispatch_window.mainloop()




##Function to retrieve the tickets for the table
def retrieve_tickets(tree):
    ##Create a cursor
    cur = conn.cursor()

    ##Execute the SQL query to get tickets
    get_tickets_query = "SELECT * FROM consumer_tickets"
    cur.execute(get_tickets_query)

    ##Fetch the results
    results = cur.fetchall()

    ##Clear existing data in the Treeview
    for item in tree.get_children():
        tree.delete(item)

    ##Insert data into the Treeview
    for row in results:
        tree.insert("", tk.END, values=row)

    ##Close the cursor
    cur.close()



##The button that calls the function 'dispatch' to start the dispatch process
dispatch_button = ctk.CTkButton(master=root, text="Dispatch", command=dispatch)
dispatch_button.grid(row=1, column=4, pady=12, padx=10)




##The function to perform the queries when searching for a consumer
def perform_search():
    ##Create a cursor
    cur = conn.cursor()

    ##Obtain user inputs from the entry textboxes
    first_name = FirstName.get().strip()
    last_name = LastName.get().strip()
    address = Address.get().strip()
    phone_number = PhoneNumber.get().strip()


    ##Construct the SQL query based on provided values from the call taker
    query = "SELECT * FROM consumer_data WHERE TRUE"
    params = []

    if first_name:
        query += " AND first_name = %s"
        params.append(first_name)
    if last_name:
        query += " AND last_name = %s"
        params.append(last_name)
    if address:
        query += " AND address = %s"
        params.append(address)
    if phone_number:
        query += " AND phone_number = %s"
        params.append(phone_number)


    ##Execute the dynamic SQL query
    cur.execute(query, tuple(params))

    ##Fetch the results
    results = cur.fetchall()


    ##Process the results (for example, display them in a label)
    result_text = "\n".join([str(row) for row in results])
    result_label.configure(text=result_text)


    ##Creating a function for the search button
    def create_ticket():
        ticket_window = ctk.CTk()
        ticket_window.geometry("800x800")
        ticket_window.title(result_text)

        ##Entries for getting the info for the sql table
        description = ctk.CTkEntry(master=ticket_window, placeholder_text="Description", width = 275, height= 275)
        description.grid(row=0, column=0, pady=20, padx=20)
        category = ctk.StringVar(value = "Type:")



        ##Function for creating a the combobox        
        def category_choice(choice):
            category_value = choice
            
            
            ##Inserting the data into the sql table consumer_tickets
            def ticket_insertion():
                if result_text:
                            priority = ""
                            ##Assign priority based on category_value
                            if category_value in ["down lines", "down poles", "fire call"]:
                                priority = "high"
                            elif category_value in ["power out", "flicker"]:
                                priority = "medium"
                            elif category_value in ["member services", "power on", "flicker"]:
                                priority = "low"
                            else:
                                ##Handle other cases if needed
                                priority = "unknown"
                            consumer_id_query_value = result_text[1][0]
                            consumer_id_query = consumer_id_query_value
                            ticket = description.get().strip()
                            ticket_status_insert = "new"
                            ticket_insertion_query = "INSERT INTO consumer_tickets (consumer_id, ticket_status, priority, category, description) VALUES (%s, %s, %s, %s, %s)"
                            ticket_params = (consumer_id_query, ticket_status_insert,  priority, category_value, ticket,)

                            ##Execute the SQL query with parameters
                            cur.execute(ticket_insertion_query, ticket_params)

                            ##Commit the transaction (assuming you are using autocommit=False)
                            conn.commit()

                             ##Close the cursor
                            cur.close()

                            ##Close the window when the ticket is created
                            ticket_window.destroy()

            ##Button that falls the function 'ticket_insertion' that creates the ticket for the consumer
            query_button = ctk.CTkButton(master=ticket_window, text="Create ticket", command=ticket_insertion)
            query_button.grid(row=2, column=0, pady=12, padx=10)


        ##Creating the combobox/drop-menu for assigning the catogry of the ticket
        combobox = ctk.CTkOptionMenu(master=ticket_window, values=["down lines", "down poles", "flicker", "power out", "power on", "fire call", "member services"], command = category_choice, variable=category)
        combobox.grid(row=0, column=2, pady=12, padx=10)


    ##Create the button that calls the function 'create_ticket' that creates the ticket for the user
    make_ticket_button = ctk.CTkButton(root, text="User", command=create_ticket)
    make_ticket_button.grid(row=25, column=1, pady=12, padx=10)
    
    
##Button to trigger the query to search for the consumer
search_button = ctk.CTkButton(master=root, text="Search", command=perform_search)
search_button.grid(row=8, column=0, pady=12, padx=10)


root.mainloop()