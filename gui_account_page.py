import tkinter as tk
import gui_customer_info_page
import gui_open_saving_or_checking_account_page
import gui_saving_account_page
import gui_checking_account_page
import gui_close_account_page
import gui_login_page
import gui_accounts_summary_page

#
# AccountPage: provides operation choices for the customer.
#
class AccountPage(tk.Frame):
    def set_title(self):
        self.controller.title('Bank - Account Info')

    def cleanup_ui(self):
        self.client_name.set('')
        self.client_id.set(0)

    def set_data(self, share_data):
        self.cleanup_ui()
        self.share_data = share_data
        self.client_id.set(share_data.customer_id)
        self.client_name.set(share_data.client_name)
        self.set_title()

    def get_size(self):
        return '330x300'

    def update_customer_info(self):
        self.controller.show_frame(gui_customer_info_page.CustomerInfoPage, self.share_data, AccountPage)

    def show_account_summary(self):
        self.controller.show_frame(gui_accounts_summary_page.AccountsSummaryPage,
                                   self.share_data, AccountPage)
        return

    def go_to_saving_account(self):
        self.controller.show_frame(gui_saving_account_page.SavingAccountPage,
                                   self.share_data, AccountPage)

    def go_to_checking_account(self):
        self.controller.show_frame(gui_checking_account_page.CheckingAccountPage,
                                   self.share_data, AccountPage)

    def go_to_open_saving_account(self):
        self.share_data.open_saving_or_checking_account_mode = 1  # 1 - saving 2 - checking
        self.controller.show_frame(gui_open_saving_or_checking_account_page.OpenSavingOrCheckingAccountPage,
                                   self.share_data, AccountPage)

    def go_to_open_checking_account(self):
        self.share_data.open_saving_or_checking_account_mode = 2  # 1 - saving 2 - checking
        self.controller.show_frame(gui_open_saving_or_checking_account_page.OpenSavingOrCheckingAccountPage,
                                   self.share_data, AccountPage)

    def close_account(self):
        self.controller.show_frame(gui_close_account_page.CloseAccountPage,
                                   self.share_data, gui_login_page.LoginPage)

    def quit_program(self):
        self.controller.show_frame(gui_login_page.LoginPage, self.share_data, gui_login_page.LoginPage)

    def set_go_back_page(self, back_go_page_name):
        self.back_go_page_name = back_go_page_name

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.share_data = None
        self.back_go_page_name = None
        self.controller = controller

        # Client Name
        row = 0
        tk.Label(self, text="Client ID").grid(row=row, column=0)
        self.client_id = tk.IntVar()
        tk.Label(self, text="???", textvariable=self.client_id).grid(row=row, column=1)

        row += 1
        tk.Label(self, text="Client Name").grid(row=row, column=0)
        self.client_name = tk.StringVar()
        tk.Label(self, text="???", textvariable=self.client_name).grid(row=row, column=1)

        # Create Choice Buttons
        button_width = 20
        row += 1
        tk.Label(self, text="Operation Choice:").grid(row=row, column=0)
        row += 1
        tk.Button(self, text="Update Customer Info", command=self.update_customer_info,
                  width=button_width).grid(row=row, column=1)
        row += 1
        tk.Button(self, text="Show Account Summary", command=self.show_account_summary,
                  width=button_width).grid(row=row, column=1)
        row += 1
        tk.Button(self, text="Go to Checking Account", command=self.go_to_checking_account,
                  width=button_width).grid(row=row, column=1)
        row += 1
        tk.Button(self, text="Go to Saving Account", command=self.go_to_saving_account,
                  width=button_width).grid(row=row, column=1)
        row += 1
        tk.Button(self, text="Open Saving Account", command=self.go_to_open_saving_account,
                  width=button_width).grid(row=row, column=1)
        row += 1
        tk.Button(self, text="Open Checking Account", command=self.go_to_open_checking_account,
                  width=button_width).grid(row=row, column=1)
        row += 1
        tk.Button(self, text="Close Account", command=self.close_account,
                  width=button_width).grid(row=row, column=1)
        row += 1
        tk.Button(self, text="Quit", command=self.quit_program,
                  width=button_width).grid(row=row, column=1)

