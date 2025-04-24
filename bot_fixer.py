
import os
import sys
import subprocess
import time

def find_bot_processes():
    """Find all running bot processes"""
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        output = result.stdout
        
        # Find all python processes running main.py
        python_processes = []
        for line in output.split('\n'):
            if 'python' in line and 'main.py' in line and 'grep' not in line:
                parts = line.split()
                if len(parts) > 1:
                    pid = parts[1]
                    python_processes.append((pid, line))
        
        return python_processes
    except Exception as e:
        print(f"Error finding processes: {e}")
        return []

def kill_process(pid):
    """Kill a process by PID"""
    try:
        subprocess.run(["kill", "-9", pid])
        return True
    except Exception as e:
        print(f"Error killing process {pid}: {e}")
        return False

def main():
    print("🔍 Searching for duplicate bot processes...")
    processes = find_bot_processes()
    
    if len(processes) <= 1:
        print("✅ Only one or no bot process found. No conflicts detected.")
        sys.exit(0)
    
    print(f"⚠️ Found {len(processes)} bot processes running! This will cause conflicts.")
    
    for i, (pid, line) in enumerate(processes):
        print(f"{i+1}. PID {pid}: {line[:80]}...")
    
    # Kill all but the newest process
    processes_to_kill = processes[:-1]  # Keep the last one (assuming it's the newest)
    
    print(f"🛑 Terminating {len(processes_to_kill)} older processes...")
    for pid, _ in processes_to_kill:
        if kill_process(pid):
            print(f"  ✅ Killed process {pid}")
        else:
            print(f"  ❌ Failed to kill process {pid}")
    
    print("\n✅ Conflict resolution complete! You should now be able to run your bot without errors.")
    print("   Run 'python healthcheck.py' to verify your bot is working properly.")

if __name__ == "__main__":
    main()
