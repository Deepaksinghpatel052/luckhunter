from .models import LsSettings
from rest_framework import serializers

class LsSettingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = LsSettings
        fields = ['id', 'Project_name', 'Title', 'Logo', 'favicon_icon','Domain','Wallet_commition','System_email','System_email_Password','Create_date','created_by','Update_date','Update_by']
        depth = 2