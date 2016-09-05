
from django.conf.urls import url, include
from department import views as team_views
import views

urlpatterns = [

    url(r'^request/(?P<request_id>[0-9]+)/approve/$', views.approve_request, name='request-approve'),
    url(r'^request/(?P<request_id>[0-9]+)/reject/$', views.reject_request, name='request-reject'),
    # url(r'^claim/(?P<claim_id>[0-9]+)/submit/$', claim_views.submit_claim, name='claim-submit'),
    # url(r'^claim/(?P<claim_id>[0-9]+)/settle/$', claim_views.settle_claim, name='claim-settle'),

    url(r'^requests/$', views.RequestList.as_view(), name='requests'),
    url(r'^request/(?P<request_id>[0-9]+)/$', views.RequestDetail.as_view()),

    # url(r'^claims/approved$', claim_views.approved_claims, name='claim-approved'),
    # url(r'^claims/rejected$', claim_views.rejected_claims, name='claim-rejected'),
   
]