# 04 – Ingestion metrics (5 symbols)

Measured over ~8 min, 47 windows of 10s.

- Messages: ~5.0 msg/s (stable, ~1/s per symbol)
- Bandwidth: 12–40 KB/s (varies with market activity)
- Volume: 1.07–3.59 GB/day, median ~2.2 GB/day
- Planning figure: ~2.5 GB/day → ~75 GB/month uncompressed

## VPS sizing
- Kafka compresses these JSON messages ~4-5x → ~15-19 GB/month on disk
- CX22 (4€, 40GB) is enough with compression + 2-4 week raw retention
- Without compression, would need CX32 (7€, 80GB)