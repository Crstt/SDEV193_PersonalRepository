from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time

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

def closePopUp():
    elements = driver.find_elements(By.CLASS_NAME, "kds-Modal-closeButton")

    # Check if the element exists
    if len(elements) > 0:
        # Element exists, perform an action
        element = elements[0]
        # Perform action on the element
        element.click()
    else:
        # Element doesn't exist, do nothing
        return
    
def hoverWelcomeButton():
    try:
        # Attempt to find the first element
        element = driver.find_element(By.CLASS_NAME, "Welcome-container--desktop")
        ActionChains(driver).move_to_element(element).perform()
    except NoSuchElementException:
        try:
            # First element not found, try finding the second element
            element = driver.find_element(By.CLASS_NAME, "Welcome-container--mobile")
            ActionChains(driver).move_to_element(element).perform()
        except NoSuchElementException:
            # Neither element found, handle the situation
            print("Both elements not found")

# Example usage
options_file = 'options.txt'  # Replace with the actual path to your options file

options = Options(options_file)

def chromeDriver():

    # Set the path to your Chrome webdriver executable
    webdriver_path = 'chromedriver.exe' 
    #webdriver_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe' 
    #webdriver_path = 'C:/Program Files/Mozilla Firefox/firefox.exe'

    # Configure Chrome options
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)
    chrome_options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe' 
    #chrome_options.page_load_strategy = 'eager'

    chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    chrome_options.add_experimental_option("useAutomationExtension", False) 

    # Create a new instance of Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

webdriver_path = 'msedgedriver.exe'

# Configure Microsoft Edge options
edge_options = webdriver.EdgeOptions()
# edge_options.add_argument('--headless')  # Run Microsoft Edge in headless mode (without GUI)
edge_options.binary_location = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
# edge_options.page_load_strategy = 'eager'

edge_options.add_argument("--disable-blink-features=AutomationControlled") 
#edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
edge_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
edge_options.add_experimental_option("useAutomationExtension", False)

# Create a new instance of Microsoft Edge driver
driver = webdriver.Edge(options=edge_options)



driver.get('https://www.kroger.com')
#driver.get('https://www.kroger.com/signin?redirectUrl=/mypurchases')

time.sleep(1)
closePopUp()

driver.save_screenshot('screenshot.png')
hoverWelcomeButton()
driver.save_screenshot('screenshot.png')

button = driver.find_element(By.CLASS_NAME, "WelcomeMenu-signIn-button")
button.click()

closePopUp()
time.sleep(1)
emailTextbox = driver.find_element(By.ID, "SignIn-emailInput")
emailTextbox.send_keys(options.email)
passwordTextbox = driver.find_element(By.ID, "SignIn-passwordInput")
passwordTextbox.send_keys(options.password)
passwordTextbox.send_keys(Keys.ENTER)

driver.save_screenshot('screenshot.png')

# Close the browser window
driver.quit()
