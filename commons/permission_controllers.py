import random
from builtins import callable, getattr
from multiprocessing import Manager, Pool, Process


class PraxoPermission:
    def _permission_controller_forsure(self, user_obj, **kwargs):
        l = []
        print(kwargs)
        for key, value in kwargs.items():
            if callable(getattr(user_obj, 'has_perm')):
                print("{0}.{1}".format(key,value))
            l.append(user_obj.has_perm("{0}.{1}".format(key,value)))
        else: l.append(False)
        print("in _permission_controller_forsure and result is:")
        print(l)


def general_permission_controller(user, **kwargs):   
    p = PraxoPermission()
    p._permission_controller_forsure(user, **kwargs)






# Multiproccesing implemented and tested.
# For this kind of cases, Multiprocessing is not usual and handy.
# Using following version of implementation just because of using multiprocessing 
# Gets error. Having it here commented, help us not to test it one more time again.


# Just in case anyone may assume importing these can solve the problem
# from django.contrib.auth.models import User
# from healthrecords import models
# from healthstandards import models
# from commons import models as model1


# def _permission_controller(user, **kwargs):
#     p = Pool()
#     result = p.starmap(_check_permission, user, kwargs)
#     print(result)


# def _check_permission(user_obj, app, perm, res):
#     print('here4')
#     if callable(getattr(user_obj, has_perm)):
#         print("{0}.{1}".format(app,perm))
#         res.append(user_obj.has_perm("{0}.{1}".format(app,perm)))
#     else: res.append(False)
#     print("in _check_permission and params are: {0}, {1}".format(app, perm))
    

# def _permission_controller(user_obj, **kwargs):
#     manager = Manager()
#     d = manager.dict(**kwargs)
#     l, jobs, i = [], [], 0
#     print(kwargs)
#     for key, value in kwargs.items():
#         print('here')
#         p = Process(target=_check_permission, args=(user_obj.id, key, value, l))
#         print('here1')
#         jobs.append(p)
#         print('here2')
#         p.start()
#         print('here3')
#     for proc in jobs:
#         print(proc)
#         proc.join()
#     print("in _permission_controller and result is:")
#     print(l)