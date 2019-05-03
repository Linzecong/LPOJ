FROM mysql:latest
MAINTAINER linzecong
ENV AUTO_RUN_DIR /docker-entrypoint-initdb.d
ENV INSTALL_DB_SQL init_database.sql
COPY ./$INSTALL_DB_SQL $AUTO_RUN_DIR/
EXPOSE 3306 33060
RUN chmod a+x $AUTO_RUN_DIR/$INSTALL_DB_SQL