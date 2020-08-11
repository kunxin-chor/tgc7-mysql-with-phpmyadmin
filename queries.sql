create table if not exists vets (
    vet_id int unsigned auto_increment primary key,
    fname varchar(100) not null,
    lname varchar(100) not null,
) engine = innodb;

create table if not exists medicines(
    `medicine_id` int unsigned auto_increment primary key,
    `name` varchar(100),
    `description` text
) engine = innodb;

/* inserting data */
/* don't specify the vet_id because it is set to auto_increment
i.e it will be automatically set */
insert into vets (fname, lname) values("William", "Tan");


/* see all rows from a table */
select * from vets;

/* want to see all the columns in a table */
describe pet_owners;

/* to delete table, use drop */
drop table vets;

/* if we want insert multiple, we have one set of value for each rows */
insert into vets (fname, lname) values ("William", "Tan"), ("Ashely", "Wong"), ("David", "Teo");

insert into pet_owners (fname, lname, email) values ("Andy", "Chua", "andy@abc.com");

/* update: */
update pet_owners set email="andy@gmail.com" where pet_owner_id=1;

/* delete */
delete from pet_owners where pet_owner_id=1;

/* alter existing table */
alter table pet_owners add contact_number varchar(20) not null;
alter table vets modify fname varchar(255) not null;
alter table vets modify lname varchar(255) not null;

/* remove columns */
alter table pet_owners drop contact_number;

/* add a phone number to vet, is required (complusory) and if does not exist for some reasons, set the default to n/a */
alter table vets add contact_number varchar(20) not null default "n/a";

/* How to put in the FK if the table already exists */
/* create the pets table first */
create table pets (
    pet_id int unsigned primary key auto_increment,
    name varchar(50) not null
) engine=InnoDB;
/* Add a foreign key from pets to pet_owners*/
alter table pets add pet_owner_id int unsigned;
alter table pets add constraint fk_pet_owner_id foreign key (pet_owner_id) references pet_owners(pet_owner_id);
/* insert a new pet */
insert into pets  (name, pet_owner_id) values ("Fluffy", 2);

/*Create table with FKs */
create table shifts (
    shift_id int unsigned primary key auto_increment,
    day tinyint not null,
    start time not null,
    end time not null,
    vet_id int unsigned,
    foreign key(vet_id) 
        references vets (vet_id) on delete set null

) engine=InnoDB;

/* insert shift for the vet */
insert into shifts (day, start, end, vet_id) values (1, '17:00', '19:00', 1 );

create table appointments (
    appointment_id int unsigned primary key auto_increment,
    customer_id int unsigned not null,
    foreign key (customer_id) references pet_owners (pet_owner_id) on delete restrict,
    pet_id int unsigned not null,
    foreign key (pet_id) references pets (pet_id),
    vet_id int unsigned not null,
    foreign key (vet_id) references vets (vet_id),
    `datetime` datetime not null
) engine =InnoDB;

/* modify the table to point to itself */
alter table appointments add preceding_appointment_id int unsigned;
alter table appointments add constraint fk_preceding_appointment_id 
    foreign key (preceding_appointment_id)  references appointments(appointment_id);


/** library schema ** /

/* 1. create database */
create database library;

use library;

create table books (
    book_id int unsigned auto_increment primary key,
    title varchar(200) not null
);

create table authors (
    author_id int unsigned auto_increment primary key,
    fname varchar(50) not null,
    lname varchar(50) not null,
    date_of_birth datetime
);

alter table books engine=InnoDB;
alter table authors engine=InnoDB;

create table writing_credits (
    writing_credit_id int unsigned auto_increment primary key,
    author_id int unsigned not null,
    foreign key (author_id) references authors (author_id) on delete cascade not,
    book_id int unsigned not null,
    foreign key (book_id) references books (book_id) on delete cascade
) engine = InnoDB;


insert into authors (fname, lname) values ("John", "Ronald Tolkien"),
                                          ("Clark", "Lewis Staple"),
                                          ("Frank", "Hebret"),
                                          ("John", "Doe"),
                                          ("Jane", "Smith");

