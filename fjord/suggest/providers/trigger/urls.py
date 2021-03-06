from django.conf.urls import patterns, url

from fjord.suggest.providers.trigger.analyzer_views import (
    TriggerRuleListView,
    TriggerRuleCreateView,
    TriggerRuleUpdateView,
)
from fjord.suggest.providers.trigger.api_views import TriggerRuleMatchViewAPI


urlpatterns = patterns(
    'fjord.suggest.providers.trigger.views',

    url(r'analytics/triggerrule/?$', TriggerRuleListView.as_view(),
        name='triggerrules'),
    url(r'analytics/triggerrule/create/?$', TriggerRuleCreateView.as_view(),
        name='triggerrules-create'),
    url(r'analytics/triggerrule/(?P<pk>\d+)/update/?$',
        TriggerRuleUpdateView.as_view(), name='triggerrules-update'),

    url(r'api/v1/analytics/triggerrule/match/?$',
        TriggerRuleMatchViewAPI.as_view(), name='triggerrule-match'),
)
