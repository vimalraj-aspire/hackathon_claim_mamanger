
from django.conf.urls import url, include
from department import views as team_views
from claim import views as claim_views


urlpatterns = [

    url(r'^claim/(?P<claim_id>[0-9]+)/approve/$', claim_views.approve_claim, name='claim-approve'),
    url(r'^claim/(?P<claim_id>[0-9]+)/reject/$', claim_views.reject_claim, name='claim-reject'),
    url(r'^claim/(?P<claim_id>[0-9]+)/submit/$', claim_views.submit_claim, name='claim-submit'),
    url(r'^claim/(?P<claim_id>[0-9]+)/settle/$', claim_views.settle_claim, name='claim-settle'),

    url(r'^claims/$', claim_views.ClaimList.as_view(), name='claims'),
    url(r'^claim/(?P<claim_id>[0-9]+)/$', claim_views.ClaimDetail.as_view()),

    url(r'^claims/approved$', claim_views.approved_claims, name='claim-approved'),
    url(r'^claims/rejected$', claim_views.rejected_claims, name='claim-rejected'),
   
]