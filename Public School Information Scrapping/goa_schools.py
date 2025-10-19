import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://service1.gbshse.in/Gbshse_institution/recognized-institutes/#/")
driver.maximize_window()
time.sleep(5)

school_codes = []
count = 0

try:
    while True:
        rows = driver.find_elements(By.XPATH, "//div[@col-id='code']")
        for row in rows:
            code = row.get_attribute("textContent").strip()
            if code and code.lower() != "code" and code not in school_codes:
                school_codes.append(code)
                count += 1

        next_button = driver.find_element(By.CSS_SELECTOR, "div.ag-paging-button[aria-label='Next Page']")
        if "ag-disabled" in next_button.get_attribute("class"):
            break

        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(1) 

    print(count, "School Codes Found")

    school_info = []
    info_count = 0

    for code in school_codes:
        search_box = driver.find_element(By.XPATH, "//input[@placeholder='Type here Code/Name/Address/Taluka to search']")
        search_box.clear()
        search_box.send_keys(code)
        time.sleep(0.4)

        button = driver.find_element(By.XPATH, "(//div[@role='row' and @row-index='0']//div[@col-id='name'])[1]")
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(0.3)
        button.click()
        time.sleep(0.8)

        name = driver.find_element(By.CSS_SELECTOR, ".school-details h6").get_attribute("textContent").strip()
        address = driver.find_element(By.CSS_SELECTOR, ".school-address span").get_attribute("textContent").strip()
        phone = driver.find_element(By.CSS_SELECTOR, ".school-phone span").get_attribute("textContent").strip()
        email = driver.find_element(By.CSS_SELECTOR, ".school-email span").get_attribute("textContent").strip()

        school_info.append({
            "Code": code,
            "Name": name,
            "Address": address,
            "Phone": phone,
            "Email": email
        })

        info_count += 1
        print(info_count, "Schools Done")
        time.sleep(0.5)

finally:
    driver.quit()
    df = pd.DataFrame(school_info)
    df.to_excel("goa school info.xlsx", index=False)
    print("Exported Excel successfully!")