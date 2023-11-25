NWCCU Data Scraper and Database Inserter
=========================================

Overview
--------
This application is designed to scrape college and university data from the Northwest Commission on Colleges and Universities (NWCCU) website and store it in a SQL database. It's built using Python and leverages Selenium for web scraping and pyodbc for database interaction.

Structure
---------
The application is divided into three main components, each encapsulated in its own file for clarity and maintainability:

1. nwccu_scraper.py (Web Scraper)
   - Contains the NWCCUScraper class responsible for navigating to the NWCCU directory webpage, extracting information about each institution listed, and storing the extracted data in a structured format.
   - Uses Selenium WebDriver for browser interaction.

2. database_manager.py (Database Manager)
   - Defines the DatabaseManager class, which handles all database-related operations including establishing a connection to the SQL Server database and inserting the scraped data into the NWCCU_Data table.
   - Utilizes pyodbc for executing SQL commands.

3. main.py (Main Application)
   - The entry point of the application.
   - Orchestrates the overall process by initiating the web scraping through NWCCUScraper and passing the scraped data to DatabaseManager for storage.

Usage
-----
To run the application, follow these steps:

1. Set up a virtual environment (techinically optional, but strongly recommended):
   - On Windows: python -m venv venv
   - On macOS and Linux: python3 -m venv venv
   - Activate the virtual environment:
     - On Windows: .\venv\Scripts\activate
     - On macOS and Linux: source venv/bin/activate

2. Install the required dependencies:
   - pip install -r requirements.txt

3. Create a config.ini file. See config.example.ini for instructions on how to update the database connection string with your database server and credentials.

4. Execute the script main.py to start the scraping and data insertion process.

Dependencies
------------
- Python
- Selenium
- WebDriver Manager (for Selenium)
- pyodbc

Schema
------
The following is the schema and script used to create the table for storing the data:

CREATE TABLE NWCCU_Data (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(255),
    Website NVARCHAR(255),
    Accredited BIT,
    AccreditationPeriod NVARCHAR(255),
    Type NVARCHAR(255),
    StatementURL NVARCHAR(255),
    MostRecentEvaluation NVARCHAR(255),
    NextEvaluation NVARCHAR(255),
    DegreeLevels NVARCHAR(255),
    PublicSanction NVARCHAR(255),
    ReasonForAccreditation NVARCHAR(MAX)
);

Notes
-----
- This application contains an additional file called beautifulSoupAttempt_NotWorking.py. This was a first attempt at scraping the website. I discovered that BeautifulSoup wouldn't work because the data I want to scrape is loaded with Javascript.

