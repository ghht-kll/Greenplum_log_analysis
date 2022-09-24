
from ast import Lambda
from audioop import reverse
from tkinter import N
import pandas as pd
import re

class Greenplum_log_analysis:
    def __init__(self) -> None:
        self.tbl_dev_from_join = dict()
        self.tbl_dev_into = dict()

        self.tbl_etl_from_join = dict()
        self.tbl_etl_into = dict()

    def read_from_file(self) -> None:
        self.reader = pd.read_csv('log_week_end.csv', usecols=['loguser','query'])

    def add_tbl_fj_i(self, tbldict, tbl) -> None:
        if tbl in tbldict:
            tbldict[tbl] = tbldict[tbl] + 1
        else:
            tbldict[tbl] = 1

    def add_tbl_etl_or_dev(self, row, tbldict) -> None:

        query_jf = re.findall(r"(((join|JOIN) tbl_\d{0,}[0-9])|((from|FROM) tbl_\d{0,}[0-9]))", row[2])

        if query_jf is not None:
            tbls_jf = re.findall(r"\d{0,}[0-9]", str(query_jf))

            for tbl_jf in tbls_jf:
                if tbldict == "etl":
                    self.add_tbl_fj_i(self.tbl_etl_from_join, tbl_jf)
                else:
                    self.add_tbl_fj_i(self.tbl_dev_from_join, tbl_jf)

        query_i = re.findall(r"((into|INTO) tbl_\d{0,}[0-9])", row[2])

        if query_i is not None:
            tbls_i =  re.findall(r"\d{0,}[0-9]", str(query_i))

            for tbl_i in tbls_i:
                if tbldict == "etl":
                    self.add_tbl_fj_i(self.tbl_etl_into, tbl_i)
                else:
                    self.add_tbl_fj_i(self.tbl_dev_into, tbl_i)

    def init_dev_or_etl(self) -> None:
        df = pd.DataFrame(self.reader)

        for row in df.itertuples():
            loguser = re.match(r"etl_\d{0,}[0-9]", row[1])

            if loguser is not None:
                self.add_tbl_etl_or_dev(row, "etl")
            else:
                self.add_tbl_etl_or_dev(row, "dev")

    def tbl_sorted(self) -> None:
        sorted_tbl_dev_from_join = dict(sorted(self.tbl_dev_from_join.items(), reverse = True, key=lambda item: item[1]))
        self.tbl_dev_from_join = sorted_tbl_dev_from_join

        sorted_tbl_dev_into = dict(sorted(self.tbl_dev_into.items(), reverse = True, key=lambda item: item[1]))
        self.tbl_dev_into = sorted_tbl_dev_into

        sorted_tbl_etl_from_join = dict(sorted(self.tbl_etl_from_join.items(), reverse = True, key=lambda item: item[1]))
        self.tbl_etl_from_join = sorted_tbl_etl_from_join

        sorted_tbl_etl_into = dict(sorted(self.tbl_etl_into.items(), reverse = True, key=lambda item: item[1]))
        self.tbl_etl_into = sorted_tbl_etl_into        

def main() -> int:
    greenplum_log_analysis = Greenplum_log_analysis()
    greenplum_log_analysis.read_from_file()
    greenplum_log_analysis.init_dev_or_etl()

    greenplum_log_analysis.tbl_sorted()

    print(greenplum_log_analysis.tbl_dev_from_join)

    return 0

if __name__ == '__main__':
    main()
