from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from backend.users.factories import UserFactory
from backend.zettle.factories import ZettleCardFactory
from backend.zettle.models import ZettleCard


class ZettleCardViewSetTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse("zettlecard-list")

    def test_create_text_card(self):
        data = {
            "title": "New Text Card",
            "card_type": ZettleCard.CardType.TEXT,
            "text": "This is a test card",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ZettleCard.objects.count(), 1)
        self.assertEqual(response.data["title"], "New Text Card")
        self.assertEqual(response.data["author"], self.user.id)

    def test_create_image_card(self):
        # Using SimpleUploadedFile for image test
        from django.core.files.uploadedfile import SimpleUploadedFile

        image = SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        )

        data = {
            "title": "New Image Card",
            "card_type": ZettleCard.CardType.IMAGE,
            "image": image,
        }
        response = self.client.post(self.list_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["image"])

    def test_list_cards(self):
        # Create multiple cards
        cards = [ZettleCardFactory() for _ in range(3)]

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_card(self):
        card = ZettleCardFactory()
        url = reverse("zettlecard-detail", kwargs={"uuid": card.uuid})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], card.title)

    def test_update_card(self):
        card = ZettleCardFactory(author=self.user)
        url = reverse("zettlecard-detail", kwargs={"uuid": card.uuid})

        data = {"title": "Updated Title", "text": "Updated text content"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")

    def test_delete_card(self):
        card = ZettleCardFactory(author=self.user)
        url = reverse("zettlecard-detail", kwargs={"uuid": card.uuid})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ZettleCard.objects.count(), 0)

    def test_filter_by_card_type(self):
        ZettleCardFactory(card_type=ZettleCard.CardType.TEXT)
        ZettleCardFactory(card_type=ZettleCard.CardType.IMAGE)
        ZettleCardFactory(card_type=ZettleCard.CardType.URL)

        response = self.client.get(
            f"{self.list_url}?card_type={ZettleCard.CardType.TEXT}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_cards(self):
        ZettleCardFactory(title="Unique Title")
        ZettleCardFactory(title="Different Name")

        response = self.client.get(f"{self.list_url}?search=Unique")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_ordering(self):
        ZettleCardFactory(title="A Card")
        ZettleCardFactory(title="B Card")
        ZettleCardFactory(title="C Card")

        response = self.client.get(f"{self.list_url}?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "A Card")

    def test_cannot_update_other_users_card(self):
        card = ZettleCardFactory(author=self.other_user)
        url = reverse("zettlecard-detail", kwargs={"uuid": card.uuid})

        data = {"title": "Trying to update"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tag_filtering(self):
        tag_card = ZettleCardFactory(title="Tag Card")
        card = ZettleCardFactory()
        card.tags.add(tag_card)

        response = self.client.get(f"{self.list_url}?tag=Tag")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_card_with_parent(self):
        parent_card = ZettleCardFactory()
        data = {
            "title": "Child Card",
            "card_type": ZettleCard.CardType.TEXT,
            "text": "This is a child card",
            "parent": str(parent_card.uuid),
        }

        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["parent"], str(parent_card.uuid))
