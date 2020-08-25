from rest_framework import serializers
from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username','email','first_name',
                'last_name', 'password', 'password2'
                )
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = User(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password !=password2:
            raise serializers.ValidationError({"password":"Password don't match."})
        user.set_password(password)
        user.save()
        return user


class UserPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk','email', 'username')


class ChangePasswordResetSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class UserChangePasswordResetSerializer(serializers.ModelSerializer):

    new_password = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('password', 'new_password'
                )
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = User()
        password = self.validated_data['password']
        new_password = self.validated_data['new_password']
        user.set_password(password)
        user.save()
        return user