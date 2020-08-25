from django.urls import path
from rest_framework import routers
from .views import (GraphicDesignsCreate, GraphicDesignDetail, GraphicDesignsList,
            LightroomPresetCreate, LightroomPresetList, LightroomPresetDetail, LightroomPresetCategoryList,
            LightroomPackageList#GraphicDesignsListCreate
)

app_name = 'shop'

# router = routers.SimpleRouter()
# router.register('designs', GraphicDesignsViewSet)


urlpatterns = [
    path('photoshop/create/', GraphicDesignsCreate.as_view(),name='photoshop-create'),
    path('photoshop/', GraphicDesignsList.as_view(), name='photoshop'),
    #path('designs/', GraphicDesignsListCreate.as_view(),name ='designs'),
    path('photoshop/<slug>/', GraphicDesignDetail.as_view(),name ='photoshop-detail'),
    path('presets/create/', LightroomPresetCreate.as_view(),name ='preset-create'),
    path('presets/', LightroomPresetList.as_view(),name ='presets'),
    path('presets/<slug>/', LightroomPresetDetail.as_view(),name ='presets-detail'),
    path('category/', LightroomPresetCategoryList.as_view(),name ='presets-category'),
    path('lightroom-presets/', LightroomPackageList.as_view(),name ='package-category'),
    #path('designs/<slug>/', test_detail,name ='designs2'),
]

#urlpatterns += router.urls