"""
Handles the interaction with neo4j.
- Holds the credentials
- Executed the given queries
"""
from neo4j import GraphDatabase


class Neo4jHandler():
    """Handles the interaction with neo4j.
        - Holds the credentials
        - Executed the given queries
    """

    def __init__(self, host=None, user=None, password=None):
        """_summary_

        Args:
            host (str, optional): The host url where neo4j database is hosted. Defaults to None. e.g, 'bolt://localhost:11003'
            user (str, optional): The username in the database. Defaults to None.
            password (str, optional): Defaults to None.
        """
        self.host = host
        self.user = user
        self.password = password
        return

    def query(self, query, params=None, password=None, user=None, host=None):
        """Executes the given query in the neo4j database.

        Args:
            query (str): _description_
            params (str, optional): Parameters for the query. Defaults to None.
            password (str, optional): Defaults to stored password.
            user (str, optional): Defaults to stored user.
            host (str, optional): Defaults to stored host.

        Returns:
            list: list of records of the result.
        """
        host = self.host if host is None else host
        user = self.user if user is None else user
        password = self.password if password is None else password
        driver = GraphDatabase.driver(host, auth=(user, password))
        with driver.session() as session:
            result = session.run(query, params)
            return [record.data() for record in result]

    def set_credentials(self, host, user, password=None):
        self.host = host
        self.user = user
        self.password = password
        return

    def get_credentials(self):
        return self.host, self.user, self.password

    def validate_credentials(self, password=None):
        password = self.password if password is None else password
        try:
            driver = GraphDatabase.driver(
                self.host, auth=(self.user, password))
            return True
        except Exception as e:
            return False

    def get_schema(self, password=None):
        """Assumes the neo4j database has APOC plugin installed.

        Args:
            password (str, optional): Defaults to stored password.

        Returns:
            Schema: Result of 'CALL apoc.meta.schema()'
        """
        password = self.password if password is None else password
        query = 'CALL apoc.meta.schema()'
        result = self.query(query=query, password=password)
        return result[0]['value']

    def get_processed_schema(self, password=None):
        schema = self.get_schema(password=password)
        filteredSchema = {}
        for idx in schema:
            entity = schema[idx]
            fEntity = {}
            fEntity['type'] = entity['type']
            fEntity['properties'] = entity['properties']
            filteredSchema[idx] = fEntity
        return filteredSchema

if __name__ == '__main__':
    host = 'bolt://localhost:11003'
    user = "neo4j"
    password = "password"
    querer = Neo4jHandler(host, user)
    # query = "MATCH (n) RETURN n LIMIT 5"
    # result = querer.query(query=query, password=password)
    result = querer.get_processed_schema(password="password")
    print(result)
