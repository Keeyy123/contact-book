import sqlite3
import sys

DB_FILE = "contacts.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def setup_database():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            phone    TEXT,
            email    TEXT,
            group_id INTEGER REFERENCES groups(id)
        )
    """)
    conn.commit()
    conn.close()

def add_group(name):
    conn = get_connection()
    conn.execute("INSERT INTO groups (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    print(f"✅ Added group: {name}")

def list_groups():
    conn = get_connection()
    rows = conn.execute("SELECT id, name FROM groups ORDER BY name").fetchall()
    conn.close()
    if not rows:
        print("No groups yet.")
        return
    print(f"\n{'ID':<5} {'Group Name'}")
    print("-" * 20)
    for row in rows:
        print(f"{row[0]:<5} {row[1]}")
    print()

def assign_group(contact_id, group_id):
    conn = get_connection()
    conn.execute(
        "UPDATE contacts SET group_id=? WHERE id=?",
        (group_id, contact_id)
    )
    conn.commit()
    conn.close()
    print(f"✅ Assigned contact {contact_id} to group {group_id}")

def list_contacts_with_groups():
    conn = get_connection()
    rows = conn.execute("""
        SELECT contacts.id, contacts.name, contacts.phone, contacts.email, 
               COALESCE(groups.name, 'No Group')
        FROM contacts
        LEFT JOIN groups ON contacts.group_id = groups.id
        ORDER BY contacts.name
    """).fetchall()
    conn.close()
    if not rows:
        print("No contacts yet.")
        return
    print(f"\n{'ID':<5} {'Name':<20} {'Phone':<15} {'Email':<25} {'Group'}")
    print("-" * 75)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<15} {row[3]:<25} {row[4]}")
    print()

def add_contact(name, phone="", email=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
        (name, phone, email)
    )
    conn.commit()
    conn.close()
    print(f"✅ Added contact: {name}")

def list_contacts():
    conn = get_connection()
    rows = conn.execute("SELECT id, name, phone, email FROM contacts ORDER BY name").fetchall()
    conn.close()
    if not rows:
        print("No contacts yet. Add one with: python3 contacts.py add 'Name' 'Phone' 'Email'")
        return
    print(f"\n{'ID':<5} {'Name':<20} {'Phone':<15} {'Email'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<15} {row[3]}")
    print()

def search_contacts(query):
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, name, phone, email FROM contacts WHERE name LIKE ?",
        (f"%{query}%",)
    ).fetchall()
    conn.close()
    if not rows:
        print(f"No contacts matching '{query}'")
        return
    print(f"\nResults for '{query}':")
    print(f"{'ID':<5} {'Name':<20} {'Phone':<15} {'Email'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<15} {row[3]}")
    print()

def update_contact(contact_id, name=None, phone=None, email=None):
    conn = get_connection()
    if name:
        conn.execute("UPDATE contacts SET name=? WHERE id=?", (name, contact_id))
    if phone:
        conn.execute("UPDATE contacts SET phone=? WHERE id=?", (phone, contact_id))
    if email:
        conn.execute("UPDATE contacts SET email=? WHERE id=?", (email, contact_id))
    conn.commit()
    conn.close()
    print(f"✏️  Updated contact ID {contact_id}")

def delete_contact(contact_id):
    conn = get_connection()
    conn.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    conn.close()
    print(f"🗑  Deleted contact ID {contact_id}")

def show_help():
    print("""
Contact Book — Commands:
  python3 contacts.py add 'Name' 'Phone' 'Email'  → Add a contact
  python3 contacts.py list                         → Show all contacts
  python3 contacts.py list-groups                 → Show all groups
  python3 contacts.py list-with-groups            → Show contacts with group
  python3 contacts.py search 'Name'               → Search by name
  python3 contacts.py update 1 name 'New Name'    → Update a field
  python3 contacts.py delete 1                    → Delete contact by ID
  python3 contacts.py add-group 'Group Name'      → Add a group
  python3 contacts.py assign 1 2                  → Assign contact to group
""")

if __name__ == "__main__":
    setup_database()

    if len(sys.argv) < 2:
        show_help()
    elif sys.argv[1] == "add" and len(sys.argv) >= 3:
        name  = sys.argv[2]
        phone = sys.argv[3] if len(sys.argv) > 3 else ""
        email = sys.argv[4] if len(sys.argv) > 4 else ""
        add_contact(name, phone, email)
    elif sys.argv[1] == "list":
        list_contacts()
    elif sys.argv[1] == "list-with-groups":
        list_contacts_with_groups()
    elif sys.argv[1] == "search" and len(sys.argv) > 2:
        search_contacts(sys.argv[2])
    elif sys.argv[1] == "update" and len(sys.argv) >= 5:
        contact_id = int(sys.argv[2])
        field      = sys.argv[3]
        value      = sys.argv[4]
        update_contact(contact_id, **{field: value})
    elif sys.argv[1] == "delete" and len(sys.argv) > 2:
        delete_contact(int(sys.argv[2]))
    elif sys.argv[1] == "add-group" and len(sys.argv) > 2:
        add_group(sys.argv[2])
    elif sys.argv[1] == "list-groups":
        list_groups()
    elif sys.argv[1] == "assign" and len(sys.argv) >= 4:
        assign_group(int(sys.argv[2]), int(sys.argv[3]))
    else:
        show_help()
