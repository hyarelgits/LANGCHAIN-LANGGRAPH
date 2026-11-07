Learning Roadmap
Day 1 ✅
Plain Text
ingest.py

Topics learned:

Plain Text
TextLoader
Text Splitter
Embeddings
Ollama
ChromaDB
Vector Storage

===============================

Day 2 ⭐
Plain Text
db_tools.py

Topics:

Plain Text
PostgreSQL
Database Connection
SQL Query
Cursor
Fetch Data
Connection Close

Typical file:


========================



import psycopg2

def get_customer(customer_id):

    conn = psycopg2.connect(
        host="localhost",
        database="loandb",
        user="postgres",
        password="postgres"
    )

    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            customer_name,
            cibil_score,
            income,
            loan_type
        FROM customers
        WHERE customer_id=%s
        """,
        (customer_id,)
    )

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result


======================


1. What is psycopg2?
Python
import psycopg2

Imagine:


Python = Person
 
PostgreSQL = Bank Manager

Python wants customer information:


Customer ID = 1001

But Python cannot directly talk to PostgreSQL.

It needs a translator.

That translator is:

psycopg2


=====
Think:

Plain Text
Python
│
▼
psycopg2
│
▼
PostgreSQL

Without psycopg2:

Python
conn = psycopg2.connect()

=================

will fail because Python doesn't know how to talk to PostgreSQL.

2. What is connect()?
Python
conn = psycopg2.connect(
host="localhost",
database="loandb",
user="postgres",
password="postgres"
)

Think:

Calling a friend on mobile phone

Before talking:
Must connect call

Same here.

Before querying database:

Must connect

Backend:

Python
│
▼
Open TCP Connection
│
▼
PostgreSQL Server

Result:

Python
conn

becomes:

Active database connection
3. What Happens When Connection Opens?

When this runs:

Python
conn = psycopg2.connect(...)

Backend:

Step 1

Find PostgreSQL server

Plain Text
localhost

Meaning:

Plain Text
This machine itself
Step 2

Locate database

Plain Text
loandb
Step 3

Check username

Plain Text
postgres
Step 4

Check password

Plain Text
postgres
Step 5

Authentication success

Result:

Plain Text
Connection Opened ✅

Now Python and PostgreSQL can talk.

4. What is cursor()?
Python
cur = conn.cursor()
 

This is the most confusing concept for beginners.

Think:

Plain Text
Database = Library
 
Cursor = Librarian

Python says:

Plain Text
Find customer 1001

Who will search?

Plain Text
Cursor

Cursor is the worker.

Without cursor:

Plain Text
Connection Exists

but nobody performs work.

Flow:

Plain Text
Connection
│
▼
Cursor
│
▼
Execute Query
5. What is execute()?
Python
cur.execute(...)

Meaning:

Plain Text
Run SQL query

Database receives:

SQL
SELECT *
FROM customers

Backend:

Plain Text
Cursor
│
▼
Send SQL
│
▼
PostgreSQL

Think:

Plain Text
Execute
=
Run this command
6. What is SQL?

SQL means:

Plain Text
Structured Query Language
 

It is the language databases understand.

Examples:

Create Table
SQL
CREATE TABLE customers
Insert Row
SQL
INSERT INTO customers
Read Data
SQL
SELECT * FROM customers
Delete Data
SQL
DELETE FROM customers

Think:

Plain Text
Python Language
≠
Database Language
 
Database Language
=
SQL
7. What Does This Query Mean?
SQL
SELECT
customer_name,
cibil_score,
income,
loan_type
FROM customers
WHERE customer_id=%s

Meaning:

Plain Text
Search customer table
 
Find customer where:
ID = 1001
 
Return:
Name
CIBIL
Income
Loan Type

Example:

Table:

Plain Text
1001 Ravi 760 50000 Home Loan

Result:

Plain Text
Ravi
760
50000
Home Loan
8. What is fetchone()?
Python
result = cur.fetchone()

Database finds:

Plain Text
Ravi
760
50000
Home Loan

Now fetchone means:

Plain Text
Bring first row to Python

Result:

Python
(
'Ravi',
760,
50000,
'Home Loan'
)

Stored in:

Python
result
Why Not fetchall()?
Python
fetchone()
 

returns:

Plain Text
One Row
Python
fetchall()

returns:

Plain Text
All Rows

Example:

Plain Text
1001
1002
1003
1004
9. Why close()?
Python
cur.close()

Think:

Plain Text
Librarian finished work

Close cursor.

Release resources.

Python
conn.close()

Think:

Plain Text
Phone call ended

Close database connection.

If you don't close:

Plain Text
Memory waste
Connection leak
Performance issues

Good practice:

Plain Text
Open
Use
Close

Always.

10. Why return result?
Python
return result

Current:

Python
result =
(
'Ravi',
760,
50000,
'Home Loan'
)

Return sends data back.

Without return:

Python
def get_customer():
...

would give:

Python
None

With return:

Python
customer = get_customer("1001")

Now:

Python
customer

contains:

Plain Text
Ravi
760
50000
Home Loan
Real MCP Flow

When Swagger asks:

Plain Text
Show customer details

Flow:

Plain Text
Router
│
▼
MCP Node
│
▼
get_customer("1001")
│
▼
psycopg2.connect()
│
▼
Cursor
│
▼
SQL Query
│
▼
PostgreSQL
│
▼
fetchone()
│
▼
Result
│
▼
Ollama
│
▼
Answer
Interview Answer

db_tools.py is a database utility module. It uses psycopg2 to connect to PostgreSQL, executes SQL queries through a cursor, fetches customer details using fetchone(), closes resources properly, and returns the result to the MCP node in LangGraph. This enables the AI assistant to retrieve real customer data instead of relying only on document-based RAG.


