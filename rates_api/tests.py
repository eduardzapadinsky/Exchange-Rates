from unittest.mock import patch, Mock

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase


class BaseAPITestCase:
    """
    A base test case class for testing API endpoints using the Django APIClient.
    """

    def setUp(self) -> None:
        """
        Set up the test case by instantiating the APIClient and setting the url_name to an empty string.
        """

        self.client = APIClient()
        self.url_name = ""

    def test_endpoint_invalid_number_less(self):
        """
        Test case for an invalid request to the endpoint with a number less than 1.
        """

        message = "400 BadRequest - Liczba wyników nie może być mniejsza niż 1 / " \
                  "The number of quotations cannot be less than one"
        url = reverse(self.url_name, args=["gbp", 0])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertIn(message, response.data.values())

    def test_endpoint_invalid_number_more(self):
        """
        Test case for an invalid request to the endpoint with a number greater than 255.
        """

        message = "400 BadRequest - Przekroczony limit 255 wyników / " \
                  "Maximum size of 255 data series has been exceeded"
        url = reverse(self.url_name, args=["gbp", 256])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertIn(message, response.data.values())

    def test_endpoint_invalid_code(self):
        """
        Test case for an invalid request to the endpoint with a non-existent code.
        """

        message = "404 NotFound"
        url = reverse(self.url_name, args=["non-existent-code", 10])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertIn(message, response.data["detail"])


class AverageRateCurrencyDateTest(APITestCase):
    """
    Test for AverageRateCurrencyDate class.
    This class defines a set of test cases for the "currency-date" endpoint of the rates API,
    which returns the average exchange rate of a given currency for a specific date.
    """

    def setUp(self) -> None:
        """
        Initializes the client and the URL name to be used in the tests.
        """

        self.client = APIClient()
        self.url_name = "rates-api:currency-date"

    def test_average_rate_currency_date_valid(self):
        """
        Tests the with valid parameters and checks if the expected average exchange rate is returned.
        """

        message = "the average GBP exchange rate dated 2023-01-02"
        average_rate = 5.2768
        url = reverse(self.url_name, args=["gbp", "2023-01-02"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(message, response.data)
        self.assertEqual(float(response.data[message]), average_rate)

    def test_average_rate_currency_date_invalid_date(self):
        """
        Tests with an invalid date and checks if a 404 response with the appropriate error message is returned.
        """

        message = "404 NotFound - Not Found - Brak danych"
        url = reverse(self.url_name, args=["gbp", "2023-01-01"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertIn(message, response.data.values())

    def test_average_rate_currency_date_invalid_code(self):
        """
        Tests with an invalid currency code and checks if a 404 response with the appropriate error message is returned.
        """

        message = "404 NotFound"
        url = reverse(self.url_name, args=["non-existent-code", "2023-01-01"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertIn(message, response.data["detail"])


class AverageRateLastQuotationsTest(BaseAPITestCase, APITestCase):
    """
    Test for AverageRateLastQuotations class.
    This class tests the functionality of an API endpoint that returns the average exchange rate for the last `n`
    quotations of a given currency.
    """

    def setUp(self) -> None:
        """
        Initializes the client and the URL name to be used in the tests.
        """

        super().setUp()
        self.url_name = "rates-api:last-quotations"

    def test_average_rate_last_quotations_valid(self):
        """
        Test that the API returns the average exchange rate for the last `n` quotations of a currency.
        """

        message = "the average GBP exchange rate for the last 10 quotations"
        url = reverse(self.url_name, args=["gbp", 10])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(message, response.data)
        self.assertIn("minimum", response.data[message])
        self.assertIn("maximum", response.data[message])

    @patch("requests.get")
    def test_average_rate_last_quotations_mock_valid(self, mock_get):
        """
        Test that the API returns the correct average exchange rate when the response is mocked.
        """

        mock_response = {"table": "A",
                         "currency": "funt szterling",
                         "code": "GBP",
                         "rates": [{"no": "077/A/NBP/2023", "effectiveDate": "2023-04-20", "mid": 5.2296},
                                   {"no": "078/A/NBP/2023", "effectiveDate": "2023-04-21", "mid": 5.2086},
                                   {"no": "079/A/NBP/2023", "effectiveDate": "2023-04-24", "mid": 5.2176}]}
        max_mock_result = max([5.2296, 5.2086, 5.2176])
        min_mock_result = min([5.2296, 5.2086, 5.2176])
        message = {
            "the average GBP exchange rate for the last 3 quotations": {
                "minimum": min_mock_result,
                "maximum": max_mock_result
            }
        }
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = mock_response
        url = reverse(self.url_name, args=["gbp", 3])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, message)


class DifferenceRateLastQuotationsTest(BaseAPITestCase, APITestCase):
    """
    Test for AverageRateLastQuotations class.
    This class tests the functionality of an API endpoint that returns the difference exchange rate for the last `n`
    quotations of a given currency.
    """

    def setUp(self) -> None:
        """
        Initializes the client and the URL name to be used in the tests.
        """

        super().setUp()
        self.url_name = "rates-api:difference-rate"

    def test_difference_rate_last_quotations_valid(self):
        """
        Tests whether the endpoint returns the expected result for a valid request with 10 quotations.
        """

        message = "the biggest GBP exchange rate difference for the last 10 quotations"
        url = reverse(self.url_name, args=["gbp", 10])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(message, response.data)

    @patch("requests.get")
    def test_difference_rate_last_quotations_mock_valid(self, mock_get):
        """
        Tests whether the endpoint returns the expected result for a valid request with mocked quotations.
        """
        mock_response = {"table": "C",
                         "currency": "funt szterling",
                         "code": "GBP",
                         "rates": [
                             {"no": "077/C/NBP/2023", "effectiveDate": "2023-04-20", "bid": 5.1883, "ask": 5.2931},
                             {"no": "078/C/NBP/2023", "effectiveDate": "2023-04-21", "bid": 5.1706, "ask": 5.2750},
                             {"no": "079/C/NBP/2023", "effectiveDate": "2023-04-24", "bid": 5.1540, "ask": 5.2582}]}
        max_mock_result = max([5.2931 - 5.1883, 5.2750 - 5.1706, 5.2582 - 5.1540])
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = mock_response
        url = reverse(self.url_name, args=["gbp", 3])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
                         {"the biggest GBP exchange rate difference for the last 3 quotations": max_mock_result})
