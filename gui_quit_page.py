import tkinter as tk

#
# QuitPage: provides ending message to customer to end the entire operation.
#
class QuitPage(tk.Frame):

    def set_go_back_page(self, back_go_page_name):
        self.back_go_page_name = back_go_page_name

    def set_data(self, share_data):
        self.controller.title('Bank - Logout')
        return

    def get_size(self):
        return '400x100'

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.back_go_page_name = None

        row = 0
        self.controller = controller
        # window
        # username label and text entry box
        tk.Label(self, text="You have been logged out successfully.").grid(row=row, column=1)
