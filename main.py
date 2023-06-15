from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Options:
    def __init__(self, file_path):
        self.email = None
        self.password = None
        self.read_options_file(file_path)

    def read_options_file(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                if key == 'email':
                    self.email = value
                elif key == 'password':
                    self.password = value

# Example usage
options_file = 'options.txt'  # Replace with the actual path to your options file

options = Options(options_file)

# Set the path to your Chrome webdriver executable
#webdriver_path = 'chromedriver.exe' 
webdriver_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe' 

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)
chrome_options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe' 

chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
chrome_options.add_experimental_option("useAutomationExtension", False) 

# Create a new instance of Chrome driver
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.kroger.com/signin?redirectUrl=/mypurchases')

button = driver.find_element(By.CLASS_NAME, "kds-Modal-closeButton")
button.click()

emailTextbox = driver.find_element(By.ID, "SignIn-emailInput")
emailTextbox.send_keys(options.email)
passwordTextbox = driver.find_element(By.ID, "SignIn-passwordInput")
passwordTextbox.send_keys(options.password)
passwordTextbox.send_keys(Keys.ENTER)


# Navigate to the Kroger "My Purchases" page
driver.get('https://www.kroger.com/mypurchases')

# TODO: Add code to perform login and interact with the page to retrieve information

# Close the browser window
driver.quit()
