import React from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import Link from '@docusaurus/Link';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: React.ReactNode;
  link: string;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Module 1: The Robotic Nervous System',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Learn the fundamentals of ROS 2, the middleware for robot control, including nodes, topics, services, and URDF for humanoids.
      </>
    ),
    link: '/docs/module-1-ros2/introduction',
  },
  {
    title: 'Module 2: The Digital Twin',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Master physics simulation and environment building with Gazebo and Unity, and learn to simulate sensors like LiDAR and cameras.
      </>
    ),
    link: '/docs/module-2-digital-twin/gazebo-simulation',
  },
  {
    title: 'Module 3: The AI-Robot Brain',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Dive into advanced perception and training with NVIDIA Isaac Sim for photorealistic simulation and Isaac ROS for hardware acceleration.
      </>
    ),
    link: '/docs/module-3-isaac/isaac-sim',
  },
  {
    title: 'Module 4: Vision-Language-Action',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Explore the convergence of LLMs and Robotics by building systems that translate voice commands into cognitive plans and actions.
      </>
    ),
    link: '/docs/module-4-vla/voice-to-action',
  },
];

function Feature({title, Svg, description, link}: FeatureItem) {
  return (
    <div className={clsx('col col--3')}>
      <Link className={styles.featureLink} to={link}>
        <div className={clsx('card', styles.featureCard)}>
          <div className="card__header text--center">
            <Svg className={styles.featureSvg} role="img" />
            <Heading as="h3">{title}</Heading>
          </div>
          <div className="card__body">
            <p>{description}</p>
          </div>
        </div>
      </Link>
    </div>
  );
}

export default function HomepageFeatures(): React.ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}