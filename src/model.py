import ydb


class Model:
    def __init__(self, endpoint: str, database: str, service_account_key: str):

        credentials = ydb.iam.ServiceAccountCredentials.from_file(
            service_account_key)
        self.driver = ydb.Driver(
            endpoint=endpoint,
            database=database,
            credentials=credentials
        )
        self.driver.wait(timeout=5, fail_fast=True)

    def get_next_number(self) -> int:
        session = self._get_session()
        tx = session.transaction().begin()
        tx.execute("UPDATE number SET number = number + 1;")
        result_sets = tx.execute("SELECT * FROM number;")
        tx.commit()
        for row in result_sets[0].rows:
            return row["number"]

    def set_number(self, number: int):
        session = self._get_session()
        session.transaction().execute(
            f"UPDATE number SET number = {number};", commit_tx=True)

    def _get_session(self):
        return self.driver.table_client.session().create()
