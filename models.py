from db import get_connection

def add_group(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO groups (name) VALUES (%s)", (name,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Added group: {name}")

def list_groups():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM groups ORDER BY name")
    rows = cur.fetchall()
    cur.close()
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
    cur = conn.cursor()
    cur.execute(
        "UPDATE contacts SET group_id=%s WHERE id=%s",
        (group_id, contact_id)
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Assigned contact {contact_id} to group {group_id}")

def add_contact(name, phone="", email=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s)",
        (name, phone, email)
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Added contact: {name}")

def list_contacts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, phone, email FROM contacts ORDER BY name")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        print("No contacts yet.")
        return
    print(f"\n{'ID':<5} {'Name':<20} {'Phone':<15} {'Email'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<15} {row[3]}")
    print()

def list_contacts_with_groups():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT contacts.id, contacts.name, contacts.phone, contacts.email,
               COALESCE(groups.name, 'No Group')
        FROM contacts
        LEFT JOIN groups ON contacts.group_id = groups.id
        ORDER BY contacts.name
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        print("No contacts yet.")
        return
    print(f"\n{'ID':<5} {'Name':<20} {'Phone':<15} {'Email':<25} {'Group'}")
    print("-" * 75)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<15} {row[3]:<25} {row[4]}")
    print()

def search_contacts(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, phone, email FROM contacts WHERE name ILIKE %s",
        (f"%{query}%",)
    )
    rows = cur.fetchall()
    cur.close()
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
    cur = conn.cursor()
    if name:
        cur.execute("UPDATE contacts SET name=%s WHERE id=%s", (name, contact_id))
    if phone:
        cur.execute("UPDATE contacts SET phone=%s WHERE id=%s", (phone, contact_id))
    if email:
        cur.execute("UPDATE contacts SET email=%s WHERE id=%s", (email, contact_id))
    conn.commit()
    cur.close()
    conn.close()
    print(f"✏️  Updated contact ID {contact_id}")

def delete_contact(contact_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id=%s", (contact_id,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"🗑  Deleted contact ID {contact_id}")

