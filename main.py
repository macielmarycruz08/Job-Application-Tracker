from job_tracker_database import create_database
from gui import start_gui

if __name__ == "__main__":
    create_database()  # Ensure the database exists
    start_gui()        # Launch the GUI
