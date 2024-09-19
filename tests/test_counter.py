"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

import pytest

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status

@pytest.fixture()
def client():
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndPoints:
    """Test cases for Counter-related endpoints"""

    def test_create_a_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    def test_duplicate_a_counter(self, client):
        """Testing Duplicate"""
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_201_CREATED
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_409_CONFLICT

    def test_update_counter(self, client):
        """Testing Update"""
        client.post('/counters/test')
        result = client.put('/counters/test')
        assert result.status_code == status.HTTP_200_OK
        assert result.json == {'test': 1}
        result = client.put('/counters/test')
        assert result.status_code == status.HTTP_200_OK
        assert result.json == {'test': 2}

        result = client.put('/counters/nonexistent')
        assert result.status_code == status.HTTP_404_NOT_FOUND

    def test_read_counter(self, client):
        """Testing Read Counter"""
        client.post('/counters/test2')
        result = client.get('counters/test2')
        assert result.status_code == status.HTTP_200_OK
        assert result.json == {'test2':0}

        result = client.get('/counters/fake')
        assert result.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_counter(self,client):
        """Testing Deleting Counter"""
        client.post('/counters/test3')
        result = client.delete('/counters/test3')
        assert result.status_code == status.HTTP_204_NO_CONTENT

        result = client.delete('/counters/fake')
        assert result.status_code == status.HTTP_404_NOT_FOUND
