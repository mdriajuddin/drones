from django.test import TestCase

# Create your tests here.
from drones import views
from drones.models import DroneCategory,Pilot

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
















class DroneCategoryTests(APITestCase):


    def post_drone_category(self, name):
        url = reverse(f"v1:{views.DroneCategoryList.name}")  
        data = {'name':name}
        response = self.client.post(url,data, format="json")
        return response




    def test_post_and_get_drone_category(self):

        """
        Ensure we can create a new DroneCategoty object.
        """
        new_drone_category_name = "some"
        response = self.post_drone_category(new_drone_category_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DroneCategory.objects.count(), 1)
        print(DroneCategory.objects.count())
        print(DroneCategory.objects.get().name)
        self.assertEqual(DroneCategory.objects.get().name, 'some')


    def test_post_existing_drone_category_name(self):
        """
        Ensure we cannot create A DroneCategory with an existing name
        """

        new_drone_category_name = "Duplicate"
        response1 = self.post_drone_category(new_drone_category_name)
        assert response1.status_code == status.HTTP_201_CREATED
        response2 = self.post_drone_category(new_drone_category_name)
        print(response2)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST


    def test_filter_drone_category_by_name(self):
        "Ensure we can filter a dorne category by name"

        drone_category_name1 = "riaj"
        # first post
        self.post_drone_category(drone_category_name1)
        # second post 
        drone_category_name2 = "jihad"
        self.post_drone_category(drone_category_name2)


        filter_by_name = {"name":drone_category_name1}        
        url = reverse(f"v1:{views.DroneCategoryList.name}")
        response = self.client.get(url, data=filter_by_name, format="json")
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
      
        # Make sure we reveive only one element in the response
      
        assert response.data["count"] == 1
        assert response.data["results"][0]['name'] == drone_category_name1

    def test_get_drone_categories_collection(self):
        """
        Ensure we can retrieve the drone categories collection
        """
        new_drone_category_name = "super"
        self.post_drone_category(new_drone_category_name)
        url = reverse(f"v1:{views.DroneCategoryList.name}")
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        # Make sure we reveive only one element in the response
        assert response.data["count"] == 1
        assert response.data['results'][0]['name'] == new_drone_category_name

    def test_update_drone_category(self):
        """
        Ensure we can update a field for a drone category
        """
        drone_categoty_name = 'category initial Name'
        response = self.post_drone_category(drone_categoty_name)
        # pk = response.data['pk']
        # print(pk)
        url  = reverse(f"v1:{views.DroneCategoryDetail.name}",None,
                 args=[response.data['pk']]
                 )

        updated_drone_category_name = 'Updated Name'
        data = {"name":updated_drone_category_name}
        patch_response = self.client.patch(url, data, format="json")
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data['name'] == updated_drone_category_name




    def test_get_drone_category(self):
        """
        Ensure we cacn get a single dron categoty by id
        """
        drone_categoty_name = "Easy to retrive"
        respose = self.post_drone_category(drone_categoty_name)
        url = reverse(f"v1:{views.DroneCategoryDetail.name}",args=[respose.data['pk']])
        get_response = self.client.get(url, format="json")
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data['name'] == drone_categoty_name




class PolotTests(APITestCase):

    def post_pilot(self, name, gender, races_count):
        url = reverse(f"v1:{views.PilotList.name}") 

        print(name, gender, races_count)       

        data = {
                        "name": name,
                        "drone_category": "cat1",
                        "owner": "riaj",
                        "manufacturing_date": "2022-10-30T21:43:00Z",
                        "has_it_competed": True,
                        "inserted_timestamp": "2022-10-30",
                        "gender":gender,
                        "reces_count": races_count                  
        }


        response = self.client.post(url, data, format="json")
        return response

    def  create_user_and_set_token_createntials(self):
        user = User.objects.create_user(
            "user1",
            'user1@gmail.com',
            'user3487343847'
        )
        token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}'
        )



    # def test_post_and_get_pilot(self):
        """
        Ensure we can create a new Pilot and then retriece it 
        Ensure we cannot retriece the persisted polot without a token

        """

        self.create_user_and_set_token_createntials()
        new_pilot_name = "Riaj"
        new_pilot_gender = Pilot.MALE
        new_pilot_races_count = 5
        response = self.post_pilot(
            new_pilot_name,
            new_pilot_gender,
            new_pilot_races_count
        )
        print(f"Pk {Pilot.objects.get().pk}")
        assert response.status_code == status.HTTP_201_CREATED
        assert Pilot.objects.count()  == 1
        saved_pilot = Pilot.objects.get()
        assert saved_pilot.name == new_pilot_name
        assert saved_pilot.gender == new_pilot_gender
        assert saved_pilot.reces_count == new_pilot_races_count

        url = reverse(f"v1:{views.PilotDetail.name}",
            args=[saved_pilot.pk]
            )
        
        authorized_get_response = self.client.get(url, format="json")
        assert authorized_get_response.status_code == status.HTTP_200_OK
        assert authorized_get_response.data['name'] ==  new_pilot_name
        # clean up credentials
        self.client.credentials()

        unauthorisez_get_response = self.client.get(url, format="json")
        assert unauthorisez_get_response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_try_to_post_without_token(self):
        """
        Ensure we cannot create a pilot without a token
        """

        new_pilot_name = 'Unauthorized Pilot'
        new_pilot_gender = Pilot.name
        new_pilot_races_count = 5
        response = self.post_pilot(
            new_pilot_name,
            new_pilot_gender,
            new_pilot_races_count
        )
        # print(response)
        # print(Pilot.objects.count())

        # assert response.status_code == status.HTTP_401_UNAUTHORIZED
        # assert Pilot.objects.count()  == 0







