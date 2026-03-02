# DCA Agent

Auto-buy gold on a schedule (Dollar Cost Averiting).

## Concept

The agent buys a fixed gold amount at regular intervals, averaging out price over time.

## Use Cases

- Agent salary savings (agent earns USDC → auto-converts to gold)
- User DCA into gold (set & forget)
- Agent treasury accumulation

## Implementation

### 1. Estimate Cost

```python
def estimate_dca_cost(agent: OroGoldAgent, gold_amount: float) -> dict:
    estimate = agent.estimate_buy(gold_amount)
    return {
        "gold": gold_amount,
        "usdc_cost": estimate["estimatedUsdcAmount"],
        "price_per_oz": estimate["goldPricePerOunce"]
    }
```

### 2. Scheduled Purchase

```python
import schedule
import time

def dca_buy(agent: OroGoldAgent, user_id: str, gold_amount: float):
    # 1. Get estimate
    estimate = agent.estimate_buy(gold_amount)
    max_usdc = estimate["estimatedUsdcAmount"] * 1.05  # 5% slippage
    
    # 2. Create purchase
    resp = requests.post(
        f"{API_BASE}/trading/purchases/user",
        json={
            "userId": user_id,
            "goldAmount": gold_amount,
            "maxUsdcAmount": max_usdc
        },
        headers=agent.headers
    )
    
    # 3. Sign & submit (custodial = partner signs)
    # ... sign with executive authority
    
    return resp.json()

# Schedule daily at 9am
schedule.every().day.at("09:00").do(
    lambda: dca_buy(agent, "user-123", 0.01)
)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 3. Track Performance

```python
def dca_stats(agent: OroGoldAgent, user_id: str, purchases: list) -> dict:
    user = agent.get_user(user_id)
    
    total_gold = sum(p["gold_amount"] for p in purchases)
    total_usdc = sum(p["usdc_spent"] for p in purchases)
    current_value = user["goldBalance"] * agent.get_price()
    
    return {
        "total_gold": total_gold,
        "total_invested": total_usdc,
        "current_value": current_value,
        "gain_loss": current_value - total_usdc,
        "avg_buy_price": total_usdc / total_gold if total_gold > 0 else 0
    }
```

## Configuration

| Parameter | Description |
|----------|-------------|
| `gold_amount` | Grams/oz per purchase |
| `frequency` | daily, weekly, biweekly, monthly |
| `slippage_tolerance` | 1-10% (default 5%) |

## Notes

- Requires `PARTNER_EXECUTIVE_AUTHORITY` scope API key
- For custodial model (partner signs transactions)
- Store purchase history for tracking
- Consider max spend limits to prevent overspending
