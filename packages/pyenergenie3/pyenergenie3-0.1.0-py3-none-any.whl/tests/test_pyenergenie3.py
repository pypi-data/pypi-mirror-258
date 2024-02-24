import unittest
from unittest.mock import Mock, patch
from pyenergenie3.core import PyEnergenie3


class TestPyEnergenie3(unittest.TestCase):
    def setUp(self):
        # Replace with the IP and password of your test device
        self.device_ip = "10.6.10.108"
        self.password = "1"
        self.energenie = PyEnergenie3(self.device_ip, self.password)

    @patch("pyenergenie3.core.requests.Session.post")
    def test_authenticate_successful(self, mock_post):
        # Mock the successful authentication response
        mock_post.return_value.ok = True

        self.energenie.authenticate()

        # Assert that the mock post method was called with the correct arguments
        mock_post.assert_called_once_with(
            f"http://{self.device_ip}/login.html", data={"pw": self.password}
        )

    @patch("pyenergenie3.core.requests.Session.post")
    def test_authenticate_failure(self, mock_post):
        # Mock a failed authentication response
        mock_post.return_value.ok = False

        with self.assertRaises(RuntimeError):
            self.energenie.authenticate()

    @patch("pyenergenie3.core.requests.Session.get")
    def test_get_all_outlet_states_successful(self, mock_get):
        # Mock the successful status response
        mock_get.return_value.ok = True
        mock_get.return_value.text = '<script>\nvar sockstates = [1, 0, 1, 0];\n</script>'

        states = self.energenie.get_all_outlet_states()

        # Assert that the states were correctly parsed
        self.assertEqual(states, [1, 0, 1, 0])

    @patch("pyenergenie3.core.requests.Session.get")
    def test_get_all_outlet_states_failure(self, mock_get):
        # Mock a failed status response
        mock_get.return_value.ok = False

        with self.assertRaises(RuntimeError):
            self.energenie.get_all_outlet_states()

    @patch("pyenergenie3.core.requests.Session.get")
    def test_get_outlet_state_successful(self, mock_get):
        # Mock a successful status response
        mock_get.return_value.ok = True
        mock_get.return_value.text = '<script>\nvar sockstates = [1, 0, 1, 0];\n</script>'

        # Call the method to get the outlet state
        outlet_number = 2  # Replace with the desired outlet number
        state = self.energenie.get_outlet_state(outlet_number)

        # Assert that the mocked get method was called with the correct arguments
        mock_get.assert_called_once_with(f"http://{self.device_ip}/status")

        # Assert that the outlet state was correctly retrieved
        self.assertEqual(state, 0)  # Replace with the expected state

    @patch("pyenergenie3.core.requests.Session.get")
    def test_get_outlet_state_failure(self, mock_get):
        # Mock a failed status response
        mock_get.return_value.ok = False

        # Call the method to get the outlet state
        outlet_number = 2  # Replace with the desired outlet number

        # Assert that the method raises a RuntimeError for a failed request
        with self.assertRaises(RuntimeError):
            self.energenie.get_outlet_state(outlet_number)

    @patch("pyenergenie3.core.requests.Session.post")
    def test_set_outlet_state_successful(self, mock_post):
        # Mock a successful response for setting outlet state
        mock_post.return_value.ok = True

        # Call the method to set the outlet state
        outlet_number = 3  # Replace with the desired outlet number
        state = 1  # Replace with the desired state (0 or 1)
        self.energenie.set_outlet_state(outlet_number, state)

        # Assert that the mocked post method was called with the correct arguments
        mock_post.assert_called_once_with(
            f"http://{self.device_ip}/",
            data={f"cte{outlet_number}": state}
        )

    @patch("pyenergenie3.core.requests.Session.post")
    def test_set_outlet_state_failure(self, mock_post):
        # Mock a failed response for setting outlet state
        mock_post.return_value.ok = False

        # Call the method to set the outlet state
        outlet_number = 3  # Replace with the desired outlet number
        state = 1  # Replace with the desired state (0 or 1)

        # Assert that the method raises a RuntimeError for a failed request
        with self.assertRaises(RuntimeError):
            self.energenie.set_outlet_state(outlet_number, state)


if __name__ == '__main__':
    unittest.main()
