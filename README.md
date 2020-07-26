# Rotating  IPs python script

Custom proxy server enabling to set separate proxies for each tab in a browser.

## How does it work?
Each HTTP request from the browser will be redirected by `base_proxy.py` script to a Django application.
There user will be able to set a proxy (loaded from preset list of proxies) to handle requests in current tab.

After setting the proxy to use and saving the setting for current tab, request will be made by Django serbig as a proxy
to web server.  

[NOTE]: If the proxy has been set, user will not be redirected to "choose proxy" view, a request will be made automatically.

##Requirements:
* Python 3 installed locally and added to $PATH
* Firefox installed
* Installing attached Firefox Add on (`request-headers-tab-id)

## Basic usage:




### Firefox extension



### Base proxy handler

Base proxy handler is required to redirect all the traffic to Django-powered application 