from twisted.enterprise.adbapi import ConnectionPool
from MySQLdb.cursors import DictCursor
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor


def get_db() -> ConnectionPool:
    settings = get_project_settings()
    return ConnectionPool(
            "MySQLdb",
            host=settings.get("DB_HOST"),
            port=settings.get("DB_PORT"),
            user=settings.get("DB_USERNAME"),
            passwd=str(settings.get("DB_PASSWORD")),
            db=settings.get("DB_DATABASE"),
            cursorclass=DictCursor,
            charset="utf8mb4",
            cp_reconnect=True,
        )

if __name__ == '__main__':
    """
    Unfortunately it won't run, so you need to move rmq/utils/sql_expressions.py to database folder and import it from there
    """
    from rmq.utils.sql_expressions import compile_expression
    from sqlalchemy import select, func

    def get_version():
        version_query = select([func.version()])
        return get_db().runQuery(*compile_expression(version_query))

    def printResult(l):
        print(l)

    get_version().addCallback(printResult)
    reactor.run()