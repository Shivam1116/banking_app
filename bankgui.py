import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont

class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds."""
    pass

class Account:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(f"Insufficient funds. Available balance: {self.balance}.")
        elif amount > 0:
            self.balance -= amount
        else:
            raise ValueError("Withdrawal amount must be positive.")

    def get_balance(self):
        return self.balance

    def display_account_info(self):
        return f"Account Number: {self.account_number}\nAccount Holder: {self.account_holder}\nBalance: {self.balance}"

class BankingSystem:
    def __init__(self, root):
        self.accounts = {}
        self.root = root
        self.root.title("Banking System")
        self.root.geometry("400x400")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Create Account", font=("Arial", 12, "bold"), fg="blue").pack(pady=5)
        self.create_account_frame = tk.Frame(self.root)
        self.create_account_frame.pack(pady=5)
        
        self.acc_num_entry = self.create_entry(self.create_account_frame, "Account Number:", 0)
        self.acc_holder_entry = self.create_entry(self.create_account_frame, "Account Holder:", 1)
        self.initial_balance_entry = self.create_entry(self.create_account_frame, "Initial Balance:", 2)
        
        tk.Button(self.create_account_frame, text="Create Account", command=self.create_account, fg="white", bg="green").grid(row=3, columnspan=2, pady=5)
        
        tk.Label(self.root, text="Transactions", font=("Arial", 12, "bold"), fg="blue").pack(pady=5)
        self.transaction_frame = tk.Frame(self.root)
        self.transaction_frame.pack(pady=5)
        
        self.trans_acc_num_entry = self.create_entry(self.transaction_frame, "Account Number:", 0)
        self.amount_entry = self.create_entry(self.transaction_frame, "Amount:", 1)
        
        tk.Button(self.transaction_frame, text="Deposit", command=self.deposit, fg="white", bg="green").grid(row=2, column=0, pady=5)
        tk.Button(self.transaction_frame, text="Withdraw", command=self.withdraw, fg="white", bg="red").grid(row=2, column=1, pady=5)
        
        tk.Label(self.root, text="Account Info", font=("Arial", 12, "bold"), fg="blue").pack(pady=5)
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=5)
        
        self.info_acc_num_entry = self.create_entry(self.info_frame, "Account Number:", 0)
        tk.Button(self.info_frame, text="Display Info", command=self.display_info, fg="white", bg="green").grid(row=1, columnspan=2, pady=5)
    
    def create_entry(self, frame, label_text, row):
        tk.Label(frame, text=label_text).grid(row=row, column=0, padx=5, pady=2, sticky='w')
        entry = tk.Entry(frame)
        entry.grid(row=row, column=1, padx=5, pady=2)
        return entry
    
    def create_account(self):
        acc_num = self.acc_num_entry.get().strip()
        acc_holder = self.acc_holder_entry.get().strip()
        try:
            initial_balance = float(self.initial_balance_entry.get().strip() or 0)
        except ValueError:
            self.show_custom_messagebox("Error", "Invalid balance amount!")
            return
        
        if acc_num and acc_holder:
            self.accounts[acc_num] = Account(acc_num, acc_holder, initial_balance)
            self.show_custom_messagebox("Success", "Account created successfully!")
        else:
            self.show_custom_messagebox("Error", "Account number and holder name cannot be empty!")
    
    def deposit(self):
        acc_num = self.trans_acc_num_entry.get().strip()
        try:
            amount = float(self.amount_entry.get().strip())
        except ValueError:
            self.show_custom_messagebox("Error", "Invalid deposit amount!")
            return
        
        if acc_num in self.accounts:
            try:
                self.accounts[acc_num].deposit(amount)
                self.show_custom_messagebox("Success", f"Deposited {amount}. New balance: {self.accounts[acc_num].get_balance()}.")
            except ValueError as e:
                self.show_custom_messagebox("Error", str(e))
        else:
            self.show_custom_messagebox("Error", "Account not found!")
    
    def withdraw(self):
        acc_num = self.trans_acc_num_entry.get().strip()
        try:
            amount = float(self.amount_entry.get().strip())
        except ValueError:
            self.show_custom_messagebox("Error", "Invalid withdrawal amount!")
            return
        
        if acc_num in self.accounts:
            try:
                self.accounts[acc_num].withdraw(amount)
                self.show_custom_messagebox("Success", f"Withdrew {amount}. New balance: {self.accounts[acc_num].get_balance()}.")
            except (InsufficientFundsError, ValueError) as e:
                self.show_custom_messagebox("Error", str(e))
        else:
            self.show_custom_messagebox("Error", "Account not found!")
    
    def display_info(self):
        acc_num = self.info_acc_num_entry.get().strip()
        if acc_num in self.accounts:
            self.show_custom_messagebox("Account Info", self.accounts[acc_num].display_account_info())
        else:
            self.show_custom_messagebox("Error", "Account not found!")

    def show_custom_messagebox(self, title, message):
        custom_font = tkFont.Font(family="Arial", size=16)  # Increased font size to 16
        top = tk.Toplevel(self.root)
        top.title(title)
        top.geometry("600x400")  # Increased the size of the messagebox
        tk.Label(top, text=message, font=custom_font, wraplength=350).pack(pady=20)  # Increased wraplength
        tk.Button(top, text="OK", command=top.destroy, font=custom_font).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingSystem(root)
    root.mainloop()
