import pymysql

#
# These functions support calls to the database for customer information to retrieve data for the UI.
#

def get_all_customer_info(cnx):
    try:
        cur = cnx.cursor()
        cur.callproc("get_all_client_info")
        rows = cur.fetchall()
    except pymysql.Error:
        raise
    return rows

def get_customer_info(cnx, username, password):
    try:
        cur = cnx.cursor()
        cur.callproc("get_client_info", [username, password])
        row = cur.fetchone()
    except pymysql.Error:
        raise
    return row

def get_customer_info_by_id(cnx, customer_id):
    try:
        cur = cnx.cursor()
        cur.callproc("get_client_info_by_id", [customer_id])
        row = cur.fetchone()
    except pymysql.Error:
        raise
    return row

def create_customer_record(cnx, name, address, DOB, sex, phoneNo, userName, passwd):
    try:
        cur = cnx.cursor()
        func_select = "select create_customer_record(%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(func_select, (userName, passwd, name, address, DOB, sex, phoneNo))
        val = cur.fetchone()
        cnx.commit()
    except pymysql.Error:
        raise
    return [d for d in val.values()][0]

def update_customer_record(cnx, clientNo, name, address, DOB, sex, phoneNo, userName, passwd):
    try:
        cur = cnx.cursor()
        func_select = "select update_customer_record(%s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(func_select, (clientNo, userName, passwd, name, address, DOB, sex, phoneNo))
        val = cur.fetchone()
        cnx.commit()
    except pymysql.Error:
        raise
    return [d for d in val.values()][0]


def open_customer_checking_account(cnx, client_no, name, initial_deposit):
    try:
        cur = cnx.cursor()
        func_select = "select open_customer_checking_account(%s, %s, %s)"
        cur.execute(func_select, (client_no, name, initial_deposit))
        val = cur.fetchone()
        cnx.commit()
    except pymysql.Error:
        raise
    return [d for d in val.values()][0]

def open_customer_savings_account(cnx, client_no, name, initial_deposit):
    try:
        cur = cnx.cursor()
        func_select = "select open_customer_savings_account(%s, %s, %s)"
        cur.execute(func_select, (client_no, name, initial_deposit))
        val = cur.fetchone()
        cnx.commit()
    except pymysql.Error:
        raise
    return [d for d in val.values()][0]

def get_checking_info_by_id(cnx, customer_id):
    try:
        cur = cnx.cursor()
        cur.callproc("get_checking_info_by_id", [customer_id])
        row = cur.fetchone()
    except pymysql.Error:
        raise
    return row

def get_savings_info_by_id(cnx, customer_id):
    try:
        cur = cnx.cursor()
        cur.callproc("get_savings_info_by_id", [customer_id])
        row = cur.fetchone()
    except pymysql.Error:
        raise
    return row

def deposit(cnx, account_type):
    try:
        cur = cnx.cursor()
        func_select = "select create_customer_record(%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(func_select, (account_type))
        val = cur.fetchone()
        cnx.commit()
    except pymysql.Error:
        raise
    return [d for d in val.values()][0]

def update_account_name(cnx, client_no, name, type):
    try:
        cur = cnx.cursor()
        cur.callproc("update_account_name", [client_no, name, type])
        cnx.commit()
    except pymysql.Error:
        raise

def get_transactions(cnx, account_no):
    try:
        cur = cnx.cursor()
        cur.callproc("get_transactions", [account_no])
        rows = cur.fetchall()
    except pymysql.Error:
        raise
    return rows

def perform_transaction(cnx, type, account_no, amount):
    try:
        cur = cnx.cursor()
        cur.callproc("perform_transaction", [type, account_no, amount])
        cnx.commit()
    except pymysql.Error:
        raise

def close_individual_account(cnx, account_no):
    try:
        cur = cnx.cursor()
        cur.callproc("close_individual_account", [account_no])
        cnx.commit()
    except pymysql.Error:
        raise

def close_client_account(cnx, client_no):
    try:
        cur = cnx.cursor()
        cur.callproc("close_client_account", [client_no])
        cnx.commit()
    except pymysql.Error:
        raise

def accounts_summary(cnx, client_no):
    try:
        cur = cnx.cursor()
        cur.callproc("accounts_summary", [client_no])
        rows = cur.fetchall()
    except pymysql.Error:
        raise
    return rows

def get_total_balance(cnx, client_no):
    try:
        cur = cnx.cursor()
        cur.callproc("get_total_balance", [client_no])
        row = cur.fetchone()
    except pymysql.Error:
        raise
    return row
