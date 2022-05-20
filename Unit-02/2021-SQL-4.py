import sqlite3
#connect to the database
con = sqlite3.connect("rockyconcrete.db")

#create a cursor/pointer to navigate the database
con.row_factory = sqlite3.Row #enables us to use column headings
cur = con.cursor() #is the pointer to use in the database

# Parameter Query
print("Please input the number corresponding to the option you wish to choose")
print("""
 1. Get Customer Details

 2. Get Order Details

 3. Get Product Details

 4. Quit
""")
Choice_input = input("Input (1-4): ")
if int(Choice_input) in range(1,5):
    Choice_input = int(Choice_input)
    if Choice_input == 1:
        search_value = input("Enter the customer name you wish to search for: ")
        sql = """
                select *
                from customers
                where cust_name like ?;"""
    elif Choice_input == 2:
        search_value = input("Enter the order number you wish to search for: ")
        sql = """
                select *
                from order_details od, products p
                where od.prod_code = p.prod_code
                and od.order_no like ?;"""
    elif Choice_input == 3:
        search_value = input("Enter the product name you wish to search for: ")
        sql = """
                select *
                from products
                where description like ?;"""
    else:
        print("Goodbye")
        exit()

    cur.execute(sql,('%'+search_value+'%',))
    results = cur.fetchall()

    print(results)

    if len(results) > 0:
        for row in results:
            if Choice_input == 1: print("Customer name:",row['cust_name'], "Customer number:",row['cust_no'], "Customer lives at:", row['street'], "in", row['town'], "Customer has a balance of:", row['curr_bal'] )
            elif Choice_input == 2: print("Order number:", row['order_no'], "Order for:", row['description'], "Order qty:", row['order_qty'], "Order price:", '$' + str(row['order_price']))
            else: print("Product:", row['description'], "Product code:", row['prod_code'], 'Prdouct Price: $' + str(row['list_price']))
    else:
        print('No records found')
else:
    print("Invalid option provided")