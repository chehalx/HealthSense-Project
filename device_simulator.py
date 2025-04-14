import requests
import time
import json
import random
import argparse
from datetime import datetime

def generate_random_health_data(device_id):
    """Generate random health data within realistic ranges"""
    return {
        "device_id": device_id,
        "glucose": random.randint(70, 200),  # mg/dL
        "bp_systolic": random.randint(90, 160),  # mmHg
        "bp_diastolic": random.randint(60, 110),  # mmHg
        "spo2": random.randint(88, 100),  # %
        "heart_rate": random.randint(50, 110),  # BPM
        "timestamp": datetime.utcnow().isoformat()
    }

def generate_scenario_health_data(device_id, scenario):
    """Generate health data for specific scenarios"""
    base_data = {
        "device_id": device_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if scenario == "healthy":
        return {
            **base_data,
            "glucose": random.randint(80, 120),
            "bp_systolic": random.randint(110, 120),
            "bp_diastolic": random.randint(70, 80),
            "spo2": random.randint(95, 100),
            "heart_rate": random.randint(60, 80)
        }
    elif scenario == "diabetes":
        return {
            **base_data,
            "glucose": random.randint(180, 250),
            "bp_systolic": random.randint(120, 140),
            "bp_diastolic": random.randint(80, 90),
            "spo2": random.randint(94, 98),
            "heart_rate": random.randint(70, 90)
        }
    elif scenario == "heart_issue":
        return {
            **base_data,
            "glucose": random.randint(80, 140),
            "bp_systolic": random.randint(150, 180),
            "bp_diastolic": random.randint(95, 110),
            "spo2": random.randint(92, 97),
            "heart_rate": random.randint(90, 120)
        }
    elif scenario == "hypoxia":
        return {
            **base_data,
            "glucose": random.randint(80, 130),
            "bp_systolic": random.randint(110, 150),
            "bp_diastolic": random.randint(70, 90),
            "spo2": random.randint(85, 92),
            "heart_rate": random.randint(90, 120)
        }
    else:  # random
        return generate_random_health_data(device_id)

def send_health_data(url, data):
    """Send health data to the server"""
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        
        if response.status_code == 200:
            print(f"Data sent successfully: {data}")
            print(f"Response: {response.json()}")
        else:
            print(f"Error sending data: {response.status_code}")
            print(f"Response: {response.text}")
            
        return response.status_code == 200
    except Exception as e:
        print(f"Exception while sending data: {e}")
        return False

def run_simulator(device_id, server_url, interval, scenario, duration):
    """Run the device simulator"""
    api_url = f"{server_url}/api/healthdata"
    
    print(f"Starting HealthSense device simulator for device: {device_id}")
    print(f"Sending data to: {api_url}")
    print(f"Interval: {interval} seconds")
    print(f"Scenario: {scenario}")
    
    start_time = time.time()
    count = 0
    
    while True:
        # Check if we've reached the duration
        if duration > 0 and time.time() - start_time > duration:
            print(f"Simulation completed after {duration} seconds. Sent {count} data points.")
            break
            
        # Generate and send data
        data = generate_scenario_health_data(device_id, scenario)
        success = send_health_data(api_url, data)
        count += 1 if success else 0
        
        # Wait for the next interval
        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='HealthSense Device Simulator')
    parser.add_argument('--device-id', default='HEALTH01', help='Device ID')
    parser.add_argument('--server', default='http://localhost:5000', help='Server URL')
    parser.add_argument('--interval', type=float, default=5.0, help='Data sending interval in seconds')
    parser.add_argument('--scenario', default='random', 
                       choices=['random', 'healthy', 'diabetes', 'heart_issue', 'hypoxia'],
                       help='Health scenario to simulate')
    parser.add_argument('--duration', type=int, default=0, 
                       help='Duration to run the simulator in seconds (0 for unlimited)')
    
    args = parser.parse_args()
    
    try:
        run_simulator(args.device_id, args.server, args.interval, args.scenario, args.duration)
    except KeyboardInterrupt:
        print("\nSimulator stopped by user.")
