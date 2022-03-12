from rest_framework import serializers
from .models import LsUserWallet

class LsUserWalletSerializers(serializers.ModelSerializer):
    class Meta:
        model = LsUserWallet
        fields = ['id', 'Wallet_id', 'user', 'wallet_admont', 'Wallet_status']
        depth = 2