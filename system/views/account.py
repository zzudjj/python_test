from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class MyMiddleware(MiddlewareMixin):

    def process_request(self, request):
        url = request.path_info
        if url == '/login/' or url == '/register/' or url == '/logout/':
            return
        info_dict = request.session.get('info')
        login_dict = {'passenger': '0', 'driver': '1', 'manager': '2'}
        pos1 = url.find('/')
        pos2 = url.find('/', pos1+1)
        login_user = url[pos1+1:pos2]
        if info_dict['identity'] == login_dict[login_user]:
            return
        return redirect('/login/')
