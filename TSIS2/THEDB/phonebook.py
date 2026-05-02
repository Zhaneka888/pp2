import sqlite3
import json
import os

_db_path = os.path.join(os.path.dirname(__file__), "phonebook.db")
conn = sqlite3.connect(_db_path)
cur = conn.cursor()
cur.executescript("""
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS phonebook (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        birthday TEXT,
        group_id INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (group_id) REFERENCES groups(id)
    );
""")
conn.commit()
cur = conn.cursor()


#HELPER: GET OR CREATE GROUP
def get_group_id(group_name):
    cur.execute("SELECT id FROM groups WHERE name=?", (group_name,))
    res = cur.fetchone()

    if res:
        return res[0]
    else:
        cur.execute("INSERT INTO groups(name) VALUES (?)", (group_name,))
        conn.commit()
        return cur.lastrowid


#ADD CONTACT
def add_contact():
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group_name = input("Group: ")

    gid = get_group_id(group_name)

    #check if contact exists
    cur.execute("SELECT id FROM phonebook WHERE name=?", (name,))
    existing = cur.fetchone()

    if existing:
        choice = input("Contact exists. overwrite? (yes/no): ")

        if choice.lower() != "yes":
            print("Skipped")
            return

        cur.execute("""
            UPDATE phonebook
            SET phone=?, email=?, birthday=?, group_id=?
            WHERE name=?
        """, (phone, email, birthday, gid, name))

    else:
        cur.execute("""
            INSERT INTO phonebook(name, phone, email, birthday, group_id)
            VALUES (?, ?, ?, ?, ?)
        """, (name, phone, email, birthday, gid))

    conn.commit()
    print("Done!")


#ADD PHONE
def add_phone():
    name = input("Name: ")
    phone = input("New phone: ")

    cur.execute("UPDATE phonebook SET phone=? WHERE name=?", (phone, name))
    conn.commit()


#FILTER BY GROUP
def filter_group():
    group_name = input("Group: ")

    cur.execute("""
        SELECT p.name, p.phone, p.email
        FROM phonebook p
        JOIN groups g ON p.group_id = g.id
        WHERE g.name = ?
    """, (group_name,))

    for row in cur.fetchall():
        print(row)


#SEARCH
def search():
    q = input("Search: ")
    pattern = f"%{q}%"

    cur.execute("""
        SELECT p.name, p.phone, p.email, p.birthday, g.name
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
        WHERE p.name LIKE ? OR p.phone LIKE ? OR p.email LIKE ?
    """, (pattern, pattern, pattern))

    rows = cur.fetchall()

    if not rows:
        print("No results")
    else:
        for row in rows:
            print(row)


#SORT
def sort_contacts():
    field = input("Sort by (name/birthday/created_at): ")

    if field not in ["name", "birthday", "created_at"]:
        field = "name"

    cur.execute(f"SELECT name, phone, email, birthday FROM phonebook ORDER BY {field}")

    for row in cur.fetchall():
        print(row)


#PAGINATION
def paginate():
    limit = 3
    offset = 0

    while True:
        cur.execute("""
            SELECT name, phone, email
            FROM phonebook
            LIMIT ? OFFSET ?
        """, (limit, offset))

        rows = cur.fetchall()

        if not rows:
            print("No more data")
            break

        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        else:
            break


#EXPORT JSON
def export_json():
    cur.execute("""
        SELECT p.name, p.phone, p.email, p.birthday, g.name
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
    """)

    data = []
    for row in cur.fetchall():
        data.append({
            "name": row[0],
            "phone": row[1],
            "email": row[2],
            "birthday": str(row[3]),
            "group": row[4]
        })

    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Exported!")


#IMPORT JSON
def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    for c in data:
        gid = get_group_id(c["group"])

        cur.execute("SELECT id FROM phonebook WHERE name=?", (c["name"],))
        if cur.fetchone():
            choice = input(f"{c['name']} exists (skip/overwrite): ")

            if choice == "skip":
                continue
            else:
                cur.execute("DELETE FROM phonebook WHERE name=?", (c["name"],))

        cur.execute("""
            INSERT INTO phonebook(name, phone, email, birthday, group_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            c["name"], c["phone"], c["email"], c["birthday"], gid
        ))

    conn.commit()
    print("Imported!")

def delete_contact():
    name = input("Enter name to delete: ")

    try:
        cur.execute("DELETE FROM phonebook WHERE name=?", (name,))
        conn.commit()
        print("Deleted successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)


#MENU
def menu():
    while True:
        print("""
1 Add Contact
2 Add Phone
3 Filter by Group
4 Search
5 Sort
6 Pagination
7 Export JSON
8 Import JSON
9 Delete Contact
0 Exit
""")

        ch = input("Choose: ")

        if ch == "1":
            add_contact()
        elif ch == "2":
            add_phone()
        elif ch == "3":
            filter_group()
        elif ch == "4":
            search()
        elif ch == "5":
            sort_contacts()
        elif ch == "6":
            paginate()
        elif ch == "7":
            export_json()
        elif ch == "8":
            import_json()
        elif ch == "9":
            delete_contact()
        else:
            break


menu()