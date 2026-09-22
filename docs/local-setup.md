# The topic
rpk topic create orderbook.raw -p 6 -r 1 -X brokers=localhost:9092

# Pro (el símbolo hace de key)
rpk topic produce orderbook.raw -k BTCUSDT -X brokers=localhost:9092
# escribe: primer mensaje de BTC   (Enter, luego Ctrl+D)
rpk topic produce orderbook.raw -k BTCUSDT -X brokers=localhost:9092
# escribe: segundo mensaje de BTC   (Enter, Ctrl+D)
rpk topic produce orderbook.raw -k ETHUSDT -X brokers=localhost:9092
# escribe: mensaje de ETH   (Enter, Ctrl+D)

# Consumir mostrando en qué partición cayó cada uno
rpk topic consume orderbook.raw -o start -X brokers=localhost:9092 -f '%p key=%k value=%v\n'