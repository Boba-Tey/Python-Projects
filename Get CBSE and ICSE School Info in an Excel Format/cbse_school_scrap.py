import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException
)
from bs4 import BeautifulSoup
import time

def scrapper():
    print("----- Processing -----")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get("https://saras.cbse.gov.in/saras/AffiliatedList/ListOfSchdirReport")
    time.sleep(2)

    radio_button = driver.find_element(By.ID, "SearchMainRadioKeyword_wise")
    radio_button.click()
    print("Set search to keyword")
    time.sleep(2)

    search_input = driver.find_element(By.NAME, "InstName_orAddress")
    search_input.clear()
    search_input.send_keys("india")
    print("Search Term: india")
    time.sleep(2)

    search_button = driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary.actionBtn")
    driver.execute_script("arguments[0].scrollIntoView(true);", search_button)
    time.sleep(1)
    search_button.click()
    print("Searching...")
    time.sleep(2)

    try:
        WebDriverWait(driver, 2).until(
            EC.text_to_be_present_in_element((By.ID, "myTable_info"), "Showing")
        )
    except (StaleElementReferenceException, TimeoutException, NoSuchElementException) as e:
        print(f"Error: {e}")
        driver.quit()

    dropdown = Select(driver.find_element("name", "myTable_length"))
    dropdown.select_by_value("100")
    print("----- Show 100 entries -----")
    time.sleep(2)

    structured_data = []
    page_count = 0
    max_pages = 5

    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("tbody")
        rows = table.find_all("tr", attrs={"role": "row"})

        for row in rows:
            content = row.find_all("td")
            if len(content) >= 7:
                entry = {
                    "Aff NO.": content[1].get_text(separator="\n", strip=True),
                    "State & District": content[2].get_text(separator="\n", strip=True).replace("\n", " "),
                    "Status": content[3].get_text(separator="\n", strip=True),
                    "School and Head Name": content[4].get_text(separator="\n", strip=True).replace("\n", " "),
                    "Address": content[5].get_text(separator="\n", strip=True).replace("\n", " ")
                }
                structured_data.append(entry)

        try:
            wait = WebDriverWait(driver, 2)
            next_button = wait.until(EC.element_to_be_clickable((By.ID, "myTable_next")))
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            driver.execute_script("arguments[0].click();", next_button)
            page_count += 1
            print(f"----- Heading to page {page_count} -----")
            time.sleep(2)

            if page_count >= max_pages:
                print("Reached maximum pagination limit.")
                break

        except (StaleElementReferenceException, TimeoutException, NoSuchElementException) as e:
            print(f"Pagination ended or failed: {e}")
            break

    driver.quit()
    print(f"----- Completed {len(structured_data)} entries! -----")
    return structured_data

if __name__ == "__main__":
    data = scrapper()
    df = pd.DataFrame(data)
    df.to_excel("cbse school info.xlsx", index=False)