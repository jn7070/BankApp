import tkinter as tk
import pymysql
import gui_account_page
import customer
import tkinter.messagebox

#
# AccountWithdrawPage: perform individual account withdraw operation.
#
class AccountWithdrawPage(tk.Frame):

    def cleanup_ui(self):
        self.account_name.set('')
        self.withdraw.set('0.00')

    def set_data(self, share_data):

        self.cleanup_ui()
        self.share_data = share_data
        # update UI elements
        self.controller.title('Bank - Withdraw')
        self.account_name.set(self.share_data.account_name)

    def get_size(self):
        return '430x90'

    def set_go_back_page(self, back_go_page_name):
        self.back_go_page_name = back_go_page_name

    def ok_button(self):
        try:
            self.withdraw.get()
        except pymysql.Error as e:
            tkinter.messagebox.showerror(title="Withdraw Error", message=e.args[1], parent=self.controller)
            return
        except:
            tkinter.messagebox.showerror(title="Perform Transaction Error", message='Please enter the numeric amount',
                                         parent=self.controller)
            return

        # DB create call here
        try:
            customer.perform_transaction(self.share_data.cnx, self.share_data.account_type,
                                         self.share_data.account_no, -self.withdraw.get())
        except pymysql.Error as e:
            tkinter.messagebox.showerror(title="Perform Transaction Error", message=e.args[1], parent=self.controller)
            return
        # then bring to account page
        self.controller.show_frame(self.back_go_page_name, self.share_data, gui_account_page.AccountPage)

    def cancel_button(self):
        self.controller.show_frame(self.back_go_page_name, self.share_data, gui_account_page.AccountPage)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.share_data = None
        self.back_go_page_name = None
        self.controller = controller

        # Account Name
        row = 0
        tk.Label(self, text="Account Name").grid(row=row, column=0)
        self.account_name = tk.StringVar()
        tk.Entry(self, textvariable=self.account_name, state='disabled').grid(row=row, column=1)

        # Withdraw Amount
        row += 1
        tk.Label(self, text="Withdraw Amount").grid(row=row, column=0)
        self.withdraw = tk.DoubleVar()
        tk.Entry(self, textvariable=self.withdraw).grid(row=row, column=1)

        # Create Button
        row += 1
        tk.Button(self, text="OK", command=self.ok_button, width=15).grid(row=row, column=1)
        tk.Button(self, text="Cancel", command=self.cancel_button, width=15).grid(row=row, column=2)
