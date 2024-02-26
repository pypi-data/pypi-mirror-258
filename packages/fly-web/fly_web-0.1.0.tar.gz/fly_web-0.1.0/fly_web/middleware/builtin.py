from fly_web.middleware.core import BaseMiddleware
from fly_web.context import capp
from fly_web.response import JsonResponse, Response


class FlyCorsMiddleware(BaseMiddleware):
    """
    fly:
        CORS_ALLOW_ORIGIN: str = "*"
    """

    async def process_response(self, request, response):
        if isinstance(response, dict):
            response = JsonResponse(response)
        if not isinstance(response, Response):
            raise TypeError(f"response must be a Response object, not {type(response)}")
        response.headers["Access-Control-Allow-Origin"] = capp.config.get("CORS_ALLOW_ORIGIN", "*")
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
