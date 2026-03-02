#!/usr/bin/env python3
"""
ORO DCA Agent - Automated gold buying on schedule
"""

import os
import time
import json
import logging
import schedule
from datetime import datetime
from typing import Optional
from threading import Thread

from oro_gold import OroGoldAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OroDCA:
    """Dollar Cost Averaging Agent for gold"""
    
    def __init__(self, api_key: str, config: dict):
        self.agent = OroGoldAgent(api_key)
        self.config = config
        self.purchase_history = []
        self.running = False
    
    def get_estimate(self, gold_amount: float) -> Optional[dict]:
        """Get USDC cost estimate"""
        return self.agent.estimate_buy(gold_amount)
    
    def execute_buy(self, gold_amount: float) -> Optional[dict]:
        """Execute a gold purchase"""
        estimate = self.get_estimate(gold_amount)
        if not estimate:
            logger.error("Failed to get estimate")
            return None
        
        # Add 5% slippage buffer
        max_usdc = estimate["estimatedUsdcAmount"] * (1 + self.config.get("slippage", 0.05))
        
        logger.info(f"Buying {gold_amount}g gold at ~${estimate['goldPricePerOunce']}/oz")
        
        # For now, just log - actual purchase needs partner setup
        purchase = {
            "timestamp": datetime.utcnow().isoformat(),
            "gold_amount": gold_amount,
            "usdc_estimate": estimate["estimatedUsdcAmount"],
            "max_usdc": max_usdc,
            "price_per_oz": estimate["goldPricePerOunce"]
        }
        
        self.purchase_history.append(purchase)
        self._save_history()
        
        logger.info(f"Purchase recorded: {purchase}")
        return purchase
    
    def run_once(self, gold_amount: float):
        """Run a single DCA purchase"""
        return self.execute_buy(gold_amount)
    
    def start(self):
        """Start scheduled DCA purchases"""
        self.running = True
        gold_amount = self.config["gold_amount"]
        frequency = self.config.get("frequency", "daily")
        
        if frequency == "daily":
            time_str = self.config.get("time", "09:00")
            schedule.every().day.at(time_str).do(self.execute_buy, gold_amount=gold_amount)
        elif frequency == "weekly":
            day = self.config.get("day", "monday")
            getattr(schedule.every(), day).do(self.execute_buy, gold_amount=gold_amount)
        elif frequency == "hourly":
            schedule.every(self.config.get("hours", 1)).hours.do(self.execute_buy, gold_amount=gold_amount)
        
        logger.info(f"DCA started: {frequency} buys of {gold_amount}g")
        
        while self.running:
            schedule.run_pending()
            time.sleep(60)
    
    def stop(self):
        """Stop DCA"""
        self.running = False
        schedule.clear()
    
    def get_stats(self) -> dict:
        """Get DCA performance stats"""
        total_gold = sum(p["gold_amount"] for p in self.purchase_history)
        total_usdc = sum(p["usdc_estimate"] for p in self.purchase_history)
        
        current_price = self.agent.get_price()
        current_value = 0
        if current_price and total_gold > 0:
            current_value = total_gold * current_price
        
        return {
            "total_purchases": len(self.purchase_history),
            "total_gold": total_gold,
            "total_invested": total_usdc,
            "current_price": current_price,
            "current_value": current_value,
            "gain_loss": current_value - total_usdc,
            "avg_price": total_usdc / total_gold if total_gold > 0 else 0
        }
    
    def _save_history(self):
        """Save purchase history to file"""
        path = self.config.get("history_file", "dca_history.json")
        with open(path, "w") as f:
            json.dump(self.purchase_history, f, indent=2)
    
    def load_history(self):
        """Load purchase history"""
        path = self.config.get("history_file", "dca_history.json")
        if os.path.exists(path):
            with open(path) as f:
                self.purchase_history = json.load(f)


# Example usage
if __name__ == "__main__":
    api_key = os.environ.get("ORO_API_KEY")
    if not api_key:
        print("Error: Set ORO_API_KEY")
        exit(1)
    
    config = {
        "gold_amount": 0.1,      # grams per purchase
        "frequency": "daily",   # daily, weekly, hourly
        "time": "09:00",        # for daily
        "slippage": 0.05,       # 5%
    }
    
    dca = OroDCA(api_key, config)
    dca.load_history()
    
    # Test estimate
    estimate = dca.get_estimate(config["gold_amount"])
    if estimate:
        print(f"Current gold price: ${estimate['goldPricePerOunce']}/oz")
        print(f"Estimated cost for {config['gold_amount']}g: ${estimate['estimatedUsdcAmount']:.2f}")
    
    # Or run once
    # dca.run_once(config["gold_amount"])
    
    # Or start scheduler
    # dca.start()
