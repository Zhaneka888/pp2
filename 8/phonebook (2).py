import psycopg2
from config import load_config


def get_connection():
    return psycopg2.connect(**load_config())


def create_functions_and_procedures():
    for filename in ("functions.sql", "procedures.sql"):
        with open(filename, "r") as f:
            sql = f.read()
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()


def search_contact():
    pattern = input("Enter name or phone to search: ")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
                rows = cur.fetchall()
                if not rows:
                    print("No contacts found")
                    return
                for row in rows:
                    print(row[0], row[1], row[2])
    except Exception as error:
        print(error)


def upsert_contact():
    name  = input("Enter name: ")
    phone = input("Enter phone (+7XXXXXXXXXX): ")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
                conn.commit()
                print("Contact saved")
    except Exception as error:
        print(error)


def insert_many_contacts():
    print("Enter contacts one by one. Type 'done' when finished.")
    names  = []
    phones = []
    while True:
        name = input("  Name (or 'done'): ")
        if name.lower() == "done":
            break
        phone = input("  Phone: ")
        names.append(name)
        phones.append(phone)
    if not names:
        print("Nothing to insert")
        return
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL insert_many_contacts(%s::VARCHAR[], %s::VARCHAR[])",
                    (names, phones)
                )
                cur.execute("SELECT name, phone, reason FROM invalid_contacts")
                invalid = cur.fetchall()
                conn.commit()
                if invalid:
                    print("Invalid contacts:")
                    for row in invalid:
                        print(f"  {row[0]} | {row[1]} | {row[2]}")
                else:
                    print("All contacts inserted")
    except Exception as error:
        print(error)


def show_paginated():
    try:
        page_size = int(input("Contacts per page: "))
        page_num  = int(input("Page number: "))
    except ValueError:
        print("Enter a number")
        return
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM get_contacts_paginated(%s, %s)",
                    (page_size, page_num)
                )
                rows = cur.fetchall()
                if not rows:
                    print("No contacts on this page")
                    return
                for row in rows:
                    print(row[0], row[1], row[2])
    except Exception as error:
        print(error)


def delete_contact():
    value = input("Enter name or phone to delete: ")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact(%s)", (value,))
                conn.commit()
                print("Done")
    except Exception as error:
        print(error)


def main():
    create_functions_and_procedures()
    while True:
        print("\n=== Phonebook ===")
        print("1 - Search contact")
        print("2 - Add / Update one contact")
        print("3 - Add many contacts")
        print("4 - Show contacts (paginated)")
        print("5 - Delete contact")
        print("0 - Exit")
        choice = input("Choose: ")
        if choice == "1":
            search_contact()
        elif choice == "2":
            upsert_contact()
        elif choice == "3":
            insert_many_contacts()
        elif choice == "4":
            show_paginated()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
