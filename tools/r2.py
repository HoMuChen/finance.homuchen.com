"""唯讀連線 fire-auto 的台股 R2 資料湖（DuckDB catalog）。

用法：uv run -q --with duckdb python tools/r2.py "SELECT * FROM tw.market.taiex ORDER BY date DESC LIMIT 5"
      或在程式裡 `from r2 import connect; con = connect()`

金鑰從環境變數或 .env.local 讀：優先 R2_READ_*，沒有就用 R2_WRITE_*。一律 READ_ONLY 掛載，只做查詢。
FinMind 資料僅限個人使用：查出來的原始數字不要寫進這個公開 repo，只寫結論或統計量。
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = "r2://trading-homuchen-com/v1/catalog.duckdb"


def _env():
    vals = {}
    env = ROOT / ".env.local"
    if env.exists():
        for line in env.read_text().splitlines():
            k, _, v = line.partition("=")
            if k.strip().startswith("R2_"):
                vals[k.strip()] = v.strip().strip('"\'')
    vals.update({k: v for k, v in os.environ.items() if k.startswith("R2_")})
    get = lambda name: vals.get(f"R2_READ_{name}") or vals.get(f"R2_WRITE_{name}")
    if not (vals.get("R2_ACCOUNT_ID") and get("ACCESS_KEY_ID") and get("SECRET_ACCESS_KEY")):
        raise RuntimeError("找不到 R2_ACCOUNT_ID／R2_*_ACCESS_KEY_ID／R2_*_SECRET_ACCESS_KEY（環境變數或 .env.local）")
    return vals["R2_ACCOUNT_ID"], get("ACCESS_KEY_ID"), get("SECRET_ACCESS_KEY")


def connect():
    import duckdb
    account, key, secret = _env()
    con = duckdb.connect()
    con.sql(f"CREATE SECRET (TYPE r2, KEY_ID '{key}', SECRET '{secret}', ACCOUNT_ID '{account}')")
    con.sql(f"ATTACH '{CATALOG}' AS tw (READ_ONLY)")
    return con


if __name__ == "__main__":
    con = connect()
    queries = sys.argv[1:] or ["SELECT schema_name, view_name, comment FROM duckdb_views() "
                               "WHERE database_name = 'tw' ORDER BY 1, 2"]
    for q in queries:
        con.sql(q).show(max_rows=60, max_width=250)
