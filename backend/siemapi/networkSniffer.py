import sys
import pyshark
import psycopg2
from datetime import datetime

# Establish a connection to the PostgreSQL database
class DatabaseHandler:
    def __init__(self, dbname="siemlight", user="siemlight", password="MCIF@ipl2024", host='localhost', port='5432'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Connected to the database")
        except psycopg2.Error as e:
            print("Unable to connect to the database:", e)

    def closeConnection(self):
        if self.conn:
            self.conn.close()
            print("Connection closed")
        else:
            print("No connection to close")

    def execute_query(self, query, values=None):
        if self.conn is None:
            print("Not connected to the database. Call connect() method first.")
            return

        try:
            with self.conn.cursor() as cur:
                if values:
                    cur.execute(query, values)
                    self.commit()
                    return
                else:
                    cur.execute(query)
                    result = cur.fetchall()
                    return result
        except psycopg2.Error as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()

    def insert_values(self, table, columns, values):
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in values])})"
        self.execute_query(query, values)

    def commit(self):
        if self.conn:
            self.conn.commit()

class NetworkSniffer:
    def __init__(self):
        self.capture = None

    def start_sniffer(self, interface):
        self.capture = pyshark.LiveCapture(interface=interface, bpf_filter='udp port 53')
        try:
            for packet in self.capture.sniff_continuously():
                if hasattr(packet, 'dns'):
                    if packet.dns.count_answers > "0":
                        strAlert = ''
                        if NetworkSniffer.searchValue(packet.dns.qry_name):
                            strAlert = 'A DNS request to {} was made from {}. This domain is a match to the internal database.'.format(packet.dns.qry_name,packet.ip.dst)
                            NetworkSniffer.insertAlert(packet.dns.qry_name, strAlert)
                        if NetworkSniffer.searchValue(packet.ip.src):
                            strAlert = "This IP Address {} returned a response to a DNS query from {}. This IP address is a match to the internal database.".format(packet.ip.src,packet.ip.dst)
                            NetworkSniffer.insertAlert(packet.dns.qry_name, strAlert)
                        if hasattr(packet.dns, "a"):
                            if NetworkSniffer.searchValue(packet.dns.a):
                                strAlert = "A DNS request returned a known malicious IP address ({}) from a query made by {}. This IP address is a match to the internal database.".format(packet.ip.a,packet.ip.src)
                                NetworkSniffer.insertAlert(packet.dns.a, strAlert)
                        else:
                            if hasattr(packet.dns,'ptr_domain_name'):
                                if NetworkSniffer.searchValue(packet.dns.ptr_domain_name):
                                    strAlert = 'A DNS request to {} was made from {}. This domain is a match to the internal database.'.format(packet.ptr_domain_name,packet.ip.dst)
                                    NetworkSniffer.insertAlert(packet.dns.qry_name, strAlert)
                            else:
                                if NetworkSniffer.searchValue(packet.dns.cname):
                                    strAlert = 'A DNS request to the CNAME {} was made from {}. This CNAME is a match to the internal database.'.format(packet.ptr_domain_name,packet.ip.dst)
                                    NetworkSniffer.insertAlert(packet.dns.cname, strAlert)
                                # print(packet.dns)
                                # print(packet.dns.cname)
                                # pass
        except Exception as e:
            # logger.error('An error occurred while sniffing and parsing packets.')
            print("Error: {}".format(e))

    @staticmethod
    def searchValue(value):
        db = DatabaseHandler()
        db.connect()
        search_query = "SELECT value FROM api_value WHERE value='"+value+"';"
        results = db.execute_query(search_query)
        db.closeConnection()
        if len(results) > 0:
            return True
        else:
            return False
    
    @staticmethod
    def insertAlert(value, message):
        alertLevel = NetworkSniffer.checkAlertLevel(value)
        current_time = datetime.now()
        formatted_time = current_time.strftime("%d-%m-%Y %H:%M:%S")
        # print("1")
        # print(type(alertLevel))
        # print("2")
        # print(type(formatted_time))
        # print("3")
        # print(type(message))
        newMessage = alertLevel+' - '+formatted_time+' - '+message
        table_name = 'api_alert'
        columns = ['level', 'message', 'acknowledge', 'created_at']
        values = [alertLevel, newMessage, False, current_time]
        db = DatabaseHandler()
        db.connect()
        db.insert_values(table_name, columns, values)
        db.closeConnection()
        

    @staticmethod
    def checkAlertLevel(value):
        db = DatabaseHandler()
        db.connect()
        search_query = "SELECT count(*) FROM api_feed ;"
        results = db.execute_query(search_query)
        print("NumFeeds: {}".format(results[0][0]))
        numFeeds = results[0][0]
        search_query = "SELECT * FROM api_value  WHERE value='"+value+"';"
        results = db.execute_query(search_query)
        print(results)
        print("CheckValue: {}".format(results[0][4]))
        checkValue = results[0][4]
        db.closeConnection()

        preLevel = checkValue/numFeeds
        if preLevel >= 1:
            return 'Critical'
        elif 0.9 <= preLevel <= 1:
            return 'High'
        elif 0.4 <= preLevel < 0.9:
            return 'Medium'
        elif 0.24 <= preLevel < 0.4:
            return 'Low'

if __name__ == "__main__":
    interface = sys.argv[1]
    sniffer = NetworkSniffer()
    sniffer.start_sniffer(interface) 
