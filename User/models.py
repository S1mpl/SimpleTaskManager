from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Email непременно должен быть указан')

        user = self.model(
            email=UserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_developer(self, email, password=None):
        if not email:
            raise ValueError('Email непременно должен быть указан')

        user = self.model(
            email=UserManager.normalize_email(email),
        )

        user.set_password(password)
        user.role = 'Developer'
        user.save(using=self._db)
        return user

    def create_manager(self, email, password=None):
        if not email:
            raise ValueError('Email непременно должен быть указан')

        user = self.model(
            email=UserManager.normalize_email(email),
        )

        user.set_password(password)
        user.role = 'Manager'
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.role = 'Admin'
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin, models.Model):

    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='Email'
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=255
    )
    firstname = models.CharField(
        verbose_name='Имя',
        max_length=40,
        null=True,
        blank=True
    )
    lastname = models.CharField(
        verbose_name='Фамилия',
        max_length=40,
        null=True,
        blank=True
    )
    role = models.CharField(
        max_length=255,
        verbose_name='Права пользователя'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name='Админ'
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Админ'
    )
    register_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации'
    )

    def get_full_name(self):
        return self.email


    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.email

    def __str__(self):
        return  self.email


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ['-register_date']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
