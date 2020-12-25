from tkinter import ttk
from tkinter import *
import tkinter as tk
import gui_login_page
import bank
import gui_statistic_balance_distribution_page

#
# BankTellerAccountsPage: pperform analysis on customers data
#
class BankTellerAccountsPage(tk.Frame):

    def cleanup_ui(self):
        for i in self.treev.get_children():
            self.treev.delete(i)   # remove all items from the treeview

    def set_data(self, share_data):
        # Must do for each display
        self.cleanup_ui()
        self.share_data = share_data
        self.controller.title('Bank - Employee Account View')

        # query database
        # update UI elements
        rows = bank.get_statistics(self.share_data.cnx)

        # to get "balance", "age" for each customer
        for row in rows:
            self.treev.insert("", 'end', values=(row['clientNo'], row['name'], row['sex'], row['age'],
                                                 row['totalBalance']))

    def get_size(self):
        return '600x310'

    def set_go_back_page(self, back_go_page_name):
        self.back_go_page_name = back_go_page_name

    def back_button(self):
        self.controller.show_frame(self.back_go_page_name, self.share_data, gui_login_page.LoginPage)

    def customer_age_report_button(self):
        row = bank.age_statistics(self.share_data.cnx)
        self.share_data.statistic_data = {'label': 'Customers: Age Distribution',
                                          'datas': {"0-20": float(row['zeroToTwentyPercent']),
                                                    "20-40": float(row['twentyToFortyPercent']),
                                                    "40-60": float(row['fortyToSixtyPercent']),
                                                    "60+": float(row['sixtyToAbovePercent'])},
                                          'explode': (0, 0.1, 0, 0.2),
                                          'colors': ['lightblue', 'lightsteelblue', 'deepskyblue', 'silver']}
        self.controller.show_frame(gui_statistic_balance_distribution_page.StatisticBalanceDistributionPage ,
                                   self.share_data, BankTellerAccountsPage)

    def customer_gender_report_button(self):
        row = bank.gender_statistics(self.share_data.cnx)
        self.share_data.statistic_data = {'label': 'Customers: Gender Distribution',
                                          'datas': {"Males": float(row['Males']),
                                                    "Females": float(row['Females'])},
                                          'explode': (0, 0.1),
                                          'colors': ['lightblue', 'lightsteelblue']}
        self.controller.show_frame(gui_statistic_balance_distribution_page.StatisticBalanceDistributionPage ,
                                   self.share_data, BankTellerAccountsPage)

    def customer_balance_report_button(self):
        row = bank.balance_statistics(self.share_data.cnx)

        self.share_data.statistic_data = {'label': 'Customers: Balance Distribution',
                                          'datas': {"$1K below": float(row['zeroToOneThousand']),
                                                    "$1K-$20K": float(row['oneThousandToTwentyThousand']),
                                                    "$20K-$100K": float(row['twentyThousandToOneHundredThousand']),
                                                    "$100K-$1M": float(row['oneHundredThousandToOneMil']),
                                                    "$1M above": float(row['aboveOneMil'])},
                                          'explode': (0.1, 0.3, 0.1, 0.1, 0.5),
                                          'colors': ['lightblue', 'lightsteelblue', 'deepskyblue', 'cyan', 'steelblue']}
        self.controller.show_frame(gui_statistic_balance_distribution_page.StatisticBalanceDistributionPage ,
                                   self.share_data, BankTellerAccountsPage)

    # sort the treeview column
    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda _col=col: self.treeview_sort_column(tv, _col, not reverse))

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.share_data = None
        self.back_go_page_name = None
        self.controller = controller

        # Report Buttons
        report_button_switcher = {
            0: self.customer_age_report_button,
            1: self.customer_gender_report_button,
            2: self.customer_balance_report_button
        }

        report_button_text_switcher = {
            0: "Age",
            1: "Gender",
            2: "Balance"
        }

        row = 0
        for c in range(len(report_button_text_switcher)):
            self.columnconfigure(c, weight=1)
            tk.Button(self, text=report_button_text_switcher.get(c),
                      command=report_button_switcher.get(c)).grid(row=0,column=c,sticky=E+W)

        rows_count = 16
        list_frame = tk.Frame(self, bg="white")
        list_frame.grid(row=1, column=0, rowspan=rows_count, columnspan=5, sticky=W+E+N+S)

        # Back Button
        row += 1 + rows_count
        tk.Button(self, text="Back", command=self.back_button, width=12).grid(row=row, column=1)

        # Using treeview widget
        columns = ("clientNo", "name", "sex", "age", 'totalBalance')
        self.treev = ttk.Treeview(list_frame, selectmode='browse', show='headings', columns=columns)

        # Calling pack method w.r.to treeview
        self.treev.pack(side='left')

        # Constructing vertical scrollbar
        # with treeview
        verscrlbar = ttk.Scrollbar(list_frame,
                                   orient="vertical",
                                   command=self.treev.yview)

        # scrollbar
        verscrlbar.pack(side='left')

        # Configuring treeview
        self.treev.configure(xscrollcommand=verscrlbar.set)

        for col in columns:
            self.treev.heading(col, text=col,
                               command=lambda _col=col: self.treeview_sort_column(self.treev, _col, False))

        # Assigning the width and anchor to respective columns
        self.treev.column("clientNo", width=90, anchor='c')
        self.treev.column("name", width=140, anchor='w')
        self.treev.column("sex", width=100, anchor='c')
        self.treev.column("age", width=100, anchor='se')
        self.treev.column("totalBalance", width=150, anchor='se')

        # Assigning the heading names to the respective columns
        self.treev.heading("clientNo", text="Id")
        self.treev.heading("name", text="Name")
        self.treev.heading("sex", text="Sex")
        self.treev.heading("age", text="Age")
        self.treev.heading("totalBalance", text="Balance")

