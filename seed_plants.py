#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'botaniq.settings')
django.setup()

from plants.models import Plant

# Sample plant data
plants_data = [
    {
        "common_names": ["Ginger", "Ginger Root"],
        "scientific_name": "Zingiber officinale",
        "plant_family": "Zingiberaceae",
        "description": "A flowering plant whose rhizome, ginger root or ginger, is widely used as a spice and folk medicine.",
        "habitat": "Tropical regions",
        "regions": ["Asia", "Africa", "Caribbean"],
        "traditional_systems": ["Ayurveda", "Traditional Chinese Medicine", "Western Herbalism"],
        "cultural_uses": ["Digestive aid", "Anti-inflammatory", "Nausea relief"],
        "parts_used": ["Rhizome"],
        "preparations": ["Tea", "Powder", "Fresh root"],
        "dosage_info": "1-2g dried rhizome, 3 times daily",
        "active_compounds": ["Gingerol", "Shogaol", "Zingiberene"],
        "research_studies": ["Anti-nausea effects", "Anti-inflammatory properties"],
        "pharmacological_actions": ["Anti-emetic", "Analgesic", "Antioxidant"],
        "safety_warnings": "May interact with blood thinners",
        "contraindications": "Pregnancy (high doses), Gallstones",
        "interactions": "Warfarin, Aspirin",
        "toxicity_info": "Generally safe in culinary amounts",
        "conservation_status": "Not endangered",
        "sustainability_info": "Widely cultivated, sustainable",
        "ethical_sourcing": "Choose organic, fair trade certified",
        "image_url": "https://example.com/ginger.jpg",
        "image_credit": "Public domain botanical illustration",
        "is_verified": True,
    },
    {
        "common_names": ["Turmeric", "Curcuma"],
        "scientific_name": "Curcuma longa",
        "plant_family": "Zingiberaceae",
        "description": "A flowering plant of the ginger family, widely used as a spice and medicinal herb.",
        "habitat": "Tropical climates",
        "regions": ["India", "Southeast Asia"],
        "traditional_systems": ["Ayurveda", "Traditional Chinese Medicine"],
        "cultural_uses": ["Anti-inflammatory", "Wound healing", "Digestive health"],
        "parts_used": ["Rhizome"],
        "preparations": ["Powder", "Paste", "Tea"],
        "dosage_info": "500mg-2g curcumin daily",
        "active_compounds": ["Curcumin", "Curcuminoids"],
        "research_studies": ["Anti-inflammatory effects", "Antioxidant properties"],
        "pharmacological_actions": ["Anti-inflammatory", "Antioxidant", "Anticancer"],
        "safety_warnings": "May cause stomach upset",
        "contraindications": "Gallstones, Pregnancy (high doses)",
        "interactions": "Blood thinners",
        "toxicity_info": "Low toxicity, generally safe",
        "conservation_status": "Not endangered",
        "sustainability_info": "Major agricultural crop",
        "ethical_sourcing": "Organic certification preferred",
        "image_url": "https://example.com/turmeric.jpg",
        "image_credit": "Botanical illustration",
        "is_verified": True,
    },
    {
        "common_names": ["Peppermint", "Mint"],
        "scientific_name": "Mentha piperita",
        "plant_family": "Lamiaceae",
        "description": "A hybrid mint, a cross between watermint and spearmint, used for culinary and medicinal purposes.",
        "habitat": "Temperate regions",
        "regions": ["Europe", "North America", "Asia"],
        "traditional_systems": ["Western Herbalism", "Traditional European Medicine"],
        "cultural_uses": ["Digestive aid", "Headache relief", "Respiratory health"],
        "parts_used": ["Leaves"],
        "preparations": ["Tea", "Essential oil", "Capsules"],
        "dosage_info": "1-2 cups tea daily",
        "active_compounds": ["Menthol", "Menthone"],
        "research_studies": ["IBS treatment", "Headache relief"],
        "pharmacological_actions": ["Antispasmodic", "Analgesic", "Antimicrobial"],
        "safety_warnings": "May cause heartburn in some individuals",
        "contraindications": "GERD, Hiatal hernia",
        "interactions": "Medications metabolized by liver",
        "toxicity_info": "Safe in normal amounts",
        "conservation_status": "Not endangered",
        "sustainability_info": "Widely cultivated",
        "ethical_sourcing": "Organic preferred",
        "image_url": "https://example.com/peppermint.jpg",
        "image_credit": "Herbal illustration",
        "is_verified": True,
    }
]

# Seed the database
for plant_data in plants_data:
    plant, created = Plant.objects.get_or_create(
        scientific_name=plant_data['scientific_name'],
        defaults=plant_data
    )
    if created:
        print(f"Created plant: {plant.scientific_name}")
    else:
        print(f"Plant already exists: {plant.scientific_name}")

print(f"Database seeded with {len(plants_data)} sample plants!")
