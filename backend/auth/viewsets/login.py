from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from ..serializers.login import LoginSerializer
from account.models import User
from django.contrib.auth.models import Permission, Group
from ..serializers.register import SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

class LoginViewSet(ViewSet):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        self.account_wizard(request=request)
        serializer =self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data,
                        status=status.HTTP_200_OK)
    
    def account_wizard(self, request):
        if not User.objects.all().exists():  #if no user exists create the admin user
            self.create_admin_user(request)

    def create_admin_user(self, request):
        obj = {
            'username':request.data['username'],
            'password':request.data['password'],
            'email':request.data['username'] + "@gmail.com",
            "firstName":request.data['username'],
            "lastName":request.data['username'],
            "gender":"M",
            'is_superuser':True,
            'is_staff':True,
            'role':"admin",
            'is_active':True,

        }
        serializer = SignupSerializer(data=obj)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        '''check if user is added to a group otherwise 
        fetch user choosen group and add user to the group
        '''
        group = Group.objects.get(name="admin")
        user.groups.add(group)

        '''token based authentication instead of 
        direct session, cookie access management
        '''
        refresh = RefreshToken.for_user(user)
    