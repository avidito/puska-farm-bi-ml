# Puska - Farm BI ML

## Overview
Puska - Farm Business Intelligence and Machine Learning Streaming Services.

## Services

**Release: 1.0.5**

|No|Name|Type|Description|Image|Version|
|--:|:--|---|:--|:--|:--|
|1|db-ops|Database|Opearational database (application data)|avidito/postgres-db|15.3-puska-ops-1.1|
|2|db-dwh|Database|Data warehouse for BI and report|avidito/postgres-db|15.3-puska-dwh-1.2|
|3|zookeeper|Manager|Cluster manager for Kafka|confluentinc/cp-zookeeper|7.5.0|
|4|kafka|Broker|Message broker for streaming data|confluentinc/cp-kafka|7.5.0|
|5|etl-batch|ETL|Batch data processing|avidito/beam-python|2.52.0-puska-batch-1.1|
|6|etl-batch|ETL|Batch data processing|avidito/kafka-stream-py|2.0.2-puska-etl-1.0|



## Documentation
1. [[PUSKA] DWH Data Design](https://docs.google.com/spreadsheets/d/12Nq72e2ZdoOw-1hXScFLmsxC-tbKiqZZFKqdH_941gE)