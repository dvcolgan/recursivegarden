from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from backend.zettle.models import ZettleCard


class CardPositioningTests(APITestCase):
    def setUp(self):
        self.card = ZettleCard.objects.create(
            title="Test Card",
            x=100,
            y=100,
        )
        self.detail_url = reverse(
            "zettle:zettlecard-detail", kwargs={"uuid": self.card.uuid}
        )
        self.list_url = reverse("zettle:zettlecard-list")

        # Create some additional cards for list testing
        self.card2 = ZettleCard.objects.create(
            title="Card 2",
            x=200,
            y=200,
        )
        self.card3 = ZettleCard.objects.create(
            title="Card 3",
            x=300,
            y=300,
        )

    def test_update_card_position(self):
        """Should be able to update a card's position via PATCH"""
        response = self.client.patch(
            self.detail_url,
            {
                "x": 200,
                "y": 300,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.card.refresh_from_db()
        self.assertEqual(self.card.x, 200)
        self.assertEqual(self.card.y, 300)

    def test_partial_position_update(self):
        """Should be able to update just x or just y"""
        response = self.client.patch(self.detail_url, {"x": 200})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.card.refresh_from_db()
        self.assertEqual(self.card.x, 200)
        self.assertEqual(self.card.y, 100)  # y should remain unchanged

    def test_list_cards(self):
        """Should return all cards in the system"""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 3
        )  # Assuming pagination is enabled

        # Verify the response contains our cards
        card_uuids = {str(card["uuid"]) for card in response.data["results"]}
        expected_uuids = {
            str(self.card.uuid),
            str(self.card2.uuid),
            str(self.card3.uuid),
        }
        self.assertEqual(card_uuids, expected_uuids)

    def test_list_cards_has_coordinates(self):
        """Cards in list should include their x/y coordinates"""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_card = response.data["results"][0]

        self.assertIn("x", first_card)
        self.assertIn("y", first_card)
        self.assertIsNotNone(first_card["x"])
        self.assertIsNotNone(first_card["y"])
