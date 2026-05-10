#!/usr/bin/env python3
"""
ORVION API Integration Tests
Comprehensive test suite for backend endpoints
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8080"
API_V1 = f"{BASE_URL}/api/v1"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def print_test(title: str):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}▶ {title}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")

def print_success(msg: str):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg: str):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg: str):
    print(f"{Colors.YELLOW}ℹ️  {msg}{Colors.END}")

def test_health_check() -> bool:
    """Test 1: Health Check"""
    print_test("Test 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check passed: {data}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False

def test_agent_registration() -> Dict[str, Any]:
    """Test 2: Agent Registration"""
    print_test("Test 2: Agent Registration")
    
    agent_data = {
        "agent_address": "0x1234567890123456789012345678901234567890",
        "agent_name": "ResearchBot-01",
        "agent_type": "research",
        "capabilities": ["data-analysis", "web-search"],
        "pricing_per_call": 0.001,
        "endpoint_url": "https://research-bot.example.com",
        "settlement_address": "0x0987654321098765432109876543210987654321"
    }
    
    try:
        response = requests.post(
            f"{API_V1}/discovery/agents",
            json=agent_data,
            timeout=5
        )
        if response.status_code == 201:
            agent = response.json()
            print_success(f"Agent registered: {agent['agent_name']} (ID: {agent['id']})")
            return {"success": True, "agent": agent}
        else:
            print_error(f"Registration failed: {response.status_code}")
            print_info(f"Response: {response.text}")
            return {"success": False}
    except Exception as e:
        print_error(f"Registration error: {str(e)}")
        return {"success": False}

def test_get_agents() -> bool:
    """Test 3: Get All Agents"""
    print_test("Test 3: Get All Agents")
    
    try:
        response = requests.get(
            f"{API_V1}/discovery/agents?limit=10",
            timeout=5
        )
        if response.status_code == 200:
            agents = response.json()
            print_success(f"Retrieved {len(agents)} agents")
            if agents:
                print_info(f"First agent: {agents[0].get('agent_name', 'N/A')}")
            return True
        else:
            print_error(f"Get agents failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Get agents error: {str(e)}")
        return False

def test_settlement_creation(agent_id: str) -> Dict[str, Any]:
    """Test 4: Settlement Creation"""
    print_test("Test 4: Settlement Creation")
    
    settlement_data = {
        "job_id": "job-test-001",
        "agent_id": agent_id,
        "amount": 100.5,
        "to_address": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd"
    }
    
    try:
        response = requests.post(
            f"{API_V1}/settlement/settlements",
            json=settlement_data,
            timeout=5
        )
        if response.status_code == 201:
            settlement = response.json()
            print_success(f"Settlement created (ID: {settlement['id']}, Status: {settlement['status']})")
            return {"success": True, "settlement": settlement}
        else:
            print_error(f"Settlement creation failed: {response.status_code}")
            print_info(f"Response: {response.text}")
            return {"success": False}
    except Exception as e:
        print_error(f"Settlement creation error: {str(e)}")
        return {"success": False}

def test_get_settlement(settlement_id: str) -> bool:
    """Test 5: Get Settlement"""
    print_test("Test 5: Get Settlement")
    
    try:
        response = requests.get(
            f"{API_V1}/settlement/settlements/{settlement_id}",
            timeout=5
        )
        if response.status_code == 200:
            settlement = response.json()
            print_success(f"Settlement retrieved: Status={settlement['status']}, Amount={settlement['amount']}")
            return True
        else:
            print_error(f"Get settlement failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Get settlement error: {str(e)}")
        return False

def test_execution_receipt() -> bool:
    """Test 6: Execution Receipt"""
    print_test("Test 6: Execution Receipt Submission")
    
    receipt_data = {
        "job_id": "job-test-001",
        "proof": "proof-hash-0x1234567890abcdef"
    }
    
    try:
        response = requests.post(
            f"{API_V1}/settlement/execution-receipts",
            json=receipt_data,
            timeout=5
        )
        if response.status_code == 201:
            receipt = response.json()
            print_success(f"Receipt submitted (ID: {receipt['id']}, Verified: {receipt['verified']})")
            return True
        else:
            print_error(f"Receipt submission failed: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Receipt submission error: {str(e)}")
        return False

def test_batch_settlement(settlement_ids: list) -> bool:
    """Test 7: Batch Settlement Processing"""
    print_test("Test 7: Batch Settlement Processing")
    
    if not settlement_ids:
        print_error("No settlement IDs to process")
        return False
    
    try:
        response = requests.post(
            f"{API_V1}/settlement/process-batch",
            json={"settlement_ids": settlement_ids},
            timeout=5
        )
        if response.status_code == 200:
            result = response.json()
            print_success(f"Batch processed: {result.get('processed_count', 0)} settlements")
            print_info(f"Transaction hash: {result.get('transaction_hash', 'N/A')}")
            return True
        else:
            print_error(f"Batch processing failed: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Batch processing error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print(f"\n{Colors.BLUE}{'*'*60}{Colors.END}")
    print(f"{Colors.BLUE}  ORVION API Integration Test Suite{Colors.END}")
    print(f"{Colors.BLUE}  Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    print(f"{Colors.BLUE}{'*'*60}{Colors.END}")
    
    results = {
        "health_check": False,
        "agent_registration": False,
        "get_agents": False,
        "settlement_creation": False,
        "get_settlement": False,
        "execution_receipt": False,
        "batch_settlement": False,
    }
    
    # Test 1: Health Check
    results["health_check"] = test_health_check()
    if not results["health_check"]:
        print_error("Backend is not responding. Aborting tests.")
        return results
    
    time.sleep(1)
    
    # Test 2: Agent Registration
    agent_result = test_agent_registration()
    results["agent_registration"] = agent_result["success"]
    agent_id = agent_result.get("agent", {}).get("id")
    
    time.sleep(1)
    
    # Test 3: Get Agents
    results["get_agents"] = test_get_agents()
    
    time.sleep(1)
    
    # Test 4: Settlement Creation
    if agent_id:
        settlement_result = test_settlement_creation(agent_id)
        results["settlement_creation"] = settlement_result["success"]
        settlement_id = settlement_result.get("settlement", {}).get("id")
        
        time.sleep(1)
        
        # Test 5: Get Settlement
        if settlement_id:
            results["get_settlement"] = test_get_settlement(settlement_id)
            
            time.sleep(1)
            
            # Test 7: Batch Settlement
            results["batch_settlement"] = test_batch_settlement([settlement_id])
    
    time.sleep(1)
    
    # Test 6: Execution Receipt
    results["execution_receipt"] = test_execution_receipt()
    
    # Print Summary
    print_test("Test Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_flag in results.items():
        status = f"{Colors.GREEN}PASSED{Colors.END}" if passed_flag else f"{Colors.RED}FAILED{Colors.END}"
        print(f"  {test_name}: {status}")
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    if passed == total:
        print(f"{Colors.GREEN}✅ All tests passed! ({passed}/{total}){Colors.END}")
    else:
        print(f"{Colors.YELLOW}⚠️  {passed}/{total} tests passed{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    return results

if __name__ == "__main__":
    run_all_tests()
