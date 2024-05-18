import { test, expect } from '@playwright/test';

// See here how to get started:
// https://playwright.dev/docs/intro
test('FAILED-CASE: text', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('div')).toHaveText('Welcome to Your Vite + Vue.jsx App');
})

test('SUCCESS-CASE: text', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('link', { name: 'About' }).click();
  await expect(page.getByText('About Info Page')).toBeVisible();
})
