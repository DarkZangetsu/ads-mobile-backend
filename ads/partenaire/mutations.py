
import graphene
from .models import Utilisateur, Image, Display, Campaign, CampaignDisplay, Revenue, CampaignImage
from .schema import (
    UtilisateurType, ImageType, DisplayType, CampaignType,
    CampaignDisplayType, RevenueType, CampaignImageType
)
import os
from django.contrib.auth.hashers import check_password

# LOGIN
class LoginUtilisateur(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        mot_de_passe = graphene.String(required=True)

    utilisateur = graphene.Field(UtilisateurType)
    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, email, mot_de_passe):
        try:
            utilisateur = Utilisateur.objects.get(email=email)
            # Si mot_de_passe est hashé, utiliser check_password, sinon comparer directement
            if utilisateur.mot_de_passe == mot_de_passe or check_password(mot_de_passe, utilisateur.mot_de_passe):
                return LoginUtilisateur(utilisateur=utilisateur, ok=True, message="Login réussi")
            else:
                return LoginUtilisateur(utilisateur=None, ok=False, message="Mot de passe incorrect")
        except Utilisateur.DoesNotExist:
            return LoginUtilisateur(utilisateur=None, ok=False, message="Utilisateur non trouvé")

# --- Utilisateur ---
class CreateUtilisateur(graphene.Mutation):
    class Arguments:
        nom = graphene.String(required=True)
        prenom = graphene.String(required=True)
        email = graphene.String(required=True)
        mot_de_passe = graphene.String()
        role = graphene.String(required=True)
        permissions = graphene.JSONString()
        actif = graphene.Boolean()
        contact = graphene.String()
        pays = graphene.String()
        ville = graphene.String()
        picture = graphene.String()
        icone = graphene.String()

    utilisateur = graphene.Field(UtilisateurType)

    def mutate(self, info, **kwargs):
        mot_de_passe = kwargs.pop('mot_de_passe', None)
        utilisateur = Utilisateur(**kwargs)
        if mot_de_passe:
            utilisateur.set_password(mot_de_passe)
        utilisateur.save()
        return CreateUtilisateur(utilisateur=utilisateur)

