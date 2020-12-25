import tkinter as tk
import pymysql
import gui_login_page
import gui_account_page
import customer
import tkinter.messagebox


#
# CloseAccountPage: provides interface to existing customer to close the customer account
#
class CloseAccountPage(tk.Frame):
    def cleanup_ui(self):
        self.available_balance.set(0.0)

    def set_data(self, share_data):
        self.cleanup_ui()
        self.share_data = share_data

        # query database to display total amount from all saving and checking accounts
        try:
            row = customer.get_total_balance(self.share_data.cnx, self.share_data.customer_id)
        except pymysql.Error as e:
            tkinter.messagebox.showerror(title="Data Error", message=e.args[1], parent=self.controller)
            return

        self.available_balance.set(row['total_balance']);
        # update UI elements
        self.controller.title('Bank - Close Account')

    def get_size(self):
        return '490x60'

    def set_go_back_page(self, back_go_page_name):
        self.back_go_page_name = back_go_page_name

    def delete_button(self):
        try:
            customer.close_client_account(self.share_data.cnx, self.share_data.customer_id)
        except pymysql.Error as e:
            tkinter.messagebox.showerror(title="Data Error", message=e.args[1], parent=self.controller)
            return

        tkinter.messagebox.showerror(title="Close Customer Account", message='Customer Account closed',
                                     parent=self.controller)

        self.controller.show_frame(gui_login_page.LoginPage, self.share_data, gui_login_page.LoginPage)
        return

    def cancel_button(self):
        self.controller.show_frame(gui_account_page.AccountPage, self.share_data, gui_login_page.LoginPage)
        return

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.share_data = None
        self.back_go_page_name = None
        self.controller = controller

        # Account Name
        # Available Balance
        row = 0
        tk.Label(self, text="Available Balance").grid(row=row, column=0)
        self.available_balance = tk.DoubleVar()
        tk.Entry(self, textvariable=self.available_balance, state='disabled').grid(row=row, column=1)
        tk.Label(self, text="will be mailed to client.").grid(row=row, column=2)

        # Back Button
        row += 1
        tk.Button(self, text="Close Account", command=self.delete_button, width=20).grid(row=row, column=1)
        tk.Button(self, text="Back", command=self.cancel_button, width=20).grid(row=row, column=2)
