# EXCHANGE RATES

Interact with the NBP API to retrieve exchange rate data using Python, Django (including Tests) and Swagger.

## Functions

Provides exchange rate in dependency for a given currency code, date and number of the last N quotations.

## Install

1. Download or clone
2. Create environment:
python -m venv venv
3. Activate environment:
source venv/Scripts/activate
4. Install requirements:
pip install -r requirements.txt
5. Run app in exchange_rates folder: 
python manage.py runserver 8000

6. Use browser (with in-build Django API interface) or command line for the next query examples: 
6.1. To query operation 1, run this command (which should have the value 5.2768 as the returning information):
curl http://127.0.0.1:8000/api/exchanges/gbp/2023-01-02/
6.2. To query operation 2, run this command (which should have the minimum and maximum value as the returning information):
curl http://127.0.0.1:8000/api/exchanges/gbp/10/
6.3. To query operation 3, run this command (which should have the biggest difference as the returning information):
curl http://127.0.0.1:8000/api/exchanges/difference/gbp/10/

7. Use a browser with the Swagger UI for the same functionality as above:
http://127.0.0.1:8000/api/swagger/

8. Run tests with different exception handling in exchange_rates folder:
python manage.py test rates_api
