import csv
import psycopg2
from config import load_config


def get_connection():
    return psycopg2.connect(**load_config())


def insert_rows(contacts):
    sql = """INSERT INTO phonebook (name, phone) VALUES (%s, %s)"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.executemany(sql, contacts)
                conn.commit()
    except Exception as error:
        print(error)


def csv_reader():
    path = input("Type the path of csv file: ")
    data = []
    try:
        with open(path, "r") as contacts:
            reader = csv.reader(contacts)
            for row in reader:
                if len(row) >= 2:
                    data.append((row[0].strip(), row[1].strip()))
        insert_rows(data)
        print("Contact(s) added")
    except FileNotFoundError:
        print("File not found")


def console_reader():
    row = input("Enter name and phone (name,phone): ").split(",")
    if len(row) == 2:
        insert_rows([(row[0].strip(), row[1].strip())])
        print("Contact added")
    else:
        print("Invalid format. Use: name,phone")


def update_contact():
    choice = input("What do you want to update (name/phone): ")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if choice == "name":
                    old_phone = input("Enter contact phone: ")
                    cur.execute("SELECT id FROM phonebook WHERE phone = %s", (old_phone,))
                    if cur.fetchone() is None:
                        print("Contact not found")
                        return
                    new_name = input("Enter new name: ")
                    cur.execute("UPDATE phonebook SET name = %s WHERE phone = %s", (new_name, old_phone))
                    conn.commit()
                    print("Name updated")
                elif choice == "phone":
                    old_phone = input("Enter old phone: ")
                    cur.execute("SELECT id FROM phonebook WHERE phone = %s", (old_phone,))
                    if cur.fetchone() is None:
                        print("Contact not found")
                        return
                    new_phone = input("Enter new phone: ")
                    cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s", (new_phone, old_phone))
                    conn.commit()
                    print("Phone updated")
                else:
                    print("Invalid choice")
    except Exception as error:
        print(error)


def search_contact():
    choice = input("Search by name or phone prefix? (name/phone): ")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if choice == "name":
                    name = input("Enter name: ")
                    cur.execute("SELECT id, name, phone FROM phonebook WHERE name ILIKE %s", (f"%{name}%",))
                elif choice == "phone":
                    prefix = input("Enter phone prefix (e.g. +7, +1): ")
                    cur.execute("SELECT id, name, phone FROM phonebook WHERE phone LIKE %s", (f"{prefix}%",))
                else:
                    print("Invalid choice")
                    return
                rows = cur.fetchall()
                if not rows:
                    print("No contacts found")
                    return
                for id, name, phone in rows:
                    print(id, name.strip(), phone)
    except Exception as error:
        print(error)


def delete_contact():
    choice = input("Delete by name or phone? (name/phone): ")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if choice == "name":
                    name = input("Enter name: ")
                    cur.execute("SELECT id FROM phonebook WHERE name = %s", (name,))
                    if cur.fetchone() is None:
                        print("Contact not found")
                        return
                    cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
                elif choice == "phone":
                    phone = input("Enter phone: ")
                    cur.execute("SELECT id FROM phonebook WHERE phone = %s", (phone,))
                    if cur.fetchone() is None:
                        print("Contact not found")
                        return
                    cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
                else:
                    print("Invalid choice")
                    return
                conn.commit()
                print("Contact(s) deleted")
    except Exception as error:
        print(error)


def main():
    while True:
        print("\n=== Phonebook ===")
        print("1 - Add from CSV")
        print("2 - Add manually")
        print("3 - Update contact")
        print("4 - Search contact")
        print("5 - Delete contact")
        print("0 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            csv_reader()
        elif choice == "2":
            console_reader()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

