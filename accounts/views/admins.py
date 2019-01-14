from ..decorators import must_be_type_of
from ..forms import AdminSignUpForm, AdminForm
from django.contrib.auth import login
from ..models import User, Role
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class AdminSignUpView(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        if request.session.is_empty():
            print('session is empty')
        login(self.request, user)
        return redirect('admin_list')
        # return HttpResponse('form created and validated.')

@method_decorator([login_required, must_be_type_of(Role.ADMIN)], name='dispatch')
class AdminListView(ListView):
    model = User
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'accounts/admins/admin.html'

    def get_queryset(self):
        user = self.request.user
        users = User.objects.all()
        # student_interests = student.interests.values_list('pk', flat=True)
        # taken_quizzes = student.quizzes.values_list('pk', flat=True)
        # queryset = Quiz.objects.filter(subject__in=student_interests) \
        #     .exclude(pk__in=taken_quizzes) \
        #     .annotate(questions_count=Count('questions')) \
        #     .filter(questions_count__gt=0)
        # return queryset
        return users

    # EX: 
    # paginate_by = 100  # if pagination is desired
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context

class AdminFormView(FormView):
    template_name = 'accounts/admins/admin_form.html'
    form_class = AdminForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)