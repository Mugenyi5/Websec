# myapp/models.py
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

def clean(self):
        errors = {}
        if errors:
            raise ValidationError(errors)
class Participant(models.Model):
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Others', 'Others'),
    ]
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+(\d+)$', message="Phone number must start with +(country code)"
    )
    phone = models.CharField(validators=[phone_regex], max_length=20)
    reference_number = models.CharField(max_length=20, blank=True, null=True)

    # Add the reference number validation rule here
    def clean(self):
        if self.reference_number:
            try:
                reference_number = int(self.reference_number)
                if not (99 <= reference_number <= 999):
                    raise ValidationError({'reference_number': 'Reference number must be between 99 and 999'})
            except ValueError:
                raise ValidationError({'reference_number': 'Reference number must be a valid integer'})

        # Remaining validation rules
        if not self.fname:
            raise ValidationError({'fname': 'First name is required'})

        if not self.email.endswith('ur.ac.rw'):
            raise ValidationError({'email': 'Email must be from ur.ac.rw'})

        if self.gender not in [choice[0] for choice in self.GENDER_CHOICES]:
            raise ValidationError({'gender': 'Invalid gender'})

        if (timezone.now().date() - self.dob).days < 365 * 18:
            raise ValidationError({'dob': 'Age must be over 18 years'})

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob= models.DateField()

    def __str__(self):
        return f'{self.fname} {self.lname}'

class Vehicle(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=20)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    manufacture_date = models.DateField()
    make = models.CharField(max_length=50)
    license = models.CharField(max_length=50, null=True, blank=True)
    def clean(self):
        plate_number = self.plate_number

        if not plate_number.startswith(('RAA', 'RAB', 'RAC', 'RAD', 'RAE', 'RAF', 'RAG', 'RAH')):
            exceptions = ['RDF', 'RNP', 'IT', 'GR']
            exception_found = any(plate_number.startswith(prefix) for prefix in exceptions)
            if not exception_found:
                raise ValidationError({'plate_number': "Plate number must start with 'RAA' to 'RAH' or be an exception."})
        manufacture_date = self.manufacture_date

        current_year = timezone.now().year
        if manufacture_date.year < 2000 or manufacture_date.year > current_year:
            raise ValidationError({'manufacture_date': f"Manufacture date must be between 2000 and {current_year}"})
