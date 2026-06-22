from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Bookings, Event_Extras, Profile, Services


class BookingProposalTests(TestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(username='client_user', password='pass123')
        self.client_profile = Profile.objects.create(user=self.client_user, name='Client User', account_type='client')

        self.provider_user = User.objects.create_user(username='provider_user', password='pass123')
        self.provider_profile = Profile.objects.create(user=self.provider_user, name='Provider User', account_type='provider')

        self.service = Services.objects.create(
            profile=self.provider_profile,
            title='Royal Wedding Package',
            description='Elegant wedding package',
            costs=15000,
            rate=50,
            cover_picture=SimpleUploadedFile('cover.jpg', b'cover-image-bytes')
        )
        self.extra = Event_Extras.objects.create(service=self.service, add_on='DJ', rate=120)

    def test_booking_proposal_requires_login(self):
        response = self.client.post(reverse('booking_proposal', args=[self.service.id]), {
            'guests': '120',
            'DJ': 'on',
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_booking_proposal_creates_booking_and_selected_extras(self):
        self.client.force_login(self.client_user)

        response = self.client.post(reverse('booking_proposal', args=[self.service.id]), {
            'guests': '120',
            'DJ': 'on',
        })

        self.assertEqual(response.status_code, 302)
        booking = Bookings.objects.get(service=self.service, consumer=self.client_profile)
        self.assertEqual(booking.guests, 120)
        self.assertEqual(booking.status, 'pending')
        self.assertEqual(booking.charges, 15000 + (120 * self.extra.rate))
        self.assertEqual(booking.extras.count(), 1)
        self.assertEqual(booking.extras.first().add_on, 'DJ')
