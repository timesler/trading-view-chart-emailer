import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverManager:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-3d-apis")
        self.driver = webdriver.Chrome(options=chrome_options)

    def save_tradingview_chart_as_image(
        self,
        url: str,
        output_filename: str,
        width: int = 1920,
        height: int = 1080,
    ):
        self.driver.set_window_size(width or 1920, height or 1080)
        try:
            self.driver.get(url)
            if "economic-calendar" in url:
                class_name = "fxs_c_calendar_wrapper"
            elif "tv_guide" in url:
                class_name = "draggable"
            elif "countryeconomy" in url:
                class_name = "table-responsive"
            else:
                class_name = "layout__area--center"
            if class_name:
                wait = WebDriverWait(self.driver, 10)
                # Ensure the chart element is loaded
                wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name)),
                    f"Timeed out waiting for {class_name} class",
                )
                time.sleep(3)
                # Locate the chart element and take a screenshot
                chart_element = self.driver.find_element(By.CLASS_NAME, class_name)
                chart_element.screenshot(str(output_filename))
            else:
                time.sleep(10)
                self.driver.save_screenshot(str(output_filename))
        except:
            print(f"FAILED TO SAVE WEBPAGE: {output_filename}")
            return False

        return True

    def close_driver(self):
        self.driver.quit()
