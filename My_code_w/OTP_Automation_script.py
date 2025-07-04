from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import csv
import pyperclip

import imaplib
import email
import re
import time

# Credentials
EMAIL = 'suprizangru@gmail.com'
PASSWORD = 'ktvdtqensqyzhxbf'  # App Password


# --- OTP Fetching Utility ---

def fetch_latest_otp(max_retries=6, wait_interval=5):
    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1}/{max_retries} to fetch OTP...")

        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(EMAIL, PASSWORD)
            mail.select("inbox")

            # Search for recent emails (last 5 minutes)
            status, messages = mail.search(None, '(UNSEEN)')
            if not messages[0]:
                status, messages = mail.search(None, 'ALL')

            message_ids = messages[0].split()

            if message_ids:
                # Check the most recent 3 emails
                for msg_id in reversed(message_ids[-3:]):
                    status, data = mail.fetch(msg_id, '(RFC822)')
                    msg = email.message_from_bytes(data[0][1])

                    subject = msg.get('Subject', '').lower()
                    sender = msg.get('From', '').lower()

                    # Skip if not from MoneyControl or OTP related
                    if not ('moneycontrol' in sender or 'otp' in subject or 'verification' in subject):
                        continue

                    print(f"Checking email from: {sender}")

                    # Get email body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()

                    # Find all 4-digit numbers
                    all_4digits = re.findall(r'\b\d{4}\b', body)
                    print(f"Found 4-digit numbers: {all_4digits}")

                    # Filter out years and common non-OTP numbers
                    potential_otps = []
                    for num in all_4digits:
                        if not re.match(r'^(19|20)\d{2}$', num):  # Not a year
                            if num not in ['1000', '2000', '3000']:  # Not round numbers
                                potential_otps.append(num)

                    if potential_otps:
                        # Take the last one found (usually the actual OTP)
                        otp = potential_otps[-1]
                        print(f"✅ Selected OTP: {otp}")
                        mail.logout()
                        return otp

            mail.logout()

        except Exception as e:
            print(f"Error in attempt {attempt + 1}: {e}")

        print(f"Retrying in {wait_interval} seconds...")
        time.sleep(wait_interval)

    raise Exception("❌ OTP not found after retries.")


# --- Browser Setup Utility ---

def create_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


# --- Main Script ---

try:
    driver = create_chrome_driver()
    wait = WebDriverWait(driver, 30)

    print("🌐 Navigating to MoneyControl...")
    driver.get("https://www.moneycontrol.com/")
    driver.maximize_window()

    # Handle cookie banner
    try:
        cookie = wait.until(EC.element_to_be_clickable((By.ID, "mc_cookie_link")))
        cookie.click()
        print("🍪 Cookie banner dismissed.")
    except TimeoutException:
        print("No cookie banner found.")

    # Navigate to login
    login_area = wait.until(EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Hello, Login']")))
    ActionChains(driver).move_to_element(login_area).perform()
    print("🖱️ Hovered over 'Hello, Login'.")

    login_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Log-in']")))
    login_link.click()
    print("🔐 Clicked 'Log-in' link.")

    iframe = wait.until(EC.presence_of_element_located((By.ID, "myframe")))
    driver.switch_to.frame(iframe)
    print("🔄 Switched to iframe.")

    email_field = wait.until(EC.visibility_of_element_located((By.NAME, "email_mirror")))
    email_field.clear()
    email_field.send_keys(EMAIL)
    print("📧 Email entered.")

    driver.find_element(By.XPATH, '//*[@id="mc_log_otp_pre"]/button').click()
    print("📨 OTP request sent.")

    # Re-check and re-enter iframe in case it refreshed or was rebuilt
    driver.switch_to.default_content()
    iframe = wait.until(EC.presence_of_element_located((By.ID, "myframe")))
    driver.switch_to.frame(iframe)
    print("🔄 Re-entered iframe after Send OTP.")

    # Wait for email to arrive
    print("⏳ Waiting 8 seconds for OTP email...")
    time.sleep(8)

    # Alternative OTP input method - use this if the main method doesn't work
    # Replace the OTP input section with this:

    otp = fetch_latest_otp()
    print(f"🔍 OTP is: {otp}")
    print("✋ Please enter this OTP manually in the browser...")

    # Focus first field to help you out
    # first_field = wait.until(EC.element_to_be_clickable((By.NAME, "otp_first")))
    # first_field.click()

    # input("💬 Press Enter once you’ve manually entered the OTP...")

    # # Enter digits one by one using send_keys and TAB
    # for digit in otp:
    #     active = driver.switch_to.active_element
    #     active.send_keys(digit)
    #     active.send_keys(Keys.TAB)
    #     print(f"✅ Sent digit '{digit}' and moved to next field.")

    # otp_fields = ["otp_first", "otp_second", "otp_third", "otp_fourth"]

    # for i, digit in enumerate(otp):
    #     pyperclip.copy(digit)
    #     field_name = otp_fields[i]  # ✅ extract the actual field name
    #     otp_input = wait.until(EC.element_to_be_clickable((By.NAME, field_name)))
    #     otp_input.click()
    #     otp_input.send_keys(Keys.CONTROL, 'v')  # Or Keys.COMMAND if you're on macOS
    #     print(f"✅ Pasted digit '{digit}' into '{field_name}'")

    proceed = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "continue disable login_btn")))
    proceed.click()
    print("🚀 OTP submitted successfully!")
    # Switch to the mobile verification iframe and close the modal
    try:
        iframe = wait.until(EC.presence_of_element_located((By.ID, "mVerifyIframe")))
        driver.switch_to.frame(iframe)
        close_icon = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mc_mobile_verify_pre"]/a')))
        close_icon.click()
        print("🔐 Mobile verification popup closed.")
        driver.switch_to.default_content()
    except TimeoutException:
        print("ℹ️ Mobile verification iframe not found or already closed.")



    # Step 1: Navigate to Watchlist page
    driver.get("https://www.moneycontrol.com/watchlist")
    print("📈 Navigated to Watchlist.")
    time.sleep(3)  # allow UI to load

    # Step 2: Count current stocks
    rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".WL1 > tbody > tr")))
    initial_count = len(rows)
    print(f"📊 Initial stock count in Watchlist: {initial_count}")

    # Step 3: Read stock symbols from CSV and add them

    def add_stock(symbol):
        print(f"➕ Adding stock: {symbol}")
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "search_str")))
        search_box.clear()
        search_box.send_keys(symbol)

        suggestion = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul.ajaxsearch_list li")))
        suggestion.click()

        add_btn = wait.until(EC.element_to_be_clickable((By.ID, "addStockBtn")))
        add_btn.click()
        time.sleep(2)


    # Load from CSV and add each stock
    with open("stocks.csv", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol = row['symbol'].strip()
            if symbol:
                add_stock(symbol)

    # Step 4: Recount stocks after additions
    rows_after = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".WL1 > tbody > tr")))
    final_count = len(rows_after)

    print(f"✅ Final stock count in Watchlist: {final_count}")
    print(f"🧮 Total stocks added: {final_count - initial_count}")

except Exception as e:
    print(f"❗ Error: {e}")

finally:
    input("Press Enter to close browser...")
    driver.quit()
    print("🧹 Browser closed.")