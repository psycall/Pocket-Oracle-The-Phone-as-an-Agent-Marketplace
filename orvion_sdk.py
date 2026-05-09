
import requests
import logging

class OrvionAgentSDK:
    """
    Simple SDK for AI Agents to interact with the ORVION Settlement Layer.
    """
    def __init__(self, base_url="http://localhost:8000", api_token=None):
        self.base_url = base_url
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}" if api_token else "",
            "Content-Type": "application/json"
        }
        self.api_v1 = f"{base_url}/api/v1"

    def register_agent(self, agent_data):
        """Register the agent in the Orvion Discovery Registry."""
        url = f"{self.api_v1}/discovery/agents"
        response = requests.post(url, json=agent_data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_job_and_escrow(self, agent_id, job_id, amount, to_address):
        """Initiate a job and escrow funds in USDC."""
        url = f"{self.api_v1}/settlement/settlements"
        data = {
            "agent_id": agent_id,
            "job_id": job_id,
            "amount": amount,
            "to_address": to_address
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def submit_proof_of_work(self, job_id, proof_hash):
        """Submit execution receipt to trigger verification and payment release."""
        url = f"{self.api_v1}/settlement/execution-receipts"
        data = {
            "job_id": job_id,
            "proof": proof_hash
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_status(self, settlement_id):
        """Check the status of a settlement."""
        url = f"{self.api_v1}/settlement/settlements/{settlement_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
