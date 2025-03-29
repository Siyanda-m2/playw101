import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 60000,
  fullyParallel: true,
  use: {
    headless: true,
    video: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'Windows_Chrome',
      use: {
        browserName: 'chromium',
        viewport: { width: 1280, height: 720 },
        connectOptions: {
          wsEndpoint: `wss://cdp.lambdatest.com/playwright?capabilities=${encodeURIComponent(
            JSON.stringify({
              browserName: 'Chrome',
              browserVersion: 'latest',
              platform: 'Windows 10',
              tunnel: false,
              console: true,
              network: true,
              username: process.env.LT_USERNAME,
              accessKey: process.env.LT_ACCESS_KEY,
            })
          )}`,
        },
      },
    },
    {
      name: 'MacOS_Firefox',
      use: {
        browserName: 'firefox',
        viewport: { width: 1280, height: 720 },
        connectOptions: {
          wsEndpoint: `wss://cdp.lambdatest.com/playwright?capabilities=${encodeURIComponent(
            JSON.stringify({
              browserName: 'Firefox',
              browserVersion: 'latest',
              platform: 'macOS Catalina',
              tunnel: false,
              console: true,
              network: true,
              username: process.env.LT_USERNAME,
              accessKey: process.env.LT_ACCESS_KEY,
            })
          )}`,
        },
      },
    },
  ],
});
