import pymysql

#
# These functions support calls to the database for employee information to retrieve data for the UI.
#

def get_employee_info(cnx, username, password):
    try:
        cur = cnx.cursor()
        cur.callproc("get_employee_info", [username, password])
        row = cur.fetchone()
    except pymysql.Error as e:
        raise
    return row

def get_employee_info_by_id(cnx, employee_id):
    try:
        cur = cnx.cursor()
        cur.callproc("get_employee_info_by_id", [employee_id])
        row = cur.fetchone()
    except pymysql.Error as e:
        raise
    return row

def update_employee_record(cnx, employeeNo, name, address, phoneNo, userName, passwd):
    try:
        cur = cnx.cursor()
        func_select = "select update_employee_record(%s, %s, %s, %s, %s, %s)"
        cur.execute(func_select, (employeeNo, userName, passwd, name, address, phoneNo))
        val = cur.fetchone()
        cnx.commit()
    except pymysql.Error as e:
        raise
    return [d for d in val.values()][0]
