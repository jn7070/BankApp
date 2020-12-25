import tkinter as tk
import tkinter.messagebox
import pymysql
import customer
import employee
import gui_customer_info_page
import gui_account_page
import gui_share_data
import gui_employee_info_page
import gui_bankteller_page

#
# LoginPage: provides interface to existing customer/new customer/employee to log into the bank system
#
class LoginPage(tk.Frame):

    def set_title(self):
        self.controller.title('Bank - Login')

    def cleanup_ui(self):
        self.username.set('')
        self.password.set('')
        self.v.set(1)

    def set_data(self, share_data):
        self.cleanup_ui()
        cnx  = share_data.cnx
        self.share_data = gui_share_data.ShareData()
        self.share_data.setNew = True
        self.share_data.cnx = cnx
        self.set_title()
        return

    def set_go_back_page(self, back_go_page_name):
        self.back_go_page_name = back_go_page_name

    def retrieve_client_info(self):
        try:
            result = customer.get_customer_info(self.share_data.cnx, self.username.get(), self.password.get())
            if result is None:
                tkinter.messagebox.showerror(title="Login Error - no match",
                                             message='Please enter username and password correctly.',
                                             parent=self.controller)
                return
            self.share_data.customer_id = result['clientNo']
            self.share_data.client_name = result['name']
            self.share_data.client_data = result
            return True
        except pymysql.Error as e:
            tkinter.messagebox.showerror(title="Login Error", message=e.args[1], parent=self.controller)

        return False

    def retrieve_employee_info(self):
        try:
            result = employee.get_employee_info(self.share_data.cnx, self.username.get(), self.password.get())
            if result is None:
                tkinter.messagebox.showerror(title="Login Error - no match",
                                             message='Please enter username and password correctly.',
                                             parent=self.controller)
                return
            self.share_data.employee_id = result['employeeNo']
            self.share_data.employee_name = result['name']
            self.share_data.employee_type = result['type']
            return True
        except pymysql.Error as e:
            tkinter.messagebox.showerror(title="Login Error", message=e.args[1], parent=self.controller)

        return False

    def validate_login(self):
        self.share_data.setNew = True
        self.share_data.userName = self.username.get()
        self.share_data.passwd = self.password.get()
        self.share_data.login_mode = self.v.get()

        if self.share_data.login_mode == 1:
            if self.retrieve_client_info():
                self.controller.show_frame(gui_account_page.AccountPage, self.share_data, LoginPage)
        elif self.share_data.login_mode == 3:  # employee paghe
            if self.retrieve_employee_info():
                if self.share_data.employee_type == 'Bank-Teller':
                    self.controller.show_frame(gui_bankteller_page.BanktellerAccountPage, self.share_data, LoginPage)
                else:
                    self.controller.show_frame(gui_employee_info_page.EmployeeInfoPage, self.share_data, LoginPage)
        else:
            self.controller.show_frame(gui_customer_info_page.CustomerInfoPage, self.share_data, LoginPage)
        return

    def ShowChoice(self):
        if self.v.get() == 3: # employee login
            self.username.set('e1')
            self.password.set('e1')

    def get_size(self):
        return '450x120'

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.back_go_page_name = None
        self.share_data = None
        self.controller = controller

        row = 0
        # window
        # username label and text entry box
        tk.Label(self, text="User Name", width=20).grid(row=row, column=0)
        self.username = tk.StringVar()
        tk.Entry(self, textvariable=self.username, width=20).grid(row=row, column=1)

        row += 1
        # password label and password entry box
        tk.Label(self, text="Password", width=20).grid(row=row, column=0)
        self.password = tk.StringVar()
        tk.Entry(self, textvariable=self.password, show='*').grid(row=row, column=1)

        row += 1
        self.v = tk.IntVar()

        tk.Radiobutton(self,
                    text="Existing Client",
                    padx=20,
                    variable=self.v,
                    command=self.ShowChoice,
                    value=1).grid(row=row, column=0)

        tk.Radiobutton(self,
                    text="New Client",
                    padx=10,
                    variable=self.v,
                    command=self.ShowChoice,
                    value=2).grid(row=row, column=1)

        tk.Radiobutton(self,
                    text="Employee",
                    padx=20,
                    variable=self.v,
                    command=self.ShowChoice,
                    value=3).grid(row=row, column=2)

        self.v.set(1)

        row += 1
        #login button
        tk.Button(self, text="Login", command=self.validate_login, width=12).grid(row=row, column=1)
