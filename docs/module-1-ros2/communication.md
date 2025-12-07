# ROS 2 Communication and Python Agents

## Module 1: The Robotic Nervous System (ROS 2)

### ROS 2 Communication Mechanisms
*   **Nodes and Executables:**
    *   Creating a basic ROS 2 Python node.
    *   Writing C++ nodes (brief overview for context).
*   **Topics (Publishers & Subscribers):**
    *   Defining custom message types (using `.msg` files).
    *   Publishing data (e.g., sensor readings, joint states).
    *   Subscribing to data (e.g., motor commands, navigation feedback).
    *   Quality of Service (QoS) settings for reliability and latency.
*   **Services (Clients & Servers):**
    *   Defining custom service types (using `.srv` files).
    *   Implementing a service server to handle requests.
    *   Implementing a service client to send requests.
*   **Actions (Clients & Servers):**
    *   Defining custom action types (using `.action` files).
    *   Developing action servers for complex tasks (e.g., "move to target").
    *   Developing action clients to send goals and receive feedback.

### Bridging Python Agents to ROS Controllers
*   **`rclpy` Library:**
    *   In-depth usage of `rclpy` for Python-based ROS 2 development.
    *   Creating nodes, publishers, subscribers, service clients/servers, and action clients/servers in Python.
*   **Controller Integration:**
    *   Designing Python agents that can interpret high-level AI commands (e.g., from an LLM) and translate them into low-level ROS 2 messages for robot actuation.
    *   Example: A Python agent that subscribes to a "target pose" topic and publishes "joint velocity" commands.