from xml.etree.ElementInclude import include
from django.urls import path
from django.urls import include
from paymentGateway.views import PaymentHandler, Webhook
from paymentGateway.views import PaymentProcessorVariables
from paymentGateway.views import Payment

urlpatterns = [
    path("", PaymentHandler.as_view()),
    path("webhook/", Webhook.as_view())
]


