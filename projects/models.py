"""
drawsql.app - per me vizatu qysh lidhen databazat
"""
from django.db import models

from users.models import Profile

import uuid
# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile , on_delete=models.SET_NULL, null=True , blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True , blank=True)
    # null = Database ; blank = Django
    featured_image = models.ImageField(null=True , blank=True , default="default.jpg")
    demo_link = models.CharField(max_length=2000 , null=True , blank=True)
    source_link = models.CharField(max_length = 2000,null=True , blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0 , null=True , blank=True)
    vote_ratio = models.IntegerField(default=0 , null=True , blank=True)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , 
                        primary_key=True , editable=False)

#   @property - mundson me thirr funkcionin si variabel    

    def __str__(self):
        return self.title

    class Meta:
       # ordering = ['created']  -modelField i paraqet postimet prej nga ma heret qe u postu
        ordering = ['-vote_ratio','-vote_total','title'] # i paraqet postimet nga ajo me shum me vota edhe reviews

    # get owner id for votes
    @property
    def reviewers(self):
#       queryset = queries reviews 
#       values_list = This is similar to values() except that instead of returning dictionaries,
#       it returns tuples when iterated over. Each tuple contains the value from the respective field or 
#       expression passed into the values_list() call — so the first item is the first field ;
#       If you only pass in a single field, you can also pass in the flat parameter. If True, 
#       this will mean the returned results are single values, rather than one-tuples. 

        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        # merr kejt reviews
        reviews = self.review_set.all()
        # filtron reviews sipas vleres 'up' edhe i numron
        upVotes = reviews.filter(value='up').count()
        # i njen kejt votat
        totalVotes = reviews.count()
        # pjeston upVotes me totalVotes duke i shumzuar me 100 per me shendrru ne perqindje
        ratio = (upVotes / totalVotes) * 100

        # update model fields
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    owner = models.ForeignKey(Profile , on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(Project , on_delete=models.CASCADE)
    body = models.TextField(null=True , blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , 
                        primary_key=True , editable=False)
    
    class Meta:
        #unique_togehter - i tregon serverit se veq owneri mundet me lon veq ni review te ni project
        unique_together = [
            ['owner','project']
        ]
    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , 
                        primary_key=True , editable=False)

    def __str__(self):
        return self.name

    