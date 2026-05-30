import sys
from db import setup_database
from models import (
    add_contact, list_contacts, list_contacts_with_groups,
    search_contacts, update_contact, delete_contact,
    add_group, list_groups, assign_group
)

def show_help():
    print("""
Contact Book — Commands:
  python3 app.py add 'Name' 'Phone' 'Email'   -> Add a contact
  python3 app.py list                          -> Show all contacts
  python3 app.py list-with-groups             -> Show contacts with group
  python3 app.py search 'Name'                -> Search by name
  python3 app.py update 1 name 'New Name'     -> Update a field
  python3 app.py delete 1                     -> Delete contact by ID
  python3 app.py add-group 'Group Name'       -> Add a group
  python3 app.py list-groups                  -> Show all groups
  python3 app.py assign 1 2                   -> Assign contact to group
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

