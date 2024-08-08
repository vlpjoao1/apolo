from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from core.pos.forms import CompanyForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Company

# Update & add Company.
class CompanyUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    '''
    Trabaja con una única compañía. No es necesario pasarle el objeto
    por la url ya que el metodo get_object asigna el objeto y no dará error
    al entrar a la vista.
    '''
    model = Company
    form_class = CompanyForm
    template_name = 'company/create.html'
    success_url = reverse_lazy('dashboard')
    permission_required = 'change_company'

    def get_object(self):  # Works with a only one company
        company = self.model.objects.all()
        if company.exists():
            return company[0]  # First instance
        return Company()  # Empty instance

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                instance = self.get_object()
                if instance.pk is not None:  # If exists a company
                    form = self.form_class(request.POST, request.FILES, instance=instance)
                else:
                    form = self.form_class(request.POST, request.FILES)
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de mi compañía'
        context['entity'] = 'Compañía'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
