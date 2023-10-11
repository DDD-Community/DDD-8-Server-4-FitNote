import logging

class AuthorizationHeaderLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Authorization 헤더 값 확인
        authorization_header = request.META.get('HTTP_AUTHORIZATION', 'No Authorization Header')

        # 로그에 Authorization 헤더 출력
        logger = logging.getLogger(__name__)
        logger.warn(f"Authorization Header: {authorization_header}")
        logger.warn('==')

        response = self.get_response(request)
        return response
