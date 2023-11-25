import os
import pendulum
from datetime import datetime
import apache_beam as beam
from beam_nuggets.io import relational_db

from etl.shared import connection, database, log, models

# Logging
sequence_logger = log.create_logger()


# Main Sequence
@log.time_it_seq("Batch - Sequence dim_lokasi", sequence_logger)
def main():
    # Variables
    TZINFO = pendulum.timezone("Asia/Jakarta")
    QUERY_DIR = os.path.join(os.path.dirname(__file__), "query")

    # ETL
    with beam.Pipeline() as pipeline:
        (
            pipeline
            | "Read DB - wilayah" >> relational_db.ReadFromDB(
                source_config = connection.get_connection("ops-db"),
                table_name = "wilayah",
                query = database.get_query(QUERY_DIR, "wilayah")
            )
            | "Enrich System Data" >> beam.Map(database.enrich_system_data(datetime.now(TZINFO)))
            | "Load Data - dim_lokasi" >> relational_db.Write(
                source_config = connection.get_connection("dwh-db"),
                table_config = relational_db.TableConfiguration(
                    name = "dim_lokasi",
                    create_if_missing = True,
                    define_table_f = models.DimLokasi,
                    create_insert_f = database.update_insert
                )
            )
        )


if __name__ == "__main__":
    main()