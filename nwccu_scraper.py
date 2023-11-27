# nwccu_scraper.py
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# The NWCCUScraper class is designed to scrape data from the NWCCU (Northwest Commission on Colleges and Universities) website.
# It uses Selenium WebDriver for interacting with the website to extract data about various colleges and universities.
class NWCCUScraper:
    def __init__(self):
        # Initializes the WebDriver for Chrome.
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # A list to store data for each college extracted from the website.
        self.colleges_data = []

    # Prints the details of all colleges stored in colleges_data.
    # This method can be used for debugging purposes to check the scraped data.
    def printColleges(self):
         for college in self.colleges_data:
            print(college)

    # Main method to start the web scraping process.
    def scrape(self):
        self.driver.get('https://nwccu.org/member-institutions/directory/')
        time.sleep(3)  # Waits for the page to load completely.

        # Fetch the state filter links
        state_links = self.driver.find_elements(By.CSS_SELECTOR, '.filterBox.states.left a')
        previous_state_link = None

        # Iterate over each state link
        for state_link in state_links:
             # Create a new instance of ActionChains for each iteration
            actions = ActionChains(self.driver)

            # Scroll to the element
            actions.move_to_element(state_link).perform()
            
            # Click the previous state link to turn off that filter (if it's not the first iteration)
            if previous_state_link:
                previous_state_link.click()
                time.sleep(3)  # Wait for the filter to reset

            # Extract state name
            state_name = state_link.text.strip()

            # Click the current state link to apply the filter
            state_link.click()
            time.sleep(3)  # Wait for the filter to be applied and the page to refresh

            # Scrape the college information for the selected state
            institution_lis = self.driver.find_elements(By.CLASS_NAME, 'institution')
            for li in institution_lis:
                try:
                    college_info = self.extract_college_info(li)
                    if college_info:
                        # Add state information to the college data
                        college_info['location'] = state_name
                        self.colleges_data.append(college_info)
                except Exception as e:
                    print(f"Error processing element: {e}")

            # Update the previous_state_link for the next iteration
            previous_state_link = state_link

        # Quits the WebDriver once scraping is complete.
        self.driver.quit()

    # Method to start the web scraping process. This runs faster since it doesn't filter by location, but also doesn't store the location of the school.
    def scrapeFast(self):
        # Navigates to the NWCCU directory page.
        self.driver.get('https://nwccu.org/member-institutions/directory/')
        time.sleep(5)  # Waits for the page to load completely.

        # 'instiution' is the class name of an li with the relevant college data.
        institution_lis = self.driver.find_elements(By.CLASS_NAME, 'institution')

        # Iterates through each element and extracts data.
        for li in institution_lis:
            try:
                college_info = self.extract_college_info(li)
                college_info['location'] = None
                if college_info:
                    self.colleges_data.append(college_info)
            except Exception as e:
                print(f"Error processing element: {e}")

        # Quits the WebDriver once scraping is complete.
        self.driver.quit()

    # Extracts detailed information from a single college element.
    def extract_college_info(self, li):
        try:
            # Extract college name
            college_name = li.find_element(By.CLASS_NAME, 'show-more').text

            # Extract college website - target the second 'a' tag in the 'li'
            a_tags = li.find_elements(By.TAG_NAME, 'a')
            college_website = a_tags[1].get_attribute('href') if len(a_tags) > 1 else None

            # Extract accreditation period
            accreditation_div = li.find_elements(By.TAG_NAME, 'div')[2].text
            accredited = 'present' in accreditation_div.lower()

            # Extract school type
            school_type_div = li.find_elements(By.TAG_NAME, 'div')[3].text
            school_type = school_type_div if school_type_div else None

            # Expand the "more" section to gather the rest of the data
            show_more_button = li.find_element(By.CLASS_NAME, 'show-more')
            show_more_button.click()
            time.sleep(1)  # Wait for the section to expand

            # Extract statement URL
            statement_url = None
            try:
                statement_div = li.find_element(By.XPATH, ".//div[b[contains(text(),'Statement')]]/following-sibling::div//a")
                statement_url = statement_div.get_attribute('href')
            except Exception:
                pass  # If no statement URL, leave it as None

            # Extract 'Most recent evaluation' data
            most_recent_evaluation_div = li.find_element(By.XPATH, ".//div[b[contains(text(),'Most recent evaluation')]]/following-sibling::div")
            most_recent_evaluation = most_recent_evaluation_div.text

            # Extract 'Next evaluation' data
            next_evaluation_div = li.find_element(By.XPATH, ".//div[b[contains(text(),'Next evaluation')]]/following-sibling::div")
            next_evaluation = next_evaluation_div.text

            # Extract 'Degree levels' data
            degree_levels_div = li.find_element(By.XPATH, ".//div[b[contains(text(),'Degree levels')]]/following-sibling::div")
            degree_levels = degree_levels_div.text

            # Extract 'Public sanction' data
            public_sanction_div = li.find_element(By.XPATH, ".//div[b[contains(text(),'Public sanction')]]/following-sibling::div")
            public_sanction = public_sanction_div.text

            # Extract 'Reason for Accreditation' data
            reason_for_accreditation_div = li.find_element(By.XPATH, ".//div[b[contains(text(),'Reason for Accreditation')]]/following-sibling::div")
            reason_for_accreditation = reason_for_accreditation_div.text

            # Compile the extracted data into a dictionary
            college_info = {
                'name': college_name,
                'website': college_website,
                'accredited': accredited,
                'accreditation_period': accreditation_div,
                'type': school_type,
                'statement_url': statement_url,  
                'most_recent_evaluation': most_recent_evaluation,  
                'next_evaluation': next_evaluation,  
                'degree_levels': degree_levels,  
                'public_sanction': public_sanction,  
                'reason_for_accreditation': reason_for_accreditation  
            }

            return college_info

        except Exception as e:
            print(f"Error processing element: {e}")
            return None
