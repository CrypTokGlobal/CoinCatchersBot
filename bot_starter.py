
import os
import sys
import subprocess
import time
import signal
import json

def check_env_vars():
    """Check for required environment variables"""
    print("🔍 Checking environment variables...")
    token = os.getenv("TELEGRAM_TOKEN", "")
    if not token:
        print("❌ TELEGRAM_TOKEN environment variable is missing!")
        print("   Please set it in the Secrets tab (🔒) in the sidebar.")
        return False
    print("✅ TELEGRAM_TOKEN found")
    return True

def clean_zombie_processes():
    """Find and clean any zombie Python processes"""
    print("🔍 Checking for zombie processes...")
    try:
        # Find Python processes
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        output = result.stdout
        
        python_processes = []
        for line in output.split('\n'):
            if 'python' in line and 'main.py' in line and not 'grep' in line:
                parts = line.split()
                if len(parts) > 1:
                    pid = parts[1]
                    python_processes.append((pid, line))
        
        if not python_processes:
            print("✅ No zombie Python processes found")
            return
            
        print(f"⚠️ Found {len(python_processes)} Python processes running")
        
        # Kill existing processes
        for pid, proc_info in python_processes:
            print(f"  🛑 Terminating process {pid}: {proc_info[:60]}...")
            try:
                os.kill(int(pid), signal.SIGKILL)
                print(f"  ✅ Process {pid} terminated")
            except Exception as e:
                print(f"  ❌ Failed to kill process {pid}: {e}")
                
        # Wait a moment to ensure processes have terminated
        time.sleep(2)
    except Exception as e:
        print(f"❌ Error checking processes: {e}")

def check_file_permissions():
    """Ensure main.py is executable"""
    print("🔍 Checking file permissions...")
    if os.path.exists("main.py"):
        try:
            os.chmod("main.py", 0o755)
            print("✅ Set main.py as executable")
        except Exception as e:
            print(f"⚠️ Could not set permissions: {e}")
    else:
        print("❌ main.py not found!")

def run_bot():
    """Run the bot with proper error handling"""
    print("\n🚀 Starting CoinCatchers Bot...")
    
    # Run the bot
    try:
        # Directly run Python with the main file
        process = subprocess.Popen([sys.executable, "main.py"], 
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  text=True,
                                  bufsize=1)
        
        # Monitor the output
        print("\n📋 Bot output:")
        print("="*50)
        
        for line in process.stdout:
            print(line, end='')
            
            # If we see the success message, the bot is running
            if "CoinCatchersBot is now watching" in line:
                print("="*50)
                print("✅ Bot is running successfully!")
                print("="*50)
                break
                
        # Keep the process running by waiting for it
        process.wait()
    except KeyboardInterrupt:
        print("\n⚠️ Bot process interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running bot: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 CoinCatchers Bot Starter")
    print("=" * 50)
    
    # Run checks and fixes
    if not check_env_vars():
        sys.exit(1)
        
    clean_zombie_processes()
    check_file_permissions()
    
    # Run the bot
    run_bot()
