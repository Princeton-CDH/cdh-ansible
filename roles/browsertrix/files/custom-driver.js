module.exports = async ({ data, page, crawler }) => {
    await crawler.loadPage(page, data);

    const markers = await page.$$('.visualization-chapter-marker')
    for (let count = 0; count < markers.length; count++) {
        await markers[count].hover();
        await crawler.sleep(1000);
    }
};