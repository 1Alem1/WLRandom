from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

def scrollPage(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def getTitlesPerPage(driver):
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "frame-title"))
        )
        titles = driver.find_elements(By.CLASS_NAME, "frame-title")
        for title in titles:
            try:
                title_text = driver.execute_script("return arguments[0].textContent;", title)
                if title_text.strip():
                    print(title_text)
            except Exception as e:
                print(f"An error with title has occurred: {e}")
                continue
    except Exception as e:
        print(f"An error with titles has occurred: {e}")
        return

def nextPage(driver):
    try:
        next_button = driver.find_elements(By.LINK_TEXT,"Older")
        if len(next_button) == 0:
            return False
        next_button = next_button[0]
        if next_button and next_button.is_enabled():
                next_button.click()
                return True
        else:
            return False
    except Exception as e:
        print("An error with next button has occurred: ", e)
        return False

def main():
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    ##option.add_argument("--headless")
    driver = Chrome(service=service, options=option)
    driver.maximize_window()
    driver.get("https://letterboxd.com/alem1/watchlist/")
    driver.implicitly_wait(1)

    try:
        while True:
            getTitlesPerPage(driver)
            scrollPage(driver)
            if not nextPage(driver):
                break
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "frame-title"))
            )
            time.sleep(2)

    except Exception as e:
        print("An error has occurred: ", e)
    

    time.sleep(3)
    driver.quit()

if __name__ == "__main__":
    main()