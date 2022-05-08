from flask import Blueprint, render_template, request
admin = Blueprint('admin',__name__,url_prefix='/admin')
from app import dbms

# -------------------------------------------
#After log in
@admin.route('/welcome',methods=["POST"])
def admin_welcome():
    nameA = request.form.get('name')
    passA = request.form.get('password')
    if nameA=="itay2341" and passA=="2341":
        return render_template("admin.html",nameA=nameA)
    return render_template("index.html") 

#---------------------------------------------------------------
#Admin navbar

#Customer page
@admin.route('/customers',methods=["POST"])        
def admin_customers():
    id = request.form.get('id')
    active = request.form.get('active')
    if id == None:
        customers=dbms.select_all_customers()
        customers2=dbms.select_customers_active()
        return render_template("admin_customers.html",x="welcome itay",customers=customers,customers2=customers2)
    elif int(id) not in dbms.select_all_customers_id():
        customers=dbms.select_all_customers()
        customers2=dbms.select_customers_active()
        return render_template("admin_customers.html",x="Update faild, no customer id like that",customers=customers,customers2=customers2)
    elif int(active)==0: active=False
    elif int(active)==1: active=True
    else:
        customers=dbms.select_all_customers()
        customers2=dbms.select_customers_active()
        return render_template("admin_customers.html",x="Update faild, the status is invaild",customers=customers,customers2=customers2)
    dbms.update_customer_status(active,int(id))
    customers=dbms.select_all_customers()
    customers2=dbms.select_customers_active()
    return render_template("admin_customers.html",x="Update successfuly",customers=customers,customers2=customers2)

#Customer page - Searching
@admin.route('/search',methods=["POST"])
def admin_search_customers():
    x = request.form.get('x')
    input4 = request.form.get('input')
    if x == "all":
        customers = dbms.select_all_customers()
        return render_template("customers_search.html",customers=customers,a= "All customers")
    elif x == "name":
        customers = dbms.select_customers_by_name(input4)
        return render_template("customers_search.html",customers=customers, a= f"Searching by name: {input4}")
    elif x == "id":
        customers = dbms.select_customers_by_id(int(input4))
        return render_template("customers_search.html",customers=customers, a= f"Searching by id: {input4}")
    else:
        customers = dbms.select_all_customers()    
        return render_template("customers_search.html",customers=customers, a= "")

#Books page
@admin.route('/books',methods=["POST"])
def admin_books():
        books_id = request.form.get('id')
        active = request.form.get('active')
        if books_id == None:
            type_id = request.form.get('type_id')
            name = request.form.get('name')
            author = request.form.get('author')
            year_published = request.form.get('year_published')
            price = request.form.get('price')
            copies = request.form.get('copies')
            img_url = request.form.get('img_url')
            category = request.form.get('category')
            if type_id == None:
                books=dbms.select_all_books()
                books2=dbms.select_books_for_users()
                return render_template("admin_books.html",x="Welcome Itay",books=books,books2=books2)
            else:
                info = request.form.get('info')
                info = info.replace("'","’")
                if int(price) <=0 :
                    books=dbms.select_all_books()
                    books2=dbms.select_books_for_users()
                    return render_template("admin_books.html",x='''Added failed! "price" colunm is invalid ''',books=books,books2=books2)
                elif int(copies) <=0 :
                    books=dbms.select_all_books()
                    books2=dbms.select_books_for_users()
                    return render_template("admin_books.html",x='''Added failed! "copies" colunm is invalid ''',books=books,books2=books2)
                elif int(type_id) not in dbms.select_all_types_id():
                    books=dbms.select_all_books()
                    books2=dbms.select_books_for_users()
                    return render_template("admin_books.html",x='''Added failed! "type_id" colunm is invalid ''',books=books,books2=books2)
                dbms.insert_books(int(type_id),name,author,year_published,int(price),int(copies),img_url,info,category)
                books=dbms.select_all_books()
                books2=dbms.select_books_for_users()
                return render_template("admin_books.html",x="Added successfuly",books=books,books2=books2)
        else:
            if active==0: active=False
            elif active==1: active=True
            else:
                books=dbms.select_all_books()
                books2=dbms.select_books_for_users()
                return render_template("admin_books.html",x='''Update failed! "status" colunm is invalid ''',books=books,books2=books2)
            dbms.update_books_status(active,int(books_id))
            books=dbms.select_all_books()
            books2=dbms.select_books_for_users()
            return render_template("admin_books.html",x="Update successfuly",books=books,books2=books2)

