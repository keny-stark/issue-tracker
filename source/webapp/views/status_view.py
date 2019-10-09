from django.db.models import ProtectedError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse, reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from webapp.forms import StatusForm
from webapp.models import Status


class StatusView(ListView):
    context_object_name = 'status'
    model = Status
    template_name = 'status/status.html'


class StatusAddView(CreateView):
    form_class = StatusForm
    template_name = 'status/add_status.html'
    model = Status

    def get_success_url(self):
        return reverse('status_views')


class DeleteStatus(DeleteView):
    template_name = 'status/status_delete.html'
    model = Status
    context_object_name = 'status'
    success_url = reverse_lazy('status_views')


class UpdateStatusView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/edit_status.html'
    redirect_url = 'status_views'

    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            return HttpResponse("<h2>This object is used, deletion is prohibited</h2>")

