from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .mqtt import *
from .serializers import RelaySerializer, DH11Serializer
from .models import Relay, DH11

def home_page(request):
    relays = Relay.objects.all()
    context = {'relays': relays}
    return render(request, 'index.html', context)

def get_sensor_page(request, mac_addr: str):
    sensor = DH11.objects.get(mac_addr=mac_addr)
    temp = sensor.temp
    humidity = sensor.humidity
    return JsonResponse({'temp': temp, 'humidity': humidity})


class DeviceList(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'home/device_list.html'

    # @extend_schema(
    #     request=RelaySerializer,
    #     responses={200: RelaySerializer}
    # )
    def get(self, request: Request):
        relays = Relay.objects.filter(user_id=request.user.id)
        sensors = DH11.objects.filter(user_id=request.user.id)
        #
        relay_serializer = RelaySerializer(relays, many=True)
        sensor_serializer = DH11Serializer(sensors, many=True)
        return Response({ 'relays': relays,
                          'dh11s': sensors},
                        status.HTTP_200_OK)

@api_view(['POST'])
def add_relay(request: Request):
    if request.method == 'POST':
        print(request.data)
        Relay.objects.create(name=request.data["name"], mac_addr=request.data["mac_addr"], state="False", user_id=request.data["user_id"])
        return Response(None, status.HTTP_201_CREATED)
    return Response(None, status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_dh11(request: Request):
    if request.method == 'POST':
        print(request.data)
        DH11.objects.create(name=request.data["name"], mac_addr=request.data["mac_addr"], temp=None, humidity=None, user_id=request.data["user_id"])
        return Response(None, status.HTTP_201_CREATED)
    return Response(None, status.HTTP_400_BAD_REQUEST)

class RelayDetail(APIView):

    def get_relay_obj(self, relay_id):
        try:
            relay = Relay.objects.get(pk=relay_id)
            return relay
        except Relay.DoesNotExist:
            return Response(None, status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, relay_id):
        relay = self.get_relay_obj(relay_id)
        relay.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)

    def put(self, request: Request, relay_id):
        print(request.data)
        relay = self.get_relay_obj(relay_id)
        relay.state = request.data['state']
        relay.save()
        return Response(None, status.HTTP_202_ACCEPTED)

class Dh11Detail(APIView):
    def get_dh11_obj(self, dh11_id):
        try:
            dh11 = DH11.objects.get(pk=dh11_id)
            return dh11
        except DH11.DoesNotExist:
            return Response(None, status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, dh11_id):
        dh11 = self.get_dh11_obj(dh11_id)
        dh11.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)


# region Bedard nakhor
# class RelaysViewSetApiView(viewsets.ModelViewSet):
#     queryset = Relay.objects.all()
#     serializer_class = RelaySerializer


# class DH11sViewSetApiView(viewsets.ModelViewSet):
#     queryset = DH11.objects.all()
#     serializer_class = DH11Serializer

# endregion
