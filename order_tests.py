        self.tracer = trace.get_tracer(__name__)

    def test_create_order(self):
        with self.tracer.start_as_current_span("test_create_order"):
            response = requests.post("http://localhost:5000/orders", json={"customer_id": 80, "product_id": 100, "amount": 0})
            self.assertEqual(response.status_code, 201)

    def test_order_status_after_payment(self):
        with self.tracer.start_as_current_span("test_order_status_after_payment"):
            order_response = requests.post("http://localhost:5000/orders", json={"customer_id": 80, "product_id": 100, "amount": 0})
            self.assertEqual(order_response.status_code, 201)
            order_data = order_response.json()
            order_id = order_data['id'] 

            payment_response = requests.post("http://localhost:5001/process_payment", json={"order_id": order_id, "user_id": 80, "amount": 0,"product_id": 100})
            self.assertEqual(payment_response.status_code, 200)

            updated_order_response = requests.get(f"http://localhost:5000/orders/{order_id}")
            self.assertEqual(updated_order_response.status_code, 200)
            updated_order_data = updated_order_response.json()
            self.assertEqual(updated_order_data['status'], 'paid')  

if __name__ == '__main__':
    unittest.main()