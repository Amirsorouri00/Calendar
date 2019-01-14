from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import Role, User
from commons import serializers as cserializers


class AdminSerializer(cserializers.DynamicFieldsModelSerializer):
    hello = serializers.SerializerMethodField('get_excluder') # define separate field
    exclud = serializers.SerializerMethodField() # define separate field
    # popularity = serializers.IntegerField() # popularity is a defined method in the model
    
    class Meta:
        model = User
        fields = ('id', 'uuid', 'hello', 'roles', 'exclud', 'popularity', 'username', 'password')
        read_only_fields = ('popularity', 'hello', 'exclud', 'roles')
        # extra_kwargs = {'popularity': {'read_only': True}, 'hello': {'read_only': True}, 'exclud': {'read_only': True}, 'id': {'read_only': True}}
        # fields = '__all__'
        # exclude = ['user_uuid']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
        # return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.uuid = validated_data.get('uuid', instance.uuid)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def get_excluder(self, obj):
        # return obj.id :Example
        return 'excluder'

    def get_exclud(self, obj):
        # return ''
        return 'exclud'
    
    def _includer():
        return '_includer'
