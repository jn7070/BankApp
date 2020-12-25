import tkinter
from tkinter import *
import tkinter as tk
import gui_login_page
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#
# StatisticBalanceDistributionPage: Display statistic data from self.share_data.statistic_data.
#
class StatisticBalanceDistributionPage(tk.Frame):
    def cleanup_ui(self):
        return

    def set_data(self, share_data):
        self.cleanup_ui()
        self.share_data = share_data

        # update UI elements
        self.controller.title('Bank - Customers Statistic')

        self.label_var.set(self.share_data.statistic_data['label'])
        self.create_charts()

    def create_charts(self):
        try:
            figure2 = Figure(figsize=(4, 3), dpi=100)
            subplot2 = figure2.add_subplot(111)

            pie_sizes = []
            label_list = []
            for data in self.share_data.statistic_data['datas']:
                label_list.append(data)
                pie_sizes.append(float(self.share_data.statistic_data['datas'][data]))

            labels2 = tuple(label_list)

            my_colors2 = self.share_data.statistic_data['colors']
            explode2 = self.share_data.statistic_data['explode']

            subplot2.pie(pie_sizes, colors=my_colors2, explode=explode2, labels=labels2, autopct='%1.1f%%', shadow=True,
                         startangle=90)
            subplot2.axis('equal')
            pie2 = FigureCanvasTkAgg(figure2, self )
            pie2.get_tk_widget().grid(column=0, row=3)
        except:
            tkinter.messagebox.showerror(title="Data Error",
                                         message='Please try again with correct data',
                                         parent=self.controller)
            return

    def get_size(self):
        return '490x410'

    def set_go_back_page(self, back_go_page_name):
        self.back_go_page_name = back_go_page_name

    def cancel_button(self):
        self.controller.show_frame(self.back_go_page_name, self.share_data, gui_login_page.LoginPage)
        return

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.share_data = None
        self.back_go_page_name = None
        self.controller = controller

        row = 0
        self.label_var = StringVar()
        self.pie_chart_label = tk.Label(self, text='Pie Chart', textvariable= self.label_var ).grid(row=row, column=0)

        # Close and Back Button
        row = 4
        tk.Button(self, text="Back", command=self.cancel_button, width=30).grid(row=row, column=0)
