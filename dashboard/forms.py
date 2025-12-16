from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from plants.models import Plant
from .models import UserProfile


class PlantForm(forms.ModelForm):
    """Form for adding/editing plants in admin dashboard"""

    # Convert JSON fields to text inputs for easier editing
    common_names = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        help_text="Enter common names separated by commas (e.g., Ginger, Ginger Root)",
        label="Common Names"
    )

    traditional_systems = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2}),
        help_text="Traditional medicine systems (e.g., Ayurveda, TCM)",
        label="Traditional Systems"
    )

    cultural_uses = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Cultural and historical uses",
        label="Cultural Uses"
    )

    parts_used = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2}),
        help_text="Plant parts used medicinally",
        label="Parts Used"
    )

    preparations = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Traditional preparation methods",
        label="Preparations"
    )

    active_compounds = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2}),
        help_text="Known active compounds",
        label="Active Compounds"
    )

    pharmacological_actions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2}),
        help_text="Pharmacological effects",
        label="Pharmacological Actions"
    )

    research_studies = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="Scientific studies and findings",
        label="Research Studies"
    )

    regions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2}),
        help_text="Geographical regions where found",
        label="Regions"
    )

    class Meta:
        model = Plant
        fields = [
            'scientific_name', 'common_names', 'plant_family', 'description',
            'habitat', 'regions', 'traditional_systems', 'cultural_uses',
            'parts_used', 'preparations', 'dosage_info', 'active_compounds',
            'pharmacological_actions', 'research_studies', 'safety_warnings',
            'contraindications', 'interactions', 'toxicity_info',
            'conservation_status', 'sustainability_info', 'ethical_sourcing',
            'image_url', 'image_credit', 'is_verified'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'dosage_info': forms.Textarea(attrs={'rows': 2}),
            'safety_warnings': forms.Textarea(attrs={'rows': 2}),
            'contraindications': forms.Textarea(attrs={'rows': 2}),
            'interactions': forms.Textarea(attrs={'rows': 2}),
            'toxicity_info': forms.Textarea(attrs={'rows': 2}),
            'sustainability_info': forms.Textarea(attrs={'rows': 2}),
            'ethical_sourcing': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_common_names(self):
        """Convert comma-separated string to list"""
        data = self.cleaned_data['common_names']
        if data:
            return [name.strip() for name in data.split(',') if name.strip()]
        return []

    def clean_traditional_systems(self):
        """Convert comma-separated string to list"""
        data = self.cleaned_data.get('traditional_systems', '')
        if data:
            return [system.strip() for system in data.split(',') if system.strip()]
        return []

    def clean_cultural_uses(self):
        """Convert newline-separated string to list"""
        data = self.cleaned_data.get('cultural_uses', '')
        if data:
            return [use.strip() for use in data.split('\n') if use.strip()]
        return []

    def clean_parts_used(self):
        """Convert comma-separated string to list"""
        data = self.cleaned_data.get('parts_used', '')
        if data:
            return [part.strip() for part in data.split(',') if part.strip()]
        return []

    def clean_preparations(self):
        """Convert newline-separated string to list"""
        data = self.cleaned_data.get('preparations', '')
        if data:
            return [prep.strip() for prep in data.split('\n') if prep.strip()]
        return []

    def clean_active_compounds(self):
        """Convert comma-separated string to list"""
        data = self.cleaned_data.get('active_compounds', '')
        if data:
            return [compound.strip() for compound in data.split(',') if compound.strip()]
        return []

    def clean_pharmacological_actions(self):
        """Convert comma-separated string to list"""
        data = self.cleaned_data.get('pharmacological_actions', '')
        if data:
            return [action.strip() for action in data.split(',') if action.strip()]
        return []

    def clean_research_studies(self):
        """Convert newline-separated string to list"""
        data = self.cleaned_data.get('research_studies', '')
        if data:
            return [study.strip() for study in data.split('\n') if study.strip()]
        return []

    def clean_regions(self):
        """Convert comma-separated string to list"""
        data = self.cleaned_data.get('regions', '')
        if data:
            return [region.strip() for region in data.split(',') if region.strip()]
        return []


class CustomUserCreationForm(UserCreationForm):
    """Extended user registration form with additional fields"""
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        help_text="Required. Enter your phone number.",
        widget=forms.TextInput(attrs={'placeholder': '+254 XXX XXX XXX'})
    )
    location = forms.CharField(
        max_length=100,
        required=True,
        help_text="Required. Enter your location (city, country).",
        widget=forms.TextInput(attrs={'placeholder': 'Nairobi, Kenya'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "location", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Create user profile
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data["phone_number"],
                location=self.cleaned_data["location"]
            )
        return user


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile"""
    email = forms.EmailField(required=True, help_text="Your email address")

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'location', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about your interest in medicinal plants...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Update user email
            profile.user.email = self.cleaned_data['email']
            profile.user.save()
            profile.save()
        return profile
