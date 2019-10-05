from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, View, ListView, CreateView, DetailView
from webapp.forms import TrackerForm, StatusForm, TypeForm
from webapp.models import Tracker, Status, Type


class IndexView(ListView):
    context_object_name = 'tracker'
    model = Tracker
    template_name = 'index.html'
    paginate_by = 3
    paginate_orphans = 1


# class DetailView(TemplateView):
#     model = None
#     context_key = 'tracker'
#
#     def get_context_data(self, **kwargs):
#         tracker_pk = kwargs.get('pk')
#         context = super().get_context_data(**kwargs)
#         context[self.context_key] = get_object_or_404(self.model, pk=tracker_pk)
#         return context


class TrackerView(DetailView):
    model = Tracker
    template_name = 'tracker.html'


class TrackerCreateView(CreateView):
    template_name = 'add_tracker.html'
    model = Tracker
    form_class = TrackerForm

    def get_success_url(self):
        return reverse('tracker', kwargs={'pk': self.object.pk})


class TracerUpdate(View):

    def get(self, request,  *args, **kwargs):
        tracker = get_object_or_404(Tracker, pk=kwargs.get('pk'))
        form = TrackerForm(data={
            'title': tracker.summary,
            'author': tracker.description,
            'text': tracker.status,
            'category': tracker.type
        })
        return render(request, 'edit.html', context={'form': form, 'tracker': tracker})

    def post(self, request, pk):
        tracker = get_object_or_404(Tracker, pk=pk)
        form = TrackerForm(data=request.POST)
        if form.is_valid():
            tracker.summary = form.cleaned_data['summary']
            tracker.description = form.cleaned_data['description']
            tracker.status = form.cleaned_data['status']
            tracker.type = form.cleaned_data['type']
            tracker.save()
            return redirect('tracker', pk=tracker.pk)
        else:
            return render(request, 'edit.html', context={'form': form, 'tracker': tracker})


class DeleteTracker(View):

    def get(self, request, pk):
        tracker = get_object_or_404(Tracker, pk=pk)
        return render(request, 'delete_tracker.html', context={'tracker': tracker})

    def post(self, request, pk):
        tracker = get_object_or_404(Tracker, pk=pk)
        tracker.delete()
        return redirect('index')


class StatusView(ListView):
    context_object_name = 'status'
    model = Status
    template_name = 'status.html'


class TypeView(ListView):
    context_object_name = 'type'
    model = Type
    template_name = 'type.html'


class TypeAddView(CreateView):
    form_class = TypeForm
    template_name = 'add_type.html'
    model = Type

    def get_success_url(self):
        return reverse('type_views')


def delete_type(request, pk):
    type = get_object_or_404(Type, pk=pk)
    type.delete()
    return redirect('type_views')


def update_type(request, pk):
        type = get_object_or_404(Type, pk=pk)
        if request.method == 'GET':
            form = TypeForm(data={
                'type': type.type
            })
            return render(request, 'edit _type.html', context={
                'type': type, 'form': form})
        elif request.method == "POST":
            form = TypeForm(data=request.POST)
            if form.is_valid():
                type.type = form.cleaned_data['type']
                type.save()
                return redirect('type_views')
            else:
                return render(request, 'edit _type.html', context={'form': form, 'type': type})


class StatusAddView(CreateView):
    form_class = StatusForm
    template_name = 'add_status.html'
    model = Status

    def get_success_url(self):
        return reverse('status_views')


def delete_status(request, pk):
    status = get_object_or_404(Status, pk=pk)
    status.delete()
    return redirect('status_views')


def update_status(request, pk):
        status = get_object_or_404(Status, pk=pk)
        if request.method == 'GET':
            form = StatusForm(data={
                'status': status.status
            })
            return render(request, 'edit_status.html', context={
                'status': status, 'form': form})
        elif request.method == "POST":
            form = StatusForm(data=request.POST)
            if form.is_valid():
                status.status = form.cleaned_data['status']
                status.save()
                return redirect('status_views')
            else:
                return render(request, 'edit_status.html', context={'form': form, 'status': status})


