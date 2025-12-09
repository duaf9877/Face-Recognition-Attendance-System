# src/view_attendance.py

from database_handler import get_all_attendance
import os

def display_attendance():
    """Retrieves and prints all attendance records in a formatted way."""
    
    all_records = get_all_attendance()
    
    if not all_records:
        print("[INFO] No attendance records found.")
        return

    print("\n--- Attendance Log ---")
    print("-" * 40)
    # Header for the columns
    print(f"{'Name':<20} | {'Date':<12} | {'Time':<10}")
    print("-" * 40)

    # Loop through each record and print it
    for record in all_records:
        name, date, time, status = record
        print(f"{name:<20} | {date:<12} | {time:<10}")
    
    print("-" * 40)
    print(f"Total Records: {len(all_records)}\n")


# This makes the script runnable
if __name__ == "__main__":
    display_attendance()