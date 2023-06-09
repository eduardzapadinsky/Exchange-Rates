# EXCHANGE RATES

Interact with the NBP API to retrieve exchange rate data using Python, Django (including Tests) and Swagger.

## Functions

Provides exchange rate in dependency for a given currency code, date and number of the last N quotations.

## Install

1. Download or clone
2. Run using Docker:  
  
   docker-compose up --build  
  
   or  
  
   Run manually:  
  * Create environment in source folder:  
   python -m venv venv  
  * Activate environment:  
   source venv/Scripts/activate  
  * Install requirements in source folder:  
   pip install -r requirements.txt  
  * Run app in source folder:  
   python manage.py runserver 8000  

3. Use browser (with in-build Django API interface) or command line for the next query examples:
  * To query operation 1, run this command (which should have the value 5.2768 as the returning information):  
   curl http://127.0.0.1:8000/api/exchanges/gbp/2023-01-02/  
  * To query operation 2, run this command (which should have the minimum and maximum value as the returning
   information):  
   curl http://127.0.0.1:8000/api/exchanges/gbp/10/  
  * To query operation 3, run this command (which should have the biggest difference as the returning information):  
   curl http://127.0.0.1:8000/api/exchanges/difference/gbp/10/  
   
   ![Chrome_01](https://user-images.githubusercontent.com/111561866/234058525-b848d4cb-b629-4d0c-9c05-870c459456af.JPG)

4. Use a browser with the Swagger UI for the same functionality as above:  
   http://127.0.0.1:8000/api/swagger/  
   
   ![Chrome_02](https://user-images.githubusercontent.com/111561866/234058595-7f98e5e6-c58b-45cc-bc86-0b5018bb3656.JPG)

5. Run tests with different exception handling in source folder:  
   python manage.py test rates_api  
