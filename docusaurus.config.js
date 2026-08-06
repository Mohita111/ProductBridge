// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'ProductBridge',
  tagline: 'Product Knowledge Base & Documentation',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://Mohita111.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/ProductBridge/',

  // GitHub pages deployment config.
  organizationName: 'Mohita111', 
  projectName: 'ProductBridge', 

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // SITE VERIFICATION META TAGS (For Algolia Crawler Verification)
  headTags: [
    {
      tagName: 'meta',
      attributes: {
        name: 'algolia-site-verification',
        content: 'D2D7B0F85BFD4AA',
      },
    },
  ],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl:
            'https://github.com/Mohita111/ProductBridge/tree/main/',
        },
        blog: false, // Set to false since Blog tab is removed
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // ALGOLIA DOCSEARCH CONFIGURATION
      algolia: {
        // Application ID from your Algolia account
        appId: '3S5NI514YQ',

        // Public Search-Only API Key (Safe to expose in open source code)
        apiKey: '866c333105b7e1ae507e8c362ee6d49c',

        // Exact Index Name in Algolia Dashboard
        indexName: 'AlgoliaSearch',

        // Contextual search allows filtering by language/version
        contextualSearch: true,

        // Path for standalone search page enabled by default
        searchPagePath: 'search',
      },

      image: 'img/docusaurus-social-card.jpg',
      colorMode: {
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'ProductBridge',
        logo: {
          alt: 'ProductBridge Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'docsSidebar',
            position: 'left',
            label: 'ProductBridge Docs',
          },
          {
            type: 'docSidebar',
            sidebarId: 'faqSidebar',
            position: 'left',
            label: 'FAQs',
          },
          {
            href: 'https://github.com/Mohita111/ProductBridge',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'ProductBridge Docs',
                to: '/docs/getting-started/product-bridge-overview',
              },
              {
                label: 'FAQs',
                to: '/docs/FAQ',
              },
              {
                label: 'Glossary',
                to: '/docs/Glossary',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
              {
                label: 'X',
                href: 'https://x.com/docusaurus',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} ProductBridge. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;