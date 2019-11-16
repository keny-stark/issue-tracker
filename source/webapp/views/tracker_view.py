from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
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


class TrackerCreateView(UserPassesTestMixin, CreateView):
    template_name = 'tracker/add_tracker.html'
    model = Tracker
    form_class = TrackerForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        form.fields['project_id'].queryset = Project.objects.filter(team_user__user=self.request.user,
                                                                    team_user__updated_at__isnull=True)
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:tracker', kwargs={'pk': self.object.pk})

    def test_func(self):
        if self.request.user.is_authenticated:
            return True
        return False


class TrackerForProjectCreateView(UserPassesTestMixin, CreateView):
    form_class = TrackerProjectForm

    def form_valid(self, form):
        project = Project.objects.get(pk=self.kwargs['pk'])
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.project_id = project
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        project = Project.objects.get(pk=self.kwargs['pk'])
        users = project.users.all()
        if self.request.user in users:
            return True
        return False

    def get_success_url(self):
        return reverse('webapp:tracker', kwargs={'pk': self.object.pk})


class TrackerUpdate(UserPassesTestMixin, UpdateView):
    model = Tracker
    form_class = TrackerForm
    template_name = 'tracker/edit.html'

    def test_func(self):
        issue = self.get_object()
        project = issue.project_id
        users_in_project = User.objects.filter(user_team__project=project, user_team__updated_at__isnull=True)
        return self.request.user in users_in_project

    def get_success_url(self):
        # if self.request.user in users_in_project:
        #     return True
        # return False
        return reverse('webapp:tracker', kwargs={'pk': self.object.pk})


class DeleteTracker(UserPassesTestMixin, DeleteView):
    template_name = 'tracker/delete_tracker.html'
    model = Tracker
    context_object_name = 'tracker'
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        tracker = self.get_object()
        project = tracker.project_id
        users_in_project = User.objects.filter(user_team__project=project, user_team__updated_at__isnull=True)
        return self.request.user in users_in_project
