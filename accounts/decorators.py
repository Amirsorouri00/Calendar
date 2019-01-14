from .models import Role
from django.contrib.auth import REDIRECT_FIELD_NAME
# from django.core.exceptions import PermissionDenied # may needed inside function: pure_must_be_type_of
from django.contrib.auth.decorators import user_passes_test


def _pure_must_be_type_of(user_type, function=None):
    def wrap(request_user, *args, **kwargs):
        # print(request_user)
        for role in request_user.roles.all():
            if user_type == role.role_id and request_user.is_active:
                # print('Inside "pure_must_be_type_of" function. and user type which is passed through is = {0}'.format(True))
                # return function(request, *args, **kwargs)
                return True
            else:
                # print('Inside "pure_must_be_type_of" function. and user type which is passed through is = {0}'.format(False))
                # raise PermissionDenied
                return False
    wrap.__doc__ = function.__doc__
    # wrap.__name__ = function.__name__
    return wrap

def must_be_type_of(user_type, function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a specific type of User,
    redirects to the log-in page if necessary.
    '''
    # print('Inside "must_be_type_of" function. and user type which is passed through is = {0} and function is\
    #  {1}'.format(user_type, function))
    result = _pure_must_be_type_of(user_type, function)
    actual_decorator = user_passes_test(
        # lambda u: pure_must_be_type_of(user_type, function),
        _pure_must_be_type_of(user_type, function),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator






def must_be_type_of_student():
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.id == Role.STUDENT,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_student,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a teacher,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_teacher,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator