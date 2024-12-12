import random
from datetime import datetime, timedelta

# # Function to generate a random log entry
# def generate_log_entry(transaction_id):
#     date_time = datetime.now() - timedelta(minutes=random.randint(0, 1000))
#     date_str = date_time.strftime("%Y-%m-%d %H:%M:%S")
#     montant = round(random.uniform(10.00, 5000.00), 2)
#     devise = random.choice(["USD", "EUR", "TND", "GBP"])
#     utilisateur = f"user{random.randint(1, 100):03d}"
#     type_transaction = random.choice(["Achat", "Virement", "Retrait", "Dépôt"])
#     statut = random.choice(["Réussi", "En attente", "Échoué"])
#     return f"{date_str}, TransactionID: {transaction_id}, Montant: {montant}, Devise: {devise}, Utilisateur: {utilisateur}, Type: {type_transaction}, Statut: {statut}"

# # Generate 190 log entries
# log_entries = [generate_log_entry(transaction_id) for transaction_id in range(12345, 12345 + 190)]

# # Write the log entries to a file
# log_file_path = "/home/hp/Bureau/ELK/transaction_logs.log"
# with open(log_file_path, "w") as file:
#     file.write("\n".join(log_entries))

# log_file_path

import csv


# Define the CSV file path
csv_file_path = "/home/hp/Bureau/ELK/transaction_lines.csv"

# Define the CSV header
csv_header = ["TransactionID", "Date", "Heure", "Montant", "Devise", "Utilisateur", "Type", "Statut"]

# Generate CSV rows
csv_rows = []
for transaction_id in range(12345, 12345 + 190):
    date_time = datetime.now() - timedelta(minutes=random.randint(0, 1000))
    date = date_time.strftime("%Y-%m-%d")
    time = date_time.strftime("%H:%M:%S")
    montant = round(random.uniform(10.00, 5000.00), 2)
    devise = random.choice(["USD", "EUR", "TND", "GBP"])
    utilisateur = f"user{random.randint(1, 100):03d}"
    type_transaction = random.choice(["Achat", "Virement", "Retrait", "Dépôt"])
    statut = random.choice(["Réussi", "En attente", "Échoué"])
    csv_rows.append([transaction_id, date, time, montant, devise, utilisateur, type_transaction, statut])

# Write the rows to a CSV file
with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)
    writer.writerows(csv_rows)

csv_file_path

