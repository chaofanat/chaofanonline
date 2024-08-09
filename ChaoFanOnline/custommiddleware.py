from django.middleware.csrf import CsrfViewMiddleware

class CustomCsrfViewMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        # 检查是否为 AJAX 请求
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # 如果是 AJAX 请求，可以从请求头中获取 CSRF 令牌
        if is_ajax:
            csrf_token = request.headers.get('x_csrftoken')
            if csrf_token:
                request.META['CSRF_COOKIE'] = csrf_token
        
        return super().process_view(request, callback, callback_args, callback_kwargs)