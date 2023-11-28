Power Outage Dispatch System

Overview

This project aims to streamline the process of dispatching linemen for power outage resolution. Traditional methods often involve manually tracking lineman availability in a Word document, leading to inefficient and time-consuming dispatching. This system introduces a more efficient approach by utilizing two distinct pieces of code: one for the dispatcher/call taker and another for the lineman.

Features

Dispatcher/Call Taker Interface
Call Intake: The dispatcher/call taker interface allows for efficient handling of consumer calls regarding power outages.
Ticket Creation: Upon receiving a call, the dispatcher can create a ticket for the outage, capturing essential information.
Ticket Management: The dispatcher can view and manage outage tickets, ensuring a centralized and organized system for tracking power outages.
Lineman Assignment: The dispatcher can assign available linemen directly from the system, eliminating the need for manual coordination.
Lineman Interface
Status Updates: Linemen have a dedicated interface to update their availability status.
Real-time Information: Linemen can access outage details, including contact information, directly from the system.
Database Integration

The system incorporates both relational (PostgreSQL) and non-relational (CouchDB) databases to efficiently manage and store data. This hybrid approach allows for flexibility in handling different types of data and relationships.

PostgreSQL
The relational database is utilized for structured data, such as lineman profiles, outage tickets, and dispatching records.

CouchDB
The non-relational database is employed for storing dynamic and unstructured data, facilitating real-time updates and information retrieval for linemen.

Usage

Dispatcher/Call Taker Interface:
Receive consumer calls and create outage tickets.
Manage and assign linemen to resolve outages.
View real-time updates from linemen.
Lineman Interface:
Update availability status.
Access outage details and contact information directly from the system.

I hope this Power Outage Dispatch System enhances the efficiency of lineman dispatching, ultimately leading to faster outage resolution and improved customer satisfaction. Thank you for using our system!
