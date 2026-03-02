#!/usr/bin/env python3
"""
ORO DCA Agent - Compatible with OpenClaw Cronjobs

Usage with OpenClaw cron:
1. Add to HEARTBEAT.md for periodic checks
2. Or use openclaw cron to schedule isolated jobs

Examples:
  openclaw cron add --name "DCA Buy" --cron "0 9 * * *" --session isolated \
    --message "Run DCA purchase: python3 /path/to/oro_dca.py --buy 0.1" \
    --announce --channel telegram --to "chat_id"
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime
from typing import Optional

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oro_gold import OroGoldAgent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OroDCA:
    """Dollar Cost Averaging Agent for gold - OpenClaw compatible"""
    
    def __init__(self, api_key: str, config: dict = None):
        self.agent = OroGoldAgent(api_key)
        self.config = config or {}
        self.purchase_history = []
        self.history_file = self.config.get("history_file", "dca_history.json")
    
    def load_history(self):
        """Load purchase history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file) as f:
                    self.purchase_history = json.load(f)
                logger.info(f"Loaded {len(self.purchase_history)} past purchases")
            except Exception as e:
                logger.warning(f"Could not load history: {e}")
                self.purchase_history = []
    
    def save_history(self):
        """Save purchase history to file"""
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.purchase_history, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
    
    def get_price(self) -> Optional[float]:
        """Get current gold price"""
        return self.agent.get_price()
    
    def estimate(self, gold_amount: float) -> Optional[dict]:
        """Get cost estimate for gold amount"""
        return self.agent.estimate_buy(gold_amount)
    
    def execute_buy(self, gold_amount: float, user_id: str = None) -> dict:
        """
        Execute a DCA purchase.
        
        Note: Actual on-chain purchase requires:
        1. Partner account with funds in vault
        2. User created in system
        3. Wallet signing (custodial = partner signs)
        
        This simulates the purchase for demo/development.
        """
        # Get estimate
        estimate = self.agent.estimate_buy(gold_amount)
        if not estimate:
            return {"success": False, "error": "Failed to get estimate"}
        
        # Calculate with slippage
        slippage = self.config.get("slippage", 0.05)
        max_usdc = estimate["estimatedUsdcAmount"] * (1 + slippage)
        
        purchase = {
            "timestamp": datetime.utcnow().isoformat(),
            "gold_amount": gold_amount,
            "usdc_estimate": estimate["estimatedUsdcAmount"],
            "max_usdc": max_usdc,
            "price_per_oz": estimate["goldPricePerOunce"],
            "user_id": user_id,
            "status": "pending_signature"  # Would be completed after on-chain
        }
        
        self.purchase_history.append(purchase)
        self.save_history()
        
        return {
            "success": True,
            "purchase": purchase,
            "message": f"✅ DCA Purchase prepared: {gold_amount}g gold (~${estimate['estimatedUsdcAmount']:.2f} USDC)"
        }
    
    def get_stats(self) -> dict:
        """Get DCA performance stats"""
        total_gold = sum(p["gold_amount"] for p in self.purchase_history)
        total_usdc = sum(p["usdc_estimate"] for p in self.purchase_history)
        
        current_price = self.get_price()
        current_value = 0
        gain_loss = 0
        
        if current_price and total_gold > 0:
            current_value = total_gold * (current_price / 31.1035)  # oz to grams
            gain_loss = current_value - total_usdc
        
        return {
            "total_purchases": len(self.purchase_history),
            "total_gold": round(total_gold, 4),
            "total_invested": round(total_usdc, 2),
            "current_price_per_oz": current_price,
            "current_value": round(current_value, 2),
            "gain_loss": round(gain_loss, 2),
            "avg_buy_price": round(total_usdc / total_gold, 2) if total_gold > 0 else 0
        }
    
    def format_status(self) -> str:
        """Format status as readable message for cron announce"""
        stats = self.get_stats()
        
        msg = "📊 **DCA Status**\n\n"
        msg += f"�Purchases: {stats['total_purchases']}\n"
        msg += f"💰 Total Gold: {stats['total_gold']}g\n"
        msg += f"💵 Total Invested: ${stats['total_invested']}\n"
        
        if stats['current_price_per_oz']:
            msg += f"📈 Current Price: ${stats['current_price_per_oz']}/oz\n"
            msg += f"💎 Current Value: ${stats['current_value']}\n"
            msg += f"📊 P/L: ${stats['gain_loss']}"
            
            if stats['gain_loss'] > 0:
                msg += " ✅"
            elif stats['gain_loss'] < 0:
                msg += " 🔻"
        
        return msg


def main():
    parser = argparse.ArgumentParser(description="ORO DCA Agent for OpenClaw")
    parser.add_argument("--api-key", "-k", help="ORO API key (or set ORO_API_KEY env)")
    parser.add_argument("--buy", type=float, help="Amount in grams to buy")
    parser.add_argument("--user-id", "-u", help="User ID for purchase")
    parser.add_argument("--estimate", "-e", type=float, help="Get estimate for amount")
    parser.add_argument("--status", "-s", action="store_true", help="Show DCA status")
    parser.add_argument("--config", "-c", help="Config JSON file")
    parser.add_argument("--history", default="dca_history.json", help="History file path")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.environ.get("ORO_API_KEY")
    if not api_key:
        print("Error: Provide --api-key or set ORO_API_KEY")
        sys.exit(1)
    
    # Load config
    config = {"history_file": args.history}
    if args.config and os.path.exists(args.config):
        with open(args.config) as f:
            config.update(json.load(f))
    
    # Initialize DCA
    dca = OroDCA(api_key, config)
    dca.load_history()
    
    # Execute command
    if args.buy:
        result = dca.execute_buy(args.buy, args.user_id)
        if result.get("success"):
            print(result["message"])
        else:
            print(f"❌ Error: {result.get('error')}")
            sys.exit(1)
    
    elif args.estimate:
        est = dca.estimate(args.estimate)
        if est:
            print(f"💰 {args.estimate}g gold = ~${est['estimatedUsdcAmount']:.2f} USDC")
            print(f"   (Price: ${est['goldPricePerOunce']}/oz)")
        else:
            print("❌ Failed to get estimate")
            sys.exit(1)
    
    elif args.status:
        print(dca.format_status())
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
