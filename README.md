# Container Escape Vulnerability and Defense Cycle

## Project Overview
Modern cloud infrastructures are highly susceptible to container escape vulnerabilities, where an adversary gains unauthorized access to the host machine. This project provides a Python-based security solution that monitors Docker events in real-time to detect and immediately neutralize containers attempting to mount sensitive host directories or the Docker socket.

## Core Features
* Real-time event monitoring uses the Docker SDK to intercept container start events
* Detection scans mount configurations for forbidden paths (`/`, `/var/run/docker.sock`)
* Automated mitigation executes an immediate stop command on non-compliant containers to prevent exploitation
* Forensic auditing logs incident metadata (Source IP, Timestamp, Event Type) into a centralized SQLite3 database

## System Components
* `monitor_docker.py`: The detection and mitigation program
* `database_setup.py`: Initializes the SQLite3 schema for security event tracking
* `logger.py`: Standardized utility for recording security events

## Demo Video
[![Watch the Demo](https://img.youtube.com/vi/3gDOM4y4Tew/maxresdefault.jpg)](https://youtu.be/3gDOM4y4Tew)

## Host Setup (Ubuntu Linux VM)

1. **File Preparation**:

Add the project files to a dedicated directory:
```bash
mkdir container-escape-mitigation
cd container-escape-mitigation
# Move all project files into this directory
```

2. **Install Dependencies**:

Ensure you have Python3 and Pip installed, then run:
```bash
sudo apt update
pip install -r requirements.txt
```

3. **Enable Remote Docker API for the Kali Attack**:

To allow for remote attack simulation, the Docker daemon must be configured to listen on the network. Edit the service file:
```bash
sudo nano /lib/systemd/system/docker.service
```
Append `-H tcp://0.0.0.0:2375` to the end of the line starting with `ExecStart`.

Reload and Restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

4. **Initialize Database**:
```bash
python3 database_setup.py
```

## Attacker Setup (Kali Linux VM)

1. **Install Docker.io**:

To simulate an external threat actor, the Kali VM requires the Docker client.
```bash
sudo apt update && sudo apt install docker.io -y
```

## Testing & Validation

1. **Start the monitor (Ubuntu)**: 
```bash
python3 monitor_docker.py
```

2. **Launch remote attack (Kali)**:

Replace <UBUNTU_IP> with your host's' IP by running `ip addr` (e.g., 192.168.1.180)
```bash
docker -H <UBUNTU_IP>:2375 run -d --name attacker-escape -v /var/run/docker.sock:/var/run/docker.sock alpine
```

3. **Verify mitigation (Ubuntu)**:

`monitor_docker.py` will detect the unauthorized socket mount and stop the container. Verify the status:
```bash
docker ps -a
```
The container should show a status of "Exited" if unauthorized signatures were detected.


4. **Verify forensic logs (Ubuntu)**:
```bash
sqlite3 security_logs.db "SELECT * FROM SecurityEvents WHERE memberName='skylarDetection';"
```

5. **Run standard operations**:

To test if an authorized container remains up, run the following where <UBUNTU_IP> is your host's' IP:
```bash
docker -H <UBUNTU_IP>:2375 run -d --name legitimate-web-server nginx
```
Repeat step 3 where the container should now show a status of "Up".
