from django import forms  
from .models import Student  
  
class EmpForm(forms.ModelForm):  
    class Meta:  
        model = Student  
        fields = ["first_name", "last_name","roll_number"]
        labels = {'first_name': "Name", "last_name": "last","roll_number": "roll",}