from .models import LsQerues
from rest_framework import serializers


class LsQeruesSerializers(serializers.ModelSerializer):
    class Meta:
        model = LsQerues
        fields = ['id', 'Complate_id', 'Type', 'Title', 'description','Answer','Open_status','Crate_date','Update_date','Create_by']
        depth = 2