from django.urls import path, re_path
from django.views.generic.base import TemplateView
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('premium', views.premium, name="premium"),
    path('canvas', views.canvas, name="canvas"),
    path('valueproposition', views.valueproposition, name="valueproposition"),
    path('customersegment',views.customersegment, name="customersegment"),
    path('channels', views.channels, name="channels"),
    path('customerrelationship', views.customerrelationship, name="customerrelationship"),
    path('revenuestream', views.revenuestream, name="revenuestream"),
    path('keysection', views.keysection, name="keysection"),
    path('buildcanvas', views.buildcanvas, name="buildcanvas"),
    path('editcanvas', views.editcanvas, name="editcanvas"),
    path('removeincanvas', views.removeincanvas, name="removeincanvas"),
    path('addincanvas', views.addincanvas, name="addincanvas"),
    path('fetchforcanvas', views.fetchforcanvas, name="fetchforcanvas"),
    path('tutorial', views.tutorial, name="tutorial"),
    path('ViewInCanvas', views.ViewInCanvas, name="ViewInCanvas"),
    
]
handler404 = 'canvas.views.handler404'