#
# ShareData: provides data to share among different pages/classes
#
class ShareData():
    def __init__(self):
        self.setNew = False

        self.cnx = None
        self.customer_id = -1
        self.employee_id = -1
        self.employee_type = ''

        self.userName = ''
        self.passwd = ''

        self.client_name = ''
        self.employee_name = ''

        self.login_mode = 1  # existing customer
        self.open_saving_or_checking_account_mode = 0  # 1 - saving, 2 - checking

        self.account_no = -1
        self.account_name = ''
        self.account_type = ''
        self.client_data = None
        self.employee_data = None

        self.statistic_data = {}
