from django.contrib.auth.models import AbstractUser, Permission
from django.db.models import CharField, Model, TextChoices, ForeignKey, CASCADE, ManyToManyField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for My Awesome Project.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    role = ManyToManyField('Role', blank=True)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        print(user)
        return user
        # user = super().save()
        # if user.groups:
        #     print(self.groups.all())
        # for group in instance.groups.all():
        #     print(group)
        #     for group_permission in group.permissions.all():
        #         instance.user_permissions.add(group_permission)


class RoleChoices(TextChoices):
    SHOP_ADMIN = 'Shop admin'
    PRODUCT_ADMIN = 'Product admin'
    CATEGORY_ADMIN = 'Category admin'


class Role(Model):
    role = CharField(max_length=32, choices=RoleChoices.choices)

    def __str__(self):
        return self.role
