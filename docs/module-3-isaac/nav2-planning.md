# Nav2: Path Planning

**Nav2** is the second generation of the ROS Navigation Stack. It is a powerful and flexible tool for autonomous robot navigation. In the context of this course, we will focus on its application to bipedal humanoid movement.

## Path Planning for Humanoids

While Nav2 is often used for wheeled robots, its principles can be adapted for humanoids.

- **Global Planner:** Finds a path from the robot's current location to a goal location, avoiding known obstacles from a map.
- **Local Planner:** Generates velocity commands to follow the global plan while avoiding local obstacles detected by sensors. For a humanoid, this is significantly more complex as it involves dynamic stability and footstep planning.
- **Behavior Trees:** Nav2 uses Behavior Trees to orchestrate the different tasks involved in navigation (e.g., planning, recovery behaviors). This allows for complex and customized navigation logic.
- **Integration with Isaac Sim:** We will use Isaac Sim to provide the simulated environment and sensor data for Nav2 to operate in.