insert into books (title) values ("Chronicles of Narina"),
                                ("Lord of the Rings, The"),
                                ("Generic Textbook"),
                                ("Dune");

insert into writing_credits (author_id, book_id) values (1, 2);
insert into writing_credits (author_id, book_id) values (2, 1), (3, 4), (4, 3), (5, 3);

/* see all books and their authors */
select books.book_id, authors.author_id, title, fname, lname from books
     join writing_credits on 
        books.book_id = writing_credits.book_id 
     join authors on
        writing_credits.author_id = authors.author_id;

delete from authors where author_id = 5;

/* copies */
create table copies (
    copy_id int unsigned auto_increment primary key,
    qty tinyint not null default 1,
    book_id int unsigned,
    foreign key(book_id) references books (book_id) on delete set null
) engine=InnoDB;

insert into copies (book_id, quality) values (1, 5), (1, 3), (2, 3), (2, 3), (2,3), (3,1);

/* for the classicmodels db */
/* select all rows but with specific columns*/
select firstName, lastName, email from employees;

/* select all customers their salesRepEmployeeNumber is null */
select * from customers where salesRepEmployeeNumber is NULL;

/* select rows with specific critera */
select * from employees where officeCode=1;
select * from employees where emplyoeeNumber=1002;

/* compound critera */
select * from employees WHERE officeCode=4 and jobTitle="Sales Rep"
select * from employees where officeCode = 1 or officeCode = 4;

select * from employees where officeCode = 1 or officeCode = 4 and jobTitle = "Sales Rep"

/* see all sales rep from office code 1 or office code 4 */
select * from employees where (officeCode = 1 or officeCode = 4) and jobTitle = "Sales Rep"

/* search by a partial strings */
select * from employees where jobTitle like "Sales%";

/* searchy by a string that ends with our critera */
select * from employees where jobTitle like "%Sales";
/* search by a substring */
select * from employees where jobTitle like "%man%";

select * from employees join offices on employees.officeCode = offices.officeCode;

/* DATES */
select * from orders where requiredDate='2003-01-13'

/* show the year, month and day component */
select orderDate, year(orderDate), month(orderDate), day(orderDate) from orders 

/* show all orders in the year 2003 */
select * from orders where year(orderDate) = '2003'

/* show all orders in the June of year 2003 */
select * from orders where year(orderDate) = '2003' and month(orderDate) = '6'

/* show all orders after 30th June 2003 */
select * from orders where orderDate > '2003-06-30'

/* show all the orders that have already been shipped */
select * from orders where shippedDate <= NOW()

/* show the current date */
select curdate();
select now(); 

/* show all orders that are required 3 days later */
select * from orders where shippedDate - NOW() = 3

/* JOINS ADVANCED */
/* show all employees from USA */
SELECT * FROM employees JOIN offices
 	ON employees.officeCode = offices.officeCode
WHERE country="USA"

SELECT * FROM employees JOIN offices
 	ON employees.officeCode = offices.officeCode
WHERE country="USA"
ORDER BY firstName

/* limit to the first 3 results */
SELECT * FROM employees JOIN offices
 	ON employees.officeCode = offices.officeCode
WHERE country="USA"
ORDER BY firstName DESC
LIMIT 3

/** AGGREGATES **/

/* select only the unique values */
select distinct lastName from employees;

/* count */
select count(*) from employees

/* sum column */
SELECT sum(creditLimit) FROM customers;
SELECT sum(creditLimit) FROM customers WHERE country="USA"

/* avg column */
SELECT avg(creditLimit) FROM customers WHERE country="USA"

/* minimal column */
SELECT min(creditLimit) FROM customers WHERE country="USA"

/* max column */
SELECT max(creditLimit) FROM customers WHERE country="USA"

/**  GROUP BY **/

/* show the average credit limit by country */
select avg(creditLimit), country from customers group by country;

/* surefire to write a working group by
 1. figure out the critera to group by
 2. which table?
 3. What do I want to summarize?
 4. Always must select the column that you group by
*/

