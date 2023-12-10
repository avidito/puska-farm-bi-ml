docker compose exec kafka kafka-topics --create --topic produksi --bootstrap-server kafka:9092
docker compose exec kafka kafka-topics --create --topic distribusi --bootstrap-server kafka:9092
docker compose exec kafka kafka-topics --create --topic populasi --bootstrap-server kafka:9092
docker compose exec kafka kafka-topics --list --bootstrap-server kafka:9092
