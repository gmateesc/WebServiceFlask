#!/usr/bin/env python

from __future__ import print_function

from flask import Flask, jsonify, abort
from flask import request, make_response

import util

#
# Create app instance
#
app = Flask(__name__)


#
# Events cache
#
events = [ ]



#
# Associate URI /schedule/api/v1/events and method GET 
# with the function get_events
#
@app.route('/schedule/api/v1/events', methods=['GET'])
def get_events():
    return jsonify({'events': events})


#
# Associate URI /schedule/api/v1/events/<event_id> and method GET 
# with the function get_event
#
@app.route('/schedule/api/v1/events/<event_id>', methods=['GET'])
def get_event(event_id):

    # <event_id> from URI is translated to thr event_id param 
    # of the func get_event()

    #event = [event for event in events if event['id'] == event_id]
    event = util.load_event(app.config, events, event_id)
    if len(event) == 0:
        abort(404)

    return jsonify({'event': event[0]})


#
# Associate URI /schedule/api/v1/events and method POST
# with the function create_event
#
@app.route('/schedule/api/v1/events', methods=['POST'])
def create_event():

    print("POST /schedule/api/v1/event")

    if not request.is_json:
        abort(400)

    json_obj = request.get_json()
    print("POST request.json = ", json_obj)

    try:
      event = {
        'id':        json_obj['id'],
        'title':     json_obj['title'],
        'initiator': json_obj['initiator'],
        'state':     json_obj['state']
      }

      util.event_type_check(event)

    except (TypeError, KeyError) as err:
      abort(400)

    util.save_event(app.config, events, event)

    #return jsonify({'foo': 'bar'}), 201
    return jsonify(event), 201


#
# Associate URI /schedule/api/v1/events/<event_id> and method DELETE
# with the function delete_event
#
@app.route('/schedule/api/v1/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = [event for event in events if event['id'] == event_id]
    if len(event) == 0:
        abort(404)
    events.remove(event[0])
    return jsonify({'result': True})


#
# Error handlers
#

@app.errorhandler(400)
def bad_request(error):
    if request.method == 'POST':
        msg = "Ensure payload is a valid JSON, e.g., "
        msg += "{'id':<str>,'title':<str>,'state':<str>, "  \
             + "'initiator':{'name':<str>,'notify':<bool>,'email':<str>}}"
    else:
        msg =""
    return make_response(jsonify({"error": "Bad request (400). " + msg}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found (404)'}), 404)


@app.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error': 'Method not allowed (405)'}), 405)




#
# Run app when this file is the main program
#

if __name__ == '__main__':

    #
    # Configure the app
    #
    app.config.from_object("conf")

    # 
    # Load SSL certificate and key into the context object
    # 
    context = (app.config['SSL_CERT_DIR'] + '/cert.pem', app.config['SSL_CERT_DIR'] + '/key.pem')

    #
    # Run the app using an SSL context
    #
    app.run(host=app.config['HOST'], port=app.config['PORT'], ssl_context=context, threaded=True)

