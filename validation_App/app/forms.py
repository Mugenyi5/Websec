# myapp/forms.py
from django import forms
from .models import Participant, Vehicle

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        widgets = {
            'manufacture_date': forms.DateInput(attrs={'type': 'date'}),
        }
def clean_manufacture_date(self):
        manufacture_date = self.cleaned_data.get('manufacture_date')
        current_year = timezone.now().year

        if manufacture_date.year < 2000 or manufacture_date.year > current_year:
            raise ValidationError("Manufacture date must be between 2000 and the current year")

        return manufacture_date

def clean_plate_number(self):
        plate_number = self.cleaned_data.get('plate_number')
        if not plate_number.startswith(('RAA', 'RAB', 'RAC', 'RAD', 'RAE', 'RAF', 'RAG', 'RAH')):
            exceptions = ['RDF', 'RNP', 'IT', 'GR']
            exception_found = any(plate_number.startswith(prefix) for prefix in exceptions)
            if not exception_found:
                raise ValidationError("Plate number must start with 'RAA' to 'RAH' or be an exception.")

        return plate_number

 
