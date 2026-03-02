# ORO Gold Agent Skill

Agent skill for integrating with ORO GRAIL gold infrastructure on Solana.

## What is this?

A reusable skill that lets AI agents work with gold (GRAIL) - check prices, manage balances, buy/sell gold via REST API.

## Quick Start

```python
from oro_gold.scripts.oro_gold import OroGoldAgent

agent = OroGoldAgent("your-api-key")
price = agent.get_price()
print(f"Gold: ${price}/oz")
```

## Features

- **Price Checker** - Get current gold price from Pyth oracle
- **Balance Checker** - Query user gold/USDC balances
- **Buy Gold** - Purchase gold for users or partner treasury
- **Sell Gold** - Convert gold to USDC

## Documentation

- [SKILL.md](SKILL.md) - Main skill reference
- [references/price-checker.md](references/price-checker.md)
- [references/balance-checker.md](references/balance-checker.md)
- [references/buy-gold.md](references/buy-gold.md)
- [references/sell-gold.md](references/sell-gold.md)

## API

Based on [Oro GRAIL API](https://docs.grail.oro.finance/).

## License

MIT
