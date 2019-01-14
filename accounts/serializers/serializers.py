from .models import Member
from rest_framework import serializers
from commons import serializers as cserializers


class ServiceaccountMemberSerializer(cserializers.DynamicFieldsModelSerializer):
    hello = serializers.SerializerMethodField('get_excluder') # define separate field
    exclud = serializers.SerializerMethodField() # define separate field
    # popularity = serializers.IntegerField() # popularity is a defined method in the model
    
    class Meta:
        model = Member
        fields = ('id', 'user_uuid', 'hello', 'exclud', 'popularity')
        read_only_fields = ('popularity', 'hello', 'exclud',)
        # extra_kwargs = {'popularity': {'read_only': True}, 'hello': {'read_only': True}, 'exclud': {'read_only': True}, 'id': {'read_only': True}}
        # fields = '__all__'
        # exclude = ['user_uuid']

    def create(self, validated_data):
        return Member.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.user_uuid = validated_data.get('user_uuid', instance.user_uuid)
        instance.save()
        return instance

    # def update(self, instance, validated_data):
    #     for f in UserSerializer.Meta.fields + UserSerializer.Meta.write_only_fields:
    #         set_attr(instance, f, validated_data[f])
    #     instance.set_password(validated_data['password'])
    #     instance.save()
    #     return instance

    def get_excluder(self, obj):
        # return obj.id ::Example
        return ''

    def get_exclud(self, obj):
        # return ''
    
    def _includer():
        return '_includer'





    

