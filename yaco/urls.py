from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('yaco.coreviews',
	url(r'^$',  									'view_redirect'),
	url(r'^home/$', 								'view_index', 		name='index'),
	url(r'^dashboard/$', 							'view_dashboard', 	name='dashboard'),
)

urlpatterns += patterns('yaco.editor.views',
	url(r'^config/$',  								'view_cfg_list', 		name="config_list"),
	url(r'^config/new$',  							'view_cfg_new', 		name="config_new"),
	url(r'^config/(?P<uuid>[a-f\d]+)$', 	 		'view_cfg_display',		name="config_display"),
	url(r'^config/(?P<uuid>[a-f\d]+)/edit$',  		'view_cfg_edit',		name="config_edit"),
	url(r'^config/(?P<uuid>[a-f\d]+)/edit/async$', 	'view_cfg_api', 		name="config_api"),
	url(r'^scriptlet/new$',  						'view_scpt_new', 		name="scriptlet_new"),
	url(r'^scriptlet/(?P<uuid>[a-f\d]+)$', 	 		'view_scpt_display',	name="scriptlet_display"),
	url(r'^scriptlet/(?P<uuid>[a-f\d]+)/edit$',  	'view_scpt_edit',		name="scriptlet_edit"),
)

urlpatterns += patterns('yaco.machine.api',
	url(r'^machine/(?P<uuid>[a-f\d]+)/config$', 	'api_config', 		name='api.config'),
	url(r'^machine/(?P<uuid>[a-f\d]+)/refresh$', 	'api_refresh', 		name='api.refresh'),
)
