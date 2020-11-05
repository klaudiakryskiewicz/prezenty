from datetime import date

from django.db import models
from django.contrib.auth.models import User


class Family(models.Model):
    name = models.CharField(max_length=120)

    def member_count(self):
        return Member.objects.filter(family_id=self.id).count()

    def __str__(self):
        return f"{self.name} {self.member_count()}"


class Member(models.Model):
    name = models.CharField(max_length=120)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    main_member = models.BooleanField(default=True)

    class Meta:
        unique_together = [['name', 'family']]

    def wish_count(self):
        return Wish.objects.filter(member_id=self.id).count()

    def no_of_free_wishes(self):
        return Wish.objects.filter(member=self, present__isnull=True).count()

    def __str__(self):
        return f"{self.name}"


class Wish(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=500, null=True, blank=True)
    link = models.CharField(max_length=300, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='wishes')

    def is_booked(self):
        if Present.objects.get(wish_id=self.id):
            return True
        return False

    def __str__(self):
        return f"{self.name} {self.description} {self.link}"


class Present(models.Model):
    wish = models.OneToOneField(Wish, on_delete=models.CASCADE)
    is_bought = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.wish.name} {self.wish.member.name} {self.is_bought}"
