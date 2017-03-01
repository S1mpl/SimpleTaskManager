from django.views.generic.base import View

class PageNumberView(View):

    def post(self, request, *args, **kwargs):
        try:
            pn = request.GET['page']
        except KeyError:
            pn = '1'
        self.success_url = self.seccess_url + '?page=' + pn
        try:
            self.success_url = self.success_url + '&search=' + request.GET['search']
        except KeyError:
            pass
        return super(PageNumberView, self).post(request, *args, **kwargs)