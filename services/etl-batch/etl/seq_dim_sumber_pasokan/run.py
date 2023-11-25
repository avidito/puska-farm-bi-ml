import os
import pendulum
from datetime import datetime
import apache_beam as beam
from beam_nuggets.io import relational_db

from etl.shared import connection, database, log, models

# Logging
sequence_logger = log.create_logger()


# Main Sequence
@log.time_it_seq("Batch - Sequence dim_sumber_pasokan", sequence_logger)
def main():
    # Variables
    TZINFO = pendulum.timezone("Asia/Jakarta")
    QUERY_DIR = os.path.join(os.path.dirname(__file__), "query")

    # ETL
    with beam.Pipeline() as pipeline:
        (
            pipeline
            | "Read DB - produksi_susu" >> relational_db.ReadFromDB(
                source_config = connection.get_connection("ops-db"),
                table_name = "produksi_susu",
                query = database.get_query(QUERY_DIR, "produksi_susu")
            )
            | "Enrich System Data" >> beam.Map(database.enrich_system_data(datetime.now(TZINFO)))
            | "Load Data - dim_sumber_pasokan" >> relational_db.Write(
                source_config = connection.get_connection("dwh-db"),
                table_config = relational_db.TableConfiguration(
                    name = "dim_sumber_pasokan",
                    create_if_missing = True,
                    define_table_f = models.DimSumberPasokan,
                    create_insert_f = database.update_insert
                )
            )
        )


if __name__ == "__main__":
    main()