from django.db import models
from django.db.models import CharField, FloatField, IntegerField, DateTimeField, TextField, ForeignKey, URLField


class Speciality(models.Model):
    code = CharField(max_length=64)
    title = CharField(max_length=64)
    picture = URLField(default='https://place-hold.it/100x60')


class Company(models.Model):
    name = CharField(max_length=64)
    location = CharField(max_length=64)
    logo = URLField(default='https://place-hold.it/100x60')
    description = TextField()
    employee_count = IntegerField()


class Vacancy(models.Model):
    title = CharField(max_length=64)
    specialty = ForeignKey(Speciality, on_delete=models.CASCADE, related_name="vacancies")
    company = ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = CharField(max_length=128)
    text = TextField()
    salary_min = FloatField()
    salary_max = FloatField()
    published_at = DateTimeField()



