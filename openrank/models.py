from django.db import models
from django.db.models import Q, F

class EngineFamily(models.Model):

    name        = models.CharField(max_length=255, unique=True)
    author      = models.CharField(max_length=255)
    website     = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Engine(models.Model):

    family       = models.ForeignKey(EngineFamily, on_delete=models.CASCADE, related_name='engines')
    version      = models.CharField(max_length=50)
    release_date = models.DateField(null=True, blank=True)

    disabled = models.BooleanField(default=False)
    latest   = models.BooleanField(default=False)
    private  = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['family'],
                condition=Q(latest=True),
                name='unique_latest_engine_per_family'
            )
        ]

    def __str__(self):
        return '%s %s' % (self.family.name, self.version)

class RatingList(models.Model):

    name         = models.CharField(max_length=255)
    thread_count = models.IntegerField()
    hashsize     = models.IntegerField()
    base_time    = models.IntegerField()
    increment    = models.IntegerField()

    engines = models.ManyToManyField('Engine', related_name='rating_lists', blank=True)

    def __str__(self):
        return '%d-thread %d + %d' % (self.thread_count, self.base_time, self.increment)

class RatingListStage(models.Model):

    rating_list   = models.ForeignKey(RatingList, on_delete=models.CASCADE, related_name='stages')
    stage_number  = models.PositiveIntegerField()
    top_n_engines = models.PositiveIntegerField()
    games         = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['rating_list', 'stage_number'],
                name='unique_stage_per_rating_list'
            )
        ]
        ordering = ['stage_number']

    def __str__(self):
        return '%s - Stage %d' % (str(self.rating_list), self.stage_number)

class Pairing(models.Model):

    stage    = models.ForeignKey('RatingListStage', on_delete=models.CASCADE, related_name='pairings')
    engine_a = models.ForeignKey('Engine', on_delete=models.CASCADE, related_name='pairings_as_a')
    engine_b = models.ForeignKey('Engine', on_delete=models.CASCADE, related_name='pairings_as_b')

    LL = models.IntegerField(default=0)
    LD = models.IntegerField(default=0)
    DD = models.IntegerField(default=0)
    DW = models.IntegerField(default=0)
    WW = models.IntegerField(default=0)

    def penta(self):
        return (self.LL, self.LD, self.DD, self.DW, self.WW)

    def __str__(self):
        return '%s vs %s, Stage %s' % (str(self.engine_a), str(self.engine_b), str(self.stage))