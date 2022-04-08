from django.shortcuts import render
from rest_framework.views import APIView
#from .models import Course
#import decimal
from courses.models import Course
from rest_framework import status
from rest_framework.response import Response
from paymentGateway.models import PaymentProcessorVariables
from paymentGateway.models import Payment
from users.models import User
from decimal import Decimal

import stripe
import os
import json


#Vergeet migratiosn niet te doen!!!!!
# MAAK MIGRATIONS ANDERS GAAT DIT NIET WERKEN NOTITIE!!!!

# EduCoding payment handler & webhook views
# we gebruiken environment variables voor onze API keys & secret keys

#STRIPE_API_KEY = os.environ.get("ENV_STRIPE_API_KEY")
API_ENDPOINT = ""
stripe.api_key = "sk_test_51Kkv5MAOagIu5p4WxjSIWTe0ysM5JZDtdWPM0nx6eRblkEqc2dOzQijOTFWi0rpdr8T9MvrtZEZ5rETa2y6oixeu00A4Ir8zfb"


class PaymentHandler(APIView): #{
    def post(self, request): #{
        if request.body: #{
            body = json.loads(request.body)
            if body and len(body): #{
                courseItemL = []
                cartCourses = []
                for x in body: #{
                    try:
                        courseObj_call = Course.objects.get(courseUUID = x)
                        courseItemObject = {
                            "price_data":{
                                "currency":"eur",
                                "unit_amount": int(courseObj_call.price * 100), # we maken onze unit_amount een integer
                                "product_data": {
                                "name":courseObj_call.title
                                },
                            },                                                  
                            "quantity":1
                        }
                        
                        courseItemL.append(courseItemObject)
                        #cartCourses.append(courseItemObject)
                        cartCourses.append(courseObj_call)
                        
                    except Course.DoesNotExist:
                        #return Exception
                        return Response(status = status.HTTP_400_BAD_REQUEST)
                    
            else:
                return Response(status = status.HTTP_400_BAD_REQUEST)  
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        
        checkoutSession = stripe.checkout.Session.create(
            payment_method_types = ["ideal"],
            line_items = courseItemL,
            mode = "payment",
            success_url = "http://localhost:3000/",
            cancel_url = "http://localhost:3000/"
        )
        
        processed = PaymentProcessorVariables.objects.create(
            # als dit niet werkt gebruik .paymentProcessorID
            paymentProcessorID = checkoutSession.payment_intent,
            paidID = checkoutSession.id,
            #user = request.user
            user = User.objects.get(id=1)
        )
        
        processed.course.add(*cartCourses)
        return Response({"url":checkoutSession.url})
        
                    #}
                #}
            #}
            
        #}

#}


class Webhook(APIView): #{
    def post(self, request): #{
        payload = request.body
        # we verifieren of verzonden data vanuit een stripe endpoint komt
        req_headers_signature = request.META["HTTP_STRIPE_SIGNATURE"]
        
        dataEvent = None
        
        try:
            dataEvent = stripe.Webhook.construct_event(
                payload=payload,req_headers_signature=req_headers_signature,API_ENDPOINT=API_ENDPOINT
            )
            # je kan het ook general maken als dit problemen veroorzaakt
        except stripe.error.SignatureVerificationError:
            # als data niet van een stripe webhook komt is het UNAUTHORIZED
            return Response(status = status.HTTP_401_UNAUTHORIZED)
        
        if dataEvent["type"] == "checkout.session.complete": #{
            session = dataEvent["data"]["object"]
            
            try:            
                intent = PaymentProcessorVariables.objects.get(paidID = session.id, paymentProcessorID = session.payment_intent)

            except PaymentProcessorVariables.DoesNotExist:
                return Response(status = status.HTTP_400_BAD_REQUEST)
            
            Payment.objects.create(
                payment_intent=intent,
                totalPricePaid=Decimal(session.amount_total / 100)
            )
            
            intent.user.courseActivated.add(*intent.course.all())
            
            return Response(status = 200)
        
        
            
            #}
        
        #}
    
    #}