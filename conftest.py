import pytest
from helpers import delete_courier


@pytest.fixture
def cleanup_courier(request):
    courier_ids = []

    def add_courier(courier_id):
        courier_ids.append(courier_id)

    def delete_created_couriers():
        for courier_id in courier_ids:
            delete_courier(courier_id)

    request.addfinalizer(delete_created_couriers)

    return add_courier
    