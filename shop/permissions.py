from rest_framework.permissions import BasePermission


class IsShopAdmin(BasePermission):
    def has_permission(self, request, view):
        # print('<------TEST------>')
        # if request.user.is_superuser:
        #     return True
        allowed_roles = [1]  # Roles: Shop Admin, Category Admin
        user_roles = set(request.user.role.values_list('id', flat=True))
        return bool(user_roles.intersection(allowed_roles))


class IsCategoryAdmin(BasePermission):
    def has_permission(self, request, view):
        # if request.user.is_superuser:
        #     return True
        for role in request.user.role.all():
            if role.id == 3:
                return True


class IsProductAdmin(BasePermission):
    def has_permission(self, request, view):
        # if request.user.is_superuser:
        #     return True
        has_product_admin_role = request.user.role.filter(id=2).exists()
        return has_product_admin_role
