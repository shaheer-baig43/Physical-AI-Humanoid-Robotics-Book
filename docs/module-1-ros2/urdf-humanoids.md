---
title: URDF for Humanoid Robots
description: Understand URDF (Unified Robot Description Format) for modeling humanoid robots, including links, joints, and visual/collision properties.
sidebar_position: 4
keywords: [URDF, humanoid robots, robot modeling, links, joints, ROS 2 URDF]
---

# Understanding URDF (Unified Robot Description Format) for humanoids

## What is URDF?
URDF is an XML format for describing all elements of a robot. It represents the robot as a tree of rigid bodies (links) connected by joints. URDF files are essential for robot visualization in tools like RViz and for physics simulation in environments like Gazebo.

### Links
A **link** represents a rigid body segment of the robot. For a humanoid, examples of links include the torso, head, upper arm, forearm, hand, thigh, shin, and foot. Each link has:
-   **Inertial properties:** mass, moment of inertia.
-   **Visual properties:** The shape and appearance of the link (e.g., mesh file).
-   **Collision properties:** A simplified geometry used for physics calculations.

### Joints
A **joint** defines the kinematic and dynamic relationship between two links. It specifies how links move relative to each other. Common joint types for humanoids include:
-   **Revolute:** A rotating joint around a single axis (e.g., elbow, knee).
-   **Continuous:** A revolute joint with no angle limits.
-   **Prismatic:** A sliding joint along a single axis.
-   **Fixed:** No movement between links (e.g., a camera rigidly attached to a robot's head).

By combining links and joints, a complete kinematic chain of the humanoid robot can be defined, from the base to the hands and feet.