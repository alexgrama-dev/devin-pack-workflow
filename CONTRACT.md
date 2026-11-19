# Pack contract (v1)

Every market pack obeys this contract. CI fails if it does not.

## Inputs
- `fixtures/<pack>/source.{csv,xlsx}` from the day's DataRepo/Uni-KPI export
- `schema.yaml` pinning column names, dtypes and market code

## Invariants
1. Row count within 0.5% of the source count.
2. `sum(spend)` within 0.1% of the source total, per market.
3. One row per (date, market, placement, creative).
4. No null in date, market, spend.
5. Manifest hash identical on re-run (idempotent).

## Exit codes
- 0 pass
- 2 contract violation
- 3 stale fixture / doctor check failed
