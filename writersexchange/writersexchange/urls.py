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
#    url(r'^applications/(\d+)/', views.application_review, name="applications"),
    url(r'^application_result/(\d+)/', views.application_result, name="application-result"),
    url(r'^events/(\d{4})/(\d+)/(\d+)/', views.day_events), #json
    url(r'^events/(\d{4})/(\d+)/', views.month_events), #json
    url(r'^events/signup/', views.event_signup), #json
    url(r'^volunteers/(\d+)/', views.volunteer_info, name="profile"),
    url(r'^events/create/', views.add_event),
    url(r'^events/new/', views.add_event_endpoint), #json
    url(r'^events/info/(\d+)/', views.event_info),
#    url(r'^applications/', views.volunteer_list),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login'}),
    url(r'^programs/(\d+)/', views.program_events),
    url(r'^programs/json/', views.program_list), #json
    url(r'^accounts/profile/', views.profile, name="accountprofile"),
    url(r'^action/', views.action, name="action"),
    url(r'^links/', views.links),
    url(r'^calendar/', views.calendar, name="calendar")

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

