from django.urls.base import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from webapp.forms import ProjectForm, TrackerForm
from webapp.models import Project


class ProjectView(ListView):
    context_object_name = 'project'
    model = Project
    template_name = 'project/projects_view.html'
    ordering = ['created_at']


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/project_detail_view.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TrackerForm()
        trackers = context['project'].tracker.order_by('-created_at')
        self.paginate_comments_to_context(trackers, context)
        return context

    def paginate_comments_to_context(self, trackers, context):
        paginator = Paginator(trackers, 2)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        context['paginator'] = paginator
        context['page_obj'] = page
        context['trackers'] = page.object_list
        context['is_paginated'] = page.has_other_pages()


class ProjectCreateView(CreateView):
    template_name = 'project/project_create.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('projects')


class ProjectUpdate(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_update.html'
    success_url = reverse_lazy('projects')


class ProjectDelete(DeleteView):
    template_name = 'project/project_delete.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('projects')
