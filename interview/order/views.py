from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request

from django.db.models import Prefetch
from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer, OrderTagOnlySerializer, OrderSpecificTagSerializer

from datetime import datetime

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer

class DeactivateOrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        order = self.get_queryset(id=kwargs['id'])
        order.is_active = False
        order.save(update_fields =['is_active'])
        
        return Response({"Success:Deactivate Order"},status=200)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)
    
class OrderFilterDateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        
        try:
            start_date_1 = datetime.strptime(kwargs['start_date'],'%Y-%m-%d').date()
            embargo_date_1 = datetime.strptime(kwargs['embargo_date'],'%Y-%m-%d').date()
            orders = self.get_queryset(start_date__gte=start_date_1,embargo_date__lte=embargo_date_1)
            serializer = self.serializer_class(orders,many=True)
            return Response(serializer.data, status=200)
        
        except Exception as e:
            print("*********EXCEPTION: ",e)
    
    def get_queryset(self,**kwargs):
        return self.queryset.filter(**kwargs)
    
class OrderTagCreateView(generics.ListAPIView):
    queryset = Order.objects.all().only('id','tags')
    serializer_class = OrderTagOnlySerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        order = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(order)

        return Response(serializer.data, status=200)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)
    
class TagOrderCreateView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSpecificTagSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:

        try:
            order = Order.objects.exclude(tags__isnull=True).prefetch_related(
                Prefetch('tags', queryset=OrderTag.objects.filter(id=kwargs['id']), to_attr='filtered_tags')
            )
            orderlist = [eachorder for eachorder in order.values()]
            print(orderlist[0])
            serializer = self.serializer_class(order,many=True)

            return Response(serializer.data, status=200)
        
        except Exception as e:
            print("********* Exception: ",e)