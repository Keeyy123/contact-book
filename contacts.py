import sqlite3
import sys

DB_FILE = "contacts.db"

def get_connection():
    """Open a connection to the SQLite database file."""
    return sqlite3.connect(DB_FILE)

def setup_database():
    """Create the contacts table if it doesn't exist yet."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            phone TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_contact(name, phone="", email=""):
    """Insert a new contact into the database."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
        (name, phone, email)
    )
    conn.commit()
    conn.close()
    print(f"✅ Added contact: {name}")

def list_contacts():
    """Print every contact in the database."""
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
    """Search contacts by name (case-insensitive partial match)."""
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
    """Update one or more fields for a contact by ID."""
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
    """Delete a contact permanently by ID."""
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
  python3 contacts.py search 'Name'               → Search by name
  python3 contacts.py update 1 name 'New Name'    → Update a field
  python3 contacts.py delete 1                    → Delete contact by ID
""")

# --- Entry point ---
if __name__ == "__main__":
    setup_database()  # Always run first — creates table if needed

    if len(sys.argv) < 2:
        show_help()

    elif sys.argv[1] == "add" and len(sys.argv) >= 3:
        name  = sys.argv[2]
        phone = sys.argv[3] if len(sys.argv) > 3 else ""
        email = sys.argv[4] if len(sys.argv) > 4 else ""
        add_contact(name, phone, email)

    elif sys.argv[1] == "list":
        list_contacts()

    elif sys.argv[1] == "search" and len(sys.argv) > 2:
        search_contacts(sys.argv[2])

    elif sys.argv[1] == "update" and len(sys.argv) >= 5:
        contact_id = int(sys.argv[2])
        field      = sys.argv[3]
        value      = sys.argv[4]
        update_contact(contact_id, **{field: value})

    elif sys.argv[1] == "delete" and len(sys.argv) > 2:
        delete_contact(int(sys.argv[2]))

    else:
        show_help()