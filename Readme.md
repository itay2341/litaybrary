# [Project1 - Library](https://startbootstrap.com/theme/creative/)



[Library](https://en.wikipedia.org/wiki/Library) is an amazing place to find books and learn. Come to watch my library.<br>
Created by [Itay Groer](https://en.wikipedia.org/w/index.php?search=itay+groer&title=Special%3ASearch&go=Go&ns0=1).


## Download and Installation

To begin using this web, choose one of the following options to get started:

- Clone the repo: `git clone https://github.com/StartBootstrap/startbootstrap-creative.git`
- [Fork, Clone, or Download on GitHub](https://github.com/StartBootstrap/startbootstrap-creative)

## Usage

### Basic Usage

After downloading, you can simply find all my project code! You need to find the `wsgi.py` file (my entrypoint). This entrypoint calls the `app` instance of Flask that made on `app.py`. This app contains several routes that connected to Blueprints with more specific routes. Blueprint for the admin side - `admin.py` and one for user side - `user.py`.<br> By authentication I can control the authorization I want to create.

### Advanced Usage

To make it your own - you should know how it works.
Clone the source files from ().
I'm using `Flask` module for the web server, and `SQLAlchemy` module to talk with the database, in my case - `SQLITE`.
The entrypoint starts from creating all database tables (it do nothing if the tables already exist).
Secondly, I'm starting a "thread" that will automatically call the same function once a day.
After this, finally, it runs the app. Basicly the server will run the `index.html` file.<br> All the html files are placing at `templates` folder and all the static files like CSS, JS and imeges are placing at `static` folder. It is Flask's standart.
Using SQLAlchemy I'm creating functions separately on a file named `mydatabase.py` located on `database` folder.


## My Tables

1. "books" table - 
   id, type_id, name, author, year_published,
   price, copies, img_url, info, category, *status* 

2. "types" table - 
   id, days_to_loan, fee_per_day, *status*

3. "customers" table - 
   id, name, city, date_of_birth,
   date_of_join, email, password, *status*, *pay_status*

4. "loans" table - 
   id, customer_id,book_id date_of_start,   date_of_return, *status*

5. "cashflow" table - 
   id, date, expenses, income, local_expenses

# Full actions

## Basic actions

1. Everyone can watch the home page, about page
2. Anyone can try to sign-up to my web
3. Anyone can try to log-in to my web

## User actions

(after log-in or sign-up)
1. Search a book by name, category or author name.
2. Loan a book.
3. Return a book.
4. Watch and Update user's personal details.
5. Watch user's active loans.
6. Watch user's history of loans.
7. Close account.

## Admin actions

1. Watch all the tables in the database.
2. Add new book.
3. Update book's copies.
4. activate / deactivate a book.
5. activate / deactivate a customer.
6. Search for a customer / for a book.
7. Watch and search the late loans.
8. Watch and search the active loans.
9. Change the status of a loan.

## Bugs and Issues

Have a bug or an issue with this web? [Open a new issue](https://github.com/itay2341/litaybrary/issues/new) here on GitHub!

## About

This is my first project.
It's a website created to manage books in library.
have fun!

L itay's brary  was created by **[Itay Groer](https://en.wikipedia.org/w/index.php?search=itay+groer&title=Special%3ASearch&go=Go&ns0=1)**.<br>
Visit my GitHub!

- <https://github.com/davidtmiller>

