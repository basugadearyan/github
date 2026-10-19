DAILY EXPENSES TRACKING SYSTEM - MYSQL STARTER

This starter is for Objectives 1-5:
1. Expense Information Management
2. Expense Categorization
3. Budget Monitoring
4. Income and Balance Tracking
5. Report and Summary Generation

CURRENTLY IMPLEMENTED:
- MySQL connection
- Automatic database creation
- Automatic table creation
- Default categories
- Tkinter GUI
- Add expense
- View expenses

NEXT MODULES TO BUILD:
- Update and Delete
- Search/filter
- Income and balance
- Budget monitoring
- Daily/weekly/monthly reports
- Pandas analysis
- Matplotlib charts
- CSV export

VS CODE + MYSQL SETUP

1. Install MySQL Server and MySQL Workbench.
2. Start MySQL Server.
3. Open this folder in VS Code.
4. Open config.py.
5. Replace YOUR_MYSQL_PASSWORD with your MySQL root password.
   Example:
   DB_PASSWORD = "1234"

6. Open VS Code Terminal.
7. Run:
   python -m venv venv

8. Activate:
   venv\Scripts\activate

9. Install packages:
   pip install -r requirements.txt

10. Run:
    python main.py

The program automatically creates:
daily_expenses_db

and these tables:
users
categories
expenses
income
budgets

In MySQL Workbench:
USE daily_expenses_db;
SHOW TABLES;
SELECT * FROM expenses;

IMPORTANT:
This version uses MySQL, not SQLite.
