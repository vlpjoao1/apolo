from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.pos.mixins import ValidatePermissionRequiredMixin
from core.reports.forms import ReportForm
from core.security.models import AccessUser


class AccessUserListView(ValidatePermissionRequiredMixin, FormView):
    form_class = ReportForm
    template_name = 'access_users/list.html'
    permission_required = 'view_access_user'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = AccessUser.objects.all()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de accesos'
        context['list_url'] = reverse_lazy('access_user_list')
        context['entity'] = 'Control de Accesos'
        return context
