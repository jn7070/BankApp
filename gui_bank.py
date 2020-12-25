import tkinter as tk
import gui_share_data
import gui_login_page
import gui_database_login_page
import gui_customer_info_page
import gui_account_page
import gui_quit_page
import gui_open_saving_or_checking_account_page
import gui_saving_account_page
import gui_checking_account_page
import gui_close_account_page
import gui_bank_teller_accounts_page
import gui_statistic_balance_distribution_page
import gui_account_deposit
import gui_account_withdraw
import gui_accounts_summary_page
import gui_employee_info_page
import gui_bankteller_page

#
# MainWindow: provides main application entry point, also where to run the application
#
class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Set the title of the main window.
        self.title('Bank')
        # Set the size of the main window to 300x300 pixels.
        self.geometry('400x200')

        # This container contains all the pages.
        container = tk.Frame(self)
        container.grid(row=1, column=1)
        self.frames = {}  # These are pages to which we want to navigate.

        # For each page...
        for F in (gui_database_login_page.DatabaseLoginPage,
                  gui_login_page.LoginPage,
                  gui_customer_info_page.CustomerInfoPage,           # client
                  gui_account_page.AccountPage,
                  gui_saving_account_page.SavingAccountPage,
                  gui_checking_account_page.CheckingAccountPage,
                  gui_open_saving_or_checking_account_page.OpenSavingOrCheckingAccountPage,
                  gui_close_account_page.CloseAccountPage,
                  gui_bank_teller_accounts_page.BankTellerAccountsPage,  # Bank Employee
                  gui_statistic_balance_distribution_page.StatisticBalanceDistributionPage,
                  gui_account_withdraw.AccountWithdrawPage,
                  gui_account_deposit.AccountDepositPage,
                  gui_accounts_summary_page.AccountsSummaryPage,
                  gui_bankteller_page.BanktellerAccountPage,
                  gui_employee_info_page.EmployeeInfoPage,
                  gui_quit_page.QuitPage):
            # ...create the page...
            frame = F(container, self)
            # ...store it in a frame...
            self.frames[F] = frame
            # ..and position the page in the container.
            frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)

        self.share_data = gui_share_data.ShareData()
        self.share_data.setNew = True

        # The first page is StartPage.
        self.show_frame(gui_database_login_page.DatabaseLoginPage, self.share_data, gui_quit_page.QuitPage)

    def show_frame(self, name, share_data, go_back_page):
        self.share_data = share_data
        frame = self.frames[name]
        frame.set_go_back_page(go_back_page)  # set back page
        frame.tkraise()
        frame.set_data(self.share_data)  # pass data between frames
        self.geometry(frame.get_size())  # reset size based on the frame size

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
