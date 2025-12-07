---
title: Python-ROS Bridge with rclpy
description: Learn how to develop ROS 2 applications using Python with the rclpy client library for nodes, publishers, and subscribers.
sidebar_position: 3
keywords: [ROS 2 Python, rclpy, ROS 2 client library, ROS 2 programming]
---

# Bridging Python Agents to ROS controllers using rclpy

## The `rclpy` Client Library
`rclpy` is the Python client library for ROS 2. It provides an interface to the underlying ROS 2 C++ API (`rcl`) and allows Python developers to easily interact with ROS 2 concepts like nodes, topics, services, and parameters. It handles the complexities of DDS communication, allowing you to focus on your application logic.

## Controller Integration
A key goal of this course is to bridge high-level AI, like a Python-based agent, with a robot's low-level controllers. `rclpy` is the tool that makes this possible.

-   **High-Level Commands:** An AI agent (which could be powered by a large language model) might generate a high-level command like "move forward at 0.5 m/s".
-   **Translation Layer:** A Python ROS 2 node using `rclpy` will subscribe to these high-level commands.
-   **Low-Level Control:** The node then translates these commands into the specific message types required by the robot's motor controllers (e.g., a `geometry_msgs/Twist` message) and publishes them on the appropriate ROS 2 topic.

This architecture allows for a clean separation between the "brains" (the AI agent) and the "body" (the robot's hardware controllers).