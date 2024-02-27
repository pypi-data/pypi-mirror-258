async () => {
    const viewportHeight = window.document.documentElement.clientHeight;
    const totalHeight = window.document.documentElement.scrollHeight;
    let scrolledHeight = window.scrollY;

    while (scrolledHeight < totalHeight) {
        scrolledHeight += viewportHeight;
        window.scrollTo(0, scrolledHeight);
        await new Promise(resolve => setTimeout(resolve, 100));
    }
}
