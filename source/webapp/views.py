from django.shortcuts import render, get_object_or_404, redirect
from django.urls.base import reverse
from django.views.generic import TemplateView, ListView, DetailView, View
from webapp.forms import TrackerForm, StatusForm, TypeForm
from webapp.models import Tracker, Status, Type


class CreateView(View):
    form_class = None
    template_name = None
    redirect_url = ''
    model = None

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_redirect_url(self):
        return reverse(self.redirect_url, kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = self.model.objects.create(**form.cleaned_data)
        return redirect(self.get_redirect_url())

    def form_invalid(self, form):
        return render(self.request, self.template_name, context={'form': form})

class IndexView(ListView):
    context_object_name = 'tracker'
    model = Tracker
    template_name = 'index.html'
    paginate_by = 3
    paginate_orphans = 1


class TrackerView(DetailView):
    model = Tracker
    template_name = 'tracker.html'


class TrackerCreateView(CreateView):
    template_name = 'add_tracker.html'
    model = Tracker
    form_class = TrackerForm
    redirect_url = 'tracker'

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


class UpdateView(View):
    context_key = 'object'
    form_class = None
    template_name = None
    model = None
    redirect_url = ''
    key_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.get_object())
        context = {'form': form}
        context[self.context_key] = self.get_object()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(instance=self.get_object(), data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_object(self):
        pk = self.kwargs.get(self.key_kwarg)
        return get_object_or_404(self.model, pk=pk)

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_redirect_url())

    def form_invalid(self, form):
        context = {'form': form}
        context[self.context_key] = form
        return render(self.request, self.template_name, context)

    def get_redirect_url(self):
        return reverse(self.redirect_url, kwargs={'pk': self.object.pk})


class DeleteView(TemplateView):
    context_key = 'object'
    form_class = None
    template_name = None
    model = None
    redirect_url = ''
    key_kwarg = 'pk'

    def get(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_key] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.get_object())
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_object(self):
        pk = self.kwargs.get(self.key_kwarg)
        return get_object_or_404(self.model, pk=pk)

    def form_valid(self, form):
        self.object = form
        self.object.delete()
        return redirect(self.get_redirect_url())

    def form_invalid(self, form):
        context = {'form': form}
        context[self.context_key] = form
        return render(self.request, self.template_name, context)

    def get_redirect_url(self):
        return reverse(self.redirect_url)


class DeleteTracker(DetailView):
    model = Tracker
    form_class = TrackerForm
    template_name = 'delete_tracker.html'
    redirect_url = 'index'


class TracerUpdate(UpdateView):
    model = Tracker
    form_class = TrackerForm
    template_name = 'edit.html'
    redirect_url = 'tracker'


class UpdateStatusView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'edit_status.html'
    redirect_url = 'status_views'


class UpdateTypeView(UpdateView):
    model = Type
    form_class = TypeForm
    template_name = 'edit_type.html'
    redirect_url = 'type_views'

# я облажался с этой домашкой ((
