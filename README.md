didroute
========

A quick and dirty Flask app for running on your Intranet (or wherever, it's
your funeral) that lets you switch the routing of a Dial-in Direct number
(DID)from VoIP.ms using the VoIP.ms REST API.

Current supports switching between IVRs and forwarders.

The use case is basically that I wanted to be able to quickly and easily change
the routing on the VoIP number to which my building buzzer is connected, and
have those that live with me do the same, without going through the hopelessly
complicated VoIP.ms web interface.

See `config.yaml.template` for an example config. Pass your config's filename
as first and only argument to `run.py`.

Dependencies:

 * Python 3.4 (older 3.x may work)
 * Flask (0.10.1) and its downstream dependencies, including Jinja2 (2.7.3)
 * PyYAML (3.11)
 * Requests (2.7.0)

`ajax-loader.gif` courtesy of [ajaxload.info](http://ajaxload.info/).
