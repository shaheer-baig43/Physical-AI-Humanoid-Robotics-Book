import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Bridging the gap between the digital brain and the physical body.',
  favicon: 'img/logo.svg',

  future: {
    v4: true,
  },

  url: 'https://shaheer-baig43.github.io',
  baseUrl: '/Physical-AI-Humanoid-Robotics-Book/',

  organizationName: 'shaheer-baig43',
  projectName: 'Physical-AI-Humanoid-Robotics-Book',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          path: 'docs', // New: Specify the docs folder path
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/shaheer-baig43/Physical-AI-Humanoid-Robotics-Book/tree/main/',
        },
        blog: false, // Disable the blog plugin
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Course Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'physicalAiSidebar',
          position: 'left',
          label: 'Course Modules',
        },
        {
          href: 'https://github.com/your-org/physical-ai-course',
          label: 'GitHub',
          position: 'right',
        },
        // Add Login link
        {
          to: '/login',
          label: 'Login',
          position: 'right',
        },
        // Add Signup link
        {
          to: '/signup',
          label: 'Signup',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Course',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
            {
              label: 'Weekly Schedule',
              to: '/docs/weekly-schedule/weeks-1-2',
            },
            {
              label: 'Hardware',
              to: '/docs/hardware-requirements/workstation-specs',
            },
          ],
        },
        {
          title: 'Modules',
          items: [
            {
              label: 'Module 1: ROS 2',
              to: '/docs/module-1-ros2/introduction',
            },
            {
              label: 'Module 2: Digital Twin',
              to: '/docs/module-2-digital-twin/gazebo-simulation',
            },
            {
              label: 'Module 3: NVIDIA Isaac',
              to: '/docs/module-3-isaac/isaac-sim',
            },
            {
              label: 'Module 4: VLA',
              to: '/docs/module-4-vla/voice-to-action',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/your-org/physical-ai-course',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Course. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
