import time
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

URLS = ["https://example.com"]  # add more as needed
OUT_DIR = Path("screenshots")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def stamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# ---- Driver setup ----
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1366,768")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")             # helpful in CI containers
options.add_argument("--disable-dev-shm-usage")  # avoids /dev/shm issues
options.add_argument("--hide-scrollbars")

driver = webdriver.Chrome(options=options)  # Selenium Manager resolves chromedriver
driver.set_page_load_timeout(60)

try:
    for url in URLS:
        driver.get(url)

        # Basic readiness: wait for <body> so we don't snapshot a blank page
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )
        except Exception:
            pass

        # Nudge lazy-loaded content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1.0)

        # Compute full document dimensions and resize for full-page capture
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.documentElement.scrollWidth)"
        )
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
        )
        driver.set_window_size(max(width, 1366), max(height, 768))
        time.sleep(0.5)  # let layout settle

        fname = OUT_DIR / f"{stamp()}_{url.replace('https://','').replace('http://','').replace('/','_')}.png"
        driver.save_screenshot(str(fname))
        print(f"Saved: {fname}")
finally:
    driver.quit()
``
