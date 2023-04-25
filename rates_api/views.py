"""
Django views for the currency exchange rates application.
These views use the requests library to interact with the NBP API to retrieve exchange rate data.
"""

import requests
from requests import JSONDecodeError

from rest_framework.views import APIView
from rest_framework.response import Response

from . import service


class AverageRateCurrencyDate(APIView):
    """
    A class-based view to retrieve the average exchange rate for a given currency code and date.
    """

    def get(self, request, code: str, date: str) -> Response:
        """
        Retrieve the average exchange rate for a given currency code and date.
        Parameters:
        -----------
        request : HttpRequest
            The request object.
        code : str
            The currency code to retrieve the exchange rate for.
        date : str
            The date to retrieve the exchange rate for in the format yyyy-mm-dd.
        Returns:
        --------
        Response
            A JSON response containing the average exchange rate for the specified currency and date.
        Raises:
        -------
        JSONDecodeError
            If the response from the API cannot be decoded to JSON.
        """

        url = f"http://api.nbp.pl/api/exchangerates/rates/a/{code}/{date}/?format=json"
        response = requests.get(url)
        try:
            average_rate = response.json()["rates"][0]["mid"]
            data = {f"the average {code.upper()} exchange rate dated {date}": average_rate}
            return Response(data)
        except JSONDecodeError:
            service.not_found_raise(response)


class AverageRateLastQuotations(APIView):
    """
    A class-based view that calculates the average minimum and maximum exchange rate for a currency
    based on the last N quotations as retrieved from the NBP API.
    """

    def get(self, request, code: str, number: int) -> Response:
        """
        Retrieves the last N quotations for a given currency code from the NBP API and calculates the average exchange
        rate, minimum, and maximum. Returns a JSON response with the calculated values.
        Parameters:
        -----------
        request : HttpRequest
            The request object.
        code : str
            The currency code to retrieve the exchange rate for.
        number: int
            The number of quotations to retrieve.
        Returns:
        --------
        Response
            A JSON response containing the calculated average exchange rate, minimum, and maximum for the given
            currency code and number of quotations.
        Raises:
        --------
            NotFound: If the requested data was not found in the response.
            BadRequest: If the request parameters are invalid.
        """

        url = f"http://api.nbp.pl/api/exchangerates/rates/a/{code}/last/{number}/?format=json"
        response = requests.get(url)
        if 1 <= number <= 255:
            average_rates = []
            try:
                average_rates_data = response.json()["rates"]
                for average_rate_data in average_rates_data:
                    average_rate = average_rate_data["mid"]
                    average_rates.append(average_rate)
                min_average_rate = min(average_rates)
                max_average_rate = max(average_rates)
                data = {
                    f"the average {code.upper()} exchange rate for the last {number} quotations":
                        {"minimum": min_average_rate,
                         "maximum": max_average_rate}
                }
                return Response(data)
            except JSONDecodeError:
                service.not_found_raise(response)
        else:
            service.bad_request_raise(number, response)


class DifferenceRateLastQuotations(APIView):
    """
    A view that retrieves the biggest difference between the bid and ask rates for a given currency code
    over a specified number of quotations from the NBP API.
    """

    def get(self, request, code: str, number: int) -> Response:
        """
        Retrieves the biggest difference between the bid and ask rates for a given currency code over a specified number of quotations.
        Parameters:
        -----------
        request : HttpRequest
            The request object.
        code : str
            The currency code to retrieve the exchange rate for.
        number: int
            The number of quotations to retrieve.
        Returns:
        --------
        Response
            A Response object that contains the biggest difference between the bid and ask rates for a given currency code over a specified
            number of quotations.
        Raises:
        --------
            NotFound: If the requested data was not found in the response.
            BadRequest: If the request parameters are invalid.
        """

        url = f"http://api.nbp.pl/api/exchangerates/rates/c/{code}/last/{number}/?format=json"
        response = requests.get(url)
        if 1 <= number <= 255:
            max_difference_rate = 0
            try:
                rates_data = response.json()["rates"]
                for rate_data in rates_data:
                    bid_rate = rate_data["bid"]
                    ask_rate = rate_data["ask"]
                    difference_rate = round(ask_rate - bid_rate, 4)
                    if difference_rate > max_difference_rate:
                        max_difference_rate = difference_rate
                data = {
                    f"the biggest {code.upper()} exchange rate difference for the last {number} quotations":
                        max_difference_rate}
                return Response(data)
            except JSONDecodeError:
                service.not_found_raise(response)
        else:
            service.bad_request_raise(number, response)
