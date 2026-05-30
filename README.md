A command-line contact management application built with Python and SQLite, structured with a modular backend architecture. 

## Project Structure
contact-book/
├── app.py        → CLI routing layer
├── models.py     → database functions
├── db.py         → connection and configuration
├── .env          → environment variables
└── contacts.db   → SQLite database
## Features

- Add, list, search, update and delete contacts
- Organize contacts into groups
- View contacts with their assigned group
- Environment-based configuration using .env
- Modular architecture separating routing, logic, and data layers

## Tech Stack

- Python 3
- SQLite3
- python-dotenv

## Setup

```bash
git clone <your-repo-url>
cd contact-book
pip install python-dotenv
python3 app.py
```

## Usage

```bash
python3 app.py add 'Name' 'Phone' 'Email'   # Add a contact
python3 app.py list                          # Show all contacts
python3 app.py list-with-groups             # Show contacts with group
python3 app.py search 'Name'                # Search by name
python3 app.py update 1 name 'New Name'     # Update a field
python3 app.py delete 1                     # Delete contact by ID
python3 app.py add-group 'Group Name'       # Add a group
python3 app.py list-groups                  # Show all groups
python3 app.py assign 1 2                   # Assign contact to group
```

## What I Learned

- Designing relational database schemas with foreign keys
- Writing SQL JOIN queries across multiple tables
- Refactoring a single-file app into a modular three-layer architecture
- Using environment variables for configuration following cloud best practices
- Incremental testing at each stage of development

## Next Steps

- Migrate from SQLite to PostgreSQL
- Connect to AWS RDS Free Tier
- Add IAM-based authentication
 

