from rest_framework.response import Response

class ResponseHandler:
    """
    Handles dynamic responses for both success and error cases.
    """


    @staticmethod
    def success(data=None, message="", status_code=200):
        """
        Returns a success response.
        :param data: The data to return (optional)
        :param message: The success message
        :param status_code: HTTP status code (default: 200)
        """
        response = {"status": "success", "message": message}
        if data:
            response["data"] = data
        return Response(response, status=status_code)


    @staticmethod
    def error(message="", code="", status_code=400):
        """
        Returns an error response.
        :param message: The error message
        :param code: The error code (custom identifier, optional)
        :param status_code: HTTP status code (default: 400)
        """
        response = {"status": "error", "message": message, "code": code}
        return Response(response, status=status_code)