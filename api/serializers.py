from rest_framework import serializers
from projects.models import Project , Tag , Review
from users.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
            
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    # overrides the current owner
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    # add atribute
    review = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__' # njejt sikur forms

    # adding reviews
    def get_review(self , obj):
        # obj = objekt i qe dojm me serializu
        reviews = obj.review_set.all()
        # serialzing
        serializer = ReviewSerializer(reviews , many=True)
        return serializer.data


