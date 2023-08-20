import psycopg2
import pandas as pd

# connect to database
conn = psycopg2.connect(
    host="localhost", database="postgres", user="postgres", password="example"
)

cur = conn.cursor()

cur.execute("""
    SELECT COUNT(DISTINCT cik) as number_of_funds
    FROM "filings"
    WHERE period_of_report='2021-06-30'
""")

result = cur.fetchone()    

print(f"Total number of funds filed for period 2021-06-30:\n{result[0]}")

cur.execute("""
    SELECT shares, holdings.cusip, security_name, ticker, period_of_report, holdings.filing_id
    FROM holdings
    INNER JOIN filings
    ON filings.filing_id = holdings.filing_id
    INNER JOIN holding_infos
    ON holdings.cusip = holding_infos.cusip
    WHERE (period_of_report = '2021-06-30' or period_of_report = '2021-03-31') and cik = '1661222'
""")

rows = cur.fetchall()    

cur.close()

holdings = pd.DataFrame(rows, columns =['Shares', 
                                        'CUSIP', 
                                        'SecurityName', 
                                        'Ticker', 
                                        'PeriodOfReport', 
                                        'FilingId'])

print(holdings)



