from django.db import models
from users.models import User
from courses.models import Course

# EduCoding Payment Gateway using STRIPE

class PaymentProcessorVariables(models.Model): #{
    paymentProcessorID = models.CharField(max_length = 225)
    paidID = models.CharField(max_length = 225)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    course = models.ManyToManyField(Course)
    createdAt = models.DateTimeField(auto_now_add = True)
    
    
#}


class Payment(models.Model): #{
    payment_intent = models.ForeignKey(PaymentProcessorVariables, on_delete = models.CASCADE)
    totalPricePaid = models.DecimalField(max_digits = 7, decimal_places = 2)
    createdAt = models.DateTimeField(auto_now_add = True)

#}