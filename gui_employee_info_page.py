import tkinter
import tkinter as tk
import pymysql
import employee
import gui_bankteller_page

#
# EmployeeInfoPage: provides interface to existing employee to update the their personal information
#
class EmployeeInfoPage(tk.Frame):
    def cleanup_ui(self):
        self.employee_name.set('')   # to be blank out
        self.user_name.set('')
        self.password.set('')
        self.address.set('')                # to be blank out
        self.salary.set('')  # to be blank out
        self.date_joined.set('')   # to be blank out
        self.phone_number.set('')   # to be blank out

    def set_data(self, share_data):
        self.cleanup_ui()

        self.share_data = share_data
        # update UI elements
        try:
            self.controller.title('Bank - Update Account')
            self.share_data.employee_data = employee.get_employee_info_by_id(self.share_data.cnx,
                                                                             self.share_data.employee_id)
            self.employee_name.set(self.share_data.employee_data['name'])
            self.user_name.set(self.share_data.employee_data['username'])
            self.password.set(self.share_data.employee_data['password'])
            self.address.set(self.share_data.employee_data['address'])
            self.salary.set(self.share_data.employee_data['salary'])
            self.date_joined.set(self.share_data.employee_data['dateJoined'])
            self.phone_number.set(self.share_data.employee_data['phoneNo'])
        except pymysql.Error as e:
            tkinter.messagebox.showerror(title="Data Error", message=e.args[1], parent=self.controller)


    def get_size(self):
        return '400x225'

    def set_go_back_page(self, back_go_page_name):
        self.back_go_page_name = back_go_page_name

    def update_button(self):
        # DB create call here
        if self.address.get() == "" or self.user_name.get() == "" or self.employee_name.get() == "" \
                or self.phone_number.get() == "":
            tkinter.messagebox.showerror(title="Missing Data", message="All entries must be required. Try again.",
                                             parent=self.controller)
            return
        try:
            employee.update_employee_record(self.share_data.cnx,
                                                self.share_data.employee_id,
                                                self.employee_name.get(),
                                                self.address.get(),
                                                self.phone_number.get(),
                                                self.user_name.get(), self.password.get())
        except pymysql.Error as e:
            if "Duplicate entry" in e.args[1] and "'login.PRIMARY'" in e.args[1]:
                tkinter.messagebox.showerror(title="Data Error", message="Username already exists.",
                                             parent=self.controller)
            else:
                tkinter.messagebox.showerror(title="Data Error", message=e.args[1], parent=self.controller)
            return

        self.share_data.employee_name = self.employee_name.get()  # need to make sure client name updated
        # then bring to account page
        if self.share_data.employee_data['type'] == 'Bank-Teller':
            self.controller.show_frame(gui_bankteller_page.BanktellerAccountPage, self.share_data,
                                       self.back_go_page_name)
        else:
            tkinter.messagebox.showerror(title="Employee Data", message="Employee record has been updated.",
                                         parent=self.controller)

    def cancel_button(self):
        self.controller.show_frame(self.back_go_page_name, self.share_data, self.back_go_page_name)
        return

    def ShowChoice(self):
        print(self.gender.get())

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.back_go_page_name = None
        self.controller = controller

        # Client Name
        row = 0
        tk.Label(self, text="Client Name").grid(row=row, column=0)
        self.employee_name = tk.StringVar()
        tk.Entry(self, textvariable=self.employee_name).grid(row=row, column=1)

        # User Name
        row += 1
        tk.Label(self, text="User Name").grid(row=row, column=0)
        self.user_name = tk.StringVar()
        tk.Entry(self, textvariable=self.user_name).grid(row=row, column=1)

        # Password
        row += 1
        tk.Label(self, text="Password").grid(row=row, column=0)
        self.password = tk.StringVar()
        tk.Entry(self, textvariable=self.password).grid(row=row, column=1)

        # Address
        row += 1
        tk.Label(self, text="Address").grid(row=row, column=0)
        self.address = tk.StringVar()
        tk.Entry(self, textvariable=self.address).grid(row=row, column=1)

        # Date Joined
        row += 1
        tk.Label(self, text="Date Joined").grid(row=row, column=0)
        self.date_joined = tk.StringVar()
        tk.Entry(self, textvariable=self.date_joined, ).grid(row=row, column=1)

        # Salary
        row += 1
        tk.Label(self, text="Salary").grid(row=row, column=0)
        self.salary = tk.StringVar()
        tk.Entry(self, textvariable=self.salary).grid(row=row, column=1)

        # Phone Number
        row += 1
        tk.Label(self, text="Phone Number").grid(row=row, column=0)
        self.phone_number = tk.StringVar()
        tk.Entry(self, textvariable=self.phone_number).grid(row=row, column=1)
        tk.Label(self, text="xxxxxxxxxx").grid(row=row, column=2)

        # Create Button
        row += 1
        tk.Button(self, text="Update", command=self.update_button).grid(row=row, column=1)
        tk.Button(self, text="Cancel", command=self.cancel_button).grid(row=row, column=2)
