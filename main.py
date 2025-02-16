from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Use the full path to ChromeDriver (since it's not in PATH yet)
service = Service("C:/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open a website
driver.get("https://www.google.com")

# Print the title of the webpage
print("Page title:", driver.title)

# Close the browser
driver.quit()
