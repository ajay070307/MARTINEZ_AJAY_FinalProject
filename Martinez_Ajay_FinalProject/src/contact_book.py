"""
Contact Book CLI Application
----------------------------
A simple command-line Contact Book that allows users to add, search, update,
delete, and list contacts. Demonstrates classes/objects, file handling, and
string processing in Python.

Author: <Ajay A. MArtinez>
"""

import os
import json


class Contact:
    """Represents a single contact with name, phone, and email."""

    def __init__(self, name: str, phone: str, email: str):
        self.name = name.strip().title()   # normalize string
        self.phone = phone.strip()
        self.email = email.strip().lower()

    def to_dict(self):
        """Return contact details as a dictionary."""
        return {"name": self.name, "phone": self.phone, "email": self.email}


class ContactBook:
    """Manages a collection of contacts with file persistence."""

    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        """Load contacts from file if it exists."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    self.contacts = [Contact(**c) for c in json.load(f)]
                except json.JSONDecodeError:
                    self.contacts = []

    def save_contacts(self):
        """Save contacts to file."""
        with open(self.filename, "w") as f:
            json.dump([c.to_dict() for c in self.contacts], f, indent=4)

    def add_contact(self, contact: Contact):
        """Add a new contact."""
        self.contacts.append(contact)
        self.save_contacts()

    def list_contacts(self):
        """List all contacts."""
        if not self.contacts:
            print("No contacts found.")
        else:
            for i, c in enumerate(self.contacts, 1):
                print(f"{i}. {c.name} | {c.phone} | {c.email}")

    def search_contact(self, keyword: str):
        """Search contacts by name, phone, or email."""
        keyword = keyword.strip().lower()
        results = [c for c in self.contacts if
                   keyword in c.name.lower() or
                   keyword in c.phone or
                   keyword in c.email]
        return results

    def update_contact(self, name: str, new_phone: str = None, new_email: str = None):
        """Update a contact's phone or email by name."""
        for c in self.contacts:
            if c.name.lower() == name.lower():
                if new_phone:
                    c.phone = new_phone.strip()
                if new_email:
                    c.email = new_email.strip().lower()
                self.save_contacts()
                return True
        return False

    def delete_contact(self, name: str):
        """Delete a contact by name."""
        for c in self.contacts:
            if c.name.lower() == name.lower():
                self.contacts.remove(c)
                self.save_contacts()
                return True
        return False


def menu():
    """CLI menu for the Contact Book application."""
    book = ContactBook()

    while True:
        print("\n--- Contact Book Menu ---")
        print("1. Add Contact")
        print("2. List Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            book.add_contact(Contact(name, phone, email))
            print("Contact added successfully!")

        elif choice == "2":
            book.list_contacts()

        elif choice == "3":
            keyword = input("Enter search keyword: ")
            results = book.search_contact(keyword)
            if results:
                for c in results:
                    print(f"{c.name} | {c.phone} | {c.email}")
            else:
                print("No matching contacts found.")

        elif choice == "4":
            name = input("Enter name to update: ")
            phone = input("New phone (leave blank to skip): ")
            email = input("New email (leave blank to skip): ")
            if book.update_contact(name, phone if phone else None, email if email else None):
                print("Contact updated successfully!")
            else:
                print("Contact not found.")

        elif choice == "5":
            name = input("Enter name to delete: ")
            if book.delete_contact(name):
                print("Contact deleted successfully!")
            else:
                print("Contact not found.")

        elif choice == "6":
            print("Exiting Contact Book. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()
