from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('compiler', views.test),
    path('',views.registeruser),
    path('about.html',views.about),
    path('blog.html',views.gg),
    path('login',views.login),
    path('test',views.gg),
    path('article/<int:pk>',views.show,name='post-data'),
    path('team',views.team),
    path('contact.html',views.contact),
    path('quiz/<int:id>/<int:uid>',views.quizhome),
    path('logout',views.logout),
    path('test2',views.test2),
    path('answer', views.answers),
    path('quiz',views.quiz),
    path('pay/', views.initiate_payment),
    path('callback', views.callback),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)