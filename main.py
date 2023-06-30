from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time

import undetected_chromedriver as uc

options_file = 'options.txt'  # Replace with the actual path to your options file

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

class Receipt:
    def __init__(self, items, tax, date):
        self.items = items
        self.date = date
        self.tax = tax
        self.total_amount_spent = sum(item.price for item in items) + tax
        self.total_discount = sum(item.originalPrice - item.price for item in items)

    def print_receipt(self):
        print("Receipt Date:", self.date)
        print("Items:")
        for item in self.items:
            print(f"- {item.name}: ${item.price}")
        print("Total Amount Spent: $", self.total_amount_spent)
        print("Total Discount: $", self.total_discount)

class Item(Receipt):
    def __init__(self, name, price, originalPrice=-1):
        super().__init__(items=None)
        self.name = name
        self.price = price
        self.originalPrice = price if originalPrice == -1 else originalPrice

class Scraper:
    def __init__(self, driver):
        self.driver = driver
        self.options = Options(options_file)
        self.items = []

        #driver.get('https://www.kroger.com')
        self.driver.get('https://www.kroger.com/signin?redirectUrl=/mypurchases')

    def logIn(self):
        time.sleep(1)
        self.closePopUp()
        time.sleep(1)
        emailTextbox = self.driver.find_element(By.ID, "SignIn-emailInput")
        emailTextbox.send_keys(self.options.email)
        passwordTextbox = self.driver.find_element(By.ID, "SignIn-passwordInput")
        passwordTextbox.send_keys(self.options.password)
        passwordTextbox.send_keys(Keys.ENTER)
    
    def closePopUp(self):
        elements = self.driver.find_elements(By.CLASS_NAME, "kds-Modal-closeButton")

        # Check if the element exists
        if len(elements) > 0:
            # Element exists, perform an action
            element = elements[0]
            # Perform action on the element
            element.click()
        else:
            # Element doesn't exist, do nothing
            return
    
    def hoverWelcomeButton(self):
        try:
            # Attempt to find the first element
            element = self.driver.find_element(By.CLASS_NAME, "Welcome-container--desktop")
            ActionChains(self.driver).move_to_element(element).perform()
        except NoSuchElementException:
            try:
                # First element not found, try finding the second element
                element = self.driver.find_element(By.CLASS_NAME, "Welcome-container--mobile")
                ActionChains(self.driver).move_to_element(element).perform()
            except NoSuchElementException:
                # Neither element found, handle the situation
                print("Both elements not found")

    def homeToLogin(self):

        time.sleep(1)

        self.closePopUp()

        #self.driver.save_screenshot('screenshot.png')
        self.hoverWelcomeButton()
        #self.driver.save_screenshot('screenshot.png')

        button = self.driver.find_element(By.CLASS_NAME, "WelcomeMenu-signIn-button")
        button.click()

    def getReceipts(self):
        self.getAllReceiptPage()
        #TODO create a navigation to the next page and repet getAllReceiptPage()
    
    def getAllReceiptPage(self):
        orderDetailLinks = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='order-details-link']")

        for i in range(len(orderDetailLinks)):
            orderDetailLinks[i].click()
            print(f"Getting receipt {i}...")
            self.getReceipt()
            self.driver.back()
            orderDetailLinks = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='order-details-link']")

    def getReceipt(self):
        items = []        
        ProductCards = driver.find_elements(By.CSS_SELECTOR, "[data-testid='PH-ProductCard']")
        
        for ProductCard in ProductCards:
            name = ProductCard.find_elements(By.CLASS_NAME, "PH-ProductCard-item-description")[0].accessible_name
            price = float(ProductCard.find_elements(By.CLASS_NAME, "kds-Price")[0].get_attribute("value"))
            try:
                original_price_elements = ProductCard.find_elements(By.CLASS_NAME, "kds-Price-original")
                if original_price_elements:
                    original_price = float(original_price_elements[0].text.replace('$', ''))
                    items.append(Item(name, price, original_price))
                else:
                    items.append(Item(name, price))
            except NoSuchElementException:
                items.append(Item(name, price))

        element = driver.find_element(By.XPATH, "//span[@class='kds-Text--m block min-w-0 w-3/5' and text()='Tax']/following-sibling::span")
        tax = float(element.text.strip().replace('$', ''))

        try:
            date_element = driver.find_element(By.XPATH, "//h2[contains(@class, 'kds-Heading') and contains(text(), 'In-store')]")
            date = date_element.text.replace('In-store ', '')
        except NoSuchElementException:
            date_element = driver.find_element(By.XPATH, "//h2[contains(@class, 'kds-Heading') and contains(text(), 'Fuel')]")
            date = date_element.text.replace('Fuel ', '')

        receipt = Receipt(items, tax, date)
        receipts.append(receipt)

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
        return webdriver.Chrome(options=chrome_options)

    def edgeDriver():
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
        return webdriver.Edge(options=edge_options)

driver = uc.Chrome()

scrape = Scraper(driver)

receipts = []

for receipt in receipts:
    receipt.print_receipt()

scrape.logIn()
scrape.getReceipts()

# Close the browser window
driver.quit()
