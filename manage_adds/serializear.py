from .models import LsAdds
from rest_framework import serializers

class LsAddserializers(serializers.ModelSerializer):
    class Meta:
        model = LsAdds
        fields = ['id', 'Title', 'Pogition', 'Description', 'Status','create_date']
        depth = 2