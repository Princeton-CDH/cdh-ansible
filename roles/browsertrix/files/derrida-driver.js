module.exports = async ({ data, page, crawler }) => {
  await crawler.loadPage(page, data);

  const markers = await page.$$('.visualization-chapter-marker')
  for (let count = 0; count < markers.length; count++) {
    await markers[count].hover();
    await crawler.sleep(1000);
  }

  // get deep zoom info.json
  const zoom_button = await page.$$('[href="#zoom"]');
  if (zoom_button.length > 0) {
    await crawler.sleep(1000);
    await zoom_button[0].click()
    await crawler.sleep(1000);
  }
};