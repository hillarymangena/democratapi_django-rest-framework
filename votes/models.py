from django.db import models
from django.utils import timezone

class Vote(models.Model):
    subject = models.CharField(max_length=255)
    vote_taken = models.DateTimeField(default=timezone.now)
    yes_votes = models.IntegerField(blank=True, null=True)
    no_votes = models.IntegerField(blank=True, null=True)

    #Beautify for viewing it in admin

    def __str__(self):
        return '{subject} - {yes_votes}/{no_votes} on {vote_taken}'.format(
            subject=self.subject,
            yes_votes=self.yes_votes,
            no_votes=self.no_votes,
            vote_taken=self.vote_taken.strftime('%C')
        )


