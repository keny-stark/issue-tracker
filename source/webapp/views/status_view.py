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
