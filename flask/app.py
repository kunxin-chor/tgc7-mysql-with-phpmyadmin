from flask import Flask, render_template, request, redirect, url_for
import os
import pymysql
import random
import companydb

app = Flask(__name__)

conn = pymysql.connect(
    host=os.environ.get('IP'),
    user=os.environ.get('C9_USER'),
    password="",
    database="classicmodels"
)


@app.route('/employees')
def show_employees():
    cursor = companydb.get_all_employees()
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


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
