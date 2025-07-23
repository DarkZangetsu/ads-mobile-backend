import graphene
from .models import Utilisateur, Image, Display, Campaign, CampaignDisplay, Revenue, CampaignImage
from .schema import (
    UtilisateurType, ImageType, DisplayType, CampaignType,
    CampaignDisplayType, RevenueType, CampaignImageType
)

class Query(graphene.ObjectType):
    all_utilisateurs = graphene.List(UtilisateurType)
    utilisateur_by_id = graphene.Field(UtilisateurType, id=graphene.Int(required=True))

    all_images = graphene.List(ImageType)
    image_by_id = graphene.Field(ImageType, id=graphene.Int(required=True))

    all_displays = graphene.List(DisplayType)
    display_by_id = graphene.Field(DisplayType, id=graphene.Int(required=True))

    all_campaigns = graphene.List(CampaignType)
    campaign_by_id = graphene.Field(CampaignType, id=graphene.Int(required=True))

    all_campaign_displays = graphene.List(CampaignDisplayType)
    campaign_display_by_id = graphene.Field(CampaignDisplayType, id=graphene.Int(required=True))

    all_revenues = graphene.List(RevenueType)
    revenue_by_id = graphene.Field(RevenueType, id=graphene.Int(required=True))

    all_campaign_images = graphene.List(CampaignImageType)
    campaign_image_by_id = graphene.Field(CampaignImageType, id=graphene.Int(required=True))

    def resolve_all_utilisateurs(root, info):
        return Utilisateur.objects.all()

    def resolve_utilisateur_by_id(root, info, id):
        try:
            return Utilisateur.objects.get(pk=id)
        except Utilisateur.DoesNotExist:
            return None

    def resolve_all_images(root, info):
        return Image.objects.all()

    def resolve_image_by_id(root, info, id):
        try:
            return Image.objects.get(pk=id)
        except Image.DoesNotExist:
            return None

    def resolve_all_displays(root, info):
        return Display.objects.all()

    def resolve_display_by_id(root, info, id):
        try:
            return Display.objects.get(pk=id)
        except Display.DoesNotExist:
            return None

    def resolve_all_campaigns(root, info):
        return Campaign.objects.all()

    def resolve_campaign_by_id(root, info, id):
        try:
            return Campaign.objects.get(pk=id)
        except Campaign.DoesNotExist:
            return None

    def resolve_all_campaign_displays(root, info):
        return CampaignDisplay.objects.all()

    def resolve_campaign_display_by_id(root, info, id):
        try:
            return CampaignDisplay.objects.get(pk=id)
        except CampaignDisplay.DoesNotExist:
            return None

    def resolve_all_revenues(root, info):
        return Revenue.objects.all()

    def resolve_revenue_by_id(root, info, id):
        try:
            return Revenue.objects.get(pk=id)
        except Revenue.DoesNotExist:
            return None

    def resolve_all_campaign_images(root, info):
        return CampaignImage.objects.all()

    def resolve_campaign_image_by_id(root, info, id):
        try:
            return CampaignImage.objects.get(pk=id)
        except CampaignImage.DoesNotExist:
            return None
