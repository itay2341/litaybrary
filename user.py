from datetime import datetime
from flask import Blueprint, render_template, request
user = Blueprint('user',__name__,url_prefix='/user')
from app import dbms

# --------------------------------------------------
#After sign up 
@user.route('/welcome',methods=["POST"])
def user_welcome():
    if request.method == 'POST':
        accName = request.form.get('name')
        accCity = request.form.get('city')
        accBday = request.form.get('date_of_birth')
        if accBday == None :return
        dt = datetime.strptime(accBday, '%Y-%m-%d')
        strBday = dt.strftime('%d-%m-%Y, %H:%M:%S')
        accEmail = request.form.get('email')
        accPass = request.form.get('password')
        dbms.insert_customer(accName,accCity,strBday,accEmail,accPass)
        idCustomer=dbms.customer_id()
        return render_template("well.html",idCustomer=idCustomer)

#After log in 
@user.route('/welcomecust',methods=["POST"])
def user_welcome2():
    accEmail = request.form.get('email')
    accPass = request.form.get('password')
    if dbms.get_customer_id_auth(accPass,accEmail)==0: return render_template("index.html")
    idCustomer=dbms.get_customer_id_auth(accPass,accEmail)
    return render_template("well2.html",idCustomer=idCustomer) 

#-----------------------------------------------------
#Customer's navbar

#Home page
@user.route('/home',methods=["POST"])
def user_home():
    idCustomer = request.form.get('idCustomer')
    return render_template("welcome.html",x ="",idCustomer=idCustomer) 

#Books page
@user.route('/books',methods=["POST"])
def user_books():
    books = dbms.select_books_for_users()
    idCustomer = request.form.get('idCustomer')
    return render_template("books.html",books=books,idCustomer=idCustomer,msg1="All",msg2="We have a variety of books - find out something you like and don't compromise!",x="")

#My loans page
@user.route('/myloans',methods=["POST"])
def user_myloans():
    idCustomer = request.form.get('idCustomer')
    history_loans = dbms.select_history_loans_for_single_user(int(idCustomer))
    active_loans = dbms.select_active_loans_for_single_user(int(idCustomer))
    return render_template("myloans.html",idCustomer=idCustomer,history_loans=history_loans ,active_loans=active_loans,x="")    

#Procedures page
@user.route('/procedures',methods=["POST"])
def user_procedures():
    idCustomer = request.form.get('idCustomer')
    return render_template("procedures.html",idCustomer=idCustomer)    

#Personal details page
@user.route('/details',methods=["POST"])
def user_datails():
    idCustomer = request.form.get('idCustomer')
    now = datetime.now()
    year=now.year
    month=now.month
    day=now.day
    if day<10:day="0"+str(day)
    if month<10:month="0"+str(month)
    customer = dbms.select_customer_by_id(int(idCustomer))
    return render_template("details.html",customer=customer,x="",idCustomer=idCustomer,year=year,month=month,day=day) 

#----------------------------------------------------------
#Inside Pages

#From books page - *book info*
@user.route('/info_book',methods=["POST"])
def user_info():
    idBook = request.form.get('idBook')
    idCustomer=request.form.get('idCustomer')
    book = dbms.get_book_by_id(int(idBook))
    types_book = dbms.select_types_from_a_book(int(idBook))
    return render_template("info_book.html",book=book,idCustomer=idCustomer,types_book=types_book)           

#From info page - *loan a book* 
@user.route('/loan',methods=["POST"])
def user_loan():
    idCustomer = request.form.get('idCustomer')
    idBook = request.form.get('idBook')
    if dbms.do_you_have_3books_open_loans(int(idCustomer))== False:
        if dbms.do_you_have_a_book_like_this(int(idCustomer),int(idBook)) == False :
            dbms.insert_loan(int(idCustomer),int(idBook))
            history_loans = dbms.select_history_loans_for_single_user(int(idCustomer))
            active_loans = dbms.select_active_loans_for_single_user(int(idCustomer))
            return render_template("myloans.html",x="You did it! enjoy from the book :)",idCustomer=idCustomer,history_loans=history_loans,active_loans=active_loans)  
        else:
            history_loans = dbms.select_history_loans_for_single_user(int(idCustomer))
            active_loans = dbms.select_active_loans_for_single_user(int(idCustomer))
            return render_template("myloans.html",x="you can't loan the same book you already have :) ",idCustomer=idCustomer,history_loans=history_loans,active_loans=active_loans)  
    else:
        history_loans = dbms.select_history_loans_for_single_user(int(idCustomer))
        active_loans = dbms.select_active_loans_for_single_user(int(idCustomer))
        return render_template("myloans.html",x="You can't loan more than 3 books without returing",idCustomer=idCustomer,history_loans=history_loans,active_loans=active_loans)  

