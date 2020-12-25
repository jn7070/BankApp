import pymysql

#
# This function supports calls to the database for login information to retrieve data for the UI to check if valid user.
#
def open_database(username, password):
    try:
        cnx = pymysql.connect(host='localhost', user=username,
                              password=password,
                              db='bankSystem', charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        return cnx
    except pymysql.err.OperationalError as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        raise
