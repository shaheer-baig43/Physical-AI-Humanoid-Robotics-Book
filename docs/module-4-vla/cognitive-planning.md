# Cognitive Planning with LLMs

A key part of Vision-Language-Action (VLA) models is the ability to perform **cognitive planning**. This involves using Large Language Models (LLMs) to translate high-level natural language commands into a sequence of concrete actions that a robot can execute.

## From Language to Actions

For example, a command like "Clean the room" is too abstract for a robot to understand directly. A cognitive planning system using an LLM would break this down into smaller steps:

1.  Identify objects that are out of place (e.g., a cup on the table).
2.  Find the correct location for the object (e.g., the kitchen sink).
3.  Plan a path to the cup.
4.  Pick up the cup.
5.  Plan a path to the kitchen sink.
6.  Place the cup in the sink.
7.  Repeat for other objects.

This sequence of actions can then be translated into ROS 2 commands for the robot's navigation and manipulation systems.
