from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import phonenumbers
import random
import time

def select_birthdate(driver):
    for _ in range(3):
        try:
            day_options = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, ".//div[contains(@role,'option') and contains(@id, 'Day-options')]")))
            valid_day_options = [day_option for day_option in day_options if int(driver.execute_script('return arguments[0].textContent', day_option)) <= 28]
            day_option = random.choice(valid_day_options)
            driver.execute_script("arguments[0].click();", day_option)
            time.sleep(2)

            month_options = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, ".//div[contains(@role,'option') and contains(@id, 'Month-options')]")))
            month_option = random.choice(month_options)
            driver.execute_script("arguments[0].click();", month_option)
            time.sleep(2)

            year_options = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, ".//div[contains(@role,'option') and contains(@id, 'Year-options')]")))
            current_year = datetime.now().year
            recent_valid_year = current_year - 15
            latest_valid_year = current_year - 60
            valid_year_options = [year_option for year_option in year_options if latest_valid_year <= int(driver.execute_script('return arguments[0].textContent', year_option)) <= recent_valid_year]
            year_option = random.choice(valid_year_options)
            driver.execute_script("arguments[0].click();", year_option)
            time.sleep(2)

            return True
        except Exception as e:
            print(f"Failed to select birthdate: {e}")
            continue
    return False

def get_phone_info(phone_number):
    number = phonenumbers.parse(phone_number)
    country_code = f"+{number.country_code}"
    phone_number_no_country_code = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.NATIONAL).replace(' ', '')
    return country_code, phone_number_no_country_code

def select_country(driver, country_code=None):
    for _ in range(3):
        try:
            press_the_wrapper = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, ".//div[@tabindex='0' and @role='button' and @aria-haspopup='true' and @aria-controls='phone-country-code-selector-wrapper']")))
            driver.execute_script("arguments[0].click();", press_the_wrapper)
            time.sleep(2)

            wrapper = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, ".//div[@id='phone-country-code-selector-wrapper']")))

            options = wrapper.find_elements(By.XPATH, ".//li[@id and @tabindex='0']")

            country = random.choice(options) if country_code is None else driver.find_element(By.XPATH, f".//li[@id and @tabindex='0']/span[contains(text(), '{country_code}')]")
            driver.execute_script("arguments[0].click();", country)
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Failed to select country: {e}")
            continue
    raise Exception("Failed to select country")

def fill_number_and_ask_for_code(driver, phone):
    for _ in range(3):
        try:
            phone_input = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, ".//input[@type='text' and @name='mobile']")))
            phone_input.clear()
            
            for digit in phone:
                phone_input.send_keys(digit)
                time.sleep(0.2)

            time.sleep(2)

            WebDriverWait(driver, 30).until_not(EC.presence_of_element_located((By.XPATH, ".//button[@type='button' and @disabled]")))

            ask_for_code = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, ".//button[@type='button']")))
            driver.execute_script("arguments[0].click();", ask_for_code)
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Failed to fill number and ask for code: {e}")
            continue
    raise Exception("Failed to fill number and ask for code")

def main():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]
    
    options_list = [
        ["--disable-blink-features=AutomationControlled", "--start-maximized", "--incognito"],
        ["--disable-notifications", "--disable-popup-blocking", "--disable-extensions"],
        ["--no-sandbox", "--disable-dev-shm-usage", "--window-size=1920,1080"],
        ["--ignore-certificate-errors", "--allow-running-insecure-content"]
    ]
    
    stealth_settings = [
        {
            "languages": ["en-US", "en"],
            "vendor": "Google Inc.",
            "platform": "Win64",
            "webgl_vendor": "Intel Inc.",
            "renderer": "Intel Iris OpenGL Engine",
            "fix_hairline": True,
            "run_on_insecure_origins": False,
            "timezone": "America/New_York",
            "audioContext": {"enable": True, "latencyHint": "interactive", "sampleRate": 44100},
            "fonts": ["Arial", "Helvetica", "Times New Roman"],
            "webgl": {"unMaskedVendor": "Intel Inc.", "unMaskedRenderer": "Intel Iris OpenGL Engine"},
            "canvas": True,
            "displayLanguage": "en-US",
            "geolocation": {"latitude": 40.7128, "longitude": -74.0060, "accuracy": 100},
            "deviceMemory": 8,
            "hardwareConcurrency": 4,
            "screenResolution": {"width": 1920, "height": 1080},
            "macAddress": "00:1A:2B:3C:4D:5E",
            "deviceInfo": {"deviceName": "PC", "osVersion": "10.0", "kernelVersion": "10.0.19041"},
            "plugins": ["Chrome PDF Plugin", "Chrome PDF Viewer"],
            "doNotTrack": "1",
            "clientRects": True
        },
        {
            "languages": ["en-US", "en-GB"],
            "vendor": "Apple Inc.",
            "platform": "MacIntel",
            "webgl_vendor": "Apple Inc.",
            "renderer": "Apple M1",
            "fix_hairline": False,
            "run_on_insecure_origins": True,
            "timezone": "Europe/London",
            "audioContext": {"enable": True, "latencyHint": "playback", "sampleRate": 48000},
            "fonts": ["Arial", "Courier New", "Verdana"],
            "webgl": {"unMaskedVendor": "Apple Inc.", "unMaskedRenderer": "Apple M1"},
            "canvas": True,
            "displayLanguage": "en-GB",
            "geolocation": {"latitude": 51.5074, "longitude": -0.1278, "accuracy": 100},
            "deviceMemory": 16,
            "hardwareConcurrency": 8,
            "screenResolution": {"width": 2560, "height": 1600},
            "macAddress": "00:1B:2C:3D:4E:5F",
            "deviceInfo": {"deviceName": "MacBook Pro", "osVersion": "11.6", "kernelVersion": "20.6.0"},
            "plugins": ["QuickTime Plug-in", "iPhotoPhotocast"],
            "doNotTrack": "0",
            "clientRects": True
        }
    ]
    
    options = Options()
    selected_options = random.choice(options_list)
    for opt in selected_options:
        options.add_argument(opt)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    user_agent = random.choice(user_agents)
    options.add_argument(f'user-agent={user_agent}')
    
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    selected_stealth = random.choice(stealth_settings)
    stealth(driver, **selected_stealth)
    
    tiktok_signup_url = "https://www.tiktok.com/signup"

    try:
        driver.get(tiktok_signup_url)
        use_phone_or_email = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, ".//div[@role='link' and @tabindex='0']")))
        driver.execute_script("arguments[0].click();", use_phone_or_email)
        time.sleep(3)
        
        ok = select_birthdate(driver)
        if not ok:
            raise Exception("Failed to select birthdate")

        phonenumber = '+923338866144'  # Insert your phone number here
        if '+' in phonenumber:
            country_code, phone_number = get_phone_info(phonenumber)

        ok = select_country(driver, country_code)
        if not ok:
            raise Exception("Failed to select country")
        
        ok = fill_number_and_ask_for_code(driver, phone_number)
        if not ok:
            raise Exception("Failed to fill number and ask for code")
        
        send_code_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-e2e="send-code-button"]')))
        driver.execute_script("arguments[0].click();", send_code_button)
        time.sleep(4)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Done")
        driver.quit()

if __name__ == "__main__":
    main()
