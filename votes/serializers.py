from rest_framework import serializers
from .models import Vote

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vote
        fields=('id','subject','vote_taken','yes_votes','no_votes')


