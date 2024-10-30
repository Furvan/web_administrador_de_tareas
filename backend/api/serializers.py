from rest_framework import serializers
from .models import Task, SuperuserTaskVisibility, CustomUser

class TaskSerializer(serializers.ModelSerializer):
    visible_to = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'user', 'state', 'is_superuser_task', 'visible_to_all', 'visible_to']
        read_only_fields = ['user']

    def create(self, validated_data):
        visible_to = validated_data.pop('visible_to', [])
        task = Task.objects.create(**validated_data)
        task.visible_to.set(visible_to)
        return task

    def update(self, instance, validated_data):
        visible_to = validated_data.pop('visible_to', [])
        instance = super().update(instance, validated_data)
        instance.visible_to.set(visible_to)
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_superuser', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance