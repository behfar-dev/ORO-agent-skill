# Balance Checker

Check a user's gold balance.

## Prerequisites

User must already exist. Create users via `POST /users` (see buy-gold.md).

## Endpoint

```
GET /users/{userId}
```

## cURL

```bash
curl -X GET https://oro-tradebook-devnet.up.railway.app/api/users/USER-ID \
  -H "x-api-key: YOUR-API-KEY"
```

## Response

```json
{
  "success": true,
  "data": {
    "userId": "user-123",
    "goldBalance": 2.5,
    "usdcBalance": 100.0,
    "walletAddress": "...",
    "kycStatus": "verified",
    "createdAt": "2024-01-10T..."
  }
}
```

## JavaScript/TypeScript

```typescript
async function getUserBalance(apiKey: string, userId: string) {
  const res = await fetch(
    `https://oro-tradebook-devnet.up.railway.app/api/users/${userId}`,
    { headers: { 'x-api-key': apiKey } }
  );
  const json = await res.json();
  return {
    gold: json.data.goldBalance,
    usdc: json.data.usdcBalance
  };
}
```

## List All Users

```
GET /users?page=1&limit=10
```

Returns paginated list of users with balances.
