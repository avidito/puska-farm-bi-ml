import os
import json
from datetime import datetime
from typing import List
from etl.shared import (
    database,
    kafka,
    log,
    schemas
)
logger = log.create_logger()
QUERY_DIR = os.path.join(os.path.dirname(__file__), "query")
SHARED_DIR = os.path.dirname(os.path.dirname(__file__), "shared", "query")


# Main Sequence
def main(data: dict):
    try:
        start_tm = datetime.now()
        # Validation
        valid_event: schemas.EventFactPopulasi = schemas.validating_event(data, schemas.EventFactPopulasi, logger)
        
        # Processing
        data_tr_1 = database.get_dwh_ids(valid_event.identifier.model_dump(), {
            "tgl_pencatatan": "id_waktu"
        })
        data_tr_2 = database.get_dwh_ids_from_id_peternak(data_tr_1, ("id_unit_ternak", "id_lokasi"), pop=False)
        prep_data = __prepare_data(data_tr_2, valid_event.action, valid_event.amount.model_dump())

        # Update DWH
        for data in prep_data:
            database.run_query(
                query_name = "upsert_fact_populasi_stream",
                query_dir = QUERY_DIR,
                params = data.model_dump()
            )
        
        logger.info("Processed - Status: OK")
        end_tm = datetime.now()
        duration = round((end_tm - start_tm).total_seconds(), 2)
        database.run_query(
            query_name = "logging",
            query_dir = SHARED_DIR,
            params = {
                "payload": json.dumps(prep_data[0].model_dump()),
                "start_tm": start_tm,
                "end_tm": end_tm,
                "duration": duration
            }
        )

    except Exception as err:
        logger.error(str(err))
        logger.info("Processed - Status: FAILED")


# Process
def __prepare_data(data: dict, action: str, amount: dict) -> List[schemas.TableFactPopulasi]:
    fmt_amount = __reformat_amount(amount)

    all_data = []
    for row_amount in fmt_amount:
        flag_delete = action == "DELETE"
        
        prep_data = {
            **data,
            **row_amount,
            "flag_delete": flag_delete
        }
        all_data.append(prep_data)
    return [schemas.TableFactPopulasi(**data) for data in all_data]


def __reformat_amount(data: dict) -> list:
    header = ("jenis_kelamin", "tipe_ternak", "tipe_usia", "jumlah")
    row_data = [
        ("jantan", "pedaging", "dewasa", data["jml_pedaging_jantan"]),
        ("jantan", "pedaging", "anakan", data["jml_pedaging_anakan_jantan"]),
        ("jantan", "perah", "dewasa", data["jml_perah_jantan"]),
        ("jantan", "perah", "anakan", data["jml_perah_anakan_jantan"]),
        ("betina", "pedaging", "dewasa", data["jml_pedaging_betina"]),
        ("betina", "pedaging", "anakan", data["jml_pedaging_anakan_betina"]),
        ("betina", "perah", "dewasa", data["jml_perah_betina"]),
        ("betina", "perah", "anakan", data["jml_perah_anakan_betina"])
    ]
    fmt_amount = [dict(zip(header, row)) for row in row_data]
    return fmt_amount

# Runtime
if __name__ == "__main__":
    kafka.get_stream_source(
        "seq_fact_populasi",
        topic = "populasi",
        host = "kafka:9092",
        process = main,
        logger = logger
    )
