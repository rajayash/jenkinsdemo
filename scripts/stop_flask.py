#!/usr/bin/env python3
import subprocess
import os
import time
import signal

def stop_flask():
    try:
        # Find process using port 80
        cmd = "sudo lsof -t -i:80"
        pids = subprocess.check_output(cmd, shell=True).decode().strip().split('\n')
        
        for pid in pids:
            if pid:
                # Kill the process
                subprocess.run(['sudo', 'kill', '-9', pid])
                print(f"Killed process {pid}")
        
        # Wait for port to be released
        time.sleep(2)
        
    except Exception as e:
        print(f"Error stopping Flask: {e}")

if __name__ == "__main__":
    stop_flask()
