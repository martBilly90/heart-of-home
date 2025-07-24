from django.contrib import admin
from .models import Listing, Agent
from .models import Listing, Agent, Message

admin.site.register(Listing)
admin.site.register(Agent)
admin.site.register(Message)