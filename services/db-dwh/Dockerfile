FROM postgres:15.3

COPY ddl/ /ddl
COPY seed/ /seed
COPY init.sh /docker-entrypoint-initdb.d/
