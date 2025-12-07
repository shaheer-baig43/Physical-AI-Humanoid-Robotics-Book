import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  physicalAiSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Introduction to Physical AI',
      link: {
        type: 'doc',
        id: 'introduction/overview',
      },
      items: [
        'introduction/overview',
        'introduction/why-physical-ai',
        'introduction/learning-outcomes',
      ],
    },
    {
      type: 'category',
      label: 'Module 1: ROS 2 - The Robotic Nervous System',
      link: {
        type: 'doc',
        id: 'module-1-ros2/introduction',
      },
      items: [
        'module-1-ros2/introduction',
        'module-1-ros2/nodes-topics-services',
        'module-1-ros2/python-ros-bridge',
        'module-1-ros2/urdf-humanoids',
        'module-1-ros2/lab-exercises',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin',
      link: {
        type: 'doc',
        id: 'module-2-digital-twin/gazebo-simulation',
      },
      items: [
        'module-2-digital-twin/gazebo-simulation',
        'module-2-digital-twin/unity-rendering',
        'module-2-digital-twin/sensor-simulation',
        'module-2-digital-twin/lab-exercises',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: NVIDIA Isaac - The AI-Robot Brain',
      link: {
        type: 'doc',
        id: 'module-3-isaac/isaac-sim',
      },
      items: [
        'module-3-isaac/isaac-sim',
        'module-3-isaac/isaac-ros',
        'module-3-isaac/nav2-planning',
        'module-3-isaac/lab-exercises',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action',
      link: {
        type: 'doc',
        id: 'module-4-vla/voice-to-action',
      },
      items: [
        'module-4-vla/voice-to-action',
        'module-4-vla/cognitive-planning',
        'module-4-vla/capstone-project',
      ],
    },
    {
      type: 'category',
      label: 'Hardware Requirements',
      link: {
        type: 'doc',
        id: 'hardware-requirements/workstation-specs',
      },
      items: [
        'hardware-requirements/workstation-specs',
        'hardware-requirements/edge-computing-kits',
        'hardware-requirements/robot-lab-options',
        'hardware-requirements/economy-student-kit',
      ],
    },
    {
      type: 'category',
      label: 'Weekly Schedule',
      link: {
        type: 'doc',
        id: 'weekly-schedule/weeks-1-2',
      },
      items: [
        'weekly-schedule/weeks-1-2',
        'weekly-schedule/weeks-3-5',
        'weekly-schedule/weeks-6-7',
        'weekly-schedule/weeks-8-10',
        'weekly-schedule/weeks-11-12',
        'weekly-schedule/week-13',
      ],
    },
    {
      type: 'category',
      label: 'Assessments',
      link: {
        type: 'doc',
        id: 'assessments/projects',
      },
      items: [
        'assessments/projects',
        'assessments/capstone',
      ],
    },

  ],
};

export default sidebars;