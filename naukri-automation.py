from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import schedule
import shutil
import os
from datetime import datetime

# Configure Chrome Debug Session
def get_chrome_driver():
    """
    Connect to an existing Chrome debug session.
    Make sure to launch Chrome with: chrome --remote-debugging-port=9222
    """
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def toggle_period_in_headline(driver):
    """
    Navigate to profile, edit headline, toggle period at end, and save.
    """
    try:
        # Navigate to profile page
        base_url = "https://www.naukri.com"
        profile_url = base_url + '/mnjuser/profile'
        driver.get(profile_url)
        
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Navigated to profile page")
        time.sleep(2)
        
        # Click on edit icon for resume headline
        wait = WebDriverWait(driver, 10)
        edit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='edit icon']"))
        )
        edit_button.click()
        
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Clicked edit button")
        time.sleep(1)
        
        # Wait for modal to open and find textarea
        textarea = wait.until(
            EC.presence_of_element_located((By.ID, "resumeHeadlineTxt"))
        )
        
        # Get current content
        current_text = textarea.get_attribute("value")
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Current headline: {current_text}")
        
        # Toggle period at the end
        if current_text.endswith("."):
            # Remove period if present
            updated_text = current_text[:-1]
            action_type = "removed"
        else:
            # Add period if not present
            updated_text = current_text + "."
            action_type = "added"
        
        # Clear the textarea and enter new text
        textarea.clear()
        textarea.send_keys(updated_text)
        
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Period {action_type}. New headline: {updated_text}")
        time.sleep(1)
        
        # Click save button
        save_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='btn-dark-ot' and @type='submit']"))
        )
        save_button.click()
        
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Profile updated successfully!")
        time.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error occurred: {str(e)}")
        return False

def prepare_resume_copy():
    """
    Create a copy of the resume with today's date in the filename.
    Returns the path to the copied resume file.
    """
    try:
        base_path = r"D:\pyhtonh\naukri-automation"
        original_file = os.path.join(base_path, "your-resume.pdf")
        
        # Create filename with today's date
        today_date = datetime.now().strftime("%Y-%m-%d")
        new_filename = f"{today_date}_your_frontend.pdf"
        new_file_path = os.path.join(base_path, new_filename)
        
        # Copy the file
        shutil.copy(original_file, new_file_path)
        
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Resume copied to: {new_file_path}")
        return new_file_path
        
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error copying resume: {str(e)}")
        return None

def upload_resume(driver):
    """
    Upload resume to Naukri profile.
    """
    try:
        # Prepare the resume copy
        resume_path = prepare_resume_copy()
        if not resume_path:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Failed to prepare resume")
            return False
        
        # Get absolute path for file upload
        resume_path = os.path.abspath(resume_path)
        
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Uploading resume from: {resume_path}")
        
        # Find and click the "Update resume" button
        wait = WebDriverWait(driver, 10)
        upload_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='Update resume' and @class='dummyUpload typ-14Bold']"))
        )
        # upload_button.click()
        
        # print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Clicked Update resume button")
        # time.sleep(1)
        
        # # Find the file input element (usually hidden) and send the file path
        # file_input = wait.until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        # )
        # file_input.send_keys(resume_path)
        
        # print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] File selected: {resume_path}")
        # time.sleep(4)
        
        # print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Resume uploaded successfully!")

        # # Press Escape to close any remaining file picker dialogs
        # pyautogui.press('esc')
        # time.sleep(0.5)
        # pyautogui.press('esc')

        # Find the file input element (usually hidden) and send the file path
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")

        # Force the input to be visible and enabled
        driver.execute_script(
            "arguments[0].style.display = 'block'; "
            "arguments[0].style.visibility = 'visible'; "
            "arguments[0].removeAttribute('disabled');", 
            file_input
        )

        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] File selected: {resume_path}")
        time.sleep(1) 

        # Send keys directly without clicking anything else
        file_input.send_keys(resume_path)   

        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Resume uploaded successfully!")
        return True
        
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error uploading resume: {str(e)}")
        return False

def scheduled_update():
    """
    Perform the profile update and resume upload tasks.
    """
    try:
        driver = get_chrome_driver()
        
        # Update headline
        toggle_period_in_headline(driver)
        
        # Upload resume
        upload_resume(driver)
        
        # Don't close the driver as we want to keep the session alive
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Failed to connect to Chrome debug session: {str(e)}")

def main():
    """
    Main function to schedule profile updates every 5 minutes.
    """
    print("="*60)
    print("Naukri Profile Auto-Update Script")
    print("="*60)
    print("Make sure Chrome is running with: chrome --remote-debugging-port=9222")
    print("="*60)
    
    # Run immediately on start
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Running initial update...")
    scheduled_update()
    
    # Schedule the task to run every 5 minutes
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Scheduling updates every 5 minutes...")
    schedule.every(5).minutes.do(scheduled_update)
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n" + "="*60)
        print("Scheduler stopped by user")
        print("="*60)

if __name__ == "__main__":
    main()
