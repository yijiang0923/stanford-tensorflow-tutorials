# LLM iOS Chat App

A ChatGPT-like iOS app that connects to your desktop LLM for private, local AI conversations.

## Overview

This project consists of two main components:
1. **Server**: A FastAPI backend that runs on your desktop and interfaces with your LLM
2. **iOS App**: A native SwiftUI app that provides a ChatGPT-like interface

## Architecture

```
[iOS App] ←→ [FastAPI Server] ←→ [Your LLM]
```

- iOS app sends messages via HTTP requests
- FastAPI server processes requests and communicates with your LLM
- Responses are sent back to the iOS app for display

## Setup Instructions

### 1. Server Setup (Desktop)

#### Prerequisites
- Python 3.8 or higher
- Your LLM setup (OpenAI API, local models, Ollama, etc.)

#### Installation
```bash
cd server
pip install -r requirements.txt
```

#### Configuration
1. Edit `main.py` and replace the `generate_llm_response` function with your actual LLM integration:

```python
async def generate_llm_response(prompt: str, history: List[ChatMessage]) -> str:
    # Replace this with your LLM integration
    # Examples:
    
    # OpenAI API
    # response = await openai.ChatCompletion.acreate(...)
    
    # Ollama
    # response = ollama.generate(model="llama2", prompt=prompt)
    
    # Local transformers
    # response = model.generate(prompt)
    
    # Your custom LLM setup
    return your_llm_response
```

#### Running the Server
```bash
python main.py
```

The server will start on `http://localhost:8000`. You can view the API documentation at `http://localhost:8000/docs`.

### 2. iOS App Setup

#### Prerequisites
- Xcode 14 or later
- iOS 16.0 or later (for deployment)
- Mac with Apple Silicon or Intel processor

#### Installation
1. Open `ios-app/LLMChat.xcodeproj` in Xcode
2. Configure your development team in the project settings
3. Update the server URL in `LLMService.swift`:

```swift
// For simulator (if server is on same machine)
private let baseURL = "http://localhost:8000"

// For physical device (replace with your desktop's IP)
private let baseURL = "http://192.168.1.100:8000"
```

#### Finding Your Desktop IP
```bash
# On macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# On Windows
ipconfig | findstr "IPv4"
```

#### Running the App
1. Select your target device (simulator or physical device)
2. Press `Cmd + R` to build and run

## Features

### Current Features
- ✅ Real-time chat interface
- ✅ Message history
- ✅ Connection status indicator
- ✅ ChatGPT-like message bubbles
- ✅ Typing indicators
- ✅ Error handling
- ✅ Clear conversation

### Planned Features
- 🔄 Message persistence
- 🔄 Multiple conversation threads
- 🔄 Message search
- 🔄 Export conversations
- 🔄 Dark mode
- 🔄 Custom themes
- 🔄 Voice input
- 🔄 Image support (if your LLM supports it)

## LLM Integration Examples

### OpenAI API
```python
import openai

async def generate_llm_response(prompt: str, history: List[ChatMessage]) -> str:
    messages = [{"role": msg.role, "content": msg.content} for msg in history]
    messages.append({"role": "user", "content": prompt})
    
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    return response.choices[0].message.content
```

### Ollama
```python
import ollama

async def generate_llm_response(prompt: str, history: List[ChatMessage]) -> str:
    # Convert history to a context string
    context = "\n".join([f"{msg.role}: {msg.content}" for msg in history])
    full_prompt = f"{context}\nuser: {prompt}\nassistant:"
    
    response = ollama.generate(model="llama2", prompt=full_prompt)
    return response['response']
```

### Hugging Face Transformers
```python
from transformers import pipeline

generator = pipeline("text-generation", model="microsoft/DialoGPT-medium")

async def generate_llm_response(prompt: str, history: List[ChatMessage]) -> str:
    # Format conversation for the model
    context = " ".join([msg.content for msg in history[-10:]])  # Last 10 messages
    full_prompt = f"{context} {prompt}"
    
    response = generator(full_prompt, max_length=200, num_return_sequences=1)
    return response[0]['generated_text'].split(prompt)[-1].strip()
```

## Troubleshooting

### Server Issues
- **Server won't start**: Check if port 8000 is available
- **LLM not responding**: Verify your LLM integration in `generate_llm_response`
- **CORS errors**: Ensure CORS is properly configured in the FastAPI app

### iOS App Issues
- **Can't connect to server**: 
  - Check if server is running on desktop
  - Verify the IP address in `LLMService.swift`
  - Ensure devices are on the same network
- **Build errors**: Make sure you're using Xcode 14+ and iOS 16+

### Network Issues
- **Connection timeout**: Increase timeout values in `LLMService.swift`
- **Firewall blocking**: Configure firewall to allow port 8000
- **Different networks**: Use VPN or port forwarding if needed

## Security Considerations

⚠️ **Important**: This setup is designed for local/private network use.

For production use, consider:
- HTTPS encryption
- Authentication/authorization
- Rate limiting
- Input validation
- Network security

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the server logs
3. Test the API endpoints directly
4. Create an issue with detailed logs

## Architecture Details

### Server Endpoints
- `GET /`: Health check
- `POST /chat`: Send message and get response
- `GET /health`: Server health status
- `DELETE /conversations/{id}`: Clear conversation

### iOS App Structure
```
LLMChat/
├── LLMChatApp.swift          # Main app entry point
├── ContentView.swift         # Root view
├── Views/
│   ├── ChatView.swift        # Main chat interface
│   └── MessageBubble.swift   # Message display component
├── Models/
│   └── ChatMessage.swift     # Data models
└── Services/
    └── LLMService.swift      # API communication
```

Enjoy chatting with your personal LLM! 🚀