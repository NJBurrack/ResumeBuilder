from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Resume
from django.core import mail
from django.test import TestCase
from resumes.tasks import send_resume_created_email



User = get_user_model()

class ResumeAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='testpass')
        self.other_user = User.objects.create_user(username='other', password='otherpass')
        self.url = reverse('resume-list-create')
        self.data = {
            'name': 'John Doe',
            'bio': 'Software developer',
            'address': '123 Main St',
            'skills': [
                {'name': 'Python', 'skill_level': 5},
                {'name': 'Django', 'skill_level': 4}
            ],
            'job_history': [
                {
                    'start_date': '2022-01-01',
                    'end_date': '2023-01-01',
                    'description': 'Backend developer',
                    'job_title': 'Engineer'
                }
            ],
            'education_history': [
                {'name': 'University X', 'qualification': 'BSc Computer Science'}
            ],
        }

    def test_create_resume(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resume.objects.count(), 1)
        self.assertEqual(Resume.objects.get().name, 'John Doe')

    def test_list_resumes(self):
        # Create resume under self.user

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Check nested fields are lists
        self.assertIsInstance(response.data[0]['skills'], list)
        self.assertIsInstance(response.data[0]['job_history'], list)
        self.assertIsInstance(response.data[0]['education_history'], list)

    def test_permissions(self):
        # Create resume as owner

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.data, format='json')
        resume_id = response.data['id']

        # Attempt update by another user - should be denied
        self.client.force_authenticate(user=self.other_user)
        update_data = {'name': 'Jane Doe'}
        response = self.client.put(reverse('resume-detail', kwargs={'pk': resume_id}), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Update by owner - should succeed
        self.client.force_authenticate(user=self.user)
        update_data = {
            'name': 'Jane Doe',
            'bio': 'Software developer',
            'address': '123 Main St',
            'skills': self.data['skills'],
            'job_history': self.data['job_history'],
            'education_history': self.data['education_history'],
        }
        response = self.client.put(reverse('resume-detail', kwargs={'pk': resume_id}), data=update_data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])
        self.assertEqual(response.data['name'], 'Jane Doe')


# Uses nested dictionaries as lists for:
# skills, job history & education histroy
# aunthenticates user for permission tests correctly
# asserts expected response data types


class ResumeEmailTaskTest(TestCase):
    def test_send_resume_created_email(self):
        send_resume_created_email(
            resume_id=123,
            user_email='testuser@example.com'
        )
        # Check that one message was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Resume Created', mail.outbox[0].subject)
        self.assertIn('123', mail.outbox[0].body)
        self.assertIn('testuser@example.com', mail.outbox[0].to)