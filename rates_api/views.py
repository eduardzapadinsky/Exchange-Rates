import requests
from requests import JSONDecodeError

from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response


class AverageRateCurrencyDate(APIView):

    def get(self, request, code: str, date: str):
        """
        Retrieve data for GET method
        :param request:
        :type request:
        :return:
        :rtype:
        """
        url = f"http://api.nbp.pl/api/exchangerates/rates/a/{code}/{date}/?format=json"
        response = requests.get(url)
        try:
            average_rate = response.json()["rates"][0]["mid"]
            data = {f"average {code.upper()} exchange rate dated {date}": average_rate}
        except JSONDecodeError:
            data = response.content
            raise NotFound(data)
        return Response(data)


class AverageRateLastQuotations(APIView):

    def get(self, request, code: str, number: int):
        """

        :param request:
        :type request:
        :param code:
        :type code:
        :param number:
        :type number:
        :return:
        :rtype:
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
                    f"average {code.upper()} exchange rate for the last {number} quotations":
                        {"minimum": min_average_rate,
                         "maximum": max_average_rate}
                }
            except JSONDecodeError:
                data = response.content
                raise NotFound(data)
        else:
            if number <= 0:
                message = "400 BadRequest - Liczba wyników nie może być mniejsza niż 1 / " \
                          "The number of quotations cannot be less than one"
            else:
                message = response.content
            data = {"detail": message}
            raise ValidationError(data, code=400)
        return Response(data)


class DifferenceRateLastQuotations(APIView):

    def get(self, request, code: str, number: int):
        """

        :param request:
        :type request:
        :param code:
        :type code:
        :param number:
        :type number:
        :return:
        :rtype:
        """
        url = f"http://api.nbp.pl/api/exchangerates/rates/c/{code}/last/{number}/?format=json"
        response = requests.get(url)
        if 1 <= number <= 255:
            difference_rates = []
            try:
                rates_data = response.json()["rates"]
                for rate_data in rates_data:
                    bid_rate = rate_data["bid"]
                    ask_rate = rate_data["ask"]
                    difference_rate = round(ask_rate - bid_rate, 4)
                    difference_rates.append(difference_rate)
                max_difference_rate = max(difference_rates)
                data = {
                    f"biggest {code.upper()} exchange rate difference for the last {number} quotations":
                        max_difference_rate}
            except JSONDecodeError:
                data = response.content
                raise NotFound(data)
        else:
            if number <= 0:
                message = "400 BadRequest - Liczba wyników nie może być mniejsza niż 1 / " \
                          "The number of quotations cannot be less than one"
            else:
                message = response.content
            data = {"detail": message}
            raise ValidationError(data, code=400)
        return Response(data)
