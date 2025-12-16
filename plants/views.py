from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.conf import settings
import requests
import os
from .models import Plant

# Optional ML imports - will be None if not available
try:
    from sentence_transformers import SentenceTransformer, util
    import numpy as np
    ML_AVAILABLE = True
except ImportError:
    SentenceTransformer = None
    util = None
    np = None
    ML_AVAILABLE = False


def get_research_summary(plant):
    """Generate AI-powered research summary using Mistral AI"""
    api_key = os.environ.get('MISTRAL_API_KEY')
    if not api_key:
        return None

    # Prepare research data
    research_data = []
    if plant.research_studies:
        research_data.extend(plant.research_studies)
    if plant.pharmacological_actions:
        research_data.append(f"Pharmacological actions: {', '.join(plant.pharmacological_actions)}")
    if plant.active_compounds:
        research_data.append(f"Active compounds: {', '.join(plant.active_compounds)}")

    if not research_data:
        return None

    # Create prompt
    prompt = f"""
    Summarize the key scientific research findings for {plant.get_primary_common_name()} ({plant.scientific_name}).

    Research data:
    {'; '.join(research_data)}

    Traditional uses: {', '.join(plant.cultural_uses) if plant.cultural_uses else 'Various traditional uses'}

    Provide a concise 2-3 sentence summary of the most important research findings, focusing on efficacy and mechanisms of action.
    """

    try:
        response = requests.post(
            'https://api.mistral.ai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'mistral-medium',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 200,
                'temperature': 0.3
            },
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content'].strip()
        else:
            print(f"Mistral API error: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error calling Mistral API: {e}")
        return None


# Global model cache to avoid reloading
_model = None

def get_sentence_model():
    """Get or create sentence transformer model"""
    global _model
    if _model is None and ML_AVAILABLE:
        try:
            _model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Warning: Could not load AI model: {e}")
            _model = None
    return _model


def smart_search_plants(query, limit=20):
    """AI-powered semantic search for plants"""
    if not query.strip():
        return Plant.objects.filter(is_verified=True)[:limit]

    # Check if ML dependencies are available
    if not ML_AVAILABLE:
        # Fallback to basic search
        return Plant.objects.filter(
            Q(scientific_name__icontains=query) |
            Q(common_names__icontains=query) |
            Q(description__icontains=query)
        )[:limit]

    model = get_sentence_model()
    if not model:
        # Fallback to basic search
        return Plant.objects.filter(
            Q(scientific_name__icontains=query) |
            Q(common_names__icontains=query) |
            Q(description__icontains=query)
        )[:limit]

    # Get all verified plants
    plants = list(Plant.objects.filter(is_verified=True))
    if not plants:
        return Plant.objects.none()

    # Create search texts combining multiple fields
    search_texts = []
    for plant in plants:
        text = f"{plant.get_primary_common_name()} {plant.scientific_name} {plant.description}"
        if plant.cultural_uses:
            text += " " + " ".join(plant.cultural_uses)
        if plant.traditional_systems:
            text += " " + " ".join(plant.traditional_systems)
        search_texts.append(text)

    try:
        # Encode query and texts
        query_embedding = model.encode(query, convert_to_tensor=True)
        text_embeddings = model.encode(search_texts, convert_to_tensor=True)

        # Calculate similarities
        similarities = util.pytorch_cos_sim(query_embedding, text_embeddings)[0]

        # Get top matches
        top_indices = np.argsort(similarities.cpu().numpy())[::-1][:limit]
        top_plants = [plants[i] for i in top_indices]
        top_scores = [float(similarities[i]) for i in top_indices]

        # Filter by reasonable similarity threshold
        results = []
        for plant, score in zip(top_plants, top_scores):
            if score > 0.3:  # Minimum similarity threshold
                results.append(plant)

        return results
    except Exception as e:
        print(f"AI search failed, falling back to basic search: {e}")
        # Fallback to basic search on any error
        return Plant.objects.filter(
            Q(scientific_name__icontains=query) |
            Q(common_names__icontains=query) |
            Q(description__icontains=query)
        )[:limit]


def plant_list(request):
    """Display list of all verified plants"""
    query = request.GET.get('q', '')
    search_type = request.GET.get('search_type', 'basic')  # 'basic' or 'smart'

    plants = Plant.objects.filter(is_verified=True)

    if query:
        if search_type == 'smart':
            # Use AI-powered semantic search
            plants = smart_search_plants(query)
        else:
            # Basic keyword search
            plants = plants.filter(
                Q(scientific_name__icontains=query) |
                Q(common_names__icontains=query) |
                Q(description__icontains=query)
            )

    context = {
        'plants': plants,
        'query': query,
        'search_type': search_type,
        'total_plants': Plant.objects.filter(is_verified=True).count(),
        'ai_available': ML_AVAILABLE and get_sentence_model() is not None,
    }
    return render(request, 'plants/plant_list.html', context)


def plant_detail(request, scientific_name):
    """Display detailed information about a specific plant"""
    plant = get_object_or_404(Plant, scientific_name=scientific_name, is_verified=True)

    # Generate AI research summary (cached to avoid repeated API calls)
    research_summary = None
    if os.environ.get('MISTRAL_API_KEY'):
        research_summary = get_research_summary(plant)

    context = {
        'plant': plant,
        'research_summary': research_summary,
        'ai_available': bool(os.environ.get('MISTRAL_API_KEY')),
    }
    return render(request, 'plants/plant_detail.html', context)