#Books page - Searching
@admin.route('/search2',methods=["POST"])
def admin_search_books():
    x = request.form.get('x')
    input4 = request.form.get('input')
    if x == "all":
        books = dbms.select_all_books()
        return render_template("books_search.html",books=books,x= "All books")
    elif x == "name":
        books = dbms.select_books_by_name_admin(input4)
        return render_template("books_search.html",books=books, x= f"Searching by name: {input4}")
    elif x == "author":
        books = dbms.select_books_by_author_admin(input4)
        return render_template("books_search.html",books=books, x= f"Searching by author: {input4}")
    else:
        books = dbms.select_all_books()    
        return render_template("books_search.html",books=books, x= "")

#Types page
@admin.route('/types',methods=["POST"])
def admin_types():
        days = request.form.get('days_to_loan')
        fee = request.form.get('fee_per_day')
        if days == None:
            type_id = request.form.get('type_id')
            active = request.form.get('active')
            if type_id == None:
                types=dbms.select_all_types()
                types2=dbms.select_types_active()
                return render_template("admin_types.html",x="welcome itay",types=types,types2=types2)
            else:
                if int(type_id) not in dbms.select_all_types_id():
                    types=dbms.select_all_types()
                    types2=dbms.select_types_active()
                    return render_template("admin_types.html",x='''the "type_id" column is invalid''',types=types,types2=types2) 
                if int(active)==0:
                    active=False
                elif int(active)==1:
                    active=True
                else:
                    types=dbms.select_all_types()
                    types2=dbms.select_types_active()
                    return render_template("admin_types.html",x='''the "status" column is invalid''',types=types,types2=types2) 
                dbms.update_type_active(active,type_id)
                types=dbms.select_all_types()
                types2=dbms.select_types_active()
                return render_template("admin_types.html",x="Update successfuly",types=types,types2=types2)
        else:
            if int(days) <=0 or int(fee) <0:
                types=dbms.select_all_types()
                types2=dbms.select_types_active()
                return render_template("admin_types.html",x="Added failed",types=types,types2=types2)
            dbms.insert_type(int(days),int(fee))
            types=dbms.select_all_types()
            types2=dbms.select_types_active()
            return render_template("admin_types.html",x="Added successfuly",types=types,types2=types2)

#Loans status
@admin.route('/loans',methods=["POST"])
def admin_loans():
    customer_id = request.form.get('customer_id')
    book_id = request.form.get('book_id')
    delay_days = request.form.get('delay_days')
    loans = dbms.select_all_loans()
    if customer_id == None:
        return render_template("admin_loans.html",x="Hello dir admin",loans=loans)
    dbms.update_loan_status_admin(int(customer_id),int(book_id),int(delay_days))    
    return render_template("admin_loans.html",x="Update Success",loans=loans)

#Active Loans page
@admin.route('/active',methods=["POST"])
def admin_active():
    x = request.form.get('x')
    con = dbms.select_active_loans()
    loans = dbms.select_all_active_loans()
    if x == "late":
        return render_template("active_loans.html",loans=con["late"])
    elif x == "time":
        return render_template("active_loans.html",loans=con["time"])
    elif x == "all" :
        return render_template("active_loans.html",loans=loans)
    else:
        return render_template("active_loans.html",loans=loans)

#Late Loans page
@admin.route('/lates',methods=["POST"])
def admin_late_loans():
    loans = dbms.select_late_loans()
    return render_template("late_loans.html",loans=loans)
 
#Cach Flow page
@admin.route('/cashFlow',methods=["POST"])
def admin_cashFlow():
    cashFlow = dbms.select_all_cashFlow()
    return render_template("cashFlow.html",cashFlow=cashFlow)

#----------Helper-------------------------
@admin.route('/copies',methods=["POST"])
def admin_copies():
    copies = request.form.get('copies')
    id = request.form.get('id')
    if int(copies) < 0 or id == None :
        books=dbms.select_all_books()
        books2=dbms.select_books_for_users()
        return render_template("admin_books.html",x='''Update faild!''',books=books,books2=books2)
    else:
        dbms.update_books_copies(int(copies),int(id))
        books=dbms.select_all_books()
        books2=dbms.select_books_for_users()
        return render_template("admin_books.html",x='''Update success!''',books=books,books2=books2)
           
