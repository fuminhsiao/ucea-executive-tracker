from rest_framework import serializers
from action.models import Action, TypeOfAction, Actor, Topic

class TypeOfActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfAction
        fields = ['id', 'name']  # ✅ 讓前端可以獲取 name

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name']  # ✅ 讓前端可以獲取 name

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']  # ✅ 讓前端可以獲取 name

class ActionSerializer(serializers.ModelSerializer):
    type_of_action = TypeOfActionSerializer(many=True)  # ✅ 直接序列化對象，而不是 ID
    actors = ActorSerializer(many=True)  # ✅ 直接序列化對象，而不是 ID
    topics = TopicSerializer(many=True)  # ✅ 直接序列化對象，而不是 ID

    class Meta:
        model = Action
        fields = '__all__'  # ✅ 確保所有字段都返回
