from django.conf.urls import patterns, include, url
from django.contrib import admin
from volunteer import views
from django.conf import settings
from django.conf.urls.static import static
from writersexchange import settings
import django
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
    url(r'^login/', 'django.contrib.auth.views.login', name="login"),
    url(r'^login/success/', views.signin, name="signinresult"),
    url(r'^signup/', views.signup, name="signup"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^application_result/(\d+)/', views.application_result, name="application-result"),
    url(r'^events/(\d{4})/(\d+)/(\d+)/', views.day_events),
    url(r'^events/(\d{4})/(\d+)/', views.month_events),
    url(r'^events/signup/', views.event_signup),
    url(r'^volunteers/(\d+)/', views.volunteer_info, name="profile"),
    url(r'^events/create/', views.add_event),
    url(r'^applications/', views.volunteer_list),
    url(r'^accounts/profile/', views.profile, name="accountprofile"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login'}),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

