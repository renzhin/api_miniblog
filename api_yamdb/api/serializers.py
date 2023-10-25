from rest_framework import serializers

from titles.models import Comment, Review


CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'author', 'text', 'review_id', 'pub_date')
        model = Comment
        read_only_fields = ('review_id', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        fields = ('id', 'author', 'text', 'score', 'title_id', 'pub_date')
        model = Review
        read_only_fields = ('title_id', 'pub_date',)
