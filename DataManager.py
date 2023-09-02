import sqlite3

def sql_connection():
    try:
        connection = sqlite3.connect('test_db.db')
        return connection
    except sqlite3.Error as error:
        return error

con = sql_connection()

def sql_connection_open():
    cur = con.cursor()
    return cur

cur = sql_connection_open()

def sql_connection_close():
    con.close()

def checkqueryanswer(ans):
    if ans:
        return ans
    else:
        return False

def sql_query(query):
    cur.execute(query)
    con.commit()
    ans = cur.fetchall()
    return checkqueryanswer(ans)



def insert(table, column, value):
    cur.execute("INSERT INTO " + table + " (" + column + ") VALUES (" + value + ");")
    con.commit()
    return True

def update(table, column, value, id):
    cur.execute("UPDATE " + table + " SET " + column + "='" + value + "' WHERE id='" + id + "';")
    con.commit()
    return True

def insertImg(table, column, value):
    cur.execute("INSERT INTO " + table + " (" + column + ") VALUES (" + value + ");")
    con.commit()
def selectOne(table, column, value, column1):
    cur.execute("SELECT " + column1 + " FROM " + table + " WHERE " + column + "='" + value + "';")
    con.commit()
    return cur.fetchall()
def selectall(table):
    cur.execute("SELECT * FROM " + table + ";")
    con.commit()
    return cur.fetchall()
def selectseveraltable(table1, table2, column, condition):
    cur.execute("SELECT " + column + " FROM " + table1 + " INNER JOIN " + table2 + " AS S ON " + condition + ";")
    con.commit()
    return cur.fetchall()
def delete(table, condition):
    cur.execute("DELETE FROM " + table + " WHERE id='" + condition + "';")
    con.commit()
    return True

# user
def select_user_id(column, id):
    cur.execute("SELECT " + column + " FROM users WHERE id='" + id + "';")
    con.commit()
    ans = cur.fetchall()
    return checkqueryanswer(ans)

def select_users_where(column, where):
    cur.execute("SELECT " + column + " FROM users WHERE " + where + ";")
    con.commit()
    ans = cur.fetchall()
    return checkqueryanswer(ans)

def select_projects_all():
    cur.execute("SELECT Company, Date, id FROM Project ORDER BY Date DESC;")
    con.commit()
    ans = cur.fetchall()
    return checkqueryanswer(ans)

def select_projects_anything(user_id):
    cur.execute("SELECT Company, Date, id FROM Project WHERE Engineer=" + user_id + " ORDER BY Date DESC;")
    con.commit()
    ans = cur.fetchall()
    return checkqueryanswer(ans)

def select_project_id(columns,id):
    print("SELECT " + columns + "  FROM Project WHERE id=" + id + ";")
    cur.execute("SELECT " + columns + "  FROM Project WHERE id=" + id + ";")
    con.commit()
    ans = cur.fetchall()
    return checkqueryanswer(ans)

def select_details(number):
    cur.execute("SELECT * FROM Images WHERE num='" + number + "';")
    con.commit()
    ans = cur.fetchall()
    return checkqueryanswer(ans)
