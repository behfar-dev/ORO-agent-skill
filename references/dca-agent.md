# DCA Agent

Auto-buy gold on a schedule (Dollar Cost Averaging). OpenClaw cron compatible.

## OpenClaw Cron Integration

### Option 1: Isolated Cron Job (Recommended)

```bash
# Daily DCA at 9am - announce to Telegram
openclaw cron add \
  --name "Daily Gold DCA" \
  --cron "0 9 * * *" \
  --tz "UTC" \
  --session isolated \
  --message "Run: python3 /path/to/oro_dca.py --buy 0.1 --status" \
  --announce \
  --channel telegram \
  --to "chat_id"
```

### Option 2: HEARTBEAT.md

Add to `HEARTBEAT.md`:

```
## DCA Check
- Get gold price: python3 /path/to/oro_dca.py --estimate 0.1
- Run DCA: python3 /path/to/oro_dca.py --buy 0.1 --status
```

### Option 3: System Event (Main Session)

```bash
openclaw cron add \
  --name "DCA Morning" \
  --cron "0 8 * * *" \
  --session main \
  --system-event "Run DCA purchase: execute /path/to/oro_dca.py --buy 0.1" \
  --wake now
```

## CLI Usage

```bash
# Set API key
export ORO_API_KEY="your-api-key"

# Get price estimate
python3 oro_dca.py --estimate 0.5

# Execute a DCA buy
python3 oro_dca.py --buy 0.5

# Check DCA status
python3 oro_dca.py --status

# Buy for specific user
python3 oro_dca.py --buy 0.1 --user-id "user-123"

# Use config file
python3 oro_dca.py --buy 0.1 --config config.json
```

## Configuration (config.json)

```json
{
  "slippage": 0.05,
  "history_file": "dca_history.json",
  "max_daily_spend": 100,
  "partner_id": "1"
}
```

## Python API

```python
from oro_gold import OroGoldAgent, OroDCA

agent = OroGoldAgent(api_key)
dca = OroDCA(api_key, {"history_file": "dca.json"})

# Load history
dca.load_history()

# Estimate
est = dca.estimate(0.5)
print(f"Cost: ${est['estimatedUsdcAmount']}")

# Execute
result = dca.execute_buy(0.5, "user-123")

# Stats
stats = dca.get_stats()
print(f"Total: {stats['total_gold']}g, P/L: ${stats['gain_loss']}")
```

## Concepts

- **Slippage**: Buffer for price movement (default 5%)
- **History**: Stored in JSON file for tracking
- **User ID**: Optional - for partner-managed users
