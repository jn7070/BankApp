import tkinter as tk
import tkinter.messagebox
import gui_share_data
import gui_login_page
import login

#
# DatabaseLoginPage: provides interface to access bank system database
#
class DatabaseLoginPage(tk.Frame):

    def set_title(self):
        self.controller.title('Bank - Database Login')

    def cleanup_ui(self):
        self.username.set('root')
        self.password.set('')

    def set_data(self, share_data):
        self.cleanup_ui()
        self.set_title()
        return

    def set_go_back_page(self, back_go_page_name):
        self.back_go_page_name = back_go_page_name

    def validate_login(self):
        try:
            self.share_data.cnx = login.open_database(self.username.get(), self.password.get())
            self.share_data.setNew = True
        except:
            tkinter.messagebox.showerror(title="Database Login Error",
                                         message='Please enter username and password correctly.',
                                         parent=self.controller)
            return

        self.controller.show_frame(gui_login_page.LoginPage, self.share_data, gui_login_page.LoginPage)

    def get_size(self):
        return '450x120'

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.back_go_page_name = None
        self.share_data = gui_share_data.ShareData()
        self.controller = controller

        row = 0
        # window
        # username label and text entry box
        tk.Label(self, text="User Name", width=20).grid(row=row, column=0)
        self.username = tk.StringVar()
        tk.Entry(self, textvariable=self.username).grid(row=row, column=1)


        row += 1
        # password label and password entry box
        tk.Label(self, text="Password", width=20).grid(row=row, column=0)
        self.password = tk.StringVar()
        tk.Entry(self, textvariable=self.password, show='*').grid(row=row, column=1)

        row += 1
        #login button
        tk.Button(self, text="Login", command=self.validate_login, width=12).grid(row=row, column=1)
