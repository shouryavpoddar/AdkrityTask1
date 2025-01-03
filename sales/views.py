from django.contrib.auth.models import User
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Telecaller, SalesLead, Config
from .serializers import TelecallerSerializer, SalesLeadSerializer
import django_filters.rest_framework


class TelecallerViewSet(viewsets.ModelViewSet):
    queryset = Telecaller.objects.all()
    serializer_class = TelecallerSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['role', 'max_leads']

    @action(detail=True, methods=['get'], url_path='leads', url_name='telecaller-leads')
    def leads(self, request, pk=None):
        try:
            telecaller = self.queryset.get(id=pk) # Check if telecaller exists
            leads = telecaller.saleslead_set.all()
            # leads = SalesLead.objects.filter(telecaller_id=t_id)
            if not leads.exists():
                return Response({'message': 'No leads found for this telecaller.'}, status=status.HTTP_200_OK)

            # Serialize the leads using SalesLeadSerializer


            serializer = SalesLeadSerializer(leads, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(detail=False, methods=['get'], url_name='role')
    # def role(self, request):
    #     try:
    #         role = request.query_params.get('role')
    #         if not role:
    #             return Response({'error': 'Role is a required query parameter.'}, status=status.HTTP_400_BAD_REQUEST)
    #
    #
    #         telecallers = self.get_queryset().all().filter(role=role)
    #         if not telecallers.exists():
    #             return Response({'message': 'No telecallers found with this role.'}, status=status.HTTP_200_OK)
    #
    #         serializer = self.get_serializer(telecallers, many=True)
    #
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SalesLeadView(APIView):
    # queryset = SalesLead.objects.all()
    # serializer_class = SalesLeadSerializer

    def post(self, request):
        try:
            # Validate required fields
            telecaller_id = request.data.get('telecaller')
            user_id = request.data.get('user')

            if not telecaller_id or not user_id:
                return Response(
                    {'error': 'Telecaller and User are required fields.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Fetch Telecaller
            try:
                telecaller = Telecaller.objects.get(id=telecaller_id)
            except Telecaller.DoesNotExist:
                return Response({'error': 'Telecaller not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Fetch User
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Create SalesLead
            lead = SalesLead.objects.create(telecaller=telecaller, user=user)

            # Serialize and return the response
            return Response(
                {'message': 'Lead created successfully.', 'lead': SalesLeadSerializer(lead).data},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response({'error': f'An unexpected error occurred: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TelecallersWithMoreThanNLeadsAPIView(APIView):

    def get(self, request, n=3):
        try:
            # Group by telecaller and count leads
            telecallers_with_leads = SalesLead.objects.values('telecaller').annotate(
                lead_count=Count('id')
            ).filter(lead_count__gt=n)

            # Paginate results
            paginator = LimitOffsetPagination()
            paginated_queryset = paginator.paginate_queryset(telecallers_with_leads, request)

            response_data = []
            for telecaller_entry in paginated_queryset:
                telecaller_id = telecaller_entry['telecaller']

                try:
                    telecaller = Telecaller.objects.get(id=telecaller_id)
                    response_data.append({
                        "id": telecaller.id,
                        "name": telecaller.name,
                        "role": telecaller.role,
                        "max_leads": telecaller.max_leads,
                    })
                except Telecaller.DoesNotExist:
                    continue

            return paginator.get_paginated_response(response_data)

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ListTelecallersAPIView(generics.ListAPIView):
    queryset = Telecaller.objects.all()
    serializer_class = TelecallerSerializer

class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()

    @action(detail=False, methods=['get'], url_path='get-key', url_name='get-config')
    def get(self, request):
        try:
            key = request.query_params.get('key')
            if not key:
                return Response({'error': 'Key is a required query parameter.'}, status=status.HTTP_400_BAD_REQUEST)

            value = Config.get(key)
            return Response({'key': key, 'value': value, 'type': Config.objects.get(key=key).type}, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='set-key', url_name='set-config')
    def set(self, request):
        try:
            key = request.data.get('key')
            value = request.data.get('value')
            if not key or not value:
                return Response({'error': 'Key and Value are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

            # Config.set(key, value)
            # array = Config.get(key)
            # print(array)
            #
            # array.append(value)
            # print(array)
            Config.set(key, value)  # Ensure Config.set is implemented correctly
            return Response({'key': key, 'value': Config.get(key), 'type': Config.objects.filter(key=key)[0].type}, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @csrf_exempt
# @api_view(['POST'])
# def set(request):
#     print("jello")
#     key = request.data.get('kdey')
#     value = request.data.get('value')
#     print(key, value)
#     if not key or not value:
#         return Response({'error': 'Key and Value are required fields.'}, status=status.HTTP_400_BAD_REQUEST)
#
#     array = Config.get(key)
#
#     array = array.append(value)
#
#     Config.set(key, array)  # Ensure Config.set is implemented correctly
#     return Response({'key': key, 'value': Config.get(key)}, status=status.HTTP_200_OK)

