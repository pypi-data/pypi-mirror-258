import { expect, test } from '@jupyterlab/galata';

test('should swap Jupyter logo with clickable Nebari logo', async ({
  page
}) => {
  // Jupyter icon should not be in the main logo
  const jupyterLogo = page.locator(
    '#jp-MainLogo > [data-icon="ui-components:jupyter"]'
  );
  await expect(jupyterLogo).toHaveCount(0);

  // Nebari logo should be in the main logo
  const link = page.locator('#jp-MainLogo > .nebariLogo-link');
  await expect(link).toHaveCount(1);

  // It should look nice and clean in the top panel
  const topPanel = page.locator('#jp-top-panel');
  expect.soft(await topPanel.screenshot()).toMatchSnapshot('top-panel.png');

  // Link should change background on hover
  await link.hover();
  expect.soft(await link.screenshot()).toMatchSnapshot('nebari-logo-hover.png');
  await link.blur();

  // Link should have a focus indicator
  await link.focus();
  expect(await link.screenshot()).toMatchSnapshot('nebari-logo-focus.png');
});

test('should register custom commands', async ({ page }) => {
  const openVScodeProxy = await page.evaluate(async () => {
    const registry = window.jupyterapp.commands;
    const id = 'nebari:open-proxy';
    const args = { name: 'vscode' };

    return {
      id,
      label: registry.label(id, args),
      isEnabled: registry.isEnabled(id, args)
    };
  });

  // Should set correct label for given command
  expect(openVScodeProxy.label).toBe('Open VS Code');

  // Should be enabled when `jupyter-vscode-proxy` is installed
  expect(openVScodeProxy.isEnabled).toBe(true);
});
