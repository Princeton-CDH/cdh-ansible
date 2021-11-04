// custom driver for archiving Derrida's Margins
module.exports = async ({ data, page, crawler }) => {
  await crawler.loadPage(page, data);

  // for the interactive histogram viz, hover over each marker
  // to load & archive the ajax reference card
  const markers = await page.$$('.visualization-chapter-marker')
  for (let count = 0; count < markers.length; count++) {
    await markers[count].hover();
    await crawler.sleep(1000);
  }

  // for image display, toggle to deep zoom mode to
  // load & archive local IIIF info.json
  const zoom_button = await page.$$('[href="#zoom"]');
  if (zoom_button.length > 0) {
    await crawler.sleep(1000);
    await zoom_button[0].click()
    await crawler.sleep(1000);
  }
};