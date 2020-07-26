function onGot(tabInfo) {
    console.log(tabInfo);
}

function onError(error) {
    console.log(`Error: ${error}`);
}

function rewriteUserAgentHeader(e) {
    const gettingCurrent = browser.tabs.getCurrent();
    gettingCurrent.then(onGot, onError);

    let headers = e.requestHeaders;
    console.log(headers);
    console.log(e.requestHeaders);
    headers["Tab-Id"] = gettingCurrent.id;

    return {requestHeaders: headers};
}

browser.webRequest.onBeforeSendHeaders.addListener(
    rewriteUserAgentHeader,
    {urls: ["<all_urls>"]},
    ["blocking", "requestHeaders"]
);