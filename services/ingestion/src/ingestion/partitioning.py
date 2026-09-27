from ingestion.models import DepthUpdate

def partition_key(update: DepthUpdate) -> str:
    return update.symbol