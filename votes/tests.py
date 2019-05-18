import json
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from .models import Vote
from .serializers import VoteSerializer
from .views import VoteList, VoteDetail


class VoteModelTests(TestCase):

    def test_str(self):
        time = timezone.now()
        vote = Vote.objects.create(
            subject="Should there be regime change in ZIM?",
            yes_votes=10,
            no_votes=15,
            vote_taken=time,
        )
        expected_string = "Regime change in ZIM? - 10/15 on {}".format(
            time.strftime('%c'),
        )
        assert expected_string == str(vote)


class VoteSerializerTests(TestCase):

    def test_serialization(self):
        time = timezone.now()
        vote = Vote.objects.create(
            subject="Is Jobs better than Gates",
            yes_votes=100,
            no_votes=100,
            vote_taken=time,
        )
        serialized = VoteSerializer(vote).data
        assert vote.id == serialized['id']
        assert vote.subject == serialized['subject']
        assert vote.yes_votes == serialized['yes_votes']
        assert vote.no_votes == serialized['no_votes']


class VoteViewTests(TestCase):

    def test_vote_list(self):
        vote = Vote.objects.create(subject='More Linux, Less Windows?')
        factory = APIRequestFactory()
        request = factory.get('/votes/', format='json')
        response = VoteList.as_view()(request)
        assert 200 == response.status_code
        response.render()
        assert vote.subject == json.loads(response.content)['results'][0]['subject']

    def test_vote_list_with_auth(self):
        vote = Vote.objects.create(subject='More Linux, Less Windows?')
        user = User.objects.create(username='api')
        factory = APIRequestFactory()
        request = factory.get('/votes/', format='json')
        force_authenticate(request, user=user)
        response = VoteList.as_view()(request)
        assert 200 == response.status_code
        response.render()
        assert vote.subject == json.loads(response.content)['results'][0]['subject']

    def test_vote_create(self):
        user = User.objects.create(username='api')
        factory = APIRequestFactory()
        request = factory.post('/votes/', {'subject': 'More Linux, Less Windows?'}, format='json')
        force_authenticate(request, user=user)
        response = VoteList.as_view()(request)
        assert 201 == response.status_code

    def test_vote_create_no_auth(self):
        factory = APIRequestFactory()
        request = factory.post('/votes/', {'subject': 'More Linux, Less Windows?'}, format='json')
        response = VoteList.as_view()(request)
        assert 403 == response.status_code

    def test_vote_detail(self):
        vote = Vote.objects.create(subject='More Linux, Less Windows?!')
        factory = APIRequestFactory()
        request = factory.get('/votes/')
        response = VoteDetail.as_view()(request, pk=vote.id)
        assert 200 == response.status_code
assert vote.subject == response.data['subject']
