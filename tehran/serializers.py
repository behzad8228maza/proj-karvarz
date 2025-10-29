from rest_framework import serializers
from .models import tehran


class tehranserializer(serializers.ModelSerializer):

    class Meta:
        model = tehran
        fields = "__all__"
