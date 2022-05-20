from flask import Flask, render_template, url_for, request, redirect
import sqlite3
import os

app = Flask(__name__)

#connect to the database
con = sqlite3.connect("rockyconcrete.db", check_same_thread=False)
con.row_factory = sqlite3.Row

#create a cursor/pointer to navigate the database
cur = con.cursor()

@app.route('/')
@app.route('/index')
def index():
    sql = """
            select * 
            from customers 
            order by cust_name asc;"""
    cur.execute(sql)
    customers = cur.fetchall()

    return render_template("index.html", customers=customers, title="Customer List")

@app.route('/customer_details', methods=['GET'])
def customer_details():
    if request.args.get('cid'):
        id = int(request.args.get('cid'))
        sql = """
                select * 
                from customers 
                where cust_no = ?;"""
        cur.execute(sql, (id,))
        customer_results = cur.fetchone()

        sql = """
                select count(distinct o.order_no) as 'order count', 
                max(order_date) as 'last order', 
                sum(order_qty * order_price) as 'total orders'
                from orders o, order_details od
                where o.order_no = od.order_no
                and cust_no = ?;"""
        cur.execute(sql, (id,))
        order_count = cur.fetchone()

        sql = """
                select *
                from orders
                where cust_no = ?
                order by order_date desc;"""
        cur.execute(sql, (id,))
        order_history = cur.fetchall()

        return render_template("customer_details.html", cdetails=customer_results, ocount=order_count, ohistory=order_history, title="Customer Info")
    else:
        return redirect(url_for("index"))

@app.route('/order_details', methods=['GET'])
def order_details():
    if request.args.get('oid'):
        id = int(request.args.get('oid'))

        sql = """
                select order_no, order_date, o.cust_no, c.cust_no, cust_name
                from orders o, customers c
                where o.cust_no = c.cust_no
                and o.order_no = ?;"""
        cur.execute(sql, (id,))
        customer_name = cur.fetchone()

        sql = """
                select * 
                from order_details od, products p
                where od.prod_code = p.prod_code
                and order_no = ?;"""
        cur.execute(sql, (id,))
        order_results = cur.fetchall()

        sql = """
                select order_no, sum(order_qty*order_price) as 'total'
                from order_details
                where order_no = ?;"""
        cur.execute(sql, (id,))
        total_cost = cur.fetchone()

        return render_template("order_details.html", custname=customer_name, total=total_cost, odetials=order_results, title="Order Details")
    else:
        return redirect(url_for("index"))

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    app.run(host,port,debug=True)