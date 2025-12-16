# BotanIQ 🌿

Discover the Botanical Intelligence of Traditional Medicine

BotanIQ is a comprehensive educational platform for learning about medicinal plants and their historical uses in traditional medicine systems worldwide.

## Features

- **Comprehensive Plant Database**: Detailed information on medicinal plants
- **AI-Powered Search**: Intelligent search using natural language
- **Research Library**: Personal dashboard for organizing studies
- **Traditional Medicine Systems**: Coverage of Ayurveda, TCM, Western Herbalism
- **Scientific Research**: Verified studies and pharmacological data
- **Safety Information**: Comprehensive contraindications and interactions

## Tech Stack

- **Backend**: Django 5.2+
- **Frontend**: Django Templates + Custom CSS
- **AI**: Hugging Face Transformers + Mistral AI
- **Database**: SQLite (development) / PostgreSQL (production)
- **Deployment**: Railway

## Quick Start

### Prerequisites
- Python 3.8+
- Git
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd botaniq
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "MISTRAL_API_KEY=your_mistral_api_key_here" > .env
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Seed the database**
   ```bash
   python seed_plants.py
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Visit** `http://127.0.0.1:8000/`

## AI Features

### Smart Search
- Uses sentence transformers for semantic understanding
- Search with natural language: "plants for anxiety", "immune boosting herbs"

### Research Summarization
- Mistral AI generates concise summaries of scientific studies
- Appears on plant detail pages

## Project Structure

```
botaniq/
├── botaniq/              # Django settings
├── plants/               # Plant database app
├── dashboard/            # User dashboard app
├── templates/            # HTML templates
├── static/               # CSS, JS (future)
├── db.sqlite3            # Database
└── manage.py
```

## API Keys Required

- **Mistral AI**: For research summarization (optional)
- **Hugging Face**: For sentence transformers (no key needed)

## Deployment

### Railway (Recommended)
1. Connect GitHub repository to Railway
2. Add environment variables in Railway dashboard:
   ```
   SECRET_KEY=your-generated-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-railway-domain.up.railway.app
   DATABASE_ENGINE=django.db.backends.postgresql
   DATABASE_NAME=railway
   DATABASE_USER=postgres
   DATABASE_PASSWORD=your-db-password
   DATABASE_HOST=your-db-host
   DATABASE_PORT=5432
   MISTRAL_API_KEY=your-mistral-api-key (optional)
   ```
3. Deploy automatically

### Local Production Testing
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your values
# Set DEBUG=False for production testing

# Run with production settings
python manage.py collectstatic
python manage.py migrate
python manage.py runserver
```

## Medical Disclaimer

**IMPORTANT**: The information provided on BotanIQ is for educational and research purposes only. It is not intended to diagnose, treat, cure, or prevent any disease. Always consult with qualified healthcare professionals before using any plant-based remedies or supplements.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Medicinal plant data compiled from public domain sources
- Research studies from peer-reviewed publications
- Traditional medicine knowledge from cultural heritage

---

Built with ❤️ for botanical education and research.
