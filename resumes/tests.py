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
            'title': 'John Doe',
            'bio': 'Software developer',
            'address': '123 Main St',
            'skills': [
                {'name': 'Python', 'level': 'Expert'},
                {'name': 'Django', 'level': 'Advanced'}
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
                {
                    'institution': 'University X',
                    'degree': 'BSc Computer Science',
                    'start_date': '2018-01-01',
                    'end_date': '2022-01-01'
                }
            ]
        }

    def test_create_resume(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resume.objects.count(), 1)
        self.assertEqual(Resume.objects.get().title, 'John Doe')

    def test_list_resumes(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Fetch the list
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_permissions(self):
        # Create a resume as 'owner'
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resume_id = response.data['id']

        # Try to update as 'other'
        self.client.force_authenticate(user=self.other_user)
        update_data = {
            'title': 'Jane Doe',
            'bio': 'Software developer',
            'address': '123 Main St',
            'skills': self.data['skills'],
            'job_history': self.data['job_history'],
            'education_history': self.data['education_history'],
        }
        response = self.client.put(reverse('resume-detail', kwargs={'pk': resume_id}), data=update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Update as owner
        self.client.force_authenticate(user=self.user)
        response = self.client.put(reverse('resume-detail', kwargs={'pk': resume_id}), data=update_data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['title'], 'Jane Doe')


class ResumeEmailTaskTest(TestCase):

    def test_send_resume_created_email(self):
        # Create a real user and resume first!
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        resume = Resume.objects.create(
            title='Test Resume',
            bio='Test bio',
            address='Test address',
            owner=user
        )
        
        # Now call the task with the REAL resume ID
        send_resume_created_email(resume.id, user.email)
        
        # Check that one message was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Resume Created', mail.outbox[0].subject)
        self.assertIn('Test Resume', mail.outbox[0].subject)
        self.assertIn('Test Resume', mail.outbox[0].body)
        self.assertEqual(['testuser@example.com'], mail.outbox[0].to)
