import configparser
from nwccu_scraper import NWCCUScraper
from database_manager import DatabaseManager

def main():
    # Initialize the configuration parser
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Read database configuration
    db_config = config['database']
    connection_string = f"Driver={db_config['driver']};" \
                        f"Server={db_config['server']};" \
                        f"Database={db_config['database']};" \
                        f"Trusted_Connection={db_config['trusted_connection']};"

    # Initialize the NWCCUScraper object and perform the web scraping
    scraper = NWCCUScraper()
    scraper.scrape()

    # Print the scraped data to the console for verification
    scraper.printColleges()

    # Initialize the DatabaseManager with the connection string,
    # and insert the scraped data into the database
    db_manager = DatabaseManager(connection_string)
    db_manager.insert_college_data(scraper.colleges_data)

if __name__ == "__main__":
    main()
