"""
Functions that raise specific exceptions with appropriate error messages.
"""

from requests import Response

from rest_framework.exceptions import NotFound, ValidationError


def not_found_raise(response: Response) -> None:
    """
    Raises a `NotFound` 404 exception with the content of the given `response`.
    Parameters:
    -----------
    response : Response
        The response object that contains the data to raise the exception with.
    Returns:
    -----------
        None
    Raises:
    -----------
        NotFound: If the data in the response indicates that the requested resource was not found.
    """

    data = response.content
    raise NotFound(data)


def bad_request_raise(number: int, response: Response) -> None:
    """
    Raises a ValidationError exception with an appropriate error message and code 400
    when an invalid number of quotations is specified.
    Parameters:
    -----------
    number : int
        An integer that represents the number of quotations to retrieve.
    response: Response
        A response object that contains metadata about the response from an API.
    Returns:
    --------
        None
    Raises:
    --------
        ValidationError: If an invalid number of quotations is specified.
    """

    if number <= 0:
        message = "400 BadRequest - Liczba wyników nie może być mniejsza niż 1 / " \
                  "The number of quotations cannot be less than one"
    else:
        message = response.content
    data = {"detail": message}
    raise ValidationError(data, code=400)
