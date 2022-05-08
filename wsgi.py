from app import app, dbms 


# #Other Thread
from threading import Timer

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args,**self.kwargs)
        print("Timer DONE-------------------------------------")

# Program entry point (main)
def main():
    print("------------------------------------------")
    dbms.create_db_tables()

    #Starting the Thread
    t = RepeatTimer(86400,dbms.insert_cash_row,[])
    t.start()
    app.run()

# Calling the main
if __name__ == "__main__": main()