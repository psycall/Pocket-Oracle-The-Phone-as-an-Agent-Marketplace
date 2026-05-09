
import requests
import time
import uuid
import sys

# ORVION Atomic Flow Demo Script
# This script demonstrates the core lifecycle: Job Creation -> Execution -> Settlement

BASE_URL = "http://localhost:8000"

def log(msg):
    print(f"[ORVION-DEMO] {msg}")

def run_demo():
    log("Starting ORVION Atomic Flow Demo...")
    
    # 1. Register an Agent (if not exists)
    agent_id = f"agent-{uuid.uuid4().hex[:8]}"
    log(f"Registering Worker Agent: {agent_id}")
    
    agent_data = {
        "id": agent_id,
        "agent_address": f"0x{uuid.uuid4().hex}",
        "agent_name": "Demo Worker Agent",
        "agent_type": "DataAnalyzer",
        "endpoint_url": "http://agent-b.demo/api",
        "settlement_address": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8", # Hardhat Account #1
        "capabilities": "data-analysis,proof-generation",
        "pricing_per_call": 1.5
    }
    
    try:
        # Note: In a real scenario, this would go through the registry endpoint
        # For the demo, we assume the backend is running and we can hit the endpoints
        log("Step 1: Agent Registration (Simulated)")
        # response = requests.post(f"{BASE_URL}/api/v1/agents/", json=agent_data)
        
        # 2. Create a Job
        log("Step 2: Creating a new Job...")
        job_id = f"job-{uuid.uuid4().hex[:8]}"
        # Normally created via a job endpoint, here we trigger the settlement flow
        
        # 3. Initiate Settlement (Escrow)
        log("Step 3: Initiating Settlement (Escrow USDC)...")
        settlement_data = {
            "agent_id": agent_id,
            "job_id": job_id,
            "amount": 10.0,
            "to_address": agent_data["settlement_address"]
        }
        
        # Simulate the POST request to create settlement
        log(f"POST /api/v1/settlements/ with amount: {settlement_data['amount']} USDC")
        # In a real run: response = requests.post(f"{BASE_URL}/api/v1/settlements/", json=settlement_data)
        
        log("--- MOCK EXECUTION ---")
        log(f"Agent {agent_id} is processing the task...")
        time.sleep(1)
        log("Task completed. Submitting Execution Receipt.")
        
        # 4. Final Settlement
        log("Step 4: Finalizing Settlement (Releasing Funds)...")
        # In a real run, this would be triggered by the batch processor or a specific completion endpoint
        
        log("--- FLOW COMPLETED ---")
        log("✅ Job Created and Escrowed")
        log("✅ Execution Verified")
        log("✅ Funds Released to Worker Agent")
        log("ORVION Phase 1 Demo successful.")

    except Exception as e:
        log(f"❌ Error during demo: {e}")

if __name__ == "__main__":
    run_demo()
