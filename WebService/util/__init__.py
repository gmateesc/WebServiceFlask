from persistence import load_store

#
# Check that the JSON payload observes the schema
#
def event_type_check(event):

    import six

    str_type = six.string_types
    int_type = six.integer_types

    #
    # Check the types of the values of the top level keys
    #

    if (not isinstance(event['id'],        str_type)) or  \
       (not isinstance(event['title'],     str_type)) or  \
       (not isinstance(event['state'],     str_type)) or  \
       (not isinstance(event['initiator'], dict)): 
       raise TypeError("invalid 'id', 'title', 'state' or 'initiator' field")


    #
    # Check the types of the values of event['initiator']
    #

    # If the notify value is "False" or "True", convert to boolean
    if isinstance(event['initiator']['notify'], str_type):
        if event['initiator']['notify'].lower() == 'false':
            event['initiator']['notify'] = False
        elif event['initiator']['notify'].lower() == 'true':
            event['initiator']['notify'] = True

    # Check the types
    if (not isinstance(event['initiator']['notify'], bool)) or \
       (not isinstance(event['initiator']['name'],   str_type)) or  \
       (not isinstance(event['initiator']['email'],  str_type)):
       raise TypeError("invalid 'initiator' field")




#
# Save a new event: persist the event to a file
# and add it to the cache
#
def save_event(config, events, event ):

    # If the event is in cache, remove it from cache
    old_event = filter ( lambda e: e['id']==event['id'], events )
    if len(old_event) != 0:
        old = old_event[0]
        events.remove(old)

    # Add new event to cache
    events.append(event)

    # Persist event to DOCUMENT_ROOT
    file_name = config['DOCUMENT_ROOT'] + "/" + event['id'] + ".json"
    load_store.store_file(file_name, event)




#
# Load an event: 
#
def load_event(config, events, event_id ):

    #
    # If the event is in cache, get it from cache
    #

    cache_event = filter ( lambda e: e['id']==event_id, events )
    if len(cache_event) != 0:

        print("DEBUG: get event %s from cache " % (event_id) )
        event = cache_event
        
    else:

      #
      # Load event from file and add to cache
      #
      import os.path
      file_name = config['DOCUMENT_ROOT'] + "/" + str(event_id) + ".json"
      if os.path.isfile(file_name):
        print("DEBUG: get event %s from file " % (event_id) )
        event = [load_store.load_file(file_name) ]
      else:
        event = []

      # Add event to cache
      if len(event) != 0:
        events.append(event[0])

    if len(event) != 0:
        print("DEBUG: event is %s " % event[0] )

    return event

