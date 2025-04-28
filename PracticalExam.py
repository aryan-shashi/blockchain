# Save this file as app.py
import streamlit as st
import hashlib
import datetime

class LibraryLedger:
    def __init__(self):
        if 'ledger' not in st.session_state:
            st.session_state['ledger'] = []

    def generate_hash(self, book_id, member_id, date_issued):
        hash_input = f"{book_id}{member_id}{date_issued}".encode()
        return hashlib.sha256(hash_input).hexdigest()

    def issue_book(self, book_title, book_id, member_name, member_id):
        date_issued = datetime.date.today()
        due_date = date_issued + datetime.timedelta(days=14)
        transaction_id = self.generate_hash(book_id, member_id, date_issued)

        record = {
            'Transaction ID': transaction_id,
            'Date Issued': str(date_issued),
            'Book Title': book_title,
            'Book ID': book_id,
            'Issued To': member_name,
            'Member ID': member_id,
            'Due Date': str(due_date),
            'Date Returned': None,
            'Remarks': 'Not yet returned'
        }

        st.session_state['ledger'].append(record)
        st.success(f"Book issued! Transaction ID: {transaction_id}")

    def return_book(self, transaction_id):
        for record in st.session_state['ledger']:
            if record['Transaction ID'] == transaction_id:
                record['Date Returned'] = str(datetime.date.today())
                record['Remarks'] = 'Returned'
                st.success(f"Book returned for Transaction ID: {transaction_id}")
                return
        st.error("Transaction ID not found.")

    def display_ledger(self):
        if st.session_state['ledger']:
            st.dataframe(st.session_state['ledger'])
        else:
            st.info("No records found in the ledger.")

# Initialize Ledger
ledger = LibraryLedger()

st.title("📚 Library Book Issuing Ledger with Hashing")

menu = st.sidebar.selectbox("Menu", ["Issue Book", "Return Book", "View Ledger"])

if menu == "Issue Book":
    st.subheader("Issue a Book")
    book_title = st.text_input("Book Title")
    book_id = st.text_input("Book ID")
    member_name = st.text_input("Member Name")
    member_id = st.text_input("Member ID")

    if st.button("Issue Book"):
        if book_title and book_id and member_name and member_id:
            ledger.issue_book(book_title, book_id, member_name, member_id)
        else:
            st.warning("Please fill all fields.")

elif menu == "Return Book":
    st.subheader("Return a Book")
    transaction_id = st.text_input("Transaction ID")

    if st.button("Return Book"):
        if transaction_id:
            ledger.return_book(transaction_id)
        else:
            st.warning("Please enter a Transaction ID.")

elif menu == "View Ledger":
    st.subheader("Ledger Records")
    ledger.display_ledger()