/* show the number of employees from office code */
select count(*),officeCode from employees group by officeCode

/* only show office code with 4 or more employees */
select count(*),officeCode from employees 
	group by officeCode having count(*) >= 4


/* show the top 3 countries by average limit but only from a selected pool */
SELECT avg(creditLimit), country FROM customers 
where country = "USA" or country = "Canada" or country = "France" 
	or country = "Israel" or country="Belgium"
group by country
having avg(creditLimit) > 0
order by avg(creditLimit) DESC
limit 3

/* alternate short form of the query above: */
SELECT avg(creditLimit), country FROM customers 
where country in ("USA", "France", "Canada", "Israel", "Beligum")
group by country
having avg(creditLimit) > 0
order by avg(creditLimit) DESC
limit 3

/* show how many sales rep per country, in descending order 
and only for countries with 2 or more sales rep */
SELECT count(*) as "number_of_sales_rep",country FROM 
	offices join employees ON offices.officeCode = employees.officeCode
where employees.jobTitle = "Sales Rep"
group by country
having number_of_sales_rep > 2
order by number_of_sales_rep desc
limit 2

/* 1. from */
/* 2. join */
/* 3. where */
/* 4. group by */
/* 5. having */
/* 6. select */
/* 7. order by */
/* 8. limit */ 

/** SUB QUERIES **/

/* Find all the customers who are in countries where there is a branch office */

/* q1. straightforward answers */
select * from customers where country = 'USA'
or country = 'France'
or country = 'Japan'
or country = 'UK'
or country = 'Australia'

/* using subquery */
select * from customers where country in (select distinct country from offices)

/* Find all the orders made in the year which the company made the most money */
SELECT * FROM orders WHERE year(orderDate) = 
(SELECT year(paymentDate) FROM payments group by year(paymentDate) 
ORDER BY sum(amount) DESC
LIMIT 1);

/* Find all the products that never have been ordered before */
SELECT productCode, productName from products where productCode not in
(SELECT distinct productCode FROM orderdetails);

/* Find all customers in USA which credit limit is higher or equal to the lowest credit limit of customers
from France */
select * from customers where 
	country = "USA" and creditLimit >
(select min(creditLimit) from customers where country="France")

/* find all the customers who have bought the top 3 most purchased product by quantity */

select * from customers join orders
	on customers.customerNumber = orders.customerNumber
join orderdetails
	on orderdetails.orderNumber = orders.orderNumber
where productCode in
(select productCode from orderdetails 
 	group by productCode
 	order by sum(quantityOrdered) desc
	limit 3)

/* but MySQL demands this */

select * from customers join orders
	on customers.customerNumber = orders.customerNumber
join orderdetails
	on orderdetails.orderNumber = orders.orderNumber
where productCode in
( select productCode from (select productCode from orderdetails 
 	group by productCode
 	order by sum(quantityOrdered) desc
	limit 3) as `inner`)

/* for each customer, find out the most expensive product bought and the number of cancelled orders */

/* for each customer, find out the highest the customer have paid for per product and
the number of cancelled */

select `left`.customerNumber, max_price, number_cancelled from 
(
SELECT customers.customerNumber, max(priceEach) as `max_price` FROM customers 
join orders on
	customers.customerNumber = orders.customerNumber
join orderdetails
	on orders.orderNumber = orderdetails.orderNumber
group by customerNumber
) as `left`
join
(
select orders.customerNumber, count(*) as `number_cancelled`
from orders
where orders.status = 'Cancelled'
group by orders.customerNumber
) as `right`
on `left`.customerNumber = `right`.customerNumber

/* get most expensive product code for each customer */
select temp.customerNumber, productCode, priceEach from customers  as temp join orders
	on temp.customerNumber = orders.customerNumber
join orderdetails
	on orders.orderNumber = orderdetails.orderNumber
where priceEach = (select max(priceEach) from customers as ct join orders
	on ct.customerNumber = orders.customerNumber
join orderdetails
	on orders.orderNumber = orderdetails.orderNumber
where ct.customerNumber=temp.customerNumber
				  )