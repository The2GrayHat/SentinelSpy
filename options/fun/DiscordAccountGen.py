import os
import time
import random
import string
import requests
import json
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
NUM_ACCOUNTS = 2000  # Total number of accounts to create
OUTPUT_FILE = "tokens.txt"
NUM_THREADS = 20  # Number of threads to use
ACCOUNTS_PER_THREAD = 100  # Accounts per thread (NUMN_ACCOUNTS / NUM_THREADS)

# Discord API endpoint for account creation
DISCORD_API = "https://discord.com/api/v9/auth/register"

# Headers for API requests
HEADERS = {
    "Content-Type": "application/json"
}

# CAPTCHA solving service credentials (optional)
# Replace with your actual credentials if using
CAPTCHA_API_KEY = "your_api_key"  # Replace with actual API key if using a service
CAPTCHA_SOLVING_URL = "https://api.2captcha.com"  # Common CAPTCHA solving service endpoint

# Proxy settings (optional - helps avoid IP bans)
PROXY_LIST = [
    # Add proxies here if needed
    # Format: "IP:PORT" or "user:pass@IP:PORT"
]

# User agent rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# Account data storage
account_list = []
lock = threading.Lock()

# Chromedriver options
CHROME_OPTIONS = webdriver.ChromeOptions()
CHROME_OPTIONS.add_argument("--headless")  # Run in background
CHROME_OPTIONS.add_argument("--disable-gpu")
CHROME_OPTIONS.add_argument("--no-sandbox")
CHROME_OPTIONS.add_argument("--disable-dev-shm-usage")

# Function to generate random email
def generate_random_email():
    """Generate a random email address"""
    domains = ["gmail.com", "yahoo.com", "outlook.com", "protonmail.com"]
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domain = random.choice(domains)
    return f"{username}@{domain}"

