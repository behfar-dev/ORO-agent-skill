# Sell Gold

Convert gold back to USDC.

## Flow

1. **Estimate** - Get USDC received for gold amount
2. **Create** - Generate sell transaction
3. **Sign** - Sign with wallet(s)
4. **Submit** - Send to blockchain

## Step 1: Get Estimate

```
POST /trading/estimate/sell
```

```json
{ "goldAmount": 0.5 }
```

Response:
```json
{
  "success": true,
  "data": {
    "goldAmount": 0.5,
    "estimatedUsdcAmount": 2543.10,
    "goldPricePerOunce": 5086.2
  }
}
```

## Step 2: Create Sell Transaction

### For User

```
POST /trading/sales/user
```

```json
{
  "userId": "user-123",
  "goldAmount": 0.5,
  "minUsdcAmount": 2400
}
```

### For Partner Treasury

```
POST /trading/sales/partner
```

```json
{
  "goldAmount": 1.0,
  "minUsdcAmount": 4800
}
```

## Step 3 & 4: Sign + Submit

Same as buy flow. See buy-gold.md.

## Withdrawal (Get USDC Out)

After selling, withdraw USDC from vault:

```
POST /trading/withdraw
```

```json
{
  "amount": 1000,
  "destination": "WalletAddress"
}
```

Requires `PARTNER_WITHDRAWAL_AUTHORITY` scope.
