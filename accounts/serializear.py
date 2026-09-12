from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from luckhunter.utils import get_absolute_media_url
from .models import LsSettings, LsUser


class LsSettingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = LsSettings
        fields = ['id', 'Project_name', 'Title', 'Logo', 'favicon_icon','Domain','Wallet_commition','System_email','System_email_Password','Create_date','created_by','Update_date','Update_by']
        depth = 2


class LsUserProfileSerializer(serializers.ModelSerializer):
    """The signed-in user's own profile - returned by GET /me/."""

    email = serializers.EmailField(source='user.email', read_only=True)
    Image = serializers.SerializerMethodField()

    class Meta:
        model = LsUser
        fields = [
            'id', 'name', 'email', 'Image', 'Contact_no', 'my_refrral_code',
            'Point', 'my_coines', 'DOJ',
        ]

    @extend_schema_field(OpenApiTypes.URI)
    def get_Image(self, obj):
        return get_absolute_media_url(obj.Image, self.context.get('request'))


class RegisterSerializer(serializers.Serializer):
    """Creates a new User + LsUser profile, mirroring accounts.views.register
    (username is set to the email, matching how the website logs in)."""

    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    email = serializers.EmailField()
    phone_no = serializers.IntegerField()
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email already exists.')
        return value

    def validate_phone_no(self, value):
        if LsUser.objects.filter(Contact_no=value).exists():
            raise serializers.ValidationError('This contact number already exists.')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': "Passwords don't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name', ''),
            email=validated_data['email'],
            password=validated_data['password'],
        )
        full_name = (validated_data['first_name'] + ' ' + validated_data.get('last_name', '')).strip()
        return LsUser.objects.create(
            user=user,
            name=full_name,
            Contact_no=validated_data['phone_no'],
        )


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Logs in with email + password instead of DRF SimpleJWT's default
    username field (this project always sets User.username == email, so
    authentication itself still keys off `username`)."""

    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get(self.username_field)
        password = attrs.get('password')

        user = authenticate(username=email, password=password)
        if user is None:
            raise exceptions.AuthenticationFailed('Email and password are incorrect.', 'no_active_account')

        try:
            profile = LsUser.objects.get(user=user)
        except LsUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('No profile found for this account.', 'no_active_account')

        if not profile.status:
            raise exceptions.AuthenticationFailed('Your account is disabled by admin.', 'account_disabled')

        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }