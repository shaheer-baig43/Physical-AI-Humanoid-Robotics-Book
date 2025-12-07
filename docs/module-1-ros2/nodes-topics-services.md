---
title: Nodes, Topics, and Services
description: "Delve into the core communication mechanisms of ROS 2: nodes, topics (publish/subscribe), and services (request/reply)."
sidebar_position: 2
keywords: [ROS 2 nodes, ROS 2 topics, ROS 2 services, publish subscribe, request reply]
---

# ROS 2 Nodes, Topics, and Services

## Nodes
In ROS 2, a **node** is an executable process that performs a specific task. Each node should ideally be responsible for a single, well-defined function (e.g., a sensor driver, a motor controller, a navigation algorithm). Nodes are independent and can be started, stopped, and restarted without affecting other parts of the system.

## Topics (Publish/Subscribe)
**Topics** are the most common way for nodes to asynchronously exchange data in ROS 2. They implement a publish/subscribe messaging pattern:
- A **publisher** node sends messages to a specific topic.
- One or more **subscriber** nodes receive messages from that topic.
- This pattern is ideal for continuous data streams like sensor readings, odometry, or video feeds.

## Services (Request/Reply)
**Services** provide a synchronous request/reply communication mechanism between nodes. Unlike topics, services are used for calls that require an immediate response. They are suitable for tasks such as:
- Triggering a specific action on a robot (e.g., "take a picture").
- Querying for information (e.g., "what is the current robot position?").

## Actions
**Actions** are for long-running, goal-oriented tasks. They are similar to services but provide feedback on their progress. Examples include "move to a target location" or "pick up an object". An action consists of a goal, feedback, and a result.