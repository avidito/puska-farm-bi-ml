import os
from etl.shared import (
    database,
    kafka,
    log,
    schemas
)
logger = log.create_logger()
QUERY_DIR = os.path.join(os.path.dirname(__file__), "query")


# Main Sequence
def main(data: dict):
    try:
        # Validation
        valid_event: schemas.EventFactProduksi = schemas.validating_event(data, schemas.EventFactProduksi, logger)
        
        # Processing
        data_tr_1 = database.get_dwh_ids(valid_event.identifier.model_dump(), {
            "tgl_produksi": "id_waktu",
            "sumber_pasokan": "id_sumber_pasokan"
        })
        data_tr_2 = database.get_dwh_id_lokasi_from_ut(data_tr_1)
        prep_data = __prepare_data(data_tr_2, valid_event.action, valid_event.amount.model_dump())

        # Update DWH
        __update_dwh(prep_data)
        
        logger.info("Processed - Status: OK")
    except Exception as err:
        logger.error(str(err))
        logger.info("Processed - Status: FAILED")


# Process
def __prepare_data(data: dict, action: str, amount: dict) -> schemas.TableFactProduksi:
    if (action == "CREATE"):
        jumlah_produksi = amount["jumlah"]
    elif (action == "DELETE"):
        jumlah_produksi = amount["jumlah"] * (-1)
    elif (action == "UPDATE"):
        jumlah_produksi = amount["jumlah"] - amount["prev_jumlah"]
    
    prep_data = {
        **data,
        "jumlah_produksi": jumlah_produksi
    }
    return schemas.TableFactProduksi(**prep_data)


# DWH Process
def __update_dwh(inp_data: schemas.TableFactProduksi):
    # Get Existing Data
    ext_data_result = database.run_query(
        query_name = "get_fact_produksi_stream",
        query_dir = QUERY_DIR,
        params = {
            "id_waktu": inp_data.id_waktu,
            "id_lokasi": inp_data.id_lokasi,
            "id_unit_ternak": inp_data.id_unit_ternak,
            "id_jenis_produk": inp_data.id_jenis_produk,
            "id_sumber_pasokan": inp_data.id_sumber_pasokan
        }
    )

    # Update Input Body
    if (ext_data_result):
        ext_data = schemas.TableFactProduksi(**ext_data_result[0])
        inp_data.jumlah_produksi = ext_data.jumlah_produksi + inp_data.jumlah_produksi
    
    # Update DWH
    database.run_query(
        query_name = "upsert_fact_produksi_stream",
        query_dir = QUERY_DIR,
        params = inp_data.model_dump()
    )


# Runtime
if __name__ == "__main__":
    kafka.get_stream_source(
        "seq_fact_produksi",
        topic = "produksi",
        host = "localhost:29200",
        process = main,
        logger = logger
    )