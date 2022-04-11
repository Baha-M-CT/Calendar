import mysql.connector

#connect to DB and run the query
class Database:

    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = "Admin_2021"
        self.db = "my_events"

    # Connect to DB
    def __connect__(self):
        self.conn = mysql.connector.connect(user=self.user, password=self.password,
                                       host=self.host,
                                       database=self.db)
        self.cur = self.conn.cursor()

    # Disconnect from DB
    def __disconnect__(self):
        self.conn.close()

    # Fetch all events for one selected Day
    def fetch(self, searchdate):
        self.__date = searchdate
        self.__connect__()
        try:
            self.cur.execute("select EventId, EventTitle, EventStart, EventTime, EventDescr from event where EventStart = '" + searchdate + "'")
            result = self.cur.fetchall()
            self.__disconnect__()
            return result
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

    # Fetch all events for current Month
    def fetchmonth(self, searchmonth, searchyear):
        self.__month = searchmonth
        self.__year = searchyear
        self.__connect__()
        self.cur.execute("select EventId, EventTitle, EventStart, EventDescr from event where month(EventStart) = '" + searchmonth + "'")
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    # Will be used for Search Function
    def __fetchsearchid__(self):
        self.__connect__()
        self.cur.execute("select EventId from event where EventDescr like '%Test description15%' LIMIT 1")
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    # Add New Event
    def addevent(self, event_title, event_notes, sel_date, sel_hour, sel_min):
        self.__title = event_title
        self.__notes = event_notes
        self.__date = sel_date
        self.__hour = sel_hour
        self.__min = sel_min
        self.__connect__()
        __time__=sel_hour+':'+sel_min+':00'
        query = "insert into event (EventTitle,EventStart,EventEnd,EventDescr,EventTime,RepeatId) VALUES(%s,%s,%s,%s,%s,1)"
        b1=(event_title,sel_date,sel_date,event_notes,__time__)
        try:
            self.cur.execute(query, b1)
            self.conn.commit()
            return self.cur.lastrowid
        except mysql.connector.Error as err:
            print(err.msg)
            if err.msg == "Data too long for column 'EventTitle' at row 1":
                return -1
            elif err.msg == "Data too long for column 'EventDescr' at row 1":
                return -2
        finally:
            self.__disconnect__()

    # Execute SQL query
    def execute(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        self.__disconnect__()
