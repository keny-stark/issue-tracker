from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls.base import reverse_lazy, reverse
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from webapp.forms import TrackerForm, TrackerProjectForm, SimpleSearchForm
from webapp.models import Tracker, Project


class IndexView(ListView):
    context_object_name = 'tracker'
    model = Tracker
    template_name = 'tracker/index.html'
    paginate_by = 3
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class TrackerView(DetailView):
    model = Tracker
    template_name = 'tracker/tracker.html'


class TrackerCreateView(LoginRequiredMixin, CreateView):
    template_name = 'tracker/add_tracker.html'
    model = Tracker
    form_class = TrackerForm
    redirect_url = 'tracker'


class TrackerForProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'tracker/edit.html'
    form_class = TrackerProjectForm

    def form_valid(self, form):
        project_pk = self.kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_pk)
        project.tracker.create(**form.cleaned_data)
        return redirect('project_detail', pk=project_pk)


class TrackerUpdate(LoginRequiredMixin, UpdateView):
    model = Tracker
    form_class = TrackerForm
    template_name = 'tracker/edit.html'

    def get_success_url(self):
        return reverse('webapp:tracker', kwargs={'pk': self.object.pk})


class DeleteTracker(LoginRequiredMixin, DeleteView):
    template_name = 'tracker/delete_tracker.html'
    model = Tracker
    context_object_name = 'tracker'
    success_url = reverse_lazy('webapp:index')
