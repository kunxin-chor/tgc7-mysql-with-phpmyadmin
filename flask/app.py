from flask import Flask, render_template, request, redirect, url_for
import os
import pymysql
import random
import math

app = Flask(__name__)

conn = pymysql.connect(
    host=os.environ.get('IP'),
    user=os.environ.get('C9_USER'),
    password="",
    database="classicmodels"
)


def create_cursor():
    return conn.cursor(pymysql.cursors.DictCursor)


@app.route('/employees')
def show_employees():
    cursor = create_cursor()
    cursor.execute("select * from employees")
    return render_template('all_employees.template.html', cursor=cursor)


@app.route('/offices')
def show_offices():
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select * from offices")
    return render_template('all_offices.template.html', offices=cursor)


@app.route('/offices/create')
def show_create_office_form():
    return render_template('create_office.template.html')


@app.route('/offices/create', methods=["POST"])
def process_create_office():
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    officeCode = random.randint(100000, 999999)

    sql = """
          insert into offices (officeCode, city, phone, addressLine1,
            addressLine2, state, country, postalCode, territory)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    cursor.execute(sql, [
        officeCode,
        request.form.get('city'),
        request.form.get('phone'),
        request.form.get('addressLine1'),
        request.form.get('addressLine2'),
        request.form.get('state'),
        request.form.get('country'),
        request.form.get('postal_code'),
        request.form.get('territory')
    ])

    conn.commit()
    return "done"


@app.route('/employees/create')
def show_create_employee():
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select officeCode, city from offices")
    return render_template("create_employee.template.html", offices=cursor)


@app.route('/employees/create', methods=["POST"])
def process_create_employee():
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """insert into employees (employeeNumber, lastName, firstName,
        extension, email, officeCode, jobTitle)
        values (%s, %s, %s, %s, %s, %s, %s)"""

    employeeNumber = random.randint(1000000, 9999999)

    cursor.execute(sql, [
        employeeNumber,
        request.form.get('lastName'),
        request.form.get('firstName'),
        request.form.get('extension'),
        request.form.get('email'),
        request.form.get('officeCode'),
        request.form.get('jobTitle')
    ])

    conn.commit()
    return "done"


@app.route('/employees/edit/<employeeNumber>')
def show_edit_employee_form(employeeNumber):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "select * from employees where employeeNumber=%s", employeeNumber)
    employee = cursor.fetchone()

    officeCursor = conn.cursor(pymysql.cursors.DictCursor)
    officeCursor.execute("select * from offices")

    return render_template('edit_employee.template.html', employee=employee,
                           offices=officeCursor)


@app.route('/employees/edit/<employeeNumber>', methods=["POST"])
def process_edit_employee(employeeNumber):
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """update employees set lastName=%s, firstName=%s, extension=%s, email=%s,
        officeCode=%s, jobTitle=%s where employeeNumber= %s"""

    cursor.execute(sql, [
        request.form.get('lastName'),
        request.form.get('firstName'),
        request.form.get('extension'),
        request.form.get('email'),
        request.form.get('officeCode'),
        request.form.get('jobTitle'),
        employeeNumber
    ])

    # see the last execute statement
    # print(cursor._last_executed)

    conn.commit()
    return "done"


@app.route('/employees/delete/<employeeNumber>')
def show_delete_employee_confirmation(employeeNumber):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select * from employees where employeeNumber = %s",
                   employeeNumber)
    # we are only expecting one result (becasue we selected by a primary key)
    # so we will just fetchone
    employee = cursor.fetchone()

    return render_template("delete_employee_confirmation.template.html",
                           employee=employee)


@app.route('/employees/delete/<employeeNumber>', methods=["POST"])
def process_delete_employee(employeeNumber):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("delete from employees where employeeNumber=%s",
                   employeeNumber)
    conn.commit()
    return "employee deleted"


@app.route('/customers')
def show_customers():

    page_number = request.args.get('page_number') or '0'
    records_per_page = 15
    # skip  (aka. offset)
    skip = int(page_number) * records_per_page

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select count(*) from customers")
    total_records = cursor.fetchone()
    max_pages = math.ceil(total_records['count(*)'] / records_per_page) - 1

    required_customer_name = request.args.get('customer_name') or ''
    required_country = request.args.get('country') or ''
    required_credit_limit = request.args.get('creditLimit') or ''



    sql = """select salesRepEmployeeNumber, customerNumber, customerName, country, city, 
        employees.firstName as employeeFirstName, employees.lastName as employeeLastName from customers left join employees
        on customers.salesRepEmployeeNumber = employees.employeeNumber WHERE 1
    """

    parameters = []

    # if reuqired_customer_name is not None and is not an empty string
    if required_customer_name:
        sql += " AND customerName like %s"
        parameters.append(f'%{required_customer_name}%')

    if required_country:
        sql += " AND country like %s"
        parameters.append('%' + required_country + '%')

    if required_credit_limit:
        sql += " AND creditLimit >= %s"
        parameters.append(float(required_credit_limit))

    # add in the paging
    sql += f" LIMIT {skip}, {records_per_page}"

    try:
        cursor.execute(sql, parameters)
        print (cursor._last_executed)
    except:
        print (cursor._last_executed)
 
    return render_template('all_customers.template.html', customers=cursor, 
        customerName=required_customer_name, 
        creditLimit = required_credit_limit, 
        country=required_country, page_number=int(page_number), max_pages=max_pages)


@app.route('/customers/by_sales_rep/<employee_number>')
def show_customers_by_sales_rep(employee_number):
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute('select * from employees where employeeNumber=%s', employee_number)
    employee = cursor.fetchone()

    sql = """select salesRepEmployeeNumber, customerNumber, customerName, country, city, 
        employees.firstName as employeeFirstName, employees.lastName as employeeLastName from customers left join employees
        on customers.salesRepEmployeeNumber = employees.employeeNumber WHERE salesRepEmployeeNumber=%s
    """

    cursor.execute(sql, employee_number)  

    return render_template('show_customers_by_sales_rep.template.html', customers=cursor, employee=employee)




@app.route('/customers/create')
def show_create_customer():
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select * from employees where jobTitle like 'Sales Rep'")
    return render_template('create_customer.template.html', sales_rep = cursor)


@app.route('/customers/create', methods=["POST"])
def process_create_customer():
    sql = """
        insert into customers (customerNumber, customerName, contactLastName, contactFirstName,
            phone, addressLine1, addressLine2, city, state, postalCode, 
            country, salesRepEmployeeNumber, creditLimit)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)      
    """
    customerNumber = random.randint(1000000, 9999999)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(sql, [
            customerNumber,
            request.form.get('customerName'),
            request.form.get('contactLastName'),
            request.form.get('contactFirstName'),
            request.form.get('phone'),
            request.form.get('addressLine1'),
            request.form.get('addressLine2'),
            request.form.get('city'),
            request.form.get('state'),
            request.form.get('postalCode'),
            request.form.get('country'),
            request.form.get('salesRepEmployeeNumber'),
            request.form.get('creditLimit')
        ])
        conn.commit()
    finally:
        cursor.close()

    return redirect(url_for('show_customers'))


@app.route('/customers/update/<customer_number>')
def show_update_customer(customer_number):

    # step one: creates the cursor
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # step two: fetch the information
    cursor.execute("select * from customers where customerNumber = %s", customer_number)
    customer = cursor.fetchone()

    # step three: select any other supporting data that we need to populate the form
    employee_cursor = conn.cursor(pymysql.cursors.DictCursor)
    employee_cursor.execute("select * from employees where jobTitle = 'Sales Rep'")

    return render_template('update_customer.template.html', sales_rep=employee_cursor,
                          customer=customer)
    


@app.route('/customers/update/<customer_number>', methods=["POST"])
def process_update_customer(customer_number):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = """
        update customers set customerName=%s, 
            contactLastName = %s,
            contactFirstName = %s,
            phone = %s,
            addressLine1=%s,
            addressLine2=%s,
            city=%s,
            state=%s,
            postalCode=%s,
            country=%s,
            salesRepEmployeeNumber=%s,
            creditLimit=%s
            WHERE customerNumber=%s
    """

    salesRepEmployeeNumber = request.form.get('salesRepEmployeeNumber')
    if salesRepEmployeeNumber == '0':
        # None in Python is the same as NULL in Mysql
        salesRepEmployeeNumber = None

    try:
        cursor.execute(sql,[
            request.form.get('customerName'),
            request.form.get('contactLastName'),
            request.form.get('contactFirstName'),
            request.form.get('phone'),
            request.form.get('addressLine1'),
            request.form.get('addressLine2'),
            request.form.get('city'),
            request.form.get('state'),
            request.form.get('postalCode'),
            request.form.get('country'),
            salesRepEmployeeNumber,
            request.form.get('creditLimit'),
            customer_number
        ])
        conn.commit()
    finally:
        cursor.close()

    return redirect(url_for('show_customers'))


@app.route('/customers/delete/<customer_number>')
def show_delete_customer_confirmation(customer_number):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # check if customer has any existing orders
    cursor.execute("select count(*) from orders where customerNumber=%s", customer_number)
    number_of_orders = cursor.fetchone()

    cursor.execute("select * from customers where customerNumber=%s", customer_number)
    customer = cursor.fetchone()
    
    if number_of_orders == 0:
        return render_template('delete_customer_confirmation.template.html', customer=customer)
    else:
        return render_template('cannot_delete_customer.template.html', customer=customer)



@app.route('/customers/delete/<customer_number>', methods=["POST"])
def process_delete_customer(customer_number):
     cursor = conn.cursor(pymysql.cursors.DictCursor)
     cursor.execute("delete from customers where customerNumber = %s", customer_number)
     return redirect(url_for('show_customers'))

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
