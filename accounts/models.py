from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    '''
    The Role entries are managed by the system,
    automatically created via a Django data migration.
    '''
    STUDENT = 1
    TEACHER = 2
    SECRETARY = 3
    SUPERVISOR = 4
    ADMIN = 5
    ROLE_CHOICES = (
        (STUDENT, 'student'),
        (TEACHER, 'teacher'),
        (SECRETARY, 'secretary'),
        (SUPERVISOR, 'supervisor'),
        (ADMIN, 'admin'),
    )
    role_id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)

    def __str__(self):
        return self.get_id_display()
        # return str(self.role_id)
    
    def get_id_display(self):
        for key, value in self.ROLE_CHOICES:
            if self.role_id == key:
                return value
        return 'unknown role.'

    def get_role(self):
        for key, value in self.ROLE_CHOICES:
            if self.role_id == value:
                return {'role_id':key, 'role_name': value}
        return 'unknown role.'

class User(AbstractUser):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    roles = models.ManyToManyField(Role)

    class Meta:
        db_table = 'accounts_user'
        managed = True
        verbose_name = u'User'
        verbose_name_plural = u'Users'
        # permissions = (("can_deliver_pizzas", "Can deliver pizzas"),)
        # Latest by priority descending, order_date ascending.
        # get_latest_by = ['-priority', 'order_date']
        # indexes = [
        #     models.Index(fields=['last_name', 'first_name']),
        #     models.Index(fields=['first_name'], name='first_name_idx'),
        # ]

        
    @property
    def popularity(self):
        likes = 12
        time = 12 #hours since created
        return likes / time if time > 0 else likes

class Profile(models.Model):
    #_safedelete_policy = NO_DELETE
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_profile', primary_key=True, on_delete=models.PROTECT)
    # Columns
    birth_date = models.DateField(blank=True, null=True)
    GENDER_CHOICES = (
        ('F', 'Female',),
        ('M', 'Male',),
        ('U', 'Unsure',),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null = False,
        default = 'U'
    )
    cell_phone = models.CharField(max_length=31, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)

    @property
    def age(self):
        return int((datetime.now().date() - self.birth_date).days / 365.25)

    def clean(self):
        print('Member is Cleaned.')
    
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        print('Member is clean_fielded.')

    def __str__(self):
        return self.user.username






