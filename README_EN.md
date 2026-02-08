# 🤖 Physical AI - Jarvis/Atreides

**Wake word-activated intelligent robotic arm system**

> "Jarvis" or "Atreides" - Just call its name and it wakes up, listens, thinks, speaks, and acts.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

- 🎤 **Wake Word Detection**: Responds to "Jarvis" or "Atreides"
- 🧠 **AI Brain**: GPT-4o-powered decision making and natural language understanding
- 🗣️ **Voice Conversation**: Listens (Whisper API) and speaks (TTS)
- 🤖 **Robot Simulation**: 6-DOF robotic arm with pick, place, move operations
- 📊 **Visualization**: 2D top-down view of robot state
- 💻 **Software-First**: Fully functional without hardware

## 🎬 Demo

```
You: "Jarvis"
Robot: "Yes, I'm listening."

You: "Pick up the red block"
Robot: "Alright, I'll find and pick up the red block."
[Executes: move → pick]
Robot: "Done."

→ Returns to standby mode
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone repository
git clone https://github.com/yourusername/physical-ai-jarvis.git
cd physical-ai-jarvis

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### 3. Run

```bash
python atreides.py
```

**Selections:**
1. Robot name: `1` (Jarvis - recommended)
2. TTS: `2` (macOS built-in - free)

**Usage:**
- Say "Jarvis" or "Atreides" to wake up
- Give voice commands
- Watch it think and act!

## 🎯 Supported Wake Words

### Jarvis Mode ⭐ (Recommended - Easy Recognition)
- "Jarvis"
- "자비스" (Korean)

### Atreides Mode (For Dune Fans)
- "Atreides"
- "아트레이디스" (Korean)

### Flexible Matching
- Partial words recognized
- Space-insensitive
- Pronunciation variations

## 🏗️ Architecture

```
Voice Input (Microphone)
    ↓
🎤 Whisper API (Speech Recognition)
    ↓
🧠 GPT-4o (AI Brain - Understanding & Planning)
    ↓
⚙️ Action Executor
    ↓
🤖 Robot Simulator
    ↓
🔊 TTS (Voice Output)
```

## 📂 Project Structure

```
physical-ai-jarvis/
├── atreides.py              # Main: Wake word-activated robot
├── src/
│   ├── brain/               # AI decision making (GPT-4o)
│   │   └── robot_brain.py
│   ├── perception/          # Voice I/O
│   │   ├── speech_recognizer.py   # Whisper API
│   │   ├── microphone.py          # Real-time recording
│   │   ├── text_to_speech.py      # TTS output
│   │   └── wake_word.py           # Wake word detection
│   ├── motion/              # Action execution
│   │   └── action_executor.py
│   └── simulation/          # Robot simulation
│       ├── simple_robot_sim.py
│       └── visualizer.py          # 2D visualization
├── demo.py                  # File-based demo
├── demo_screenshot.py       # Visual demo with images
└── tests/                   # Test scripts
```

## 🛠️ Tech Stack

### Core
- **Python 3.13+**
- **OpenAI GPT-4o** - Natural language understanding
- **OpenAI Whisper** - Speech recognition
- **sounddevice** - Real-time microphone input

### Optional
- **OpenAI TTS** - High-quality voice output (paid)
- **macOS say** - Built-in TTS (free alternative)
- **matplotlib** - Visualization

## 💡 Example Commands

### Basic Actions
- "Pick up the red block"
- "Go to home position"
- "Open the gripper"
- "Close the gripper"

### Conversation
- "Hello" → Greeting
- "What's your name?" → Introduction
- "Thank you" → Acknowledgment

## 🎨 Visualization

The system includes a 2D top-down view showing:
- Robot arm position (blue line)
- Gripper state (green=open, red=closed)
- Objects in workspace (colored blocks)
- Work area boundary

Generate visualization screenshots:
```bash
python demo_screenshot.py
```

## 📋 Development Roadmap

- [x] AI Brain (GPT-4o integration)
- [x] Speech Recognition (Whisper API)
- [x] Real-time Microphone Input
- [x] Text-to-Speech Output
- [x] Wake Word Detection
- [x] Robot Simulation
- [x] Action Execution System
- [x] 2D Visualization
- [ ] Vision System (Camera + Object Detection)
- [ ] Hardware Integration (myCobot, xArm, etc.)
- [ ] Advanced Multi-step Tasks
- [ ] Multimodal (Vision + Voice)

## 🔧 Hardware Integration (Future)

Software-ready for hardware integration with:
- **myCobot 280** (~$500-800)
- **xArm Lite 6** (~$1500)
- **Universal Robots** (UR3/UR5)
- Any 6-DOF robotic arm with serial/ROS interface

## 📖 Documentation

- [Quick Start Guide](QUICKSTART.md)
- [Korean README](README.md)

## 🧪 Testing

```bash
# Test wake word detection
python test_wake_word.py

# Test voice I/O
python test_voice_io.py

# Test AI brain
python test_brain_auto.py

# Test speech recognition
python test_speech.py

# Check microphone
python test_mic_check.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by Iron Man's Jarvis
- Named after House Atreides from Dune by Frank Herbert
- "Fear is the mind-killer" - Dune

## 💬 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Issues: [GitHub Issues](https://github.com/yourusername/physical-ai-jarvis/issues)

## ⭐ Star History

If you find this project interesting, please consider giving it a star!

---

**Made with ❤️ by Physical AI enthusiasts**
