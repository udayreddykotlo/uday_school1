from django.urls import path
from curriculam import views

app_name='curriculam'

urlpatterns = [

    path('',views.StandardListView.as_view(), name='standard_list'),
    path('<slug:slug>/',views.SubjectListView.as_view(), name='subject_list'),
    path('<str:standard>/<slug:slug>/',views.LessionListView.as_view(), name='lession_list'),
    path('<str:standard>/<str:slug>/create/', views.LessionCreateView.as_view(),name='lession_create'),
    path('<str:standard>/<str:subject>/<slug:slug>/', views.LessionDetailView.as_view(),name='lession_detail'),
    path('<str:standard>/<str:subject>/<slug:slug>/update/', views.LessionUpdateView.as_view(),name='lession_update'),
    path('<str:standard>/<str:subject>/<slug:slug>/delete/', views.LessionDeleteView.as_view(),name='lession_delete'),

]