# Function to generate random password
def generate_random_password():
    """Generate a random password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(chars, k=12))

# Function to generate random username
def generate_random_username():
    """Generate a random username"""
    length = random.randint(5, 15)
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Function to solve CAPTCHA using a solving service
def solve_captcha(captcha_sitekey, captcha_rqdata, captcha_rqtoken):
    """Solve CAPTCHA using a solving service"""
    if not CAPTCHA_API_KEY:
        print("No CAPTCHA solving service configured")
        return None

    try:
        # Send CAPTCHA to solving service
        payload = {
            "key": CAPTCHA_API_KEY,
            "method": "userrecaptcha",
            "googlekey": captcha_sitekey,
            "pageurl": "https://discord.com/register",
            "json": 1
        }

        # Test with 2captcha.com
        response = requests.post(f"{CAPTCHA_SOLVING_URL}/in.php", data=payload)
        response_data = response.json()

        if response_data.get("status") == 1:
            print(f"CAPTCHA sent. ID: {response_data['request']}")

            # Wait for solution
            payload = {"key": CAPTCHA_API_KEY, "action": "get", "id": response_data["request"], "json": 1}
            for attempt in range(30):  # Wait up to 30 attempts
                time.sleep(10)  # Wait 10 seconds between attempts
                response = requests.get(f"{CAPTCHA_SOLVING_URL}/res.php", params=payload)
                if response.json().get("status") == 1:
                    return response.json()["request"]

        return None
    except Exception as e:
        print(f"Error solving CAPTCHA: {str(e)}")
        return None

# Advanced function to create account with CAPTCHA solving using browser automation
def create_account_with_captcha(email, password, username, thread_id):
    """Create a new Discord account with CAPTCHA solving"""
    driver = None
    try:
        # Set up WebDriver options
        user_agent = random.choice(USER_AGENTS)
        chromium_options = webdriver.ChromeOptions()
        chromium_options.add_argument(f"user-agent={user_agent}")

        if PROXY_LIST:
            proxy = random.choice(PROXY_LIST)
            chromium_options.add_argument(f'--proxy-server={proxy}')

        # Create a separate session ID for each thread to prevent conflicts
        session_id = f"session-{thread_id}-{random.randint(1000, 9999)}"
        chromium_options.add_experimental_option("sessionId", session_id)

        # Initialize WebDriver
        driver = webdriver.Chrome(options=chromium_options)

        # Navigate to Discord registration
        driver.get("https://discord.com/register")

        # Fill in the form
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)

        # Wait for CAPTCHA to appear
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='hcaptcha.com']"))
            )

            # Switch to CAPTCHA iframe
            iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src*='hcaptcha.com']")
            driver.switch_to.frame(iframe)

            # Extract CAPTCHA data
            captcha_sitekey = driver.execute_script("return document.querySelector('meta[name=hcaptcha-sitekey]')?.content")
            driver.switch_to.default_content()

            print(f"Thread {thread_id} - CAPTCHA detected. Solving...")

            # Solve CAPTCHA
            captcha_token = solve_captcha(captcha_sitekey, None, None)

            if captcha_token:
                # Switch back to main page
                driver.switch_to.default_content()

                # Enter the CAPTCHA solution
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                for iframe in iframes:
                    try:
                        driver.switch_to.frame(iframe)
                        if "hcaptcha" in driver.page_source:
                            print(f"Thread {thread_id} - Found CAPTCHA iframe")
                            input_field = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.ID, "hcaptcha-box"))
                            )
                            driver.switch_to.window(driver.window_handles[0])
                            driver.find_element(By.ID, "hcaptcha-response").send_keys(captcha_token)
                            driver.find_element(By.XPATH, ".//button[@type='submit']").click()
                            break
                    except:
                        pass
                    finally:
                        driver.switch_to.default_content()

                # Click the registration button
                driver.find_element(By.XPATH, ".//button[@type='submit']").click()

                # Wait for registration to complete
                WebDriverWait(driver, 20).until(
                    EC.url_contains("discord.com/channels/@me")
                )

                print(f"Thread {thread_id} - CAPTCHA solved and account created successfully!")

                # Extract token from browser storage
                token_script = "localStorage.getItem('token');"
                token = driver.execute_script(token_script)

                if token:
                    # Get user info
                    user_id_script = "localStorage.getItem('user_id');"
                    user_id = driver.execute_script(user_id_script)

                    # Store account info
                    account_info = f"Thread {thread_id} - Username: {username} | ID: {user_id} | Email: {email} | Token: {token}"
                    with lock:
                        account_list.append(account_info)
                    return True

        except Exception as e:
            print(f"Thread {thread_id} - CAPTCHA handling failed: {str(e)}")

        return False
    except Exception as e:
        print(f"Thread {thread_id} - Error creating account with browser: {str(e)}")
        return False
    finally:
        if driver:
            driver.quit()

# Main function to create account using API first, then browser if needed
def create_account(email, password, username, thread_id):
    """Create a new Discord account with fallback to browser automation"""
    # Rotate user agents
    user_agent = random.choice(USER_AGENTS)
    headers = HEADERS.copy()
    headers["User-Agent"] = user_agent

    if PROXY_LIST:
        proxy = random.choice(PROXY_LIST)
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
    else:
        proxies = None

    # Create account data
    account_data = {
        "email": email,
        "password": password,
        "username": username,
        "date_of_birth": f"2000-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        "invite": None,
        "consent": True,
        "gift_code_sku_id": None,
        "family_id": None,
    }

    try:
        # Try API creation first
        response = requests.post(
            DISCORD_API,
            headers=headers,
            data=json.dumps(account_data),
            proxies=proxies,
            timeout=30
        )

        # Check if account creation was successful
        if response.status_code == 201:
            # Extract token from response
            data = response.json()
            token = data.get("token")

            if token:
                # Get user info
                user_data_response = requests.get(
                    f"https://discord.com/api/v9/users/@me",
                    headers=headers,
                    proxies=proxies,
                    timeout=30
                )

                if user_data_response.status_code == 200:
                    user_data = user_data_response.json()
                    user_id = user_data.get("id")

                    # Store account info
                    account_info = f"Thread {thread_id} - Username: {username} | ID: {user_id} | Email: {email} | Token: {token}"
                    with lock:
                        account_list.append(account_info)
                    return True

        # If API creation failed, try with browser automation
        if response.status_code == 400 and ("captcha-required" in response.text or "captcha_required" in response.text):
            print(f"Thread {thread_id} - CAPTCHA required, switching to browser automation...")
            return create_account_with_captcha(email, password, username, thread_id)

        # Print error message for debugging
        print(f"Thread {thread_id} - API account creation failed. Status code: {response.status_code}")
        print(f"Thread {thread_id} - Response: {response.text}")

        return False
    except Exception as e:
        print(f"Thread {thread_id} - Error in API account creation: {str(e)}")
        # If API method fails, try browser method
        return create_account_with_captcha(email, password, username, thread_id)

# Function that each thread will execute
def account_creation_thread(start_index, end_index, thread_id):
    """Function that each thread will execute to create accounts"""
    accounts_created = 0

    for i in range(start_index, end_index):
        try:
            # Generate random account data
            email = generate_random_email()
            password = generate_random_password()
            username = generate_random_username()

            print(f"Thread {thread_id} - Creating account {accounts_created + 1}/{ACCOUNTS_PER_THREAD}")
            print(f"Thread {thread_id} - Email: {email}")
            print(f"Thread {thread_id} - Username: {username}")

            # Create account
            success = create_account(email, password, username, thread_id)

            if success:
                accounts_created += 1
                print(f"Thread {thread_id} - Account created successfully!")
            else:
                print(f"Thread {thread_id} - Failed to create account")

            # Add delay to avoid rate limiting
            delay = random.uniform(1.0, 3.0)
            print(f"Thread {thread_id} - Waiting {delay:.2f} seconds before next attempt...")
            time.sleep(delay)

        except Exception as e:
            print(f"Thread {thread_id} - Error: {str(e)}")
    print(f"Thread {thread_id} - Finished creating accounts")

# Function to save token data to file
def save_token(token_data, file_name=OUTPUT_FILE):
    """Save token data to file"""
    if not token_data:
        return False

    # Create file if it doesn't exist
    if not os.path.exists(file_name):
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(f"{token_data}\n")
        return True

    # Append to existing file
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"{token_data}\n")
    return True

# Function to save all collected tokens
def save_all_tokens():
    """Save all collected tokens to file"""
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("".join(account_list))
    else:
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write("".join(account_list))

    print(f"Saved {len(account_list)} account tokens to {OUTPUT_FILE}")

# Main execution function
def main():
    global account_list
    # Create output file if it doesn't exist
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            pass  # Just create the file

    # Calculate accounts per thread
    accounts_per_thread = NUM_ACCOUNTS // NUM_THREADS
    remaining = NUM_ACCOUNTS % NUM_THREADS

    # Create and start threads
    threads = []
    for i in range(NUM_THREADS):
        start_index = i * accounts_per_thread
        end_index = (i + 1) * accounts_per_thread

        # Distribute remaining accounts
        if i < remaining:
            end_index += 1

        print(f"Creating thread {i+1}/{NUM_THREADS} to create {end_index - start_index} accounts")

        thread = threading.Thread(
            target=account_creation_thread,
            args=(start_index, end_index, i+1)
        )

        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Save all collected tokens
    save_all_tokens()

    print(f"Successfully created and saved {NUM_ACCOUNTS} Discord accounts.")

if __name__ == "__main__":
    main()
