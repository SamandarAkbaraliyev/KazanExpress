from django.contrib.auth import get_user_model, login
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .serializers import UserSerializer
from django.views.decorators.vary import vary_on_cookie
from django.views.decorators.cache import cache_page

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    # @cache_page(60 * 15)
    @vary_on_cookie
    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
# class LoginView(views.APIView):
#     throttle_classes = (UserLoginRateThrottle, )
#
#     def post(self, request, format=None):
#         serializer = serializers.LoginSerializer(data=self.request.data,
#                                                  context={'request': self.request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return Response(None, status=status.HTTP_202_ACCEPTED)
