# Voice-to-Action

**Voice-to-Action** is the process of converting spoken language into robotic actions. This is a crucial component of creating natural and intuitive human-robot interactions.

## Using OpenAI Whisper

For this module, we will use **OpenAI Whisper** for voice command recognition.

- **Whisper:** A state-of-the-art automatic speech recognition (ASR) system from OpenAI. It is highly accurate and can transcribe speech from various languages and accents.
- **Integration:** We will set up a ROS 2 node that uses a microphone to capture audio, sends it to the Whisper API (or a locally run model), and receives the transcribed text.
- **From Text to Command:** The transcribed text is then passed to the cognitive planning module, which interprets the command and generates a plan for the robot.
