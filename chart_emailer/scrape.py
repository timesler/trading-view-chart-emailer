import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverManager:
    def __init__(self, width: int = 1920, height: int = 1080):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--window-size={width}x{height}")
        self.driver = webdriver.Chrome(options=chrome_options)

    def save_tradingview_chart_as_image(self, url, output_filename):
        if "economic-calendar" in url:
            class_name = "fxs_c_calendar_wrapper"
        elif "tv_guide" in url:
            class_name = "draggable"
        else:
            class_name = "layout__area--center"
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 5)
        # Ensure the chart element is loaded
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name)),
            f"Timeed out waiting for {class_name} class",
        )
        # Locate the chart element and take a screenshot
        chart_element = self.driver.find_element(By.CLASS_NAME, class_name)
        chart_element.screenshot(str(output_filename))

    def close_driver(self):
        self.driver.quit()
