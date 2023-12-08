import unittest
import requests
from opentelemetry import trace

class DeliveryServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.tracer = trace.get_tracer(__name__)

    def test_arrange_delivery(self):
        with self.tracer.start_as_current_span("test_arrange_delivery"):
            response = requests.post("http://localhost:5003/deliveries", json={"order_id": 1, "product_id": 100})
            self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('order_id', data)
        self.assertIn('product_id', data)
    def test_get_delivery(self):
        response = requests.get("http://localhost:5003/deliveries/1")
        self.assertEqual(response.status_code, 200)
      
    def test_update_delivery(self):
        response = requests.put("http://localhost:5003/deliveries/1", json={'status': 'delivered'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'delivered')
    def test_delivery_process_and_rollback(self):
            delivery_creation_url = "http://localhost:5003/deliveries"  
            delivery_data = {
                'order_id': 1,
                'product_id': 101,
                'quantity': 5  
            }
            delivery_response = requests.post(delivery_creation_url, json=delivery_data)
            self.assertEqual(delivery_response.status_code, 201)
            delivery_id = delivery_response.json()['id']

            delivery_update_url = f"http://localhost:5003/deliveries/{delivery_id}"
            update_response = requests.put(delivery_update_url, json={'status': 'FAILED'})
            self.assertEqual(update_response.status_code, 200)

            inventory_check_url = f"http://localhost:5002/inventory/101"
            inventory_response = requests.get(inventory_check_url)
            self.assertEqual(inventory_response.status_code, 200)
            updated_quantity = inventory_response.json()['quantity']
            self.assertEqual(updated_quantity, 95)  


if __name__ == '__main__':
    unittest.main()