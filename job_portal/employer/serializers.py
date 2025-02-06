from rest_framework import serializers
from users.models import EmployerProfile

class EmployerProfileSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source="user.id")
    class Meta:
        model = EmployerProfile
        fields = ''
        read_only_fields = [ 'is_approved', 'user'] 