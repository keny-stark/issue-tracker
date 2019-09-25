from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from webapp.forms import TrackerForm, Status, Type
from webapp.models import Tracker


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracker'] = Tracker.objects.all()
        return context


class TrackerView(TemplateView):
    template_name = 'tracker.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = kwargs.get('pk')
        context['tracker'] = get_object_or_404(Tracker, pk=article_pk)
        return context


class CreateView(View):

    def get(self, request, *args, **kwargs):
        form = TrackerForm()
        return render(request, 'add_tracker.html', context={'form': form})

    def post(self, request, *args, **kwargs):
            form = TrackerForm(data=request.POST)
            if form.is_valid():
                tracker = Tracker.objects.create(
                    summary=form.cleaned_data['summary'],
                    description=form.cleaned_data['description'],
                    status=form.cleaned_data['status'],
                    type=form.cleaned_data['type']
                )
                return redirect('tracker', pk=tracker.pk)
            else:
                return render(request, 'add_tracker.html', context={'form': form})


class TracerUpdate(View):

    def get(self, request, pk):
        tracker = get_object_or_404(Tracker, pk=pk)
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