class UpdateUtilisateur(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        nom = graphene.String()
        prenom = graphene.String()
        email = graphene.String()
        mot_de_passe = graphene.String()
        role = graphene.String()
        permissions = graphene.JSONString()
        actif = graphene.Boolean()
        contact = graphene.String()
        pays = graphene.String()
        ville = graphene.String()
        picture = graphene.String()
        icone = graphene.String()

    utilisateur = graphene.Field(UtilisateurType)

    def mutate(self, info, id, **kwargs):
        try:
            utilisateur = Utilisateur.objects.get(pk=id)
            mot_de_passe = kwargs.pop('mot_de_passe', None)
            for k, v in kwargs.items():
                setattr(utilisateur, k, v)
            if mot_de_passe:
                utilisateur.set_password(mot_de_passe)
            utilisateur.save()
            return UpdateUtilisateur(utilisateur=utilisateur)
        except Utilisateur.DoesNotExist:
            return None

class DeleteUtilisateur(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    ok = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Utilisateur.objects.get(pk=id).delete()
            return DeleteUtilisateur(ok=True)
        except Utilisateur.DoesNotExist:
            return DeleteUtilisateur(ok=False)

# --- Image ---
class CreateImage(graphene.Mutation):
    class Arguments:
        image = graphene.String(required=True)
        description = graphene.String()
        id_utilisateur_partenaire = graphene.Int()
    image_obj = graphene.Field(ImageType)
    def mutate(self, info, image, description=None, id_utilisateur_partenaire=None):
        image_path = os.path.join('media', image)
        image_obj = Image.objects.create(
            image=image_path,
            description=description,
            id_utilisateur_partenaire_id=id_utilisateur_partenaire
        )
        return CreateImage(image_obj=image_obj)
class UpdateImage(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        image = graphene.String()
        description = graphene.String()
    image_obj = graphene.Field(ImageType)
    def mutate(self, info, id, image=None, description=None):
        try:
            image_obj = Image.objects.get(pk=id)
            if image:
                image_obj.image = os.path.join('media', image)
            if description is not None:
                image_obj.description = description
            image_obj.save()
            return UpdateImage(image_obj=image_obj)
        except Image.DoesNotExist:
            return None
class DeleteImage(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    ok = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Image.objects.get(pk=id).delete()
            return DeleteImage(ok=True)
        except Image.DoesNotExist:
            return DeleteImage(ok=False)

# --- Display ---
class CreateDisplay(graphene.Mutation):
    class Arguments:
        display_name = graphene.String(required=True)
        localisation = graphene.String()
        id_utilisateur_partenaire = graphene.Int()
        actif = graphene.Boolean()
    display = graphene.Field(DisplayType)
    def mutate(self, info, display_name, localisation=None, id_utilisateur_partenaire=None, actif=True):
        display = Display.objects.create(
            display_name=display_name,
            localisation=localisation,
            id_utilisateur_partenaire_id=id_utilisateur_partenaire,
            actif=actif
        )
        return CreateDisplay(display=display)
class UpdateDisplay(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        display_name = graphene.String()
        localisation = graphene.String()
        id_utilisateur_partenaire = graphene.Int()
        actif = graphene.Boolean()
    display = graphene.Field(DisplayType)
    def mutate(self, info, id, **kwargs):
        try:
            display = Display.objects.get(pk=id)
            for k, v in kwargs.items():
                if v is not None:
                    setattr(display, k, v)
            display.save()
            return UpdateDisplay(display=display)
        except Display.DoesNotExist:
            return None
class DeleteDisplay(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    ok = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Display.objects.get(pk=id).delete()
            return DeleteDisplay(ok=True)
        except Display.DoesNotExist:
            return DeleteDisplay(ok=False)

# --- Campaign ---
class CreateCampaign(graphene.Mutation):
    class Arguments:
        campaign_name = graphene.String(required=True)
        status = graphene.String()
        start_date = graphene.types.datetime.Date()
        end_date = graphene.types.datetime.Date()
        budget = graphene.Float()
        description = graphene.String()
        id_utilisateur_createur = graphene.Int()
        id_image = graphene.Int()
    campaign = graphene.Field(CampaignType)
    def mutate(self, info, **kwargs):
        campaign = Campaign.objects.create(**kwargs)
        return CreateCampaign(campaign=campaign)
class UpdateCampaign(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        campaign_name = graphene.String()
        status = graphene.String()
        start_date = graphene.types.datetime.Date()
        end_date = graphene.types.datetime.Date()
        budget = graphene.Float()
        description = graphene.String()
        id_utilisateur_createur = graphene.Int()
        id_image = graphene.Int()
    campaign = graphene.Field(CampaignType)
    def mutate(self, info, id, **kwargs):
        try:
            campaign = Campaign.objects.get(pk=id)
            for k, v in kwargs.items():
                if v is not None:
                    setattr(campaign, k, v)
            campaign.save()
            return UpdateCampaign(campaign=campaign)
        except Campaign.DoesNotExist:
            return None
class DeleteCampaign(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    ok = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Campaign.objects.get(pk=id).delete()
            return DeleteCampaign(ok=True)
        except Campaign.DoesNotExist:
            return DeleteCampaign(ok=False)

# --- CampaignDisplay ---
class CreateCampaignDisplay(graphene.Mutation):
    class Arguments:
        id_campaign = graphene.Int(required=True)
        id_display = graphene.Int(required=True)
        date_debut_affichage = graphene.types.datetime.Date()
        date_fin_affichage = graphene.types.datetime.Date()
        nombre_affichages = graphene.Int()
    campaign_display = graphene.Field(CampaignDisplayType)
    def mutate(self, info, id_campaign, id_display, date_debut_affichage=None, date_fin_affichage=None, nombre_affichages=0):
        campaign_display = CampaignDisplay.objects.create(
            id_campaign_id=id_campaign,
            id_display_id=id_display,
            date_debut_affichage=date_debut_affichage,
            date_fin_affichage=date_fin_affichage,
            nombre_affichages=nombre_affichages
        )
        return CreateCampaignDisplay(campaign_display=campaign_display)
class UpdateCampaignDisplay(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        id_campaign = graphene.Int()
        id_display = graphene.Int()
        date_debut_affichage = graphene.types.datetime.Date()
        date_fin_affichage = graphene.types.datetime.Date()
        nombre_affichages = graphene.Int()
    campaign_display = graphene.Field(CampaignDisplayType)
    def mutate(self, info, id, **kwargs):
        try:
            campaign_display = CampaignDisplay.objects.get(pk=id)
            for k, v in kwargs.items():
                if v is not None:
                    setattr(campaign_display, k, v)
            campaign_display.save()
            return UpdateCampaignDisplay(campaign_display=campaign_display)
        except CampaignDisplay.DoesNotExist:
            return None
class DeleteCampaignDisplay(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    ok = graphene.Boolean()
    def mutate(self, info, id):
        try:
            CampaignDisplay.objects.get(pk=id).delete()
            return DeleteCampaignDisplay(ok=True)
        except CampaignDisplay.DoesNotExist:
            return DeleteCampaignDisplay(ok=False)

# --- Revenue ---
class CreateRevenue(graphene.Mutation):
    class Arguments:
        revenue = graphene.Float(required=True)
        source = graphene.String()
        description = graphene.String()
        date_revenue = graphene.types.datetime.Date()
        id_utilisateur_partenaire = graphene.Int()
        id_campaign = graphene.Int()
        id_display = graphene.Int()
    revenue_obj = graphene.Field(RevenueType)
    def mutate(self, info, revenue, source=None, description=None, date_revenue=None, id_utilisateur_partenaire=None, id_campaign=None, id_display=None):
        revenue_obj = Revenue.objects.create(
            revenue=revenue,
            source=source,
            description=description,
            date_revenue=date_revenue,
            id_utilisateur_partenaire_id=id_utilisateur_partenaire,
            id_campaign_id=id_campaign,
            id_display_id=id_display
        )
        return CreateRevenue(revenue_obj=revenue_obj)
class UpdateRevenue(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        revenue = graphene.Float()
        source = graphene.String()
        description = graphene.String()
        date_revenue = graphene.types.datetime.Date()
        id_utilisateur_partenaire = graphene.Int()
        id_campaign = graphene.Int()
        id_display = graphene.Int()
    revenue_obj = graphene.Field(RevenueType)
    def mutate(self, info, id, **kwargs):
        try:
            revenue_obj = Revenue.objects.get(pk=id)
            for k, v in kwargs.items():
                if v is not None:
                    setattr(revenue_obj, k, v)
            revenue_obj.save()
            return UpdateRevenue(revenue_obj=revenue_obj)
        except Revenue.DoesNotExist:
            return None
class DeleteRevenue(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    ok = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Revenue.objects.get(pk=id).delete()
            return DeleteRevenue(ok=True)
        except Revenue.DoesNotExist:
            return DeleteRevenue(ok=False)

# --- CampaignImage ---
class CreateCampaignImage(graphene.Mutation):
    class Arguments:
        id_campaign = graphene.Int(required=True)
        id_image = graphene.Int(required=True)
        ordre_affichage = graphene.Int()
    campaign_image = graphene.Field(CampaignImageType)
    def mutate(self, info, id_campaign, id_image, ordre_affichage=1):
        campaign_image = CampaignImage.objects.create(
            id_campaign_id=id_campaign,
            id_image_id=id_image,
            ordre_affichage=ordre_affichage
        )
        return CreateCampaignImage(campaign_image=campaign_image)
class UpdateCampaignImage(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        id_campaign = graphene.Int()
        id_image = graphene.Int()
        ordre_affichage = graphene.Int()
    campaign_image = graphene.Field(CampaignImageType)
    def mutate(self, info, id, **kwargs):
        try:
            campaign_image = CampaignImage.objects.get(pk=id)
            for k, v in kwargs.items():
                if v is not None:
                    setattr(campaign_image, k, v)
            campaign_image.save()
            return UpdateCampaignImage(campaign_image=campaign_image)
        except CampaignImage.DoesNotExist:
            return None
class DeleteCampaignImage(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    ok = graphene.Boolean()
    def mutate(self, info, id):
        try:
            CampaignImage.objects.get(pk=id).delete()
            return DeleteCampaignImage(ok=True)
        except CampaignImage.DoesNotExist:
            return DeleteCampaignImage(ok=False)

class Mutation(graphene.ObjectType):
    # Utilisateur
    create_utilisateur = CreateUtilisateur.Field()
    update_utilisateur = UpdateUtilisateur.Field()
    delete_utilisateur = DeleteUtilisateur.Field()
    login_utilisateur = LoginUtilisateur.Field()
    # Image
    create_image = CreateImage.Field()
    update_image = UpdateImage.Field()
    delete_image = DeleteImage.Field()
    # Display
    create_display = CreateDisplay.Field()
    update_display = UpdateDisplay.Field()
    delete_display = DeleteDisplay.Field()
    # Campaign
    create_campaign = CreateCampaign.Field()
    update_campaign = UpdateCampaign.Field()
    delete_campaign = DeleteCampaign.Field()
    # CampaignDisplay
    create_campaign_display = CreateCampaignDisplay.Field()
    update_campaign_display = UpdateCampaignDisplay.Field()
    delete_campaign_display = DeleteCampaignDisplay.Field()
    # Revenue
    create_revenue = CreateRevenue.Field()
    update_revenue = UpdateRevenue.Field()
    delete_revenue = DeleteRevenue.Field()
    # CampaignImage
    create_campaign_image = CreateCampaignImage.Field()
    update_campaign_image = UpdateCampaignImage.Field()
    delete_campaign_image = DeleteCampaignImage.Field()
