from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User
    """
    class Meta:
        model = User
        fields = ('password', 'first_name', 'last_name', 'email', 'username', )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('is_staff', 'is_superuser', 'is_active',
                            'date_joined', 'username')

    def restore_object(self, attrs, instance=None):
        # call set_password on user object. Without this the password will be
        # stored in plain text.
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user
