'''
DOCKER MONITOR
Monitors Docker events for unauthorized socket or host root mounting to detect container escape vulnerabilities.
'''

import docker
from logger import log_event

def container_escape_monitor():
    client = docker.from_env()
    print("Monitoring for host escape attempts... (Press Ctrl+C to stop)")
    
    for event in client.events(decode=True):
        # Attain the container ID from the Docker "Actor" field
        container_id = event.get("Actor", {}).get("ID")

        # Only proceed with containers that are starting w/ a valid ID
        if event.get("Type") != "container" or event.get("Action") != "start" or not container_id:
            continue

        try:
            container = client.containers.get(container_id)
            mounts = container.attrs.get('Mounts', [])
            
            print(f"Checking container: {container.name}")

            for mount in mounts:
                src = mount.get('Source', '')

                # Detection logic checks for dangerous mounts
                if src == "/" or "docker.sock" in src or "host_root" in src:

                    # Docker does not store the IP in Docker events so the Kali IP is hardcoded for the demo
                    attacker_ip = "192.168.1.131"

                    print(f"SECURITY VIOLATION: {src}!!!")
                    
                    # Log the event to the SecurityEvents DB
                    log_event(
                        member_name="skylarDetection", 
                        source_ip=attacker_ip, 
                        event_type="containerEscape", 
                        severity=3, 
                        raw_data=f"Vulnerable mount detected: {src}"
                    )

                    # Mitigation stops the container
                    print(f"Stopping container {container.name}...")
                    container.stop()
                    break # Exit mount loop

            else:
                print(f"Container {container.name} passed security check.")  

        except Exception as e:
            print(f"Error checking container: {e}")

if __name__ == "__main__":
    container_escape_monitor()
