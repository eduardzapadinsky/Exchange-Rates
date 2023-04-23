from rest_framework.exceptions import NotFound, ValidationError


def not_found_raise(response):
    data = response.content
    raise NotFound(data)


def bad_request_raise(number, response):
    if number <= 0:
        message = "400 BadRequest - Liczba wyników nie może być mniejsza niż 1 / " \
                  "The number of quotations cannot be less than one"
    else:
        message = response.content
    data = {"detail": message}
    raise ValidationError(data, code=400)
