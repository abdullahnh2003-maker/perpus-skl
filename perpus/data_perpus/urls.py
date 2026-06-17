from django.urls import path
from . import views

urlpatterns = [

    # Dashboard
    path('', views.dashboard, name='dashboard'),
    # Buku
    path('buku/', views.buku_list, name='buku_list'),
    path('buku/create/', views.buku_create, name='buku_create'),
    path('buku/<int:id>/', views.buku_detail, name='buku_detail'),
    path('buku/<int:id>/edit/', views.buku_update, name='buku_update'),
    path('buku/<int:id>/delete/', views.buku_delete, name='buku_delete'),
    # Siswa
    path('siswa/', views.siswa_list, name='siswa_list'),
    path('siswa/create/', views.siswa_create, name='siswa_create'),
    path('siswa/<int:id>/', views.siswa_detail, name='siswa_detail'),
    path('siswa/<int:id>/edit/', views.siswa_update, name='siswa_update'),
    path('siswa/<int:id>/delete/', views.siswa_delete, name='siswa_delete'),
    path('peminjaman/', views.peminjaman_list, name='peminjaman_list'),
    path('peminjaman/create/', views.peminjaman_create, name='peminjaman_create'),
    path('peminjaman/<int:id>/kembalikan/', views.peminjaman_return, name='peminjaman_return'),
]