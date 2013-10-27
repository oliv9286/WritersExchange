from django.conf.urls import patterns, include, url
from django.contrib import admin
from volunteer import views
from writersexchange import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'writersexchange.views.home', name='home'),
    # url(r'^writersexchange/', include('writersexchange.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', views.index, name='index'),
    url(r'^apply/', views.apply, name="apply"),
    url(r'^query/', views.query, name="query"),
    url(r'^login/', views.login, name="login"),
    url(r'^login/success/', views.signin, name="signinresult"),
    url(r'^signup/', views.signup, name="signup"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^applications/(\w+)/', views.application_review, name="applications"),
    url(r'^application_result/(\w+)/', views.application_result),
    url(r'^events/(\d{4})/(\d+)/(\d+)/', views.day_events),
    url(r'^events/(\d{4})/(\d+)/', views.month_events),
    url(r'^events/signup/', views.event_signup),
    url(r'^applications/', views.volunteer_list),
    url(r'^volunteers/(\d+)/', views.volunteer_info),
    url(r'^events/create/', views.add_event)
)

