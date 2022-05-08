'''
MIT License

Copyright (c) 2018 Mahmud Ahsan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# Install Library
'''
Source: https://github.com/zzzeek/sqlalchemy/
http://docs.sqlalchemy.org/en/latest/intro.html#installation
macOS / Linux:
pip3 install SQLAlchemy 

Windows:
pip install SQLAlchemy 

# SQLite DB Browser http://sqlitebrowser.org

# http://docs.sqlalchemy.org/en/latest/core/tutorial.html
# http://docs.sqlalchemy.org/en/latest/core/types.html
'''

# -----------------------------------
#      Database Model
#      Itay Groer | @itay2341
# -----------------------------------

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey ,Boolean
from datetime import datetime , timedelta
from mailer import Mailer


# Global Variables
SQLITE                    = 'sqlite'
# MYSQL                   = 'mysql'
# POSTGRESQL              = 'postgresql'
# MICROSOFT_SQL_SERVER    = 'mssqlserver'

# Table Names
CUSTOMERS         =  'customers'
BOOKS             =  'books'
LOANS             =  "loans"
TYPES             =  "types"
CASHFLOW          =  "cashflow"


class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        # MYSQL: 'mysql://scott:tiger@localhost/{DB}',
        # POSTGRESQL: 'postgresql://scott:tiger@localhost/{DB}',
        # MICROSOFT_SQL_SERVER: 'mssql+pymssql://scott:tiger@hostname:port/{DB}'
    }

    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)

            self.db_engine = create_engine(engine_url)
            print(self.db_engine)

        else:
            print("DBType is not found in DB_ENGINE")


    #Create all DataBase tables !$$$
    def create_db_tables(self):
        metadata = MetaData()
        customers = Table(CUSTOMERS, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String,nullable=False),
                      Column('city', String,nullable=False),
                      Column('date_of_birth', String,nullable=False),
                      Column('date_of_join', String,nullable=False),
                      Column('email', String,nullable=False),
                      Column('password', String,nullable=False),
                      Column('status', Boolean,nullable=False),
                      Column('pay_status', Boolean,nullable=False)
                      )

        books = Table(BOOKS, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('type_id',None, ForeignKey('types.id')),
                      Column('name', String,nullable=False),
                      Column('author', String,nullable=False),
                      Column('year_published', String,nullable=False),
                      Column('price', Integer,nullable=False),
                      Column('copies', Integer,nullable=False),
                      Column('img_url', String,nullable=False),
                      Column('info', String,nullable=False),
                      Column('category', String),
                      Column('status', Boolean,nullable=False)
                      )

        types = Table(TYPES, metadata,
                        Column('id', Integer, primary_key=True),
                        Column('days_to_loan',Integer,nullable=False),
                        Column('fee_per_day', Integer, nullable=False),
                        Column('status', Boolean,nullable=False)
                        )      

        loans = Table(LOANS, metadata,
                        Column('id', Integer, primary_key=True),
                        Column('customer_id', None, ForeignKey('customers.id')),
                        Column('book_id', None, ForeignKey('books.id')),
                        Column('date_of_start',String,nullable=False),
                        Column('date_of_return', String, nullable=False),
                        Column('status', Integer,nullable=False)
                        )

        cashflow = Table(CASHFLOW, metadata,
                        Column('id', Integer, primary_key=True),
                        Column('date',String,nullable=False),
                        Column('expenses',Integer,nullable=False),
                        Column('income', Integer,nullable=False),
                        Column('local_expenses', Integer,nullable=False)
                        )                                       

        try:
            metadata.create_all(self.db_engine)
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    #Do something
    def execute_query(self, query=''):
        if query == '' : return
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)
                print("or if you hacker :)")

    #get data from table
    def select_data(self, table='', query=''):
        query = query if query != '' else f"SELECT * FROM '{table}';"
        res = []
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    res.append( row)
                result.close()
        # print("\n")
        return res
    
    #get single data from tble
    def select_single_data(self,query=''):
        if query == '' : return
        x=[]
        with self.db_engine.connect() as connection:
            try:
                result=connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    x.append(row)
                result.close()
                x2=x.pop()
                x=x2[0]
        return x

    #get entity from table by id
    def get_data_by_id(self,table,id):
        query1 = f"SELECT * FROM '{table}' WHERE id={id};"
        res = self.select_data(query=query1)
        return res


#------------------CUSTOMERS----------------------

    #Only after sign up
    def insert_customer(self,_name,_city,_date_of_birth,_email,_password):
        _date_of_join = datetime.now()
        str1 = _date_of_join.strftime('%d-%m-%Y, %H:%M:%S')
        query = f"INSERT INTO '{CUSTOMERS}' (name, city, date_of_birth, date_of_join, email, password, status, pay_status) VALUES ('{_name}','{_city}','{_date_of_birth}','{str1}','{_email}','{_password}',{True},{True});"
        self.execute_query(query)

#Select_________________________________________
    #Admin only $$$
    def select_all_customers(self):
        x=self.select_data(table=CUSTOMERS)
        return x

    #Admin only $$$
    def select_customers_active(self):
        query1 = f"SELECT * FROM '{CUSTOMERS}' WHERE '{CUSTOMERS}'.status = {True};"
        x=self.select_data(query=query1)
        return x

    #Admin only $$$
    def select_customers_by_name(self,_name):
        query1 = f"SELECT * FROM {CUSTOMERS} WHERE {CUSTOMERS}.name ='{_name}';"
        x=self.select_data(query=query1)
        return x

    #Admin only $$$
    def select_customer_by_id(self,_id):
        query1 = f"SELECT * FROM {CUSTOMERS} WHERE {CUSTOMERS}.id ='{_id}';"
        x=self.select_data(query=query1)
        return x[0]

    #Admin only $$$
    def select_all_customers_id(self):
        x=self.select_data(query=f"SELECT id from '{CUSTOMERS}'")
        a=[]
        for s in x:
            for r in s:
                a.append(r)
        return a

    #Users only $$$
    def select_customers_by_name(self,_name):
        query1 = f'''SELECT *  FROM '{CUSTOMERS}' WHERE '{CUSTOMERS}'.name like "%{_name}%";'''
        x = self.select_data(query=query1)
        return x

    #Users only $$$
    def select_customers_by_id(self,_id):
        query1 = f'''SELECT *  FROM '{CUSTOMERS}' WHERE '{CUSTOMERS}'.id = {_id};'''
        x = self.select_data(query=query1)
        return x

#Update_________________________________________
    #Admin and Users $$$
    def update_customer_name(self,_name,_id):
        query = f"UPDATE {CUSTOMERS} SET name='{_name}' WHERE id={_id}"
        self.execute_query(query)

    #Admin and Users $$$
    def update_customer_city(self,_city,_id):
        query = f"UPDATE {CUSTOMERS} SET city='{_city}' WHERE id={_id}"
        self.execute_query(query)      
    
    #Admin and Users $$$
    def update_customer_date_of_birth(self,_date_of_birth,_id):
        query = f"UPDATE {CUSTOMERS} SET date_of_birth='{_date_of_birth}' WHERE id={_id}"
        self.execute_query(query)

    #Admin and Users $$$
    def update_customer_email(self,_email,_id):
        query = f"UPDATE {CUSTOMERS} SET email='{_email}' WHERE id={_id}"
        self.execute_query(query)

    #Admin and Users $$$
    def update_customer_password(self,_password,_id):
        query = f"UPDATE {CUSTOMERS} SET password='{_password}' WHERE id={_id}"
        self.execute_query(query)    

    #Admin and Users $$$
    def update_customer_status(self,_status,_id):
        query = f"UPDATE '{CUSTOMERS}' SET status={_status} WHERE id={_id}"
        self.execute_query(query)  

#Helpers_________________________________________
    #To know on the page the "id" customer that just created
    def customer_id(self):
        query1=f"SELECT MAX(id) FROM '{CUSTOMERS}';"
        x=self.select_single_data(query=query1)
        return x

    #Auth - return id or 0
    def get_customer_id_auth(self,_pass,_email):
        query = f"SELECT id FROM '{CUSTOMERS}' WHERE email='{_email}' and password='{_pass}' and status= {True} ;"
        res = []
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    res.append( row)
                result.close()
                try:
                    x2=res.pop()
                except:
                    res=0
                else:
                    res=x2[0]
        return res

#------------------BOOKS----------------------------------
 
    #Admin only $$$
    def insert_books(self,_type_id,_name,_author,_year_published,_price,_copies,_img_url,_info,_category):
        query = f"INSERT INTO '{BOOKS}' (type_id,name,author,year_published,price,copies,img_url,info,category,status) VALUES ({_type_id},'{_name}','{_author}','{_year_published}',{_price},{_copies},'{_img_url}','{_info}','{_category}',{True});"
        self.execute_query(query)
        query2 = f"SELECT local_expenses FROM {CASHFLOW} WHERE  {CASHFLOW}.id = {1} ;"
        expenses=self.select_single_data(query=query2)
        new_expenses = int(expenses) + (_price*_copies)
        query3 = f"UPDATE {CASHFLOW} SET local_expenses={new_expenses} WHERE {CASHFLOW}.id = {1} ;"
        self.execute_query(query3)

#Select_________________________________________
    #Admin only $$$
    def select_all_books(self):
        x=self.select_data(table=BOOKS)
        return x

    #Admin and Users $$$
    def select_books_for_users(self):
        query1 = f"SELECT {BOOKS}.id , {BOOKS}.name ,'{BOOKS}'.author, '{BOOKS}'.year_published, '{BOOKS}'.img_url, '{BOOKS}'.info, '{TYPES}'.days_to_loan, '{TYPES}'.fee_per_day, '{BOOKS}'.category    FROM '{BOOKS}' inner join '{TYPES}' on '{BOOKS}'.type_id = '{TYPES}'.id WHERE '{BOOKS}'.status = {True} and '{TYPES}'.status = {True} and '{BOOKS}'.copies > 0;"
        res = self.select_data(query=query1)
        return res

    #Users only $$$
    def select_books_by_category(self,_category):
        query1 = f"SELECT {BOOKS}.id , {BOOKS}.name ,'{BOOKS}'.author, '{BOOKS}'.year_published, '{BOOKS}'.img_url, '{BOOKS}'.info, '{TYPES}'.days_to_loan, '{TYPES}'.fee_per_day, '{BOOKS}'.category    FROM '{BOOKS}' inner join '{TYPES}' on '{BOOKS}'.type_id = '{TYPES}'.id WHERE '{BOOKS}'.status = {True} and '{TYPES}'.status = {True} and '{BOOKS}'.copies > 0 and '{BOOKS}'.category='{_category}';"
        x = self.select_data(query=query1)
        return x

    #Users only $$$
    def select_books_by_name(self,_name):
        query1 = f'''SELECT {BOOKS}.id , {BOOKS}.name ,'{BOOKS}'.author, '{BOOKS}'.year_published, '{BOOKS}'.img_url, '{BOOKS}'.info, '{TYPES}'.days_to_loan, '{TYPES}'.fee_per_day, '{BOOKS}'.category    FROM '{BOOKS}' inner join '{TYPES}' on '{BOOKS}'.type_id = '{TYPES}'.id WHERE '{BOOKS}'.status = {True} and '{TYPES}'.status = {True} and '{BOOKS}'.copies > 0 and '{BOOKS}'.name like "%{_name}%";'''
        x = self.select_data(query=query1)
        return x



    #Users only $$$
    def select_books_by_name_admin(self,_name):
        query1 = f'''SELECT *  FROM '{BOOKS}' WHERE '{BOOKS}'.name like "%{_name}%";'''
        x = self.select_data(query=query1)
        return x        

    #Users only $$$
    def select_books_by_author_admin(self,_author):
        query1 = f'''SELECT *  FROM '{BOOKS}' WHERE '{BOOKS}'.author like "%{_author}%";'''
        x = self.select_data(query=query1)
        return x        

    #Users only $$$
    def select_books_by_author(self,_author):
        query1 = f'''SELECT {BOOKS}.id , {BOOKS}.name ,'{BOOKS}'.author, '{BOOKS}'.year_published, '{BOOKS}'.img_url, '{BOOKS}'.info, '{TYPES}'.days_to_loan, '{TYPES}'.fee_per_day, '{BOOKS}'.category    FROM '{BOOKS}' inner join '{TYPES}' on '{BOOKS}'.type_id = '{TYPES}'.id WHERE '{BOOKS}'.status = {True} and '{TYPES}'.status = {True} and '{BOOKS}'.copies > 0 and '{BOOKS}'.author like "%{_author}%";'''
        x = self.select_data(query=query1)
        return x

#Update_________________________________________
    #Admin only $$$
    def update_books_type(self,_type_id,_id):
        query = f"UPDATE {BOOKS} SET type_id={_type_id} WHERE id={_id}"
        self.execute_query(query)  

    #Admin only $$$
    def update_books_name(self,_name,_id):
        query = f"UPDATE '{BOOKS}' SET name='{_name}' WHERE id={_id}"
        self.execute_query(query)  

    #Admin only $$$
    def update_books_author(self,_author,_id):
        query = f"UPDATE '{BOOKS}' SET author='{_author}' WHERE id={_id}"
        self.execute_query(query)  

    #Admin only $$$
    def update_books_year_published(self,_year_published,_id):
        query = f"UPDATE '{BOOKS}' SET year_published='{_year_published}' WHERE id={_id}"
        self.execute_query(query)  
  
    #Admin only $$$
    def update_books_img_url(self,_img_url,_id):
        query = f"UPDATE '{BOOKS}' SET img_url='{_img_url}' WHERE id={_id}"
        self.execute_query(query)  

    #Admin only $$$
    def update_books_info(self,_info,_id):
        query = f"UPDATE '{BOOKS}' SET info='{_info}' WHERE id={_id}"
        self.execute_query(query)  

    #Admin only $$$
    def update_books_category(self,_category,_id):
        query = f"UPDATE '{BOOKS}' SET category='{_category}' WHERE id={_id}"
        self.execute_query(query)  
  
    #Admin only $$$
    def update_books_status(self,_status,_id):
        query = f"UPDATE '{BOOKS}' SET status={_status} WHERE id={_id}"
        self.execute_query(query)  

    #Admin only $$$
    def update_books_copies(self,_copies_after,_id):
        query1 = f"SELECT price FROM {BOOKS} WHERE  {BOOKS}.id = {_id} ;"
        price=self.select_single_data(query=query1)
        query2=f"SELECT copies FROM {BOOKS} WHERE  {BOOKS}.id = {_id} ;"
        copies_before=self.select_single_data(query=query2)
        query3 = f"UPDATE {BOOKS} SET copies={_copies_after} WHERE id={_id}"
        self.execute_query(query3)        
        copies = int(_copies_after) - int(copies_before)
        query4 = f"SELECT local_expenses FROM {CASHFLOW} WHERE  {CASHFLOW}.id = {1} ;"
        expenses=self.select_single_data(query=query4)
        new_expenses = int(expenses) + (int(copies)*int(price))
        query5 = f"UPDATE {CASHFLOW} SET local_expenses={new_expenses} WHERE {CASHFLOW}.id = {1} ;"
        self.execute_query(query5)

  

#Helpers_________________________________________
    #Admin only $$$
    def books_id(self):
        query1=f"SELECT MAX(id) FROM '{BOOKS}';"
        x = self.select_single_data(query=query1)
        return x

    #Admin only $$$
    def get_book_by_id(self,_id):
        query1=f"SELECT * FROM '{BOOKS}' WHERE '{BOOKS}'.id={_id};"
        x=self.select_data(query=query1)
        return x[0]

#------------------Types--------------------------------------

    #Admin only $$$
    def insert_type(self,_days_to_loan,_fee_per_day):
        query = f"INSERT INTO {TYPES} (days_to_loan,fee_per_day,status) VALUES ({_days_to_loan},{_fee_per_day},{True});"
        self.execute_query(query)

#Select_________________________________________
    #Admin only $$$
    def select_all_types(self):
        x=self.select_data(table=TYPES)
        return x

    #Admin only $$$
    def select_types_active(self):
        query1 = f"SELECT * FROM '{TYPES}' WHERE  '{TYPES}'.status = {True} ;"
        x = self.select_data(query=query1)
        return x

#Update_________________________________________
    #Admin only $$$
    def update_type_active(self,_status,_id):
        query = f"UPDATE {TYPES} SET status={_status} WHERE id={_id}"
        self.execute_query(query)    

#Helpers_________________________________________
    #Admin only $$$
    def select_all_types_id(self):
        x=self.select_data(query=f"SELECT id from '{TYPES}'")
        a=[]
        for s in x:
            for r in s:
                a.append(r)
        return a

    #Admin only $$$
    def select_types_from_a_book(self,_id_book):
        x=self.select_data(query=f"SELECT '{TYPES}'.days_to_loan , '{TYPES}'.fee_per_day from '{TYPES}' inner join '{BOOKS}' on '{BOOKS}'.type_id = '{TYPES}'.id WHERE '{BOOKS}'.id = {_id_book};")
        a=[]
        for s in x:
            for r in s:
                a.append(r)
        return a

#------------------Loans---------------------------------

    #Admin only $$$
    def insert_loan(self,_customer_id,_book_id):
        days_to_loan=self.days_to_loan_a_book(_book_id)
        now = datetime.now()
        delta = timedelta(days=days_to_loan)
        date_of_return= now + delta
        if date_of_return.strftime('%a')=="Sat":
            delta = timedelta(days=days_to_loan+1)
            date_of_return= now + delta
            strReturn = date_of_return.strftime('%d-%m-%Y, %H:%M:%S')
        else:
            strReturn = date_of_return.strftime('%d-%m-%Y, %H:%M:%S')
        strStrat = now.strftime('%d-%m-%Y, %H:%M:%S')
        query = f"INSERT INTO {LOANS} (customer_id,book_id,date_of_start,date_of_return,status) VALUES ({_customer_id},{_book_id},'{strStrat}','{strReturn}',{2341});"
        self.execute_query(query)
        x = self.select_single_data(query=f"SELECT copies FROM '{BOOKS}' where '{BOOKS}'.id = {_book_id} ;")
        query3 = f"UPDATE {BOOKS} SET copies={x-1} WHERE id={_book_id};"
        self.execute_query(query3)   

#Select_________________________________________
    #Admin only $$$
    def select_all_loans(self):
        x=self.select_data(table=LOANS)
        return x

    #User only $$$
    def select_history_loans_for_single_user(self,_id):
        query1 = f"SELECT {LOANS}.id , {BOOKS}.name ,'{BOOKS}'.author, '{BOOKS}'.year_published, '{BOOKS}'.img_url, '{BOOKS}'.info, '{TYPES}'.days_to_loan, '{TYPES}'.fee_per_day, '{BOOKS}'.category, '{LOANS}'.date_of_start, '{LOANS}'.date_of_return, '{LOANS}'.status   FROM '{TYPES}' inner join '{BOOKS}' on '{BOOKS}'.type_id = '{TYPES}'.id inner join '{LOANS}' on '{LOANS}'.book_id = '{BOOKS}'.id inner join '{CUSTOMERS}' on '{LOANS}'.customer_id = '{CUSTOMERS}'.id  WHERE  '{CUSTOMERS}'.id = {_id} and '{LOANS}'.status != {2341} ;"
        res = self.select_data(query=query1)
        return res




    #User only $$$
    def select_history_loans_for_single_user_by_name(self,_id , _name):
        query1 = f'''SELECT '{LOANS}'.id , '{BOOKS}'.name ,'{BOOKS}'.author, '{BOOKS}'.year_published, '{BOOKS}'.img_url, '{BOOKS}'.info, '{TYPES}'.days_to_loan, '{TYPES}'.fee_per_day, '{BOOKS}'.category, '{LOANS}'.date_of_start, '{LOANS}'.date_of_return, '{LOANS}'.status   FROM '{TYPES}' inner join '{BOOKS}' on '{BOOKS}'.type_id = '{TYPES}'.id inner join '{LOANS}' on '{LOANS}'.book_id = '{BOOKS}'.id inner join '{CUSTOMERS}' on '{LOANS}'.customer_id = '{CUSTOMERS}'.id  WHERE  '{CUSTOMERS}'.id = {_id} and '{LOANS}'.status != {2341}  and '{BOOKS}'.name like "%{_name}%" ;'''
        res = self.select_data(query=query1)
        return res

    #User only $$$
    def select_history_loans_for_single_user_by_category(self,_id , _category):
        query1 = f'''SELECT {LOANS}.id , {BOOKS}.name ,'{BOOKS}'.author, '{BOOKS}'.year_published, '{BOOKS}'.img_url, '{BOOKS}'.info, '{TYPES}'.days_to_loan, '{TYPES}'.fee_per_day, '{BOOKS}'.category, '{LOANS}'.date_of_start, '{LOANS}'.date_of_return, '{LOANS}'.status   FROM '{TYPES}' inner join '{BOOKS}' on '{BOOKS}'.type_id = '{TYPES}'.id inner join '{LOANS}' on '{LOANS}'.book_id = '{BOOKS}'.id inner join '{CUSTOMERS}' on '{LOANS}'.customer_id = '{CUSTOMERS}'.id  WHERE  '{CUSTOMERS}'.id = {_id} and '{LOANS}'.status != {2341} and '{BOOKS}'.category like "%{_category}%" ;'''
        res = self.select_data(query=query1)
        return res



    #User only $$$
    def select_active_loans_for_single_user(self,_id):
        query1 = f"SELECT {LOANS}.id , {BOOKS}.name ,'{BOOKS}'.author, '{BOOKS}'.year_published, '{BOOKS}'.img_url, '{BOOKS}'.info, '{TYPES}'.days_to_loan, '{TYPES}'.fee_per_day, '{BOOKS}'.category, '{LOANS}'.date_of_start, '{LOANS}'.date_of_return, '{LOANS}'.status, '{BOOKS}'.id   FROM '{TYPES}' inner join '{BOOKS}' on '{BOOKS}'.type_id = '{TYPES}'.id inner join '{LOANS}' on '{LOANS}'.book_id = '{BOOKS}'.id inner join '{CUSTOMERS}' on '{LOANS}'.customer_id = '{CUSTOMERS}'.id  WHERE  '{CUSTOMERS}'.id = {_id} and '{LOANS}'.status = {2341} ;"
        res = self.select_data(query=query1)
        return res

    def select_late_loans(self):
        query1 = f"SELECT '{LOANS}'.id, '{LOANS}'.customer_id, '{LOANS}'.book_id, '{LOANS}'.date_of_start, '{LOANS}'.date_of_return, '{LOANS}'.status, '{CUSTOMERS}'.name, '{CUSTOMERS}'.city, '{CUSTOMERS}'.date_of_birth, '{CUSTOMERS}'.date_of_join, '{CUSTOMERS}'.email, '{CUSTOMERS}'.password, '{CUSTOMERS}'.status, '{CUSTOMERS}'.pay_status, '{BOOKS}'.name  , '{BOOKS}'.author, '{BOOKS}'.category , '{TYPES}'.days_to_loan, '{TYPES}'.fee_per_day  FROM '{CUSTOMERS}' inner join '{LOANS}' on '{CUSTOMERS}'.id = '{LOANS}'.customer_id inner join '{BOOKS}' on '{BOOKS}'.id = '{LOANS}'.book_id inner join '{TYPES}' on '{TYPES}'.id = '{BOOKS}'.type_id  WHERE  '{LOANS}'.status > {0} and  '{LOANS}'.status != {2341} ;"
        res = self.select_data(query=query1)
        return res

    def select_active_loans(self):
        onTime = []
        lates = []
        query1 = f"SELECT '{LOANS}'.id, '{LOANS}'.customer_id, '{LOANS}'.book_id, '{LOANS}'.date_of_start, '{LOANS}'.date_of_return, '{LOANS}'.status, '{CUSTOMERS}'.name, '{CUSTOMERS}'.city, '{CUSTOMERS}'.date_of_birth, '{CUSTOMERS}'.date_of_join, '{CUSTOMERS}'.email, '{CUSTOMERS}'.password, '{CUSTOMERS}'.status, '{CUSTOMERS}'.pay_status, '{BOOKS}'.name  , '{BOOKS}'.author, '{BOOKS}'.category , '{TYPES}'.days_to_loan, '{TYPES}'.fee_per_day  FROM '{CUSTOMERS}' inner join '{LOANS}' on '{CUSTOMERS}'.id = '{LOANS}'.customer_id inner join '{BOOKS}' on '{BOOKS}'.id = '{LOANS}'.book_id inner join '{TYPES}' on '{TYPES}'.id = '{BOOKS}'.type_id  WHERE '{LOANS}'.status = {2341} ;"
        # query1 = f"SELECT * FROM '{LOANS}' WHERE  '{LOANS}'.status = {2341} ;"
        res = self.select_data(query=query1)
        for item in res :
            date = datetime.strptime(item[4],'%d-%m-%Y, %H:%M:%S')
            today = datetime.now()
            if today > date:lates.append(item)
            else:onTime.append(item)
        con = {
            "time":onTime,
            "late":lates
        }     
        return con

    def select_all_active_loans(self):
        query1 = f"SELECT '{LOANS}'.id, '{LOANS}'.customer_id, '{LOANS}'.book_id, '{LOANS}'.date_of_start, '{LOANS}'.date_of_return, '{LOANS}'.status, '{CUSTOMERS}'.name, '{CUSTOMERS}'.city, '{CUSTOMERS}'.date_of_birth, '{CUSTOMERS}'.date_of_join, '{CUSTOMERS}'.email, '{CUSTOMERS}'.password, '{CUSTOMERS}'.status, '{CUSTOMERS}'.pay_status, '{BOOKS}'.name  , '{BOOKS}'.author, '{BOOKS}'.category , '{TYPES}'.days_to_loan, '{TYPES}'.fee_per_day  FROM '{CUSTOMERS}' inner join '{LOANS}' on '{CUSTOMERS}'.id = '{LOANS}'.customer_id inner join '{BOOKS}' on '{BOOKS}'.id = '{LOANS}'.book_id inner join '{TYPES}' on '{TYPES}'.id = '{BOOKS}'.type_id  WHERE '{LOANS}'.status = {2341} ;"
        # query1 = f"SELECT * FROM '{LOANS}' WHERE  '{LOANS}'.status = {2341} ;"
        res = self.select_data(query=query1)
        return res

#Update_________________________________________
    #Admin only $$$
    def update_loan_status_admin(self,_customer_id , _book_id,_delay_days):
        query1 = f"SELECT '{LOANS}'.id FROM '{LOANS}' WHERE '{LOANS}'.customer_id = {_customer_id} and '{LOANS}'.book_id = {_book_id} and {LOANS}.status = {2341};"
        x=self.select_single_data(query=query1)
        query2 = f"UPDATE '{LOANS}' SET status={_delay_days} WHERE '{LOANS}'.id={x};"
        self.execute_query(query=query2)    

    #User only $$$
    def return_a_book_for_customers(self,_customer_id , _book_id,_loan_id):
        query1 = f"SELECT date_of_return FROM '{LOANS}' WHERE '{LOANS}'.customer_id ={_customer_id} and '{LOANS}'.book_id ={_book_id} and '{LOANS}'.status ={2341};"
        x=self.select_single_data(query=query1)
        no_str = datetime.strptime(x,'%d-%m-%Y, %H:%M:%S')
        today = datetime.now()
        delta = today - no_str
        query2 = f"UPDATE '{LOANS}' SET status={delta.days} WHERE id={_loan_id};"
        self.execute_query(query=query2)
        y = self.select_single_data(query=f"SELECT copies FROM '{BOOKS}' where '{BOOKS}'.id = {_book_id} ;")
        query3 = f"UPDATE '{BOOKS}' SET copies={y+1} WHERE '{BOOKS}'.id = {_book_id};"
        self.execute_query(query=query3)

#Helpers_________________________________________
    #Check if the user has a book like this
    #Return False or the id of this loan
    def do_you_have_a_book_like_this(self,_customer_id , _book_id):
        query1 = f"SELECT '{LOANS}'.id FROM '{LOANS}' WHERE  '{LOANS}'.customer_id = {_customer_id} and '{LOANS}'.book_id = {_book_id} and '{LOANS}'.status = {2341} ;"
        res = self.select_data(query=query1)
        if res == []:
            return False
        else:
            return res

    #Check if the user has 3 books that he still not returned
    #Return False or True if he has 3 books
    def do_you_have_3books_open_loans(self,_customer_id):
        query1 = f"SELECT '{LOANS}'.id FROM '{LOANS}' WHERE  '{LOANS}'.customer_id = {_customer_id} and '{LOANS}'.status = {2341} ;"
        res = self.select_data(query=query1)
        if len(res)<3:
            return False
        else:
            return True

    #Helper to insert row to the LOANS
    def days_to_loan_a_book(self,_book_id):
        query1 = f"SELECT days_to_loan FROM {TYPES} inner join {BOOKS} on {BOOKS}.type_id={TYPES}.id WHERE {BOOKS}.id={_book_id};"
        x=self.select_single_data(query=query1)
        return x

#------------------CashFlow------------------------------

    #Select     #admin        $$$
    def select_all_cashFlow(self):
        x=self.select_data(table=CASHFLOW)
        return x

    #Insert     #admin  2 functions      $$$
    def insert_cash_row(self):
        today = datetime.now()
        mail = Mailer(email='itaygroer@gmail.com', password='itayitay')
        if  today.day == 1 :
            query1 = f"SELECT count(*) FROM {CUSTOMERS} WHERE  {CUSTOMERS}.pay_status = {True} ;"
            x=self.select_single_data(query=query1)
            sum = int(x) * 30
            today = datetime.now()
            str = today.strftime('%d-%m-%Y, %H:%M:%S')
            query2 = f"SELECT local_expenses FROM {CASHFLOW} WHERE  {CASHFLOW}.id = {1} ;"
            expenses=self.select_single_data(query=query2)
            query3 = f"INSERT INTO {CASHFLOW} (date, expenses, income, local_expenses) VALUES ('{str}',{int(expenses)},{sum},{0});"
            self.execute_query(query3)
            query4 = f"UPDATE {CASHFLOW} SET local_expenses={0} WHERE {CASHFLOW}.id = {1} ;"
            self.execute_query(query4)
            query5 = f"UPDATE {CUSTOMERS} SET pay_status={False} WHERE status={False};"
            self.execute_query(query5)
            mail.send(receiver='itay2341@gmail.com', subject='Cash-Flow', message='DONE!')
        else:
            mail.send(receiver='itay2341@gmail.com', subject='Cash-Flow', message='Not today!')

