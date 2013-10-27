
def events_to_month_info(eventList):
    dateSet = set()
    for evt in eventList:
        dateSet.add(evt.date.day)
    jsonMap = {}
    jsonMap['count'] = len(eventList)
    jsonMap['dates'] = list(dateSet)
    return jsonMap

def event_to_json(evt):
    return {'startTime':date_to_minute_hour(evt.startTime),
            'endTime':date_to_minute_hour(evt.endTime),
            'name':evt.name.name,
            'id':evt.id,
            'description':''}

def date_to_minute_hour(date):
    return {'minute':date.minute, 'hour':date.hour}

def events_to_day_info(eventList):
    return map(event_to_json, eventList)

def program_to_json(program):
    return {'name':program.name, 'id':program.id}
