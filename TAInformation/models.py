from abc import abstractmethod

from django.db import models


# Create your models here.

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, default='email')
    password = models.CharField(max_length=20, default='email')
    email = models.EmailField(max_length=20, default='email')  # models.EmailField(max_length=20)
    home_address = models.CharField(max_length=20, default='"101 W. Wisconsin Ave, Milwaukee, WI 53203"')
    role = models.IntegerField(default=1)
    phone = models.CharField(max_length=13, default='')


class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=20)
    instructor_id = models.IntegerField()
    meeting_time = models.CharField(max_length=20)
    semester = models.CharField(max_length=20)
    course_type = models.CharField(max_length=20)
    description = models.CharField(max_length=200)


class Lab(models.Model):
    lab_id = models.IntegerField(primary_key=True)
    lab_name = models.CharField(max_length=20)
    ta_id = models.IntegerField()
    course_id = models.IntegerField()
    has_grader = models.BooleanField()
    description = models.CharField(max_length=200)


class LabCourseJunction(models.Model):
    lab_id = models.ForeignKey(Lab, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)


class LabTAJunction(models.Model):
    lab_id = models.ForeignKey(Lab, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
