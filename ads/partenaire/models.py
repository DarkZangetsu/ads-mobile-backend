from django.db import models

class Utilisateur(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('commercial', 'Commercial'),
        ('partenaire', 'Partenaire'),
        ('client', 'Client'),
        ('directeur_commercial', 'Directeur Commercial'),
        ('responsable_site', 'Responsable Site'),
        ('proprietaire', 'Propriétaire'),
    ]
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    mot_de_passe = models.CharField(max_length=255, blank=True, null=True)

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.mot_de_passe = make_password(raw_password)
        return self.mot_de_passe

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.mot_de_passe)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    permissions = models.JSONField(default=dict)
    actif = models.BooleanField(default=True)
    contact = models.CharField(max_length=150, blank=True, null=True)
    pays = models.CharField(max_length=150, blank=True, null=True)
    ville = models.CharField(max_length=150, blank=True, null=True)
    picture = models.TextField(blank=True, null=True)
    last_connexion = models.DateTimeField(auto_now=True)
    icone = models.CharField(max_length=50, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'utilisateurs'
        indexes = [
            models.Index(fields=['role'], name='idx_utilisateurs_role'),
        ]

class Image(models.Model):
    image = models.TextField()
    description = models.TextField(blank=True, null=True)
    id_utilisateur_partenaire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    date_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'image'

class Display(models.Model):
    display_name = models.TextField()
    localisation = models.TextField(blank=True, null=True)
    id_utilisateur_partenaire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='displays', blank=True, null=True)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'display'

class Campaign(models.Model):
    STATUS_CHOICES = [
        ('upload', 'Upload'),
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    campaign_name = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upload')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    id_utilisateur_createur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='created_campaigns', blank=True, null=True)
    id_image = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'campaign'
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__isnull=True) | models.Q(start_date__lte=models.F('end_date')),
                name='check_campaign_dates',
            ),
        ]
        indexes = [
            models.Index(fields=['status'], name='idx_campaign_status'),
            models.Index(fields=['start_date', 'end_date'], name='idx_campaign_dates'),
        ]

class CampaignDisplay(models.Model):
    id_campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    id_display = models.ForeignKey(Display, on_delete=models.CASCADE)
    date_debut_affichage = models.DateField(blank=True, null=True)
    date_fin_affichage = models.DateField(blank=True, null=True)
    nombre_affichages = models.IntegerField(default=0)

    class Meta:
        db_table = 'campaignDisplay'
        unique_together = ('id_campaign', 'id_display')
        constraints = [
            models.CheckConstraint(
                check=models.Q(date_fin_affichage__isnull=True) | models.Q(date_debut_affichage__lte=models.F('date_fin_affichage')),
                name='check_display_dates',
            ),
        ]
        indexes = [
            models.Index(fields=['date_debut_affichage', 'date_fin_affichage'], name='idx_campaign_displays_dates'),
        ]

class Revenue(models.Model):
    revenue = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_revenue = models.DateField(auto_now_add=True)
    id_utilisateur_partenaire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='revenues', blank=True, null=True)
    id_campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, blank=True, null=True)
    id_display = models.ForeignKey(Display, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'revenue'
        indexes = [
            models.Index(fields=['date_revenue'], name='idx_revenue_date'),
        ]

class CampaignImage(models.Model):
    id_campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    id_image = models.ForeignKey(Image, on_delete=models.CASCADE)
    ordre_affichage = models.IntegerField(default=1)

    class Meta:
        db_table = 'campaignImage'
        unique_together = ('id_campaign', 'id_image')
