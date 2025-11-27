import subprocess
import sys
import os

def main():
    agents = []
    print("Starting Multi-Agent Shopping Assistant...")
    print("---------------------------------------")
    
    try:
        # Run ADK Web Interface on the agents directory
        # This will discover all agent subdirectories
        chat_process = subprocess.Popen(["adk", "web", "agents"], cwd=os.getcwd())
        agents.append(chat_process)
        
        # Wait for the process
        chat_process.wait()

    except KeyboardInterrupt:
        print("\nStopping all agents...")
    finally:
        print("Cleaning up processes...")
        
        # Clear cache
        print("Clearing agent cache...")
        try:
            import shutil
            cache_dir = os.path.join(os.getcwd(), ".adk_cache")
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                print("Cache cleared.")
        except Exception as e:
            print(f"Warning: Could not clear cache: {e}")
        
        for p in agents:
            if p.poll() is None: # If still running
                p.terminate()
                try:
                    p.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    p.kill()
        print("All agents stopped.")

if __name__ == "__main__":
    main()
