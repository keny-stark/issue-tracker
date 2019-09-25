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
        context['article'] = get_object_or_404(Tracker, pk=article_pk)
        return context


class CreateView(View):
    def create(self, request, *args, **kwargs):
        if request.method == 'GET':
            form = TrackerForm()
            return render(request, 'add_tracker.html', context={'form': form})
        elif request.method == 'POST':
            form = TrackerForm(data=request.POST)
            if form.is_valid():
                tracker = Tracker.objects.create(
                    title=form.cleaned_data['title'],
                    author=form.cleaned_data['author'],
                    text=form.cleaned_data['text'],
                    category=form.cleaned_data['category']
                )
                return redirect('tracker', pk=tracker.pk)
            else:
                return render(request, 'add_tracker.html', context={'form': form})


class TracerUpdate(View):
    def update(self, request, pk):
        tracker = get_object_or_404(Tracker, pk=pk)
        if request.method == 'GET':
            form = TrackerForm(data={
                'title': tracker.title,
                'author': tracker.author,
                'text': tracker.text,
                # 'category': tracker.category_id
            })
            return render(request, 'edit.html', context={'form': form, 'article': tracker})
        elif request.method == 'POST':
            form = TrackerForm(data=request.POST)
            if form.is_valid():
                tracker.title = form.cleaned_data['title']
                tracker.author = form.cleaned_data['author']
                tracker.text = form.cleaned_data['text']
                tracker.category = form.cleaned_data['category']
                tracker.save()
                return redirect('article_view', pk=tracker.pk)
            else:
                return render(request, 'edit.html', context={'form': form, 'article': tracker})


class DeleteTracker(View):
    def delete(self, request, pk):
        tracker = get_object_or_404(Tracker, pk=pk)
        if request.method == 'GET':
            return render(request, 'edit.html', context={'tracker': tracker})
        elif request.method == 'POST':
            tracker.delete()
            return redirect('index')
