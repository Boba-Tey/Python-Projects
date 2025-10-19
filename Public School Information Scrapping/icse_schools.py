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
    driver.get("https://locate.cisce.org/result")
    time.sleep(2)

    dropdown = Select(driver.find_element("name", "result_length"))
    dropdown.select_by_value("100")
    print("----- Show 100 entries -----")
    time.sleep(2)

    structured_data = []
    page_count = 0
    max_pages = 32

    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", attrs={"id": "result"})
        rows = table.find_all("tr", attrs={"role": "row"})

        for row in rows:
            uls = row.find_all("ul")
            if len(uls) >= 5:
                school_name = [li.get_text(strip=True) for li in uls[0].find_all("li")]
                contact = [li.get_text(strip=True) for li in uls[1].find_all("li")]
                category = [li.get_text(strip=True) for li in uls[2].find_all("li")]
                course = [li.get_text(strip=True) for li in uls[3].find_all("li")]
                head_name = [li.get_text(strip=True) for li in uls[4].find_all("li")]

                entry = {
                    "School Code": school_name[0] if school_name else "",
                    "Name/Address": "\n".join(school_name[1:]) if len(school_name) > 1 else "",
                    "Contact Details": "\n".join(contact),
                    "Category": "\n".join(category),
                    "Course": "\n".join(course),
                    "Name of Head of School": "\n".join(head_name)
                }
                structured_data.append(entry)

        try:
            wait = WebDriverWait(driver, 2)
            next_button = wait.until(EC.element_to_be_clickable((By.ID, "result_next")))
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
    df.to_excel("icse school info.xlsx", index=False)