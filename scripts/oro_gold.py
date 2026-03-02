#!/usr/bin/env python3
"""
ORO Gold Agent - Simple CLI for gold operations
"""

import os
import sys
import json
import requests
from typing import Optional

API_BASE = "https://oro-tradebook-devnet.up.railway.app/api"

class OroGoldAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"x-api-key": api_key}
    
    def get_price(self) -> Optional[float]:
        """Fetch current gold price"""
        resp = requests.get(f"{API_BASE}/trading/gold-price", headers=self.headers)
        if resp.ok:
            return resp.json()["data"]["goldPricePerOunce"]
        print(f"Error: {resp.text}")
        return None
    
    def get_user(self, user_id: str) -> Optional[dict]:
        """Get user details and balance"""
        resp = requests.get(f"{API_BASE}/users/{user_id}", headers=self.headers)
        if resp.ok:
            return resp.json()["data"]
        print(f"Error: {resp.text}")
        return None
    
    def list_users(self, page: int = 1, limit: int = 10) -> Optional[list]:
        """List all users"""
        resp = requests.get(f"{API_BASE}/users?page={page}&limit={limit}", headers=self.headers)
        if resp.ok:
            return resp.json()["data"]
        print(f"Error: {resp.text}")
        return None
    
    def estimate_buy(self, gold_amount: float) -> Optional[dict]:
        """Estimate USDC cost for gold"""
        resp = requests.post(
            f"{API_BASE}/trading/estimate/buy",
            json={"goldAmount": gold_amount},
            headers=self.headers
        )
        if resp.ok:
            return resp.json()["data"]
        print(f"Error: {resp.text}")
        return None
    
    def get_partner(self) -> Optional[dict]:
        """Get partner details"""
        resp = requests.get(f"{API_BASE}/distribution/partner/me", headers=self.headers)
        if resp.ok:
            return resp.json()["data"]
        print(f"Error: {resp.text}")
        return None


def main():
    api_key = os.environ.get("ORO_API_KEY")
    if not api_key:
        print("Error: Set ORO_API_KEY env variable")
        sys.exit(1)
    
    agent = OroGoldAgent(api_key)
    
    # Example: Get gold price
    price = agent.get_price()
    if price:
        print(f"🪙 Gold price: ${price:.2f}/oz")


if __name__ == "__main__":
    main()
