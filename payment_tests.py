import unittest
import requests
from opentelemetry import trace

class PaymentServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.tracer = trace.get_tracer(__name__)

    def test_process_payment(self):
        with self.tracer.start_as_current_span("test_process_payment"):
            response = requests.post("http://localhost:5001/process_payment", json={'user_id': 199,
                'order_id': 23,  
                'amount': 0,
                'product_id': 100})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['status'], 'SUCCESS')
    def test_insufficient_funds(self):
        with self.tracer.start_as_current_span("test_process_payment"):
            response = requests.post("http://localhost:5001/process_payment", json={
                'user_id': 199,
                'order_id': 23,  
                'amount': 51,
                'product_id': 101
            })
            self.assertEqual(response.status_code, 400)
            data = response.json()
            self.assertEqual(data['status'], 'INSUFFICIENT_FUND')
    def test_payment_timeout(self):
        with self.tracer.start_as_current_span("test_process_payment"):
            response = requests.post("http://localhost:5001/process_payment", json={
                'user_id': 199,
                'order_id': 999,  
                'amount': 50,
                'product_id': 100
            })
            self.assertEqual(response.status_code, 500)
            data = response.json()
            self.assertEqual(data['status'], 'TIMEOUT')
    
    


if __name__ == '__main__':
    unittest.main()