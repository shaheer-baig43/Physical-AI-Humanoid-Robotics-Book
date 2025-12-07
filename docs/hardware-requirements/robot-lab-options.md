---
title: Robot Lab Options
description: "Options for setting up a robot lab for the Physical AI course."
---

# The Robot Lab

For the "Physical" part of the course, you have three tiers of options depending on budget.

### Option A: The "Proxy" Approach (Recommended for Budget)
Use a quadruped (dog) or a robotic arm as a proxy. The software principles (ROS 2, VSLAM, Isaac Sim) transfer 90% effectively to humanoids.
- **Robot:** Unitree Go2 Edu (~$1,800 - $3,000).
- **Pros:** Highly durable, excellent ROS 2 support, affordable enough to have multiple units.
- **Cons:** Not a biped (humanoid).

### Option B: The "Miniature Humanoid" Approach
Small, table-top humanoids.
- **Robot:** Unitree H1 is too expensive ($90k+), so look at Unitree G1 (~$16k) or Robotis OP3 (older, but stable, ~$12k).
- **Budget Alternative:** Hiwonder TonyPi Pro (~$600).
- **Warning:** The cheap kits (Hiwonder) usually run on Raspberry Pi, which cannot run NVIDIA Isaac ROS efficiently. You would use these only for kinematics (walking) and use the Jetson kits for AI.

### Option C: The "Premium" Lab (Sim-to-Real specific)
If the goal is to actually deploy the Capstone to a real humanoid:
- **Robot:** Unitree G1 Humanoid.
- **Why:** It is one of the few commercially available humanoids that can actually walk dynamically and has an SDK open enough for students to inject their own ROS 2 controllers.

---

# Summary of Architecture

To teach this successfully, your lab infrastructure should look like this:

| Component     | Hardware                    | Function                                                 |
| ------------- | --------------------------- | -------------------------------------------------------- |
| **Sim Rig**   | PC with RTX 4080 + Ubuntu 22.04 | Runs Isaac Sim, Gazebo, Unity, and trains LLM/VLA models. |
| **Edge Brain**| Jetson Orin Nano            | Runs the "Inference" stack. Students deploy their code here. |
| **Sensors**   | RealSense Camera + Lidar    | Connected to the Jetson to feed real-world data to the AI. |
| **Actuator**  | Unitree Go2 or G1 (Shared)  | Receives motor commands from the Jetson.                 |

If you do not have access to RTX-enabled workstations, we must restructure the course to rely entirely on cloud-based instances (like AWS RoboMaker or NVIDIA's cloud delivery for Omniverse), though this introduces significant latency and cost complexity.

---

# Option 2 High OpEx: The "Ether" Lab (Cloud-Native)

Best for: Rapid deployment, or students with weak laptops.

### 1. Cloud Workstations (AWS/Azure)
Instead of buying PCs, you rent instances.
- **Instance Type:** AWS g5.2xlarge (A10G GPU, 24GB VRAM) or g6e.xlarge.
- **Software:** NVIDIA Isaac Sim on Omniverse Cloud (requires specific AMI).
- **Cost Calculation:**
  - Instance cost: ~$1.50/hour (spot/on-demand mix).
  - Usage: 10 hours/week × 12 weeks = 120 hours.
  - Storage (EBS volumes for saving environments): ~$25/quarter.
  - **Total Cloud Bill:** ~$205 per quarter.

### 2. Local "Bridge" Hardware
You cannot eliminate hardware entirely for "Physical AI." You still need the edge devices to deploy the code physically.
- **Edge AI Kits:** You still need the Jetson Kit for the physical deployment phase.
  - **Cost:** $700 (One-time purchase).
- **Robot:** You still need one physical robot for the final demo.
  - **Cost:** $3,000 (Unitree Go2 Standard).

### 3. The Latency Trap (Hidden Cost)
Simulating in the cloud works well, but controlling a real robot from a cloud instance is dangerous due to latency.
**Solution:** Students train in the Cloud, download the model (weights), and flash it to the local Jetson kit.
