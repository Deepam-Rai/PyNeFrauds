from neo4j import GraphDatabase


class NeoQuerer():
    def __init__(self, host, user, password=None):
        self.host = host
        self.user = user
        self.password = password
        return

    def neo4j_query(self, query, params=None, password=None, user=None, host=None):
        host = self.host if host is None else host
        user = self.user if user is None else user
        password = self.password if password is None else password
        driver = GraphDatabase.driver(host, auth=(user, password))
        with driver.session() as session:
            result = session.run(query, params)
            return [record.data() for record in result]

    def get_schema(self, password=None):
        query = 'CALL apoc.meta.schema()'
        result = self.neo4j_query(query=query, password=password)
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
    querer = NeoQuerer(host, user)
    # query = "MATCH (n) RETURN n LIMIT 5"
    # result = querer.neo4j_query(query=query, password=password)
    result = querer.get_processed_schema(password="password")
    print(result)
