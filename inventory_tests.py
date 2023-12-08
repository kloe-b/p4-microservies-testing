class InventoryTests(unittest.TestCase):

    def test_handle_payment_event_success(self):

        inventory_check_url = "http://localhost:5002/inventory/100"
        inventory_response_first = requests.get(inventory_check_url)
        inventory_data_first = inventory_response_first.json()

        payment_process_url = "http://localhost:5001/process_payment"

        payment_data = {
            'user_id': 67,
            'order_id': 20,
            'amount': 5,
            'product_id': 100,
        }
        response = requests.post(payment_process_url, json=payment_data)
        self.assertEqual(response.status_code, 200)  

        inventory_check_url = "http://localhost:5002/inventory/100"
        inventory_response = requests.get(inventory_check_url)
        self.assertEqual(inventory_response.status_code, 200)
        
        inventory_data = inventory_response.json()
        self.assertEqual(inventory_data['quantity'],inventory_data_first['quantity']-5)  

    def test_inventory_reservation_and_failure(self):
            order_url = "http://localhost:5000/orders"  
            order_data = {
                'customer_id': 290, 
                'product_id': 102,
                'amount': 10 

            }
            order_response = requests.post(order_url, json=order_data)
            self.assertEqual(order_response.status_code, 201) 
            order_data = order_response.json()
            order_id = order_data['id']
            payment_url = "http://localhost:5001/process_payment"  
            payment_data = {
                'user_id': 290,
                'order_id': order_id,
                'product_id': 102,
                'amount': 10 
            }
            payment_response = requests.post(payment_url,json=payment_data)
            
            inventory_url = f"http://localhost:5002/inventory/{order_data['product_id']}"  # Replace with your actual endpoint
            inventory_response = requests.get(inventory_url)
            self.assertEqual(inventory_response.status_code, 200)

            inventory_data = inventory_response.json()
            # Check if the inventory level reflects a successful reservation or a failure
            order_status_url = f"http://localhost:5000/orders/{payment_data['order_id']}"  # Replace with your actual endpoint
            status_response = requests.get(order_status_url)
            self.assertEqual(status_response.status_code, 200)

            status_data = status_response.json()
            expected_status = 'payment_failed'  
            self.assertEqual(status_data['status'], expected_status)
            

if __name__ == '__main__':
    unittest.main()
