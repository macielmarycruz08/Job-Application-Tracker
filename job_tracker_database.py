import sqlite3
import csv

def create_database():
    conn = sqlite3.connect('job_tracker.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS JobApplications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT NOT NULL,
        company TEXT NOT NULL,
        application_date TEXT NOT NULL,
        status TEXT NOT NULL,
        notes TEXT
    )''')
    conn.close()

def add_application(job_title, company, application_date, status, notes):
    conn = sqlite3.connect('job_tracker.db')
    conn.execute("INSERT INTO JobApplications (job_title, company, application_date, status, notes) VALUES (?, ?, ?, ?, ?)",
                 (job_title, company, application_date, status, notes))
    conn.commit()
    conn.close()

def view_applications():
    conn = sqlite3.connect('job_tracker.db')
    cursor = conn.execute("SELECT * FROM JobApplications")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_application(app_id, job_title, company, application_date, status, notes):
    conn = sqlite3.connect('job_tracker.db')
    conn.execute("UPDATE JobApplications SET job_title=?, company=?, application_date=?, status=?, notes=? WHERE id=?",
                 (job_title, company, application_date, status, notes, app_id))
    conn.commit()
    conn.close()

def delete_application(app_id):
    conn = sqlite3.connect('job_tracker.db')
    conn.execute("DELETE FROM JobApplications WHERE id=?", (app_id,))
    conn.commit()
    conn.close()

def export_to_csv(filename):
    rows = view_applications()
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Job Title", "Company", "Date", "Status", "Notes"])
        writer.writerows(rows)

def import_from_csv(filename):
    conn = sqlite3.connect('job_tracker.db')
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            conn.execute("INSERT INTO JobApplications (job_title, company, application_date, status, notes) VALUES (?, ?, ?, ?, ?)",
                         (row['Job Title'], row['Company'], row['Date'], row['Status'], row['Notes']))
    conn.commit()
    conn.close()
