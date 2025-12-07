---
title: Introduction to ROS 2
description: An introduction to ROS 2, the open-source robotic middleware, covering its architecture, benefits, and basic concepts.
sidebar_position: 1
keywords: [ROS 2, robotics middleware, open-source, robotic operating system]
---

# Introduction to ROS 2 (Robot Operating System)

## What is ROS 2?
ROS 2 is a set of software libraries and tools that help you build robot applications. It is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robotic platforms.

- **Evolution from ROS 1 to ROS 2:** Based on DDS (Data Distribution Service), ROS 2 offers real-time capabilities, enhanced security, and multi-robot support.
- **Key concepts:** It is a distributed, modular system that promotes reusability.

## ROS 2 Architecture
- **Nodes:** Independent executable processes.
- **Topics:** Asynchronous data streams for publishing and subscribing to messages.
- **Services:** Synchronous request/response communication.
- **Actions:** Long-running, goal-oriented tasks with feedback.
- **Parameters:** Dynamic configuration of nodes.
- **Launch Files:** Orchestrating multiple ROS 2 nodes and processes.

## Setting up ROS 2 Environment
- **Installation:** Typically on Ubuntu 22.04 LTS (Humble Hawksbill or Iron Irwini).
- **Workspace:** A directory where you manage your ROS 2 packages.
- **`colcon` build system:** The standard tool for building ROS 2 packages.