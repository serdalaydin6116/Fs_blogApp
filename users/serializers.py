from rest_framework import serializers, validators
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from dj_rest_auth.serializers import TokenSerializer



class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

     ##forms.py version 
     #(we can handle this by overwriting and checking the uniqueness of the emails that were entered ın the afore-mentioned codes)
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Please use another Email, that one already taken")
    #     return email
   

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2'
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }

    def create(self, validated_data):
        password = validated_data.get("password")
        validated_data.pop("password2")

        user = User.objects.create(**validated_data)
        user.password = make_password(password)
        user.save()
        return user

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "The Passwords you entered do not match with each other..."})
        return data

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=(

            'username',
            'email',
        )
    
class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')

class CustomTokenSerializer(TokenSerializer):

    user = UserSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ('key', 'user')

    

