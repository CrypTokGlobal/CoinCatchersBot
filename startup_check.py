
#!/usr/bin/env python3
import os
import sys
import socket
import json
import subprocess

def check_environment():
    """Check if the environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check Python version
    python_version = sys.version.split()[0]
    print(f"  • Python version: {python_version}")
    
    # Check for Telegram token
    token = os.getenv("TELEGRAM_TOKEN", "")
    if token:
        masked_token = token[:4] + "..." + token[-4:] if len(token) > 8 else "***"
        print(f"  • TELEGRAM_TOKEN: {masked_token} ✅")
    else:
        print("  • TELEGRAM_TOKEN: Missing ❌")
        print("    Set the TELEGRAM_TOKEN in the Secrets tab (🔒)")
        return False
    
    # Check for critical files
    critical_files = ["main.py", "wallet.py", "config.py"]
    missing_files = [f for f in critical_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"  • Missing critical files: {', '.join(missing_files)} ❌")
        return False
    else:
        print("  • All critical files present ✅")
    
    return True

def run_quick_test():
    """Run a quick test to check basic functionality"""
    print("\n🧪 Running quick functionality test...")
    
    # Check if port 8080 is already in use
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('0.0.0.0', 8080))
    if result == 0:
        print("  • Port 8080 is already in use ⚠️")
        print("    This might indicate another instance is running")
    else:
        print("  • Port 8080 is available ✅")
    sock.close()
    
    # Check that the requirements are installed
    print("\n📦 Checking package installation...")
    required_packages = ["python-telegram-bot", "solana", "requests", "httpx"]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  • {package}: Installed ✅")
        except ImportError:
            print(f"  • {package}: Missing ❌")
            print(f"    Run 'pip install {package}' to install it")
    
    print("\n🔍 Testing wallet functionality...")
    try:
        import wallet
        wallet_module_exists = True
        print("  • wallet module imported successfully ✅")
    except ImportError:
        wallet_module_exists = False
        print("  • wallet module import failed ❌")
    
    return wallet_module_exists

def fix_common_issues():
    """Try to fix common issues"""
    print("\n🔧 Attempting to fix common issues...")
    
    # Kill any existing Python processes
    try:
        print("  • Checking for existing Python processes...")
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        output = result.stdout
        
        for line in output.split('\n'):
            if 'python' in line and 'main.py' in line and not 'grep' in line:
                parts = line.split()
                if len(parts) > 1:
                    pid = parts[1]
                    print(f"  • Found Python process: {pid}, terminating...")
                    subprocess.run(["kill", "-9", pid])
    except Exception as e:
        print(f"  • Error checking processes: {e}")
    
    # Reset port bindings
    print("  • Freeing port 8080...")
    try:
        os.system("fuser -k 8080/tcp")
    except:
        pass
    
    print("  • Fixes applied ✅")

def main():
    print("=" * 50)
    print("🤖 CoinCatchers Bot Startup Check")
    print("=" * 50)
    
    env_ok = check_environment()
    test_ok = run_quick_test()
    
    if not (env_ok and test_ok):
        print("\n⚠️ Some checks failed. Attempting to fix issues...")
        fix_common_issues()
        
        print("\n🔄 Try running the bot again with the 'Run' button")
        print("   If problems persist, contact @CoinCatchers88 or @Shilling_Queen")
    else:
        print("\n✅ All checks passed! The bot should run fine.")
        print("   Use the 'Run' button to start the bot")

if __name__ == "__main__":
    main()
