#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Test the API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, this is a test."}],
        max_tokens=10
    )
    print("✅ API key is working!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ API key test failed: {e}")
