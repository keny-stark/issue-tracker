from django.urls.base import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from webapp.forms import TrackerForm
from webapp.models import Tracker


class IndexView(ListView):
    context_object_name = 'tracker'
    model = Tracker
    template_name = 'tracker/index.html'
    paginate_by = 3
    paginate_orphans = 1


class TrackerView(DetailView):
    model = Tracker
    template_name = 'tracker/tracker.html'


class TrackerCreateView(CreateView):
    template_name = 'tracker/add_tracker.html'
    model = Tracker
    form_class = TrackerForm
    redirect_url = 'tracker'


class TrackerUpdate(UpdateView):
    model = Tracker
    form_class = TrackerForm
    template_name = 'tracker/edit.html'
    redirect_url = 'tracker'
    success_url = reverse_lazy('index')


class DeleteTracker(DeleteView):
    template_name = 'tracker/delete_tracker.html'
    model = Tracker
    context_object_name = 'tracker'
    success_url = reverse_lazy('index')
