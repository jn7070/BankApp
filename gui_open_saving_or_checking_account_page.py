import tkinter as tk
import pymysql
import gui_login_page
import customer
import tkinter.messagebox

#
# OpenSavingOfCheckingAccountPage: provides details to open a savings or checking account.
#
class OpenSavingOrCheckingAccountPage(tk.Frame):
    def cleanup_ui(self):
        self.account_name.set('')
        self.initial_deposit.set('0.00')

    def set_data(self, share_data):

        self.cleanup_ui()
        self.share_data = share_data
        # update UI elements
        if self.share_data.open_saving_or_checking_account_mode == 1:
            self.controller.title('Bank - Open Saving Account')
        else:
            self.controller.title('Bank - Open Checking Account')

    def get_size(self):
        return '400x90'

    def set_go_back_page(self, back_go_page_name):
        self.back_go_page_name = back_go_page_name

    def create_button(self):
        # DB create call here
        try:
            self.initial_deposit.get()
        except:
            tkinter.messagebox.showerror(title="Create Account Error", message='Please enter the numeric amount',
                                         parent=self.controller)
            return

        try:
            if self.share_data.open_saving_or_checking_account_mode == 1:
                self.controller.title('Bank - Open Saving Account')
                result = customer.open_customer_savings_account(self.share_data.cnx, self.share_data.customer_id,
                                                                self.account_name.get(), self.initial_deposit.get())
            else:
                self.controller.title('Bank - Open Checking Account')
                result = customer.open_customer_checking_account(self.share_data.cnx, self.share_data.customer_id,
                                                                 self.account_name.get(), self.initial_deposit.get())

        except pymysql.Error as e:
            tkinter.messagebox.showerror(title="Create Account Error", message=e.args[1], parent=self.controller)
            return

            # then bring to account page
        self.controller.show_frame(self.back_go_page_name, self.share_data, gui_login_page.LoginPage)
        return

    def cancel_button(self):
        self.controller.show_frame(self.back_go_page_name, self.share_data, gui_login_page.LoginPage)
        return

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.share_data = None
        self.back_go_page_name = None
        self.controller = controller

        # Account Name
        row = 0
        tk.Label(self, text="Account Name").grid(row=row, column=0)
        self.account_name = tk.StringVar()
        tk.Entry(self, textvariable=self.account_name).grid(row=row, column=1)

        # Account Name
        row += 1
        tk.Label(self, text="Initial Deposit Amount").grid(row=row, column=0)
        self.initial_deposit = tk.DoubleVar()
        tk.Entry(self, textvariable=self.initial_deposit).grid(row=row, column=1)

        # Create Button
        row += 1
        tk.Button(self, text="Create", command=self.create_button).grid(row=row, column=1)
        tk.Button(self, text="Cancel", command=self.cancel_button).grid(row=row, column=2)
