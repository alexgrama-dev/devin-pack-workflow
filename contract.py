import pandera.pandas as pa
from pandera.pandas import Column, DataFrameSchema, Check

spend_schema = DataFrameSchema(
    {
        "date": Column("datetime64[ns]", nullable=False),
        "market": Column(str, Check.isin(["AE", "SA", "EG", "KW", "QA", "OM", "BH"])),
        "placement": Column(str),
        "creative": Column(str, nullable=True),
        "impressions": Column(int, Check.ge(0)),
        "spend": Column(float, Check.ge(0)),
    },
    checks=[
        Check(lambda df: not df.duplicated(["date", "market", "placement", "creative"]).any(),
              name="one_row_per_key"),
    ],
    strict=True,
    coerce=True,
)

def assert_reconciled(df, source_total: float, market: str, tol: float = 0.001) -> None:
    got = float(df.loc[df["market"] == market, "spend"].sum())
    if source_total and abs(got - source_total) / source_total > tol:
        raise ValueError(f"{market}: spend {got:.2f} vs source {source_total:.2f} outside {tol:.3%}")
