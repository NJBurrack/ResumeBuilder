from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Resume

class ResumeAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('resume-list-create')
        self.data = {
            'name': 'John Doe',
            'bio': 'Software developer',
            'skills': 'Python, Django, REST',
            'address': '123 Main St',
            'job_history': 'Company A, Company B',
            'education_history': 'University X',
        }

    def test_create_resume(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resume.objects.count(), 1)
        self.assertEqual(Resume.objects.get().name, 'John Doe')

    def test_list_resumes(self):
        Resume.objects.create(**self.data)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
