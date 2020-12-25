import tkinter as tk
import gui_employee_info_page
import gui_login_page
import gui_bank_teller_accounts_page

#
# BanktellerAccountPage: provides operation choices for the bank teller employee
#
class BanktellerAccountPage(tk.Frame):
    def set_title(self):
        self.controller.title('Bank - Bank Teller Page')

    def cleanup_ui(self):
        self.employee_name.set('')
        self.employee_id.set(0)

    def set_data(self, share_data):
        self.cleanup_ui()
        self.share_data = share_data
        self.employee_id.set(share_data.employee_id)
        self.employee_name.set(share_data.employee_name)
        self.set_title()

    def get_size(self):
        return '330x150'

    def update_employee_info(self):
        self.controller.show_frame(gui_employee_info_page.EmployeeInfoPage, self.share_data, BanktellerAccountPage)

    def customer_accounts_statistic(self):
        self.controller.show_frame(gui_bank_teller_accounts_page.BankTellerAccountsPage,
                                   self.share_data, BanktellerAccountPage)

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
        tk.Label(self, text="Employee ID").grid(row=row, column=0)
        self.employee_id = tk.IntVar()
        tk.Label(self, text="???", textvariable=self.employee_id).grid(row=row, column=1)

        row += 1
        tk.Label(self, text="Employee Name").grid(row=row, column=0)
        self.employee_name = tk.StringVar()
        tk.Label(self, text="???", textvariable=self.employee_name).grid(row=row, column=1)

        # Create Choice Buttons
        button_width = 20
        row += 1
        tk.Label(self, text="Operation Choice:").grid(row=row, column=0)
        row += 1
        tk.Button(self, text="Update Employee Info", command=self.update_employee_info,
                  width=button_width).grid(row=row, column=1)
        row += 1
        tk.Button(self, text="Customer Accounts Stats", command=self.customer_accounts_statistic,
                  width=button_width).grid(row=row, column=1)
        row += 1
        tk.Button(self, text="Quit", command=self.quit_program,
                  width=button_width).grid(row=row, column=1)

