import requests
from bs4 import BeautifulSoup
import os
import time

tracked_courses = []

# Function to start tracking a course based on user input
def start_tracking():
    keep_adding = "yes"
    while keep_adding == "yes":
        dept = input("Department (e.g., COMM): ")
        course = input("Course (e.g., 393): ")
        section = input("Section (e.g., 101): ")
        check_restricted = input("Do you want to check both general and restricted seats? (yes/no): ").lower()

        while check_restricted not in ["yes", "no"]:
            check_restricted = input("Invalid input. Please enter 'yes' or 'no': ").lower()

        if (dept, course, section, check_restricted) in tracked_courses:
            print("This course is already being tracked.")
        else:
            tracked_courses.append((dept, course, section, check_restricted))
            print("Course added to tracking list.")
        
        print("Current tracking list: ")
        for course in tracked_courses:
            print(course[0] + " " + course[1] + " " + course[2] + "")
        
        keep_adding = input("Do you want to track another course? (yes/no): ")

# Function to stop tracking a course
def stop_tracking():
    keep_removing = "yes"
    while keep_removing == "yes":
        dept = input("Department (e.g., COMM): ")
        course = input("Course (e.g., 393): ")
        section = input("Section (e.g., 101): ")
        check_restricted = input("Are you tracking both general and restricted seats? (yes/no): ").lower()
        
        while check_restricted not in ["yes", "no"]:
            check_restricted = input("Invalid input. Please enter 'yes' or 'no': ").lower()

        if (dept, course, section, check_restricted) in tracked_courses:
            tracked_courses.remove((dept, course, section, check_restricted))
            print("Course removed from tracking list.")
        else:
            print("This course is not being tracked.")

        print("Current tracking list: ")
        for course in tracked_courses:
            print(course[0] + " " + course[1] + " " + course[2] + "")
        
        keep_removing = input("Do you want to stop tracking another course? (yes/no): ")

# Function to scrape course availability
def scrape_course_availability(dept, course, section, check_restricted):
    url = f"https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept={dept}&course={course}&section={section}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        strong = soup.find_all('strong')
        
        if len(strong) > 1:
            general = int(strong[len(strong)-2].text)
            restricted = int(strong[len(strong)-1].text)

            if (general > 0 or (check_restricted == "yes" and restricted > 0)):
                title = "Course Available"
                message = f"A seat is available for {dept} {course} {section}!"
                send_notification(title, message)
                tracked_courses.remove((dept, course, section, check_restricted))

        else:
            print("Course not found.")
            tracked_courses.remove((dept, course, section, check_restricted))
    else:
        print("Failed to retrieve course information. Status code:", response.status_code)
        tracked_courses.remove((dept, course, section, check_restricted))

# Function to send a desktop notification
def send_notification(title, message):
    os.system(f"osascript -e 'display notification \"{message}\" with title \"{title}\"'")

# Main
if __name__ == "__main__":
    print("Enter the course you want to track: ")
    start_tracking()
        
    while len(tracked_courses) > 0:
        for course in tracked_courses:
            scrape_course_availability(course[0], course[1], course[2], course[3])

        stop_tracking_option = input("Do you want to stop tracking any courses? (yes/no): ")
        if stop_tracking_option.lower() == "yes":
            stop_tracking()
        
        start_tracking_option = input("Do you want to start tracking any other courses? (yes/no): ")
        if start_tracking_option.lower() == "yes":
            start_tracking()
        
        time.sleep(900)