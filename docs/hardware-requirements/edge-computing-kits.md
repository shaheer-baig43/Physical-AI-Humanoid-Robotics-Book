---
title: Edge Computing Kits
description: "Information on the Physical AI Edge Kits for deploying robotic systems."
---

# The "Physical AI" Edge Kit

Since a full humanoid robot is expensive, students learn "Physical AI" by setting up the nervous system on a desk before deploying it to a robot. This kit covers Module 3 (Isaac ROS) and Module 4 (VLA).

- **The Brain: NVIDIA Jetson Orin Nano (8GB) or Orin NX (16GB).**
  - **Role:** This is the industry standard for embodied AI. Students will deploy their ROS 2 nodes here to understand resource constraints vs. their powerful workstations.

- **The Eyes (Vision): Intel RealSense D435i or D455.**
  - **Role:** Provides RGB (Color) and Depth (Distance) data. Essential for the VSLAM and Perception modules.

- **The Inner Ear (Balance): Generic USB IMU (BNO055).**
  - **Role:** Often built into the RealSense D435i or Jetson boards, but a separate module helps teach IMU calibration.

- **Voice Interface: A simple USB Microphone/Speaker array (e.g., ReSpeaker).**
  - **Role:** For the "Voice-to-Action" Whisper integration.
