# Naukri Automation Script

This repository contains a Python script (`naukri-automation.py`) that automates Naukri profile headline toggling and resume upload using an existing Chrome debug session on Windows(keep your naukri session logged-in).

## Requirements

- Windows 10 / Windows 11
- Python 3.8 or newer
- Google Chrome installed
- ChromeDriver compatible with your installed Chrome version
- `selenium` Python package
- `schedule` Python package
- `pyautogui` Python package (optional but included in the script)

## Setup

1. Install Python
   - Download and install Python from https://www.python.org/downloads/.
   - During installation, enable `Add Python to PATH`.

2. Install dependencies
   Open PowerShell and run:
   ```powershell
   pip install selenium schedule pyautogui
   ```

3. Download ChromeDriver
   - Check your Chrome version in Chrome: `Settings` > `About Chrome`.
   - Download the matching ChromeDriver from https://chromedriver.chromium.org/downloads.
   - Extract `chromedriver.exe` and place it somewhere on your system, or add its folder to your PATH.

4. Launch Chrome with remote debugging enabled
   Open PowerShell and run:
   ```powershell
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebugProfile"
   ```
   - This starts Chrome in a debugging mode the script can attach to.
   - Keep this Chrome window open while the script runs.

5. Log in to Naukri in the debugging Chrome session
   - In the opened Chrome window, sign in to your Naukri account.
   - Verify that you can access your profile page and resume update area.

6. Place your resume file
   - Put your base resume file in the repository folder: `D:\pyhtonh\naukri-automation\your-resume.pdf`
   - The script copies this file and uploads the copy with a date-based name.

## Usage

1. Open PowerShell in the repository folder:
   ```powershell
   cd D:\pyhtonh\naukri-automation
   ```

2. Run the script:
   ```powershell
   python naukri-automation.py
   ```

3. What the script does
   - Connects to the existing Chrome debug session at `127.0.0.1:9222`
   - Opens the Naukri profile page
   - Toggles the final `.` in the resume headline
   - Copies `your-resume.pdf` to a dated file like `2026-06-13_you_frontend.pdf`
   - Uploads the resume copy via the Naukri resume upload form
   - Repeats the update every 5 minutes until stopped

4. Stop the script
   - Press `Ctrl+C` in the PowerShell window.

## Notes

- The script expects the Chrome debugger address to be `127.0.0.1:9222`.
- The resume upload path is currently hard-coded to `D:\pyhtonh\naukri-automation`.
- Make sure the login session is active and the profile page elements still exist on Naukri.
- If Naukri changes its page structure, Selenium locators may need to be updated.

## Troubleshooting

- `selenium.common.exceptions.WebDriverException`: Check ChromeDriver version compatibility and ensure Chrome is launched with `--remote-debugging-port=9222`.
- `NoSuchElementException` or `TimeoutException`: The script may not find the page elements; confirm you are logged in and the profile page is valid.
- Resume upload fails: Make sure `kalyani-resume.pdf` exists in the repository directory.

## Customization

- Change the resume file name in `prepare_resume_copy()` if your base file is named differently.
- Update the scheduling interval in `main()` if you want a different repeat rate.
