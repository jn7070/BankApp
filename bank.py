import pymysql

#
# These functions support calls to the database for bank information of the customers to retrieve data for the UI.
#

def get_statistics(cnx):
    try:
        cur = cnx.cursor()
        cur.callproc("get_statistics", [])
        rows = cur.fetchall()
    except pymysql.Error as e:
        raise
    return rows


def age_statistics(cnx):
    try:
        cur = cnx.cursor()
        cur.callproc("age_statistics", [])
        row = cur.fetchone()
    except pymysql.Error as e:
        raise
    return row


def gender_statistics(cnx):
    try:
        cur = cnx.cursor()
        cur.callproc("gender_statistics", [])
        row = cur.fetchone()
    except pymysql.Error as e:
        raise
    return row


def balance_statistics(cnx):
    try:
        cur = cnx.cursor()
        cur.callproc("balance_statistics", [])
        row = cur.fetchone()
    except pymysql.Error as e:
        raise
    return row
