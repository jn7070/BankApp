import tkinter
import tkinter as tk
import pymysql
import gui_account_page
import customer


#
# CustomerInfoPage: provides interface to existing customer to update the their personal information
#                   or new customer to provide personal information for new account creation
#
class CustomerInfoPage(tk.Frame):
    def cleanup_ui(self):
        self.client_name.set('')
        self.user_name.set('')
        self.password.set('')
        self.address.set('')
        self.birth_date.set('2000-10-10')
        self.gender.set(1)
        self.phone_number.set('')

    def set_data(self, share_data):

        self.cleanup_ui()

        self.share_data = share_data
        # update UI elements
        try:
            if share_data.customer_id == 0 or share_data.customer_id == -1:
                self.create_or_update_btn_text.set('Create')
                self.controller.title('Bank - Create Account')
                if share_data.userName != '':
                    self.user_name.set(share_data.userName)
                if share_data.passwd != '':
                    self.password.set(share_data.passwd)
            else:
                self.create_or_update_btn_text.set('Update')
                self.controller.title('Bank - Update Account')
                self.share_data.client_data = customer.get_customer_info_by_id(self.share_data.cnx,
                                                                               self.share_data.customer_id)
                self.client_name.set(self.share_data.client_data['name'])
                self.user_name.set(self.share_data.client_data['username'])
                self.password.set(self.share_data.client_data['password'])
                self.address.set(self.share_data.client_data['address'])
                self.birth_date.set(self.share_data.client_data['DOB'])
                if self.share_data.client_data['sex'] == "F":
                    self.gender.set(2)
                else:
                    self.gender.set(1)
                self.phone_number.set(self.share_data.client_data['phoneNo'])
        except pymysql.Error as e:
            tkinter.messagebox.showerror(title="Data Error", message=e.args[1], parent=self.controller)

    def get_size(self):
        return '400x225'

    def set_go_back_page(self, back_go_page_name):
        self.back_go_page_name = back_go_page_name

    def create_or_update_button(self):
        # DB create call here
        sex = 'M'
        if self.gender.get() == 2:
            sex = 'F'
        if self.address.get() == "" or self.user_name.get() == "" or self.client_name.get() == "" \
                or self.phone_number.get() == "" or self.birth_date.get() == "":
            tkinter.messagebox.showerror(title="Missing Data", message="All entries must be required. Try again.",
                                         parent=self.controller)
            return
        try:
            if self.share_data.customer_id == 0 or self.share_data.customer_id == -1:
                self.share_data.customer_id = customer.create_customer_record(self.share_data.cnx,
                                                                              self.client_name.get(),
                                                                              self.address.get(), self.birth_date.get(),
                                                                              sex, self.phone_number.get(),
                                                                              self.user_name.get(), self.password.get())
                self.share_data.userName = self.client_name.get()
            else:
                customer.update_customer_record(self.share_data.cnx,
                                                self.share_data.customer_id,
                                                self.client_name.get(),
                                                self.address.get(), self.birth_date.get(),
                                                sex, self.phone_number.get(),
                                                self.user_name.get(), self.password.get())
        except pymysql.Error as e:
            if "Duplicate entry" in e.args[1] and "'login.PRIMARY'" in e.args[1]:
                tkinter.messagebox.showerror(title="Data Error", message="Username already exists.",
                                             parent=self.controller)
            else:
                tkinter.messagebox.showerror(title="Data Error", message=e.args[1], parent=self.controller)
            return

        self.share_data.client_name = self.client_name.get()  # need to make sure client name updated
        # then bring to account page
        self.controller.show_frame(gui_account_page.AccountPage, self.share_data, self.back_go_page_name)
        return

    def cancel_button(self):
        self.controller.show_frame(self.back_go_page_name, self.share_data, self.back_go_page_name)
        return

    def ShowChoice(self):
        print(self.gender.get())

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.back_go_page_name = None
        self.controller = controller

        # Client Name
        row = 0
        tk.Label(self, text="Client Name").grid(row=row, column=0)
        self.client_name = tk.StringVar()
        tk.Entry(self, textvariable=self.client_name).grid(row=row, column=1)

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

        # Birth Date
        row += 1
        tk.Label(self, text="Birth Date").grid(row=row, column=0)
        self.birth_date = tk.StringVar()
        tk.Entry(self, textvariable=self.birth_date).grid(row=row, column=1)
        tk.Label(self, text="yyyy-mm-dd").grid(row=row, column=2)

        # Gender
        row += 1
        tk.Label(self, text="Gender").grid(row=row, column=0)
        self.gender = tk.IntVar()
        tk.Radiobutton(self,
                       text="Male",
                       padx=20,
                       variable=self.gender,
                       command=self.ShowChoice,
                       value=1).grid(row=row, column=1)

        tk.Radiobutton(self,
                       text="Female",
                       padx=20,
                       variable=self.gender,
                       command=self.ShowChoice,
                       value=2).grid(row=row, column=2)
        self.gender.set(1)

        # Phone Number
        row += 1
        tk.Label(self, text="Phone Number").grid(row=row, column=0)
        self.phone_number = tk.StringVar()
        tk.Entry(self, textvariable=self.phone_number).grid(row=row, column=1)
        tk.Label(self, text="xxxxxxxxxx").grid(row=row, column=2)

        # Create Button
        row += 1
        self.create_or_update_btn_text = tk.StringVar()
        tk.Button(self, text="Create", textvariable=self.create_or_update_btn_text,
                  command=self.create_or_update_button).grid(row=row, column=1)
        tk.Button(self, text="Cancel", command=self.cancel_button).grid(row=row, column=2)
