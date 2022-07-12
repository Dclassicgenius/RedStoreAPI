from rest_framework import serializers
from accounts.models import Account, UserProfile
from phonenumber_field.modelfields import PhoneNumberField

class UserProfileSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}


class AccountCreationSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=80, required=True)
    phone_number = PhoneNumberField(blank=False, null=False)
    password = serializers.CharField(min_length=8, write_only=True, style={'input_type':'password'})

    profile = UserProfileSerializer(required=False)


    class Meta:
        model = Account
        fields = ('id','first_name', 'last_name', 'username', 'email', 'phone_number', 'password', 'profile', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True}}

        read_only_fields = ('id','is_admin', 'is_staff', 'is_active', 'is_superuser', 'date_joined', 'last_login')

    def validate(self, attrs):
        username_exists = Account.objects.filter(username=attrs['username']).exists()

        if username_exists:
            raise serializers.ValidationError(detail="Username exists")

        email_exists = Account.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise serializers.ValidationError(detail="user with email exists")

        phone_number_exists = Account.objects.filter(phone_number=attrs['phone_number']).exists()

        if phone_number_exists:
            raise serializers.ValidationError(detail="User with phone_number exists")

        return super().validate(attrs)

    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = Account.objects.create(
            first_name = validated_data.get('first_name'),
            last_name = validated_data.get('last_name'),
            username = validated_data.get('username'),
            email = validated_data.get('email'),
            phone_number = validated_data.get('phone_number'),
            
        )
        user.set_password(validated_data['password'])
        
        UserProfile.objects.create(
            user = user,
            address = profile_data.get('address'),
            profile_picture = profile_data.get('profile_picture'),
            city = profile_data.get('city'),
            state = profile_data.get('state'),
            country = profile_data.get('country')
        )

        user.save()
        return user
    

class AccountDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=80, required=True)
    phone_number = PhoneNumberField(blank=False, null=False)

    profile = UserProfileSerializer(required=False)


    class Meta:
        model = Account
        fields = ('id','first_name', 'last_name', 'username', 'email', 'phone_number', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

        read_only_fields = ('id',)

    
    def update(self, instance, validated_data):

        profile_data = validated_data.pop('profile')
        profile = instance.profile
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()

        
        for data in profile_data:
            setattr(profile, data, profile_data[data])
        profile.save()

        return instance