#From loans page - *return a book*
@user.route('/return',methods=["POST"])
def user_return():
    idCustomer = request.form.get('idCustomer')
    idLoan = request.form.get('idLoan')
    idBook = request.form.get('idBook')
    dbms.return_a_book_for_customers(int(idCustomer),int(idBook),int(idLoan))
    history_loans = dbms.select_history_loans_for_single_user(int(idCustomer))
    active_loans = dbms.select_active_loans_for_single_user(int(idCustomer))
    return render_template("myloans.html",idCustomer=idCustomer,history_loans=history_loans ,active_loans=active_loans,x="")    

#From loans page - *search a loan*
@user.route('/searchloans',methods=["POST"])
def user_search_loans():
    idCustomer = request.form.get('idCustomer')
    active_loans = dbms.select_active_loans_for_single_user(int(idCustomer))
    x = request.form.get('x')
    input4= request.form.get('input')
    if x == "name":
        if dbms.select_history_loans_for_single_user_by_name(int(idCustomer),input4) ==[]:
            history_loans =[]
            return render_template("myloans.html",idCustomer=idCustomer,history_loans=history_loans,active_loans=active_loans,x="no such a loan like this")    
        else:
            history_loans= dbms.select_history_loans_for_single_user_by_name(int(idCustomer),input4)
            return render_template("myloans.html",idCustomer=idCustomer,history_loans=history_loans,active_loans=active_loans,x="your results")    
    elif x == "category":
        if  dbms.select_history_loans_for_single_user_by_category(int(idCustomer),input4) ==[]:
            history_loans =[]
            return render_template("myloans.html",idCustomer=idCustomer,history_loans=history_loans,active_loans=active_loans,x="no such a loan like this")
        else:
            history_loans= dbms.select_history_loans_for_single_user_by_category(int(idCustomer),input4)
            return render_template("myloans.html",idCustomer=idCustomer,history_loans=history_loans,active_loans=active_loans,x="your results")    
    else:
        history_loans = dbms.select_history_loans_for_single_user(int(idCustomer))
        active_loans = dbms.select_active_loans_for_single_user(int(idCustomer))
        return render_template("myloans.html",idCustomer=idCustomer,history_loans=history_loans ,active_loans=active_loans,x="")    

#From details page - *update name/city/Birth-day*
@user.route('/detailsEdit',methods=["POST"])
def user_detailsEdit():
    idCustomer = request.form.get('idCustomer')
    name = request.form.get('name')
    city = request.form.get('city')
    date = request.form.get('date')
    now = datetime.now()
    year=now.year
    month=now.month
    day=now.day
    if day<10:day="0"+str(day)
    if month<10:month="0"+str(month)
    if name == None:
        if city == None:
            if date == None:#to check it with the thunder client 
                return render_template("index.html") 
            else:
                dt = datetime.strptime(date, '%Y-%m-%d')
                strBday = dt.strftime('%d-%m-%Y, %H:%M:%S')
                dbms.update_customer_date_of_birth(strBday,int(idCustomer))
                customer = dbms.select_customer_by_id(int(idCustomer))
                return render_template("details.html",customer=customer,x="Your birth-day is updated",idCustomer=idCustomer,year=year,month=month,day=day) 
        else:
            dbms.update_customer_city(city,int(idCustomer))
            customer = dbms.select_customer_by_id(int(idCustomer))
            return render_template("details.html",customer=customer,x="Your city is updated",idCustomer=idCustomer,year=year,month=month,day=day) 
    else:
        dbms.update_customer_name(name,int(idCustomer))
        customer = dbms.select_customer_by_id(int(idCustomer))
        return render_template("details.html",customer=customer,x="Your name is updated",idCustomer=idCustomer,year=year,month=month,day=day) 

#From details page -  *update email/password*
@user.route('/detailsEdit2',methods=["POST"])
def user_detailsEdit2():
    idCustomer = request.form.get('idCustomer')
    email = request.form.get('email')
    pass1 = request.form.get('pass')
    now = datetime.now()
    year=now.year
    month=now.month
    day=now.day
    if day<10:day="0"+str(day)
    if month<10:month="0"+str(month)
    if email == None:
        if pass1 == None:#to check it with the thunder client 
            return render_template("index.html") 
        else:
            dbms.update_customer_password(pass1,int(idCustomer))
            customer = dbms.select_customer_by_id(int(idCustomer))
            return render_template("details.html",customer=customer,x="Your password is updated",idCustomer=idCustomer,year=year,month=month,day=day) 
    else:
        dbms.update_customer_email(email,int(idCustomer))
        customer = dbms.select_customer_by_id(int(idCustomer))
        return render_template("details.html",customer=customer,x="Your email is updated",idCustomer=idCustomer,year=year,month=month,day=day) 

#From details page - *close account*
@user.route('/status',methods=["POST"])
def user_status():
    idCustomer = request.form.get('idCustomer')
    if dbms.select_active_loans_for_single_user(int(idCustomer))== []:
        dbms.update_customer_status(False,int(idCustomer))
        return render_template("index.html")  
    else:
        history_loans = dbms.select_history_loans_for_single_user(int(idCustomer))
        active_loans = dbms.select_active_loans_for_single_user(int(idCustomer))
        return render_template("myloans.html",x="You can't close your account - you need to bring all the books back!",idCustomer=idCustomer,history_loans=history_loans,active_loans=active_loans)  

#From home page or the footer - *about me*
@user.route('/about')
def user_about():
    idCustomer = request.args['idCustomer']
    if idCustomer == None: return render_template("index.html")
    return render_template("aboutme.html",idCustomer=idCustomer)  

#---------------------------------------------------------
#Customer's navbar2 - Books navbar

#From books page - customer choose to category for a book 
@user.route('/category',methods=["POST"])
def user_category():
    idCustomer = request.form.get('idCustomer')
    category = request.form.get('category')
    if dbms.select_books_by_category(category) == []:
        return render_template("books.html",idCustomer=idCustomer,books=[],msg1=category,msg2="",x="no more books from this category")  
    else:
        books= dbms.select_books_by_category(category)
        return render_template("books.html",idCustomer=idCustomer,books=books,msg1=category,msg2="",x="")    

#From books page - customer is searching a book 
@user.route('/search',methods=["POST"])
def user_search():
    idCustomer = request.form.get('idCustomer')
    x = request.form.get('x')
    input4= request.form.get('input')
    if x == "name":
        if dbms.select_books_by_name(input4) != []:
            books= dbms.select_books_by_name(input4)
            return render_template("books.html",idCustomer=idCustomer,books=books,msg1="All",msg2="We have a variety of books - find out something you like and don't compromise!",x="")    
        else:
            books= dbms.select_books_for_users()
            return render_template("books.html",idCustomer=idCustomer,books=books,msg1="All",msg2="We have a variety of books - find out something you like and don't compromise!",x="no such a book with this name")    
    if x == "author":
        if dbms.select_books_by_author(input4) != []:
            books= dbms.select_books_by_author(input4)
            return render_template("books.html",idCustomer=idCustomer,msg1="All",msg2="We have a variety of books - find out something you like and don't compromise!",books=books,x="")    
        else:
            books= dbms.select_books_for_users()
            return render_template("books.html",idCustomer=idCustomer,msg1="All",msg2="We have a variety of books - find out something you like and don't compromise!",books=books,x="no such a book with this author name")    
    if x != "name" and x != "author":
        books= dbms.select_books_for_users()
        return render_template("books.html",idCustomer=idCustomer,msg1="All",msg2="We have a variety of books - find out something you like and don't compromise!",books=books,x="Search invaild")

