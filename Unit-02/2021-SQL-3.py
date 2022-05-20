import sqlite3

#connect to the database
con = sqlite3.connect("rockyconcrete.db")

#create a cursor/pointer to navigate the database
con.row_factory = sqlite3.Row #enables us to use column headings
cur = con.cursor() #is the pointer to use in the database

# Parameter Query
name_input = input("Enter the name to search for: ")

sql = """
        select c.cust_name, c.cust_no, o.cust_no, cr_limit, curr_bal, max(order_no) as order_no, order_date
        from customers c, orders o
        where c.cust_no = o.cust_no
        and c.cust_name like ?;"""

cur.execute(sql,('%'+name_input+'%',))
results = cur.fetchall()

if len(results) > 0:
    for row in results:
        print(row['cust_name'], 'cust_no:', row['cust_no'], 'avaliable credit:', row['cr_limit'] - row['curr_bal'], 'Most recent order number and its date:', row['order_no'], row['order_date'])
else:
    print('No records found')