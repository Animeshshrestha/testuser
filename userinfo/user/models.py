import uuid

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class TimeStampedUUID(models.Model):

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract=True

class UserManager(BaseUserManager):

	def _create_user(self, username, email, password, **extra_fields):
		if not email:
			raise ValueError('User must have email address')

		email = self.normalize_email(email)
		user = self.model(username=username, email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, username, email=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(username, email, password, **extra_fields)

	def create_superuser(self, username, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')

		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(username, email, password, **extra_fields)


class UserInfo(AbstractBaseUser, PermissionsMixin):

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	username = models.CharField(
		_('username'),
		max_length=150,
		blank=True,
		help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
		error_messages={
			'unique': _("A user with that phone already exists."),
		},

	)
	email = models.EmailField(_('email address'), max_length=50, unique=True, null=True, blank=True)

	is_staff = models.BooleanField(
		_('staff status'),
		default=False,
		help_text=_('Designates whether the user can log into this admin site.'),
	)

	is_active = models.BooleanField(
		_('active'),
		default=True,
		help_text=_(
			'Designates whether this user should be treated as active. '
			'Unselect this instead of deleting accounts.'
		),
	)
	email_confirmed = models.BooleanField(
		_('email active'),
		default=False,
		help_text=_(
			'Designates whether this user should be treated as active. '
			'Unselect this instead of deleting accounts.'
		),
	)
	is_student = models.BooleanField(default=False)
	is_teacher = models.BooleanField(default=False)

	last_login =  models.DateTimeField(_('last_login'), auto_now_add=False, auto_now=False, null=True)

	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True, auto_now=False)

	objects = UserManager()

	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']


class UserProfile(TimeStampedUUID):

	user = models.OneToOneField(UserInfo,on_delete=models.SET_NULL, null=True)
	firstname = models.CharField(max_length=50, null=True, blank=True)
	lastname = models.CharField(max_length=50, null=True, blank=True)
	city = models.CharField(max_length=50, blank=True, null=True)
	country = models.CharField(max_length=50, blank=True, null=True)
	phone_number = models.CharField(max_length=20, null=True, blank=True)
	date_of_birth = models.DateTimeField()
	email = models.EmailField(unique=True, null=True)
	GENDER_CHOICES=[('Male','Male'),
	('Female','Female'),('Others','Others')]
	gender = models.CharField(max_length=20, choices= GENDER_CHOICES)
	describe_about_yourself = models.TextField(blank=True, null=True)

	def __str__(self):
		return ('{} , {}'.format(self.firstname,self.lastname))		

class Education(TimeStampedUUID):
	DEGREE_CHOICES = (
		(0, 'P.hD'),
		(1, 'Master'),
		(2, 'Bachelor'),
		(3, 'Intermediate'),
		(4, 'Other'),
	)
	MARKS_CHOICES = (
	(1,'GPA'),
	(2,'PERCENTAGE'),
	)
	user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True)
	degree = models.IntegerField(choices=DEGREE_CHOICES)

	program = models.CharField(max_length=100)
	board  = models.CharField(max_length=100)
	institution = models.CharField(max_length=100)
	marks = models.IntegerField(choices=MARKS_CHOICES, blank=True, null=True)
	marks_obtained = models.CharField(max_length=10, blank=True, null=True)

	start = models.DateField()
	end = models.DateField(blank=True, null=True)
	currently_studying = models.BooleanField(default=False)
	

	def __str__(self):
		return self.program

class WorkExperience(TimeStampedUUID):
	
	user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True)
	job_title = models.CharField(max_length=100)
	organization = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	responsibilities = models.TextField()
	job_level = models.CharField(max_length=20, null=True, blank=True)
	from_date = models.DateField()
	to_date = models.DateField(blank=True, null=True)
	
	def __str__(self):
		return self.job_title

class Skills(TimeStampedUUID):

	user = models.OneToOneField(UserInfo, on_delete=models.SET_NULL, null=True)
	skill = models.CharField(max_length=50)

	def __str__(self):
		return self.skill

class Training(TimeStampedUUID):

	user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=255)
	institution = models.CharField(max_length=100)
	start_date = models.DateField()
	end_date = models.DateField()

	def __str__(self):
		return self.name

class SocialAccount(TimeStampedUUID):

	user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True)
	account_name = models.CharField(max_length=100)
	url = models.URLField(max_length=200)

	def __str__(self):
		return self.account_name