#College Event Management and Registration System

#Key Features:
#Admin panel to create and manage events
#Participant registration form
#View registered participants
#Export participant list to CSV
#Dashboard showing event statistics

import streamlit as st
import pandas as pd
import sqlite3

st.title("College Event Management and Registration System")

conn = sqlite3.connect('event.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS events
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        time TEXT,
        location TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS participants
          (id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT,
          email TEXT,
          phone INTEGER,
          event_id INTEGER,
          year INTEGER,
          FOREIGN KEY (event_id) REFERENCES events (id))''')

conn.commit()
conn.close()

def create_event():
    st.header("Create Event")
    name = st.text_input("Event Name")
    date = st.text_input("Date (YYYY-MM-DD)")
    time = st.text_input("Time (HH:MM)")
    location = st.text_input("Location")

    if st.button("Create"):
        conn = sqlite3.connect('event.db')
        c = conn.cursor()
        c.execute("INSERT INTO events (name, date, time, location) VALUES (?, ?, ?, ?)", (name, date, time, location))
        conn.commit()
        conn.close()
        st.success("Event created successfully!")

def view_events():
    st.header("View Events")

    conn = sqlite3.connect('event.db')
    c = conn.cursor()
    c.execute("SELECT * FROM events")
    events = c.fetchall()
    conn.close()

    if events:
        df = pd.DataFrame(events, columns=["ID", "Name", "Date", "Time", "Location"])
        st.dataframe(df)
    else:
        st.write("No events found.")

#register participants
def register_participant():
    st.header("Register Participant")

    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    event_id = st.number_input("Event ID")
    year = st.number_input("Year")

    if st.button("Register"):
        conn = sqlite3.connect('event.db')
        c = conn.cursor()
        c.execute("INSERT INTO participants (name, email, phone, event_id, year) VALUES (?, ?, ?, ?, ?)", (name, email, phone, event_id, year))
        conn.commit()
        conn.close()
        st.success("Participant registered successfully!")

#View registered participants
def view_participants():
    st.header("View Participants")

    conn = sqlite3.connect('event.db')
    c = conn.cursor()
    c.execute("SELECT * FROM participants")
    participants = c.fetchall()
    conn.close()

    if participants:
        df = pd.DataFrame(participants, columns=["ID", "Name", "Email", "Phone", "Event ID", "Year"])
        st.dataframe(df)
    else:
        st.write("No participants found.")

#export csv data
def export_participants():
    st.header("Export Participants")

    conn = sqlite3.connect('event.db')
    c = conn.cursor()
    c.execute("SELECT * FROM participants")
    participants = c.fetchall()
    conn.close()

    if participants:
        df = pd.DataFrame(participants, columns=["ID", "Name", "Email", "Phone", "Event ID", "Year"])
        csv_data = df.to_csv(index=False)
        st.download_button("Download CSV", csv_data, file_name="participants.csv")
    else:
        st.write("No participants found.")


#Dashboard showing event statistics
def view_stats():
    st.header("Event Statistics")

    conn = sqlite3.connect('event.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM events")
    num_events = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM participants")
    num_participants = c.fetchone()[0]
    conn.close()

    st.write(f"Number of Events: {num_events}")
    st.write(f"Number of Participants: {num_participants}")

#main function
def main():
    st.sidebar.title("Features")
    pages = {
        "Create Event": create_event,
        "View Events": view_events,
        "Register Participant": register_participant,
        "View Participants": view_participants,
        "Export Participants": export_participants,
        "View Statistics": view_stats
    }
    selected_page = st.sidebar.selectbox("Select a page", list(pages.keys()))
    pages[selected_page]()

if __name__ == "__main__":
    main()
