# Bug report exercise

The order summary endpoint returns an incorrect total when an item quantity is greater than one.

## Reproduction

```text
GET /orders/demo-100
Expected total: 28.00
Observed total: 15.50
```

## Investigation questions

1. Which input and calculation path produce the mismatch?
2. What regression test should be added before changing the implementation?
3. Does the fix preserve the response contract and rounding behavior?
4. What other boundary cases should be tested?

