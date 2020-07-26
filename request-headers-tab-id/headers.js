"use strict";

/*
This is the page for which we want to rewrite the User-Agent header.
*/
var targetPage = "https://httpbin.org/*";

/*
Set UA string to Opera 12
*/
var ua = "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16";

/*
Rewrite the User-Agent header to "ua".
*/
function rewriteUserAgentHeaderAsync(e) {
  var asyncRewrite = new Promise((resolve, reject) => {
    window.setTimeout(() => {
      for (var header of e.requestHeaders) {
        if (header.name.toLowerCase() === "user-agent") {
          header.value = ua;
        }
      }
      resolve({requestHeaders: e.requestHeaders});
    }, 2000);
  });

  return asyncRewrite;
}

/*
Add rewriteUserAgentHeader as a listener to onBeforeSendHeaders,
only for the target page.

Make it "blocking" so we can modify the headers.
*/
browser.webRequest.onBeforeSendHeaders.addListener(
  rewriteUserAgentHeaderAsync,
  {urls: [targetPage]},
  ["blocking", "requestHeaders"]
);