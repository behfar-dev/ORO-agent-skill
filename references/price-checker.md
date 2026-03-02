# Price Checker

Fetch current gold price from ORO API.

## Endpoint

```
GET /trading/gold-price
```

## cURL

```bash
curl -X GET https://oro-tradebook-devnet.up.railway.app/api/trading/gold-price \
  -H "x-api-key: YOUR-API-KEY"
```

## Response

```json
{
  "success": true,
  "data": {
    "goldPricePerOunce": 5086.2,
    "currency": "USDC",
    "timestamp": "2024-01-15T10:30:00.000Z"
  }
}
```

## JavaScript/TypeScript

```typescript
async function getGoldPrice(apiKey: string) {
  const res = await fetch(
    'https://oro-tradebook-devnet.up.railway.app/api/trading/gold-price',
    { headers: { 'x-api-key': apiKey } }
  );
  const json = await res.json();
  return json.data.goldPricePerOunce;
}
```

## Python

```python
import requests

def get_gold_price(api_key: str) -> float:
    resp = requests.get(
        'https://oro-tradebook-devnet.up.railway.app/api/trading/gold-price',
        headers={'x-api-key': api_key}
    )
    return resp.json()['data']['goldPricePerOunce']
```

## Notes

- Price comes from Pyth oracle
- Denominated in USDC
- Updates in real-time
