import hashlib
import datetime

class LibraryLedger:
    def __init__(self):
        self.ledger = []

    def generate_hash(self, book_id, member_id, date_issued):
        hash_input = f"{book_id}{member_id}{date_issued}".encode()
        return hashlib.sha256(hash_input).hexdigest()

    def issue_book(self, book_title, book_id, member_name, member_id):
        date_issued = datetime.date.today()
        due_date = date_issued + datetime.timedelta(days=14)  # 2 weeks loan period
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

        self.ledger.append(record)
        print(f"Book issued! Transaction ID: {transaction_id}")

    def return_book(self, transaction_id):
        for record in self.ledger:
            if record['Transaction ID'] == transaction_id:
                record['Date Returned'] = str(datetime.date.today())
                record['Remarks'] = 'Returned'
                print(f"Book returned for Transaction ID: {transaction_id}")
                return
        print("Transaction ID not found.")

    def display_ledger(self):
        for record in self.ledger:
            print(record)
            print('-' * 50)

# Example usage
ledger = LibraryLedger()

# Issue books
ledger.issue_book("Pride and Prejudice", "BK1001", "Alice Johnson", "M102")
ledger.issue_book("1984", "BK1002", "Mark Spencer", "M089")

# Display current ledger
ledger.display_ledger()

# Simulate a book return (copy Transaction ID from previous output)
# ledger.return_book("paste_transaction_id_here")
# ledger.display_ledger()
