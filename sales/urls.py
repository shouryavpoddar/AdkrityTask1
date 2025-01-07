from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TelecallerViewSet, SalesLeadView, TelecallersWithMoreThanNLeadsAPIView, ConfigViewSet, \
    LeadSourceConfigViewSet

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'telecallers', TelecallerViewSet, basename='telecaller')
router.register(r'Config', ConfigViewSet, basename='config')
router.register(r'LeadSourceConfig', LeadSourceConfigViewSet, basename='lead-source-config')
# Define additional paths for APIs not handled by the router
urlpatterns = [
    # Include router-generated URLs for ViewSets
    path('', include(router.urls)),

    # Explicit path for SalesLeadView (APIView)
    path('leads/', SalesLeadView.as_view(), name='sales-leads'),

    # Custom action path for retrieving leads by telecaller
    path('<int:pk>/leads/', TelecallerViewSet.as_view({'get': 'leads'}), name='telecaller-leads'),

    path('telecallers/leads/more_than/<int:n>/', TelecallersWithMoreThanNLeadsAPIView.as_view(), name='telecallers-more-than-n-leads'),

    path('home/', set, name="set-key"),
]