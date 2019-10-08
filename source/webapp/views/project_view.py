from django.urls.base import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from webapp.forms import ProjectForm, TrackerForm
from webapp.models import Project


class ProjectView(ListView):
    context_object_name = 'project'
    model = Project
    template_name = 'project/projects_view.html'
    ordering = ['-created_at']
    paginate_by = 3
    paginate_orphans = 1


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/project_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TrackerForm()
        trackers = context['project'].comments.order_by('-created_at')
        self.paginate_comments_to_context(trackers, context)
        return context

    def paginate_comments_to_context(self, trackers, context):
        paginator = Paginator(trackers, 3, 0)
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
    redirect_url = 'project'


class ProjectUpdate(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_update.html'
    redirect_url = 'project'


class ProjectDelete(DeleteView):
    template_name = 'project/project_delete.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('project_detail')
