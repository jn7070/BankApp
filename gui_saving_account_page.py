import tkinter as tk
from tkinter import ttk
from tkinter import *
import pymysql
import gui_login_page
import customer
import gui_account_deposit
import gui_account_withdraw
import tkinter.messagebox

#
# SavingAccountPage: provides interface to work with saving account.
#
class SavingAccountPage(tk.Frame):

    def cleanup_ui(self):
        self.available_balance.set(0.0)
        for i in self.treev.get_children():
            self.treev.delete(i)   # remove all items from the treeview

    def set_data(self, share_data):
        self.cleanup_ui()
        self.share_data = share_data

        # query database
        # update UI elements
        self.controller.title('Bank - Saving Account')

        try:
            result = customer.get_savings_info_by_id(self.share_data.cnx, self.share_data.customer_id)
            if result == None:
                tkinter.messagebox.showerror(title="No Savings Account", message="Please open a new account.",
                                             parent=self.controller)
                self.controller.show_frame(self.back_go_page_name , self.share_data, gui_login_page.LoginPage)
                return
            self.account_name.set(result['name'])
            self.account_no = result['accountNo']
            self.available_balance.set(result['balance'])
            self.annual_interest_rate.set(str(result['annualInterestRate']*100)+'%')
            self.annual_minimum_balance.set(result['minBalance'])
            self.withdraw_limit.set(result['withdrawalLimit'])
            self.share_data.account_name = result['name']
            self.share_data.account_no = result['accountNo']
            self.share_data.account_type = 'Savings'
        except pymysql.Error as e:
            tkinter.messagebox.showerror(title="Data Error", message=e.args[1], parent=self.controller)

        try:
            rows = customer.get_transactions(self.share_data.cnx, result['accountNo'])
            for row in rows:
                self.treev.insert("", 'end', values=(row['transactionNo'], row['date'], row['amount'],
                                                     row['curBalance']))
        except pymysql.Error as e:
            tkinter.messagebox.showerror(title="Data Error", message=e.args[1], parent=self.controller)

    def get_size(self):
        return '600x430'

    def set_go_back_page(self, back_go_page_name):
        self.back_go_page_name = back_go_page_name

    def update_account_name_button(self):
        try:
            customer.update_account_name(self.share_data.cnx, self.share_data.customer_id,
                                                  self.account_name.get(), 'Savings')
        except pymysql.Error as e:
            tkinter.messagebox.showerror(title="Account Name Error", message=e.args[1], parent=self.controller)

    def close_account_button(self):
        # perform close account
        try:
            customer.close_individual_account(self.share_data.cnx, self.share_data.account_no)
        except pymysql.Error as e:
            tkinter.messagebox.showerror(title="Close Account Error", message=e.args[1], parent=self.controller)
            return

        tkinter.messagebox.showinfo(title="Checking Account", message="Account Closed.",
                                         parent=self.controller)
        self.controller.show_frame(self.back_go_page_name , self.share_data, gui_login_page.LoginPage)

    def deposit_button(self):
        self.share_data.account_no = self.account_no
        self.share_data.account_name = self.account_name.get()
        self.share_data.account_type = 'Savings'
        self.controller.show_frame(gui_account_deposit.AccountDepositPage, self.share_data, SavingAccountPage)


    def withdraw_button(self):
        self.share_data.account_no = self.account_no
        self.share_data.account_name = self.account_name.get()
        self.share_data.account_type = 'Savings'
        self.controller.show_frame(gui_account_withdraw.AccountWithdrawPage, self.share_data, SavingAccountPage)


    def cancel_button(self):
        self.controller.show_frame(self.back_go_page_name, self.share_data, gui_login_page.LoginPage)

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda _col=col: self.treeview_sort_column(tv, _col, not reverse))

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.share_data = None
        self.back_go_page_name = None
        self.controller = controller
        self.account_no = -1


        # Account Name
        row = 0
        tk.Label(self, text="Account Name").grid(row=row, column=0)
        self.account_name = tk.StringVar()
        tk.Entry(self, textvariable=self.account_name).grid(row=row, column=1)
        tk.Button(self, text="Update", command=self.update_account_name_button).grid(row=row, column=2)

        # Available Balance
        row += 1
        tk.Label(self, text="Available Balance").grid(row=row, column=0)
        self.available_balance = tk.DoubleVar()
        tk.Entry(self, textvariable=self.available_balance, state='disabled').grid(row=row, column=1)

        # Annual Interest Rate
        row += 1
        tk.Label(self, text="Annual Interest Rate").grid(row=row, column=0)
        self.annual_interest_rate = tk.StringVar()
        tk.Entry(self, textvariable=self.annual_interest_rate, state='disabled').grid(row=row, column=1)

        # Annual Minimum Balance
        row += 1
        tk.Label(self, text="Minimum Balance").grid(row=row, column=0)
        self.annual_minimum_balance = tk.StringVar()
        tk.Entry(self, textvariable=self.annual_minimum_balance, state='disabled').grid(row=row, column=1)

        # Withdraw Limit
        row += 1
        tk.Label(self, text="Withdraw Limit").grid(row=row, column=0)
        self.withdraw_limit = tk.StringVar()
        tk.Entry(self, textvariable=self.withdraw_limit, state='disabled').grid(row=row, column=1)

        row += 1
        # Transaction Tree Column
        rows_count = 15
        ListFrame = tk.Frame(self, bg="white")
        ListFrame.grid(row=row, column=0, rowspan=rows_count, columnspan=5, sticky=W+E+N+S)

        # Using treeview widget
        columns = ("transactionNo", "date", "amount", 'balance')
        self.treev = ttk.Treeview(ListFrame, selectmode='browse', show='headings', columns=columns)

        # Calling pack method w.r.to treeview
        self.treev.pack(side='left')

        # Constructing vertical scrollbar
        # with treeview
        verscrlbar = ttk.Scrollbar(ListFrame,
                                   orient="vertical",
                                   command=self.treev.yview)

        # Calling pack method w.r.to verical
        # scrollbar
        verscrlbar.pack(side='left', fill='x')

        # Configuring treeview
        self.treev.configure(xscrollcommand=verscrlbar.set)

        for col in columns:
            self.treev.heading(col, text=col,
                               command=lambda _col=col: self.treeview_sort_column(self.treev, _col, False))

        # Assigning the width and anchor to  the
        # respective columns
        self.treev.column("transactionNo", width=90, anchor='c')
        self.treev.column("date", width=110, anchor='se')
        self.treev.column("amount", width=110, anchor='se')
        self.treev.column("balance", width=120, anchor='se')

        # Assigning the heading names to the
        # respective columns
        self.treev.heading("transactionNo", text="Id")
        self.treev.heading("date", text="Date")
        self.treev.heading("amount", text="Amount")
        self.treev.heading("balance", text="Balance")

        # Back Button
        row += rows_count
        tk.Button(self, text="Close Account", command=self.close_account_button, width=12).grid(row=row, column=0)
        tk.Button(self, text="Deposit", command=self.deposit_button, width=12).grid(row=row, column=1)
        tk.Button(self, text="Withdraw", command=self.withdraw_button, width=12).grid(row=row, column=2)
        tk.Button(self, text="Back", command=self.cancel_button, width=12).grid(row=row, column=3)

