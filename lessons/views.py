from django.shortcuts import render
from .models import Lesson, Assignment, Submission
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

