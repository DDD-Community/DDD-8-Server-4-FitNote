import logging

class AuthorizationHeaderLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Authorization 헤더 값 확인
        authorization_header = request.META.get('HTTP_AUTHORIZATION', 'No Authorization Header')

        # 로거 설정
        logger = logging.getLogger('custom.authorization')

        if authorization_header is None:
            logger.warn("Authorization Header is absent")
        elif authorization_header == '':
            logger.warn("Authorization Header is empty")
        else:
            logger.warn(f"Authorization Header value: {authorization_header}")

        response = self.get_response(request)
        return response
