
import requests
import os
import json
import time
import sys

def check_bot_status():
    """Check if the bot is running properly"""
    print("🔍 Checking bot status...")
    
    # Check HTTP server
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Bot HTTP server is running")
            print(f"   Status: {status['status']}")
            print(f"   Uptime: {status['uptime_seconds']} seconds")
            print(f"   Version: {status['version']}")
        else:
            print(f"❌ Bot HTTP server returned status code {response.status_code}")
    except Exception as e:
        print(f"❌ Bot HTTP server is not responding: {e}")
    
    # Check for running Python processes
    try:
        import subprocess
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        output = result.stdout
        
        # Count Python processes
        python_processes = [line for line in output.split('\n') if 'python' in line and 'main.py' in line]
        
        if python_processes:
            print(f"✅ Found {len(python_processes)} bot process(es) running")
            for i, process in enumerate(python_processes):
                parts = process.split()
                if len(parts) > 1:
                    pid = parts[1]
                    print(f"   Process {i+1}: PID {pid}")
        else:
            print("❌ No bot processes found running")
    except Exception as e:
        print(f"❌ Error checking processes: {e}")
    
    # Check Telegram connection
    try:
        token = os.getenv("TELEGRAM_TOKEN", "")
        if token:
            response = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=5)
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info.get("ok"):
                    bot_data = bot_info.get("result", {})
                    print(f"✅ Connected to Telegram as @{bot_data.get('username', 'Unknown')}")
                else:
                    print(f"❌ Telegram API error: {bot_info.get('description', 'Unknown error')}")
            else:
                print(f"❌ Telegram API returned status code {response.status_code}")
        else:
            print("⚠️ TELEGRAM_TOKEN not found in environment")
    except Exception as e:
        print(f"❌ Error checking Telegram connection: {e}")

if __name__ == "__main__":
    check_bot_status()
