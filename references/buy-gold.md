# Buy Gold

Purchase gold for a user or partner treasury.

## Flow

1. **Estimate** - Get USDC cost for desired gold amount
2. **Create** - Generate purchase transaction
3. **Sign** - Sign with wallet(s)
4. **Submit** - Send to blockchain

## Step 1: Get Estimate

```
POST /trading/estimate/buy
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

## Step 2: Create Purchase

### For User (Custodial)

```
POST /trading/purchases/user
```

```json
{
  "userId": "user-123",
  "goldAmount": 0.5,
  "maxUsdcAmount": 2700
}
```

### For Partner Treasury

```
POST /trading/purchases/partner
```

```json
{
  "goldAmount": 1.0,
  "maxUsdcAmount": 5500
}
```

## Step 3: Sign Transaction

### Custodial (Partner signs only)

```typescript
import { Keypair, Transaction, Connection } from "@solana/web3.js";

const tx = Transaction.from(Buffer.from(serializedTx, 'base64'));
const authority = Keypair.fromSecretKey(/* bytes */);
const sig = await connection.sendTransaction(tx, [authority]);
```

### Self-Custody (User + Authority sign)

```typescript
import { Keypair, VersionedTransaction } from "@solana/web3.js";

const tx = VersionedTransaction.deserialize(Buffer.from(serializedTx, 'base64'));
tx.sign([userKeypair, executiveAuthority]);
```

## Step 4: Submit

```
POST /transactions/submit
```

```json
{ "serializedTransaction": "base64-signed-tx" }
```

## Slippage Protection

Always set `maxUsdcAmount` higher than estimate:

```
maxUsdcAmount = estimatedUsdcAmount * 1.05  // 5% buffer
```

## Create User First

If user doesn't exist:

```
POST /users
```

```json
{
  "walletAddress": "SolanaWalletAddress",
  "email": "user@example.com",
  "kycReference": "external-kyc-id"
}
```
