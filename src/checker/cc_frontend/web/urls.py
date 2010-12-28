from django.conf.urls.defaults import patterns, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    ( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ) ),

    # Uncomment the next line to enable the admin:
    ( r'^admin/', include( 'django.contrib.admin.site.urls' ) ),
) 

# Top level links pages
urlpatterns += patterns( 'checker.cc_frontend.web.views',
    ( r'^$', 'default' ),
    ( r'^about/$', 'default', { 'action' : 'about' } ),
    ( r'^references/$', 'default', { 'action' : 'references' }),
    ( r'^news/$', 'default', { 'action' : 'news' }),
)

# Contest level links
urlpatterns += patterns( 'checker.cc_frontend.web.contests',
    ( r'^contests/$', 'default' ),
    ( r'^contests/all/$', 'show_all_contests' ),
    ( r'^contests/all/(?P<page>\d+)/$', 'show_all_contests' ),
    ( r'^contests/(?P<contest_id>\d+)/$', 'show_contest' ),
    ( r'^contests/(?P<contest_id>\d+)/(?P<action>\w+)/$', 'show_contest' ),
    ( r'^contests/(?P<contest_id>\d+)/(?P<action>\w+)/(?P<page>\d+)/$', 'show_contest' ),
)

# Problem level links
urlpatterns += patterns( 'checker.cc_frontend.web.problems',
    (r'^problems/$', 'problems_default'),
    (r'^problems/all/', 'show_all_problems'),
    (r'^problems/all/(?P<page>\d+)/$', 'show_all_problems'),
    (r'^problems/(?P<problem_id>\d+)/$', 'show_problem'),
    (r'^problems/(?P<problem_id>\d+)/submit/$', 'submit_solution'),
    (r'^problems/(?P<problem_id>\d+)/(?P<action>\w+)/$', 'show_problem'),
)

# Submission level links
urlpatterns += patterns('checker.cc_frontned.web.submissions',
    (r'^$', 'show_all_submissions'),
    (r'^(?P<page>\d+)/$', 'show_all_submissions'),
    (r'^contest-(?P<contest_id>\d+)/$', 'show_contest_submissions'),
    (r'^contest-(?P<contest_id>\d+)/(?P<page>\d+)/$', 'show_contest_submissions'),
    (r'^problem-(?P<problem_id>\d+)/$', 'show_problem_submissions'),
    (r'^problem-(?P<problem_id>\d+)/(?P<page>\d+)/$', 'show_problem_submissions'),
    (r'^submission/(?P<submission_id>\d+)/$'),
)
