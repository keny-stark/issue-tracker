from abc import ABC
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy
from django.core.paginator import Paginator
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from webapp.forms import ProjectForm, SimpleSearchForm, TeamForm
from webapp.models import Project, Team
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from webapp.mixins import StatsMixin


class ProjectView(StatsMixin, ListView):
    context_object_name = 'project'
    model = Project
    template_name = 'project/projects_view.html'
    ordering = ['created_at']

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
            query = Q(title__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class ProjectDetailView(StatsMixin, DetailView):
    model = Project
    template_name = 'project/project_detail_view.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] = TrackerProjectForm()
        context['users_in_project'] = User.objects.filter(user_team__project=context['project'],
                                                          user_team__updated_at__isnull=True)
        trackers = context['project'].tracker_project.order_by('-created_at')
        self.paginate_comments_to_context(trackers, context)
        return context

    def paginate_comments_to_context(self, trackers, context):
        paginator = Paginator(trackers, 8)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        context['paginator'] = paginator
        context['page_obj'] = page
        context['trackers'] = page.object_list
        context['is_paginated'] = page.has_other_pages()


class ProjectCreateView(LoginRequiredMixin, StatsMixin, CreateView):
    template_name = 'project/project_create.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('projects')
    raise_exception = PermissionDenied

    def form_valid(self, form):
        users = form.cleaned_data.pop('users').values('pk')
        self.object = form.save()
        self.create_team(users)
        return HttpResponseRedirect(self.get_success_url())

    def create_team(self, users):
        users_team = list(users)
        users_team.append({'pk': self.request.user.pk})
        for user_obj in users_team:
            if user_obj:
                Team.objects.create(project=self.object, user_id=user_obj.get('pk'))


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        users = User.objects.exclude(pk=self.request.user.pk)
        kwargs['users'] = users
        return kwargs

    def get_success_url(self):
        return reverse('webapp:project_detail', kwargs={'pk': self.object.pk})


class ProjectUpdate(UserPassesTestMixin, StatsMixin, LoginRequiredMixin, UpdateView, ABC):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_update.html'
    success_url = reverse_lazy('projects')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        users = User.objects.exclude(pk=self.request.user.pk)
        kwargs['users'] = users
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        del form.fields['users']
        return form

    def test_func(self):
        project = Project.objects.get(pk=self.kwargs['pk'])
        team = project.project_user_team.filter(user=self.request.user)
        if len(team) != 0:
            return True
        return False

# [user1, user2, user3, user4] post data
# [user1, user2] initial
# create()

# [user2, user3] post data
# [user1, user2, user3, user4] initial
# delete()




class TeamUpdate(UserPassesTestMixin, StatsMixin, LoginRequiredMixin, UpdateView, ABC):
    model = Team
    form_class = TeamForm
    # template_name = 'project/project_update.html'
    success_url = reverse_lazy('projects')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        users = User.objects.exclude(pk=self.request.user.pk)
        kwargs['users'] = users
        return kwargs

    def test_func(self):
        team = Team.objects.get(pk=self.kwargs['pk'])
        team_in_team = team.objects.filter(user=self.request.user)
        if len(team_in_team) != 0:
            return True
        return False


class ProjectDelete(UserPassesTestMixin, StatsMixin, DeleteView):
    template_name = 'project/project_delete.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('projects')

    def test_func(self):
        project = Project.objects.get(pk=self.kwargs['pk'])
        team = project.project_user_team.filter(user=self.request.user)
        if len(team) != 0:
            return True
        return False
