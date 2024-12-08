from django.contrib import admin
from order.models import *


admin.site.register(Address)
admin.site.register(Orders)
admin.site.register(Payments)

