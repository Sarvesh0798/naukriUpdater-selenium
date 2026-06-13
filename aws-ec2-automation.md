# AWS EC2 Automation Guide for Naukri Script

This guide explains how to deploy the existing `naukri-automation.py` script on a Windows Server 2019 EC2 instance, place files on the D: drive, create a Windows Task Scheduler task to run the script at 8:20 AM, and use AWS EventBridge schedules to start and stop the instance automatically.

## 1. EC2 Instance Setup

1. Open the AWS Management Console and go to EC2.
2. Launch a new instance using a Windows Server 2019 AMI.
3. Choose instance type:
   - `t2.medium` for moderate performance and lower cost
   - `t2.large` for more CPU/RAM capacity
4. Configure the instance:
   - Network and subnet as required.
   - Auto-assign public IP (with only your laptop's IP address in SG ingress) if you need remote RDP access.
5. Add storage(30gb) and tags as needed.
6. Attach an IAM role that allows EC2 start/stop actions.

### IAM role permissions

Create or attach an IAM role with a policy containing at least:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:StartInstances",
        "ec2:StopInstances",
        "ec2:DescribeInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

> For security, narrow the `Resource` field to the specific instance ARN once you know the instance ID.

## 2. Copy Files to D: Drive

1. Connect to the Windows Server instance using RDP.
2. Create a folder on the D: drive, for example:
   - `D:\pyhtonh\naukri-automation`
3. Copy the repository files into that folder, including:
   - `naukri-automation.py`
   - `README.md`
   - `requirements.txt`
4. Place your base resume file in the folder:
   - `D:\pyhtonh\naukri-automation\your-resume.pdf`

## 3. Install Python and Dependencies

1. Install Python 3.8+ on the Windows instance.
2. Add Python to PATH during installation.
3. Open PowerShell and install dependencies:
   ```powershell
   pip install selenium schedule pyautogui
   ```
4. If you use the repository `requirements.txt`, install:
   ```powershell
   pip install -r D:\pyhtonh\naukri-automation\requirements.txt
   ```

## 4. Launch Chrome with Remote Debugging

The script connects to an existing Chrome debug session. Run Chrome with these flags:
```powershell
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebugProfile"
```

1. Launch this from PowerShell.
2. Sign in to Naukri in the opened Chrome session.
3. Keep this Chrome window open while the script runs.

## 5. Create Windows Task Scheduler Task

Create a task that runs the script at 8:20 AM Monday through Friday.

### Task settings

- Trigger: Daily at `8:20 AM`
- Action: Start a program
  - Program/script: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`
  - Add arguments:
    ```powershell
    -NoProfile -ExecutionPolicy Bypass -File "D:\pyhtonh\naukri-automation\run_naukri_automation.ps1"
    ```
  - Start in: `D:\pyhtonh\naukri-automation`
- Run whether user is logged on or not
- Run with highest privileges

### Alternative direct Python action

- Program/script: `C:\Python39\python.exe`
- Add arguments: `D:\pyhtonh\naukri-automation\naukri-automation.py`
- Start in: `D:\pyhtonh\naukri-automation`

## 6. Create a PowerShell wrapper script (optional)

If you want a simple file to run from Task Scheduler, create `run_naukri_automation.ps1` with:
```powershell
$repoPath = "D:\pyhtonh\naukri-automation"
$scriptPath = Join-Path $repoPath "naukri-automation.py"
$pythonExe = "C:\Python39\python.exe"
Start-Process -FilePath $pythonExe -ArgumentList "`"$scriptPath`"" -WorkingDirectory $repoPath -NoNewWindow
```

> Update `C:\Python39\python.exe` to match the installed Python path on your EC2 instance.

## 7. AWS EventBridge Scheduler Rules

Create two EventBridge scheduled rules to start and stop the instance automatically.

### Rule 1: Start instance
- Name: `start-instance-weekdays`
- Schedule expression: `cron(0 8 ? * MON-FRI *)`
- Target: EC2 StartInstances
- Instance IDs: the target instance ID

### Rule 2: Stop instance
- Name: `stop-instance-weekdays`
- Schedule expression: `cron(30 16 ? * MON-FRI *)`
- Target: EC2 StopInstances
- Instance IDs: the target instance ID

## 8. Recommended process

1. Use EventBridge to power on the instance at 8:00 AM Monday to Friday.
2. Use Task Scheduler on the instance to launch the Naukri script at 8:20 AM.
3. Use EventBridge to stop the instance at 4:30 PM Monday to Friday.

## 9. What to verify

- The Windows instance is launched from a Windows Server 2019 AMI.
- The EC2 instance type is `t2.medium` or `t2.large`.
- The IAM role attached to the instance permits EC2 start/stop/describe.
- The Windows folder path is `D:\pyhtonh\naukri-automation`.
- Chrome is running with remote debugging enabled.
- Naukri is logged in inside that Chrome session.
- The resume file exists at `D:\pyhtonh\naukri-automation\your-resume.pdf`.
- Task Scheduler is configured for Monday–Friday at 8:20 AM.
- EventBridge schedules are set to start at 8:00 AM and stop at 4:30 PM Monday–Friday.

## 10. Notes

- This guide does not add any new Python automation file.
- It uses the existing `naukri-automation.py` script and Windows scheduling.
- Use AWS EventBridge only for instance power control, not for running the local Python script directly.
