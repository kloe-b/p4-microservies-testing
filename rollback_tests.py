import unittest
import requests
from opentelemetry import trace

class RollbackTestCase(unittest.TestCase):

    def setUp(self):
        self.order_service_url = "http://localhost:5000"  
        self.payment_service_url = "http://localhost:5001"  
        # self.inventory_service_url = "http://localhost:5002"  # URL for Inventory service


    def test_insufficient_inventory_rollback(self):
            product_id = 102
          
            order_response = requests.post(f"{self.order_service_url}/orders", json={
                'customer_id': 399,
                'product_id': product_id,
                'amount': 120 
            })
            self.assertEqual(order_response.status_code, 201)
            order_id = order_response.json()['id']
            user_credits= requests.get(f"{self.payment_service_url}/users/399")
            payment_response = requests.post(f"{self.payment_service_url}/process_payment", json={
                'user_id': 399,
                'order_id': order_id,
                'amount': 120,
                'product_id': product_id
            })

            user_credits_response = requests.get(f"{self.payment_service_url}/users/399")  
            self.assertEqual(user_credits_response.status_code, 200)
            user_credits = user_credits_response.json()['credits']
            expected_credits_after_rollback = user_credits  
            self.assertEqual(user_credits, expected_credits_after_rollback)


if __name__ == '__main__':
    unittest.main()