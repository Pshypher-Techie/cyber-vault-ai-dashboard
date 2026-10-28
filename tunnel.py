import subprocess
import re
import sys
import time

def start_tunnel():
    print("Launching Pinggy public HTTPS tunnel on port 443 for local port 8000...")
    cmd = [
        "C:\\Windows\\System32\\OpenSSH\\ssh.exe",
        "-p", "443",
        "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "-R", "0:localhost:8000",
        "a.pinggy.io"
    ]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    public_url = None
    start_time = time.time()

    # Read output to capture the public URL
    while time.time() - start_time < 20:
        line = process.stdout.readline()
        if not line:
            time.sleep(0.5)
            continue
        print(line, end="")
        match = re.search(r'(https://[a-zA-Z0-9-]+\.a\.pinggy\.link)', line)
        if match:
            public_url = match.group(1)
            break

    if public_url:
        print(f"\n=======================================================")
        print(f"CYBER-VAULT IS NOW COMPLETELY LIVE ON THE INTERNET!")
        print(f"Public Live HTTPS URL: {public_url}")
        print(f"=======================================================\n")
        with open("live_url.txt", "w", encoding="utf-8") as f:
            f.write(public_url)
        return process, public_url
    else:
        print("Could not obtain public tunnel URL automatically.")
        return process, None

if __name__ == "__main__":
    proc, url = start_tunnel()
    if proc:
        try:
            proc.wait()
        except KeyboardInterrupt:
            proc.terminate()

