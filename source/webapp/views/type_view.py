from django.http import HttpResponseRedirect
from django.urls.base import reverse, reverse_lazy
from django.db.models.deletion import ProtectedError
from django.http import HttpResponse
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from webapp.forms import TypeForm
from webapp.models import Type


class TypeView(ListView):
    context_object_name = 'type'
    model = Type
    template_name = 'type/type.html'


class TypeAddView(CreateView):
    form_class = TypeForm
    template_name = 'type/add_type.html'
    model = Type

    def get_success_url(self):
        return reverse('type_views')


class UpdateTypeView(UpdateView):
    model = Type
    form_class = TypeForm
    template_name = 'type/edit _type.html'
    redirect_url = 'type_views'


class DeleteType(DeleteView):
    template_name = 'type/type_delete.html'
    model = Type
    context_object_name = 'type'
    success_url = reverse_lazy('type_views')

    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            return HttpResponse("<h2>This object is used, deletion is prohibited</h2>")
