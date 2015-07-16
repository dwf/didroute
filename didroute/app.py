from flask import Flask, render_template, flash, Markup

# Module-level variables that mostly get set in the run.py script.
# There must be a cleaner way to do this, but Flask seems to want to
# center around this app object being nothing more than a request router.
# There are probably patterns I'm unaware of.

app = Flask('didroute')
api = None
did_routes = None
did_id = None


@app.route('/')
def index(result=None):
    # Determine current routing for the (single) DID we care about.
    kind, which = api.dids[did_id]['routing'].split(':')
    # We only support ivrs and fwds. If it's in another state,
    if kind == 'ivr':
        # This should always succeed.
        name = [v['name'] for v in api.ivrs.values()
                if v['ivr'] == which][0]
    elif kind == 'fwd':
        # This should also always succeed.
        name = [v['description'] for v in api.forwarders.values()
                if v['forwarding'] == which][0]
    else:
        raise ValueError

    # This, on the other hand, relies on the routes in config.yaml
    # including the one that's currently assigned.
    current = [i for i, d in enumerate(did_routes)
               if d['name'] == name][0]

    # Highlight with a border around the currently selected DID routing.
    my_routes = list(dict(d) for d in did_routes)
    for i, route in enumerate(my_routes):
        if i == current:
            route['border'] = 2
        else:
            route['border'] = 0
    return render_template('template.html', did_routes=my_routes,
                           result=result, current=current)


@app.route('/set/<int:route_index>')
def set_route(route_index):
    # No fancy AJAX stuff here.
    name = did_routes[route_index]['name']
    kind = did_routes[route_index]['kind']
    if kind == 'fwd':
        result = api.dids[did_id].set_routing(api.forwarders[name])
    elif kind == 'ivr':
        result = api.dids[did_id].set_routing(api.ivrs[name])
    else:
        raise ValueError
    if result['status'] == 'success':
        flash(Markup('Mazel tov! You changed the routing for '
                     '<strong>{}</strong> to <strong>{}</strong>.'
                     .format(did_id, name)), 'big_flash')
        flash('It may take a few minutes to take effect.'
              .format(did_id, name), 'small_flash')
    return index()
