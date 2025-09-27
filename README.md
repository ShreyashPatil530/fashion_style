# AI Fashion Stylist

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Computer%20Vision-orange.svg)](https://ultralytics.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-red.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained-Yes-brightgreen.svg)](https://github.com/yourusername/fashion_style)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/fashion_style/pulls)

An intelligent web application that analyzes your outfit photos using AI and provides personalized fashion recommendations, style suggestions, and shopping links.

## Features

- **AI-Powered Image Analysis**: Uses YOLOv8 computer vision to detect clothing items in photos
- **Intelligent Style Suggestions**: OpenAI GPT-4 powered fashion recommendations
- **Smart Shopping Integration**: Automated product search with SerpAPI
- **Real-time Processing**: Fast outfit analysis with detailed feedback
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **User-Friendly Interface**: Intuitive drag-and-drop file upload
- **Fallback Systems**: Graceful handling when APIs are unavailable

## Technology Stack

### Backend
- **Flask** - Python web framework
- **YOLOv8** - Object detection and computer vision
- **OpenAI GPT-4** - AI-powered style suggestions
- **SerpAPI** - Shopping link integration
- **MySQL** - Database for user data storage
- **OpenCV** - Image processing
- **Pillow** - Image manipulation

### Frontend
- **HTML5/CSS3** - Structure and styling
- **Bootstrap 5** - Responsive UI framework
- **JavaScript (ES6+)** - Interactive functionality
- **Font Awesome** - Icons

### APIs & Services
- **OpenAI API** - Natural language processing
- **SerpAPI** - Search engine results
- **MySQL Database** - Data persistence

## Prerequisites

Before running this application, make sure you have:

- Python 3.8+ installed
- MySQL server running (optional - has fallback mode)
- API keys for:
  - OpenAI API
  - SerpAPI

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/fashion_style.git
cd fashion_style
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_KEY=your_serpapi_key_here

# Database Configuration (Optional)
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=fashion_stylist
```

### 5. Database Setup (Optional)
```bash
# Run database initialization - app works without this
python db.py
```

### 6. Run the Application
```bash
# Development mode
python app.py

# The application will be available at http://localhost:5000
```

## Testing

Run the comprehensive test suite:
```bash
python test_app.py
```

This will test:
- Server connectivity
- Component functionality
- Complete analysis pipeline
- API integrations

## Project Structure

```
fashion_style/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (not in repo)
├── README.md             # Project documentation
├──
├── yolo_detect.py        # YOLO computer vision module
├── openai_api.py         # OpenAI integration
├── serpapi_api.py        # SerpAPI integration
├── db.py                 # Database operations
├── test_app.py           # Application tests
├──
├── templates/
│   └── index.html        # Main HTML template
├──
├── static/
│   ├── style.css        # Custom CSS styles
│   └── script.js        # Frontend JavaScript
└──
└── uploads/             # Temporary file storage (auto-created)
```

## Configuration

### API Keys Setup

#### OpenAI API
1. Visit [OpenAI Platform](https://platform.openai.com)
2. Create account and generate API key
3. Add to `.env` file

#### SerpAPI
1. Visit [SerpAPI](https://serpapi.com)
2. Sign up for free account (100 searches/month)
3. Get API key from dashboard

### Database Configuration

The application supports MySQL with automatic fallback:
- **With MySQL**: Uses database for data persistence
- **Without MySQL**: Falls back to in-memory storage
- **No setup required**: App works immediately without database

## Usage Guide

### 1. Upload Photo
- Click upload area or drag & drop image
- Supported formats: JPG, PNG, GIF, BMP, WebP
- Maximum file size: 16MB

### 2. Analysis Process
- AI detects clothing items in photo
- Analyzes colors, styles, and categories
- Generates personalized suggestions

### 3. View Results
- **Detected Items**: Lists found clothing with confidence scores
- **AI Suggestions**: Detailed styling recommendations
- **Shopping Links**: Related products from major retailers

### 4. Shopping Integration
- Click "Shop Now" buttons for product links
- Links redirect to retailer websites
- Prices and ratings displayed

## API Endpoints

### Main Endpoints
- `GET /` - Main application interface
- `POST /analyze` - Image analysis endpoint
- `GET /test` - Server health check

### Request Format
```javascript
// POST /analyze
FormData: {
  image: File,
  user_id: String (optional)
}
```

### Response Format
```json
{
  "success": true,
  "detected_items": [
    {
      "item": "blue shirt",
      "confidence": 0.85,
      "color": "blue",
      "category": "top"
    }
  ],
  "ai_suggestions": "Detailed styling advice...",
  "shopping_links": [
    {
      "title": "Blue Casual Shirt",
      "price": "$29.99",
      "source": "Amazon",
      "link": "https://...",
      "rating": "4.5/5"
    }
  ]
}
```

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guide
- Add tests for new features
- Update documentation as needed
- Ensure graceful fallback handling

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Shreyash Patil**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## Acknowledgments

- **YOLOv8** by Ultralytics for computer vision capabilities
- **OpenAI** for natural language processing
- **SerpAPI** for search integration
- **Bootstrap** for responsive UI components
- **Font Awesome** for icons

## Performance Notes

### Resource Usage
- **Memory**: ~500MB-1GB during processing
- **CPU**: Moderate usage during image analysis
- **Storage**: Temporary files cleaned automatically

### Optimization Features
- Automatic file cleanup
- Fallback mechanisms for API failures
- Responsive design for all devices
- Efficient image processing

## Security

- File type validation and size limits
- Secure filename handling
- Environment variable protection
- No sensitive data in client-side code

## Future Enhancements

- [ ] User accounts and history
- [ ] Advanced color analysis
- [ ] Seasonal recommendations
- [ ] Social sharing features
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Style trend analysis

## Troubleshooting

### Common Issues

**Server won't start:**
- Check Python version (3.8+ required)
- Verify all dependencies installed
- Ensure .env file configured

**Image analysis fails:**
- Check file format and size
- Verify API keys in .env
- Check internet connection

**Database errors:**
- Verify MySQL running
- Check database credentials
- App works without database (fallback mode)

### Getting Help

1. Check the [Issues](https://github.com/yourusername/fashion_style/issues) page
2. Create a new issue with detailed description
3. Include error messages and system info

---

**If you find this project helpful, please give it a star!**
