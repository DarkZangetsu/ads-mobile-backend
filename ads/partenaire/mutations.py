from graphene_file_upload.scalars import Upload
import graphene
from .models import Utilisateur, Image, Display, Campaign, CampaignDisplay, Revenue, CampaignImage
from .schema import (
    UtilisateurType, ImageType, DisplayType, CampaignType,
    CampaignDisplayType, RevenueType, CampaignImageType
)
import os
from django.contrib.auth.hashers import check_password
from django.core.files.storage import default_storage

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
# Mutation pour upload d'image via multipart/form-data
class UploadImage(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)
        description = graphene.String()
        id_utilisateur_partenaire = graphene.Int()
        id_campaign = graphene.Int()

    image_obj = graphene.Field(ImageType)
    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, file, description=None, id_utilisateur_partenaire=None, id_campaign=None):
        try:
            image_obj = Image.objects.create(
                image=file,
                description=description,
                id_utilisateur_partenaire_id=id_utilisateur_partenaire
            )
            # Si une campagne est précisée, rattacher l'image à la campagne
            if id_campaign:
                campaign = Campaign.objects.get(pk=id_campaign)
                CampaignImage.objects.create(id_campaign=campaign, id_image=image_obj)
                # Compter le nombre d'images rattachées à cette campagne
                nb_images = CampaignImage.objects.filter(id_campaign=campaign).count()
                # Si la campagne était en 'upload' et a au moins 3 images, passer à 'pending'
                if campaign.status == 'upload' and nb_images >= 3:
                    campaign.status = 'pending'
                    campaign.save()
            return UploadImage(image_obj=image_obj, ok=True, message="Image uploadée avec succès")
        except Exception as e:
            return UploadImage(image_obj=None, ok=False, message=f"Erreur upload: {e}")

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
        id_displays = graphene.List(graphene.Int, required=False)
    campaign = graphene.Field(CampaignType)
    def mutate(self, info, id_displays=None, **kwargs):
        campaign = Campaign.objects.create(**kwargs)
        # Rattacher les displays sélectionnés à la campagne
        if id_displays:
            for display_id in id_displays:
                display = Display.objects.get(pk=display_id)
                CampaignDisplay.objects.create(id_campaign=campaign, id_display=display)
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
        from datetime import date
        try:
            campaign = Campaign.objects.get(pk=id)
            status = kwargs.get('status', None)
            # Si le commercial annule (status 'cancelled'), repasser à 'upload' et supprimer les images rattachées
            if status == 'cancelled':
                campaign_images = CampaignImage.objects.filter(id_campaign=campaign)
                for ci in campaign_images:
                    if ci.id_image and ci.id_image.image:
                        ci.id_image.image.delete(save=False)
                        ci.id_image.delete()
                    ci.delete()
                kwargs['status'] = 'upload'
            # Si le commercial valide, passer à 'submitted'
            elif status == 'submitted':
                kwargs['status'] = 'submitted'
            # Si la campagne est soumise et la date de fin est passée, passer à 'completed'
            elif campaign.status == 'submitted' and campaign.end_date and campaign.end_date <= date.today():
                kwargs['status'] = 'completed'
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

class Mutation(graphene.ObjectType):
    # Utilisateur
    create_utilisateur = CreateUtilisateur.Field()
    update_utilisateur = UpdateUtilisateur.Field()
    delete_utilisateur = DeleteUtilisateur.Field()
    login_utilisateur = LoginUtilisateur.Field()

    # Image
    upload_image = UploadImage.Field()

    # Display
    create_display = CreateDisplay.Field()
    update_display = UpdateDisplay.Field()
    delete_display = DeleteDisplay.Field()

    # Campaign
    create_campaign = CreateCampaign.Field()
    update_campaign = UpdateCampaign.Field()
    delete_campaign = DeleteCampaign.Field()

    # Revenue
    create_revenue = CreateRevenue.Field()
    update_revenue = UpdateRevenue.Field()
    delete_revenue = DeleteRevenue.Field()
