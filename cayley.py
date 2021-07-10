import json
import requests

class CayleyConnector:
    """The CayleyConnector."""

    def __init__(self, host='127.0.0.1', port=64210, protocol='http'):
        """The constructor of a Cayley connector.
        
        Args:
            host (str): The host of the Cayley database. By default, 127.0.0.1.
            port (int): The port of Cayley database's HTTP server. By 
                default, 64210.
            protocol (str): The protocol that is used to connect to Cayley 
                database's HTTP server. Could be either 'http' or 'https'.
                By default, 'http'.
        """
        if protocol not in ['http', 'https']:
            raise Exception('not a valid protocol.')
        self.url = f'{protocol}://{host}:{port}'

        # Set the default query engine to gizmo
        self.query_engine = 'gizmo'

    def write(self, body):
        """Write a list of quads.
        
        Note:
            When only writing one quad, place the quad in a list first.

        Args:
            body (list): A list of quad(s).

        Returns:
            dict: A dictionary of the response object.
        """
        return json.loads(requests.post(self.url + '/api/v1/write', json=body).text)

    def delete(self, body):
        """Delete a list of quads.
        
        Note:
            When deleting only one quad, place the quad in a list first.

        Args:
            body (list): A list of quad(s).

        Returns:
            dict: A dictionary of the response object.
        """
        return json.loads(requests.post(self.url + '/api/v1/delete', json=body).text)

    def query(self, query):
        """Query the Cayley database.

        Note:
            By default, the connector will query with the Gizmo query engine.
            To use other engines, use
            ```cayley.set_query_engine(query_engine_name)```

        Args:
            query (str): The query. Usually in the form of a string of 
                JavaScript code or JSON.

        Returns:
            dict: A dictionary of the response object.
        """
        return json.loads(requests.post(
            self.url + f'/api/v1/query/{self.query_engine}', data=query).text)

    def query_shape(self, query):
        """Query shape.

        Note:
            By default, the connector will query with the Gizmo query engine.
            To use other engines, use
            ```cayley.set_query_engine(query_engine_name)```

        Args:
            query (str): The query. Usually in the form of a string of 
                JavaScript code or JSON.

        Returns:
            dict: A dictionary of the response object.
        """
        if self.query_engine == 'graphql':
            raise Exception('GraphQL does not support querying the shape.')
        return json.loads(requests.post(
            self.url + f'/api/v1/shape/{self.query_engine}', data=query).text)
    
    def set_query_engine(self, query_engine):
        """Change the query engine.
        
        Note:
            By default, the connector uses the Gizmo query engine.

        Args:
            query_engine (str): The name of the query engine. Cayley supports
            'gizmo', 'graphql', or 'mql'.
        """
        if query_engine not in ['gizmo', 'graphql', 'mql']:
            raise Exception('invalid query engine.')
        self.query_engine = query_engine

    def ping(self):
        """Test the connection. Should print pong if success."""
        res = json.loads(requests.post(
            self.url + f'/api/v1/query/gizmo', data='g.Emit("pong")').text)
        assert res['result'][0] == 'pong'
        print('pong')


def quad(subject, predicate, object, label = ''):
    """Prepare a quad.
    
    Args:
        subject (str): The subject.
        predicate (str): The predicate.
        object (str): The object.
        label (str): Optional. The label.

    Returns:
        dict: The dictionary of a quad.
    """
    json = {
        'subject': subject,
        'predicate': predicate,
        'object': object,
        'label': label
    }
    if len(label) == 0:
        del json['label']
    return json
