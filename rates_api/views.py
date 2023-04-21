import requests

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
        average_rate = response.json()["rates"][0]["mid"]
        data = {f"average rate for {code.upper()} dated {date}": average_rate}
        return Response(data)
