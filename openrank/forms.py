from django import forms
from .models import EngineFamily, Engine, RatingList, RatingListStage

class EngineFamilyForm(forms.ModelForm):
    class Meta:
        model = EngineFamily
        fields = [ 'name', 'author', 'website' ]

class EngineForm(forms.ModelForm):
    class Meta:
        model = Engine
        fields = [ 'family', 'version', 'release_date', 'disabled', 'latest' ]
        widgets = { 'release_date': forms.DateInput(attrs={ 'type' : 'date'}) }

class RatingListForm(forms.ModelForm):
    class Meta:
        model = RatingList
        fields = ['name', 'thread_count', 'hashsize', 'base_time', 'increment']

class RatingListStageForm(forms.ModelForm):
    class Meta:
        model = RatingListStage
        fields = ['top_n_engines', 'games']