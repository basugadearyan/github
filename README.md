# 💰 Daily Expenses Tracking System
A user-friendly personal finance management application built with Python, Tkinter, and MySQL. Track daily spending, manage income, monitor monthly budgets, and understand your financial habits through organized records, reports, and visual analytics.

**📖 Overview**

The Daily Expenses Tracking System is a desktop application designed to simplify personal financial management. Instead of maintaining expense records manually in notebooks or spreadsheets, users can record their daily transactions in a centralized system, categorize spending, and review their financial position. The application provides a graphical user interface (GUI) for managing expenses, recording income, setting monthly budgets, and generating financial summaries. It calculates daily and monthly expenses and helps users determine their available balance by comparing recorded income with expenses. Built using Python and Tkinter with MySQL database connectivity, the system offers an organized way to store, retrieve, update, and analyze financial information.

**✨ Key Features**

Expense Management: Add, view, update, search, and delete expense records, including expense name, amount, date, category, payment mode, and description.

Income and Balance Tracking: Record income sources and calculate total income, total expenses, and available balance.
Expense Categorization: Organize spending into categories such as Food, Transport, Education, Shopping, Bills, and Entertainment.
Monthly Budget Management: Set spending limits and compare recorded expenses with budget amounts.
Financial Dashboard: Display key information, including daily expenses, monthly expenses, total income, and balance.
Category-wise Reports: Analyze spending by category to identify where most of the money is spent.
Visual Analytics: Use Matplotlib charts to visualize expense distribution and spending patterns, if implemented.
Database Management: Store financial records in MySQL for structured data management and retrieval.
CSV Export: Export expense records for external analysis, if the export feature is implemented.

**💻 Technology Stack**

Programming Language: Python 3
Frontend GUI: Tkinter and themed Tkinter widgets
Database: MySQL
Database Connectivity: MySQL Connector for Python
Data Analysis: Pandas
Data Visualization: Matplotlib
Date and Time Handling: Python datetime module
Data Processing: Python functions, SQL queries, and calculation logic
🚀 Installation & Setup Prerequisites Make sure you have Python 3.x and MySQL Server installed on your computer. 1. Open the project Open your Daily_Expenses_Tracking_MySQL_Starter project folder in Visual Studio Code. 2. Install required libraries Open the VS Code terminal and run: pip install mysql-connector-python pandas matplotlib

3. Configure the MySQL database Open your database configuration file, such as config.py, and enter your MySQL credentials. DB_HOST = "localhost" DB_USER = "root" DB_PASSWORD = "YOUR_MYSQL_PASSWORD" DB_NAME = "daily_expenses_db"

4. Run the application Start the application from the VS Code terminal: python main.py

The Tkinter window should open if the database configuration, dependencies, and application files are set up correctly.

🛠️ System Architecture The application can be organized into three logical layers. 1. Presentation Layer Tkinter GUI for entering expenses, recording income, managing budgets, and viewing reports.

2. Business Logic Layer Python functions validate inputs, process transactions, calculate totals, and prepare summaries.

3. Data Layer MySQL stores expense records, income information, categories, and budgets.

**Workflow**

Enter Information: The user enters an expense or income record through the GUI.
Validate Input: Python checks the required fields and validates the information.
Process Data: The application performs the necessary calculations and prepares SQL operations.
Store Records: MySQL saves the information for future retrieval.
Generate Results: The system calculates totals and summaries using the stored records.
Display Information: The GUI displays updated records, balances, reports, and supported charts.
📊 Sample Dashboard Output Daily Expenses Dashboard Illustrative sample — October 2026 Today's Expenses ₹240

Monthly Expenses ₹1,589

Monthly Income ₹6,500

Available Balance ₹4,911

These values are calculated from the sample records discussed earlier; they are not live readings from your application.

Example: Category-wise Expense Distribution Category Amount Shopping ₹650 Bills ₹299 Entertainment ₹250 Food ₹200 Education ₹150 Transport ₹40 Total ₹1,589 This report helps users identify high-spending categories and decide where they may be able to reduce expenses.

**🔮 Future Scope**

Mobile Application: Develop an Android application to manage expenses while travelling.
Cloud Synchronization: Store financial records in a cloud database for access across multiple devices.
Automatic Expense Categorization: Suggest categories based on transaction descriptions and previous records.
Advanced Financial Analytics: Generate weekly, monthly, and yearly spending trends.
Budget Notifications: Alert users when their spending approaches or exceeds a defined budget.
PDF and Excel Reports: Generate downloadable financial statements for record keeping.
Savings Goal Tracking: Allow users to set financial goals and monitor their progress.
Secure User Authentication: Add login, registration, and user-specific financial records.

**✅ Conclusion** The Daily Expenses Tracking System provides an organized solution for recording expenses, managing income, monitoring budgets, and reviewing financial summaries. By combining Python, Tkinter, and MySQL, the project reduces manual record keeping and makes personal financial information easier to manage. The system can help students and individuals understand their spending habits, track their available balance, and develop better budgeting practices. Future enhancements such as automated categorization, budget alerts, and advanced analytics can make the application more useful and reliable.

Project Title: Daily Expenses Tracking System Using Python, Tkinter, and MySQL

Developed by: Aryan Laxman Basugade and Shivraj Sunil Patil
