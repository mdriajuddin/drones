
from django.shortcuts import render

# Create your views here.



from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import  reverse
from drones.models import (
    DroneCategory,
    Drone,
    Pilot,
    Competition
)

from drones.serializers import (
    DroneCategorySerializer,
    DroneSerializer,
    PilotSerializer,
    PilotCompetitionSerializer
)


from rest_framework.throttling import UserRateThrottle
from rest_framework.throttling import ScopedRateThrottle


from rest_framework import filters



from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


from rest_framework import permissions
from drones import custompermission




class ApiRoot(generics.GenericAPIView):
    name = "api-root"

    def get(self, request, *args, **kwargs):
        return Response({
            "drone-categories":reverse(DroneCategoryList.name, request=request),
            "drones": reverse(DroneList.name, request=request),
            "pilots":reverse(PilotList.name, request=request),
            "competitions":reverse(CompetitionList.name, request=request)
        })






class DroneCategoryList(generics.ListCreateAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = "dronecategory-list"

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    
    filterset_fields = ('name',)
    search_fields = (
        '^name',
    )
    ordering_fields = (
        'name',
    )







class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = "dronecategory-detail"

class DroneList(generics.ListCreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer 
    name = "drone-list"

    filter_fields = (
        'name',
        'drone_category',
        'manufacturing_date',
        'has_it_competed',
    )

    search_fields = (
        '^name',
    )
    ordering_fields = (
        'name',
        'manufacturing_date',
    )
    # permission_classes = [ permissions.IsAuthenticatedOrReadOnly,custompermission.IsCurrentUserOwnerOrReadOnly]


    # permission_classes = (
    #     permissions.IsAuthenticatedOrReadOnly,
    #     custompermission.IsCurrentUserOwnerOrReadOnly,

    # )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = "drone-detail"

    permission_classes = [ permissions.IsAuthenticatedOrReadOnly,custompermission.IsCurrentUserOwnerOrReadOnly]


class PilotList(generics.ListCreateAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = "pilot-list"

    filter_fields = (
        'name',
        'gender',
        'races_count',
    )

    search_fields = (
        '^name',
    )

    ordering_fields = (
        'name',
        'races_count'
    )

    # throttle_scope = 'drones'
    # throttle_classes = (ScopedRateThrottle,)

    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]











class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-detail'

    throttle_scope = 'drones'
    throttle_classes = (ScopedRateThrottle,)

    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]





from django_filters import rest_framework as filters

class CompetiontionFileter(filters.FilterSet):
    distance_in_feet = filters.NumberFilter()
    min_distance_in_feet = filters.NumberFilter(field_name="distance_in_feet",lookup_expr='gt')
    max_distance_in_feet = filters.NumberFilter(field_name="distance_in_feet",lookup_expr='lt')
    form_achivement_date = filters.DateTimeFilter(
        field_name="distance_achivement_date", lookup_expr='gt'
    )
    to_achivement_date = filters.DateTimeFilter(
        field_name='distance_achivement_date', lookup_expr='lt'
    )
    drone_name = filters.AllValuesFilter(
        field_name="drone__name"
    )
    pilot_name = filters.AllValuesFilter(
        field_name="pilot__name"
    )
    class Meta:
        model = Competition

        fields = [
            
            'distance_in_feet',
            'form_achivement_date',
            'to_achivement_date',
            'min_distance_in_feet',
            'max_distance_in_feet',
            # drone__name will be accessed as drone_name
            'drone_name',
            # pilot__name will be accessrd as pilot_name
            'pilot_name',
        ]



class CompetitionList(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = "competition-list"
    filterset_class = CompetiontionFileter
    ordering_fields = (
        # 'distance_in_feet',
        'distance_achievement_date',
    )
    search_fields = (
        '^distance_in_feet',
    )

class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = "competition-detail"



