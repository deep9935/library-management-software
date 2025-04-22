import datetime

# Users and roles
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "student1": {"password": "stud123", "role": "student"}
}

BOOK_FILE = "books.txt"
ISSUE_FILE = "issued.txt"
STUDENT_FILE = "students.txt"

def login():
    print("=== Login ===")
    username = input("Username: ")
    password = input("Password: ")
    user = users.get(username)
    if user and user["password"] == password:
        print(f"Login successful as {user['role'].title()}\n")
        return user["role"]
    print("Invalid credentials\n")
    return None

def add_book():
    with open(BOOK_FILE, "a") as f:
        book_id = input("Book ID: ")
        title = input("Title: ")
        author = input("Author: ")
        f.write(f"{book_id},{title},{author},Available\n")
    print("Book added.\n")

def display_books():
    print("\n--- Book List ---")
    try:
        with open(BOOK_FILE, "r") as f:
            for line in f:
                print(line.strip())
    except FileNotFoundError:
        print("No books found.\n")

def issue_book():
    student_name = input("Enter student name: ")
    book_id = input("Enter Book ID to issue: ")
    today = datetime.date.today()
    due_date = today + datetime.timedelta(days=7)

    with open(BOOK_FILE, "r") as f:
        books = f.readlines()

    for i in range(len(books)):
        parts = books[i].strip().split(",")
        if parts[0] == book_id and parts[3] == "Available":
            books[i] = f"{parts[0]},{parts[1]},{parts[2]},Issued\n"
            with open(BOOK_FILE, "w") as fw:
                fw.writelines(books)
            with open(ISSUE_FILE, "a") as fi:
                fi.write(f"{student_name},{book_id},{today},{due_date}\n")
            print("Book issued successfully.\n")
            return

    print("Book not available or incorrect ID.\n")

def return_book():
    student_name = input("Enter student name: ")
    book_id = input("Enter Book ID to return: ")
    today = datetime.date.today()

    try:
        with open(ISSUE_FILE, "r") as f:
            records = f.readlines()
    except FileNotFoundError:
        print("No issue records found.\n")
        return

    updated_records = []
    found = False

    for record in records:
        name, b_id, issue_date, due_date = record.strip().split(",")
        if name == student_name and b_id == book_id:
            found = True
            due = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
            if today > due:
                days_late = (today - due).days
                fine = days_late * 2
                print(f"Book returned late by {days_late} days. Fine: ₹{fine}")
            else:
                print("Book returned on time. No fine.")
        else:
            updated_records.append(record)

    if found:
        with open(ISSUE_FILE, "w") as f:
            f.writelines(updated_records)

        with open(BOOK_FILE, "r") as f:
            books = f.readlines()
        for i in range(len(books)):
            parts = books[i].strip().split(",")
            if parts[0] == book_id:
                parts[3] = "Available"
                books[i] = ",".join(parts) + "\n"
        with open(BOOK_FILE, "w") as f:
            f.writelines(books)
        print("Return processed.\n")
    else:
        print("No matching issue record found.\n")

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Book")
        print("2. View Books")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Logout")
        choice = input("Enter choice: ")
        if choice == "1":
            add_book()
        elif choice == "2":
            display_books()
        elif choice == "3":
            issue_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def student_menu():
    while True:
        print("\n--- Student Menu ---")
        print("1. View Books")
        print("2. Return Book")
        print("3. Logout")
        choice = input("Enter choice: ")
        if choice == "1":
            display_books()
        elif choice == "2":
            return_book()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    role = login()
    if role == "admin":
        admin_menu()
    elif role == "student":
        student_menu()
