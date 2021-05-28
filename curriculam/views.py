from django.shortcuts import render
from django.views.generic import (TemplateView, DetailView, ListView, FormView, CreateView,
                  UpdateView, DeleteView)
from curriculam.models import Standard, Subject, Lession, Comment
from curriculam.forms import LessionForm, CommentForm,ReplyForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Create your views here.
class StandardListView(ListView):
    context_object_name='standards'
    model= Standard
    template_name='curriculam/standard_list_view.html'

class SubjectListView(DetailView):
    context_object_name = 'standards'
    model = Standard
    template_name = 'curriculam/subject_list_view.html'

class LessionListView(DetailView):
    context_object_name = 'subjects'
    model = Subject
    template_name = 'curriculam/lession_list_view.html'

class LessionDetailView(DetailView, FormView):
    context_object_name='lessions'
    model= Lession
    template_name='curriculam/lession_detail_view.html'

    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super(LessionDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(request=self.request)
        # context['comments'] = Comment.objects.filter(id=self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)
        # print("the form name is : ", form)
        # print("form name: ", form_name)
        # print("form_class:",form_class)

        if form_name=='form' and form.is_valid():
            print("comment form is returned")
            return self.form_valid(form)
        elif form_name=='form2' and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)

    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy('curriculam:lession_detail',kwargs={'standard':standard.slug,
                                                             'subject':subject.slug,
                                                             'slug':self.object.slug})

class LessionCreateView(CreateView):
    form_class = LessionForm
    context_object_name = 'subject'
    model= Subject
    template_name = 'curriculam/lession_create.html'

    def get_success_url(self):
        self.object=self.get_object()
        standard = self.object.standard
        return reverse_lazy('curriculam:lession_list',kwargs={'standard':standard.slug,
                                                               'slug':self.object.slug})

    def form_valid(self, form, *args, **kwargs):
        self.object=self.get_object()
        fm=form.save(commit=False)
        fm.created_by = self.request.user
        fm.Standard = self.object.standard
        fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class LessionUpdateView(UpdateView):
    fields=('name','position','video','ppt','Notes')
    model=Lession
    template_name='curriculam/lession_update.html'
    context_object_name='lessions'

class LessionDeleteView(DeleteView):
    model= Lession
    context_object_name='lessions'
    template_name='curriculam/lession_delete.html'

    def get_success_url(self):
        print(self.object)
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy('curriculam:lession_list',kwargs={'standard':standard.slug,'slug':subject.slug})
