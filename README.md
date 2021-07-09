# CayleyConnector for Python
A simple connector for Cayley databases. The connector leverages the HTTP API provided by Cayley.

## Usage

1. Install the `requests` module

    ```bash
    $ pip3 install requests
    ```

1. Copy `cayley.py` to your working directory.

1. Import the connector from the library

    ```python
    from cayley import quad
    from cayley import CayleyConnector
    ```

1. Create an instance of the connector

    ```python
    cayley = CayleyConnector(host='127.0.0.1', port=64210, protocol='http')
    ```

    Note: If you would like to stick to the above choice, feel free to leave all arguments empty as this is the choice by default.

1. Write quads to Cayley

    ```python
    cayley.write([
        quad(subject='Bob', predicate='is a friend of', object='Alice'),
        quad(subject='Bob', predicate='is a friend of', object='Shawn')
    ])
    ```

    We should get
    ```json
    {
        'result': 'Successfully wrote 2 quads.'
    }
    ```

    Note: The label property can be empty.

1. Query from Cayley

    ```python
    cayley.query("g.V('Bob').Out('is a friend of').All()")
    ```

    We should get
    ```json
    {
        'result': [{'id': 'Alice'}, {'id': 'Shawn'}]
    }
    ```

    Note: By default, the connector will query with the Gizmo query engine. To use other engines, call `cayley.set_query_engine(query_engine_name)` where `query_engine_name` can be `gizmo`, `graphql`, or `mql`.