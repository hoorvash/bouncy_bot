# Bouncy Bot

Welcome to **Bouncy Bot** — an AI-powered dance sequence generator! This project extracts audio features from uploaded music, analyzes its characteristics, and generates a JSON dance sequence. It can also simulate video generation based on the audio and the choreography.

While we're excited about the possibilities, **video generation is still in progress**, and currently, only a limited set of dance genres can be selected.

---

## Features

### 🔊 Audio Feature Extraction
- Extracts key audio features such as **BPM**, **Key**, **Tempo**, and **Emotion** using `librosa`.
- Dynamically adjusts dance movements to match the tone and style of the uploaded music.

### 🕺 Dance Movement Generation
- Generates a JSON choreography sequence for professional 5-second dance moves.
- Uses **OpenAI GPT-4** for crafting smooth, creative, and logical transitions between dance poses.
- Limited dance genres include:
  - **Hip Hop**
  - **Tap Dance**
  - **Broadway**
  - **Contemporary**

### 🎥 Simulated Video Generation
- The video generation feature is **still in progress**.
- Currently, placeholder videos are saved alongside the generated JSON.

---

## Installation

### Prerequisites
- Python 3.8+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
