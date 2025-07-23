import graphene
from graphene_django import DjangoObjectType
from .models import Utilisateur, Image, Display, Campaign, CampaignDisplay, Revenue, CampaignImage

class UtilisateurType(DjangoObjectType):
    class Meta:
        model = Utilisateur
        fields = "__all__"

class ImageType(DjangoObjectType):
    class Meta:
        model = Image
        fields = "__all__"

class DisplayType(DjangoObjectType):
    class Meta:
        model = Display
        fields = "__all__"

class CampaignType(DjangoObjectType):
    class Meta:
        model = Campaign
        fields = "__all__"

class CampaignDisplayType(DjangoObjectType):
    class Meta:
        model = CampaignDisplay
        fields = "__all__"

class RevenueType(DjangoObjectType):
    class Meta:
        model = Revenue
        fields = "__all__"

class CampaignImageType(DjangoObjectType):
    class Meta:
        model = CampaignImage
        fields = "__all__"
