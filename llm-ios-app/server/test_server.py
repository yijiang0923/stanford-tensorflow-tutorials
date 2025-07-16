#!/usr/bin/env python3
"""
Test script for the LLM server API endpoints.
Run this after starting the server to verify everything is working.
"""

import asyncio
import json
from datetime import datetime
import httpx

BASE_URL = "http://localhost:8000"

async def test_server():
    """Test all server endpoints"""
    async with httpx.AsyncClient() as client:
        print("🧪 Testing LLM Server API\n")
        
        # Test 1: Health check
        print("1. Testing health check...")
        try:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✅ Health check passed")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Health check error: {e}")
        
        print()
        
        # Test 2: Root endpoint
        print("2. Testing root endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/")
            if response.status_code == 200:
                print("✅ Root endpoint passed")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Root endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Root endpoint error: {e}")
        
        print()
        
        # Test 3: Chat endpoint
        print("3. Testing chat endpoint...")
        try:
            test_message = {
                "message": "Hello, can you hear me?",
                "conversation_history": []
            }
            
            response = await client.post(
                f"{BASE_URL}/chat",
                json=test_message,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print("✅ Chat endpoint passed")
                data = response.json()
                print(f"   User: {test_message['message']}")
                print(f"   Assistant: {data['response']}")
                print(f"   Timestamp: {data['timestamp']}")
            else:
                print(f"❌ Chat endpoint failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Chat endpoint error: {e}")
        
        print()
        
        # Test 4: Chat with history
        print("4. Testing chat with conversation history...")
        try:
            test_message_with_history = {
                "message": "What did I just say?",
                "conversation_history": [
                    {
                        "role": "user",
                        "content": "Hello, can you hear me?",
                        "timestamp": datetime.now().isoformat()
                    },
                    {
                        "role": "assistant", 
                        "content": "Hello! How can I assist you today?",
                        "timestamp": datetime.now().isoformat()
                    }
                ]
            }
            
            response = await client.post(
                f"{BASE_URL}/chat",
                json=test_message_with_history,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print("✅ Chat with history passed")
                data = response.json()
                print(f"   User: {test_message_with_history['message']}")
                print(f"   Assistant: {data['response']}")
            else:
                print(f"❌ Chat with history failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Chat with history error: {e}")
        
        print("\n🎉 Server testing completed!")

if __name__ == "__main__":
    print("Make sure your server is running (python main.py) before running this test.\n")
    asyncio.run(test_server())