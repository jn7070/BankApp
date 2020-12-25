from tkinter import ttk
from tkinter import *
import tkinter as tk
import pymysql
import gui_login_page
import gui_account_page
import customer
import tkinter.messagebox

#
# AccountsSummaryPage: creates the customer accounts summary page of the customer's account(s) and balances.
#
class AccountsSummaryPage(tk.Frame):

    def cleanup_ui(self):
        self.client_name.set('')
        self.total_balance.set(0.0)
        for i in self.treev.get_children():
            self.treev.delete(i)   # remove all items from the treeview
        return

    def set_data(self, share_data):
        self.cleanup_ui()
        self.share_data = share_data

        # query database
        # update UI elements
        self.controller.title('Bank - Customer Accounts Summary')

        self.client_name.set(self.share_data.client_name)
        try:
            rows = customer.accounts_summary(self.share_data.cnx, self.share_data.customer_id)
            if rows == None:
                tkinter.messagebox.showerror(title="No Accounts", message="Please open a new account.",
                                             parent=self.controller)
                self.controller.show_frame(self.back_go_page_name , self.share_data, gui_login_page.LoginPage)
                return

        except pymysql.Error as e:
            tkinter.messagebox.showerror(title="Data Error", message=e.args[1], parent=self.controller)

        total_balance = 0.
        for row in rows:
            self.treev.insert("", 'end', values=(row['accountNo'], row['name'], row['balance']))
            total_balance += row['balance']
        self.total_balance.set(total_balance)


    def get_size(self):
        return '450x140'

    def set_go_back_page(self, back_go_page_name):
        self.back_go_page_name = back_go_page_name

    def cancel_button(self):
        self.controller.show_frame(self.back_go_page_name, self.share_data, gui_account_page.AccountPage)
        return

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

        columns = ("accountNo", "name", 'balance')

        row = 0
        # Account Name
        tk.Label(self, text=" Name").grid(row=row, column=0)
        self.client_name = tk.StringVar()
        tk.Entry(self, textvariable=self.client_name, state='disabled').grid(row=row, column=1)

        row += 1
        tk.Label(self, text="Total Balance").grid(row=row, column=0)
        self.total_balance = tk.DoubleVar()
        tk.Entry(self, textvariable=self.total_balance, state='disabled').grid(row=row, column=1)

        row += 1
        rows_count = 2

        ListFrame = tk.Frame(self, bg="gray")
        ListFrame.grid(row=row, column=0, rowspan=rows_count, columnspan=len(columns)*2+1, sticky=W+E+N+S)

        # Back Button
        row += 1 + rows_count
        tk.Button(self, text="Back", command=self.cancel_button, width=12).grid(row=row, column=2)

        # Using treeview widget
        self.treev = ttk.Treeview(ListFrame, selectmode='browse', show='headings', columns=columns, height=2)

        # Calling pack method w.r.to treeview
        self.treev.pack(side='left')

        for col in columns:
            self.treev.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(self.treev, _col, False))

        # Assigning the width and anchor to  the
        # respective columns
        self.treev.column("accountNo", width=100, anchor='c')
        self.treev.column("name", width=150, anchor='c')
        self.treev.column("balance", width=150, anchor='ce')

        # Assigning the heading names to the
        # respective columns
        self.treev.heading("accountNo", text="Id")
        self.treev.heading("name", text="Name")
        self.treev.heading("balance", text="Balance")

