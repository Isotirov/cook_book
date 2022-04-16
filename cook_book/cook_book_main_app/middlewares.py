from cook_book.cook_book_main_app.views import internal_error


def handle_exception(get_response):
    def middleware(request):
        response = get_response(request)
        if response.status_code >= 400:
            return internal_error(request)
        return response
    return middleware
