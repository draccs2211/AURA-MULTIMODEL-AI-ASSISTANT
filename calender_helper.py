from datetime import datetime, timedelta
from calender_auth import get_calendar_service


def create_event(title, date_str, time_str, duration_minutes=60):
    """
    Create a calendar event with title, date (YYYY-MM-DD), time (HH:MM), and duration (minutes)
    """
    service = get_calendar_service()

    start_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    end_time = start_time + timedelta(minutes=duration_minutes)

    event = {
        'summary': title,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event


def read_events_for_day(date_str):
    """
    Fetch all events for the given date (format: YYYY-MM-DD)
    """
    service = get_calendar_service()
    start_of_day = datetime.strptime(date_str, "%Y-%m-%d")
    end_of_day = start_of_day + timedelta(days=1)

    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_of_day.isoformat() + 'Z',
        timeMax=end_of_day.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    return events


def add_event_to_calendar(title, date_str, time_str, duration=60):
    """
    Wrapper to add event and return success/failure boolean
    """
    try:
        event = create_event(title, date_str, time_str, duration)
        return True if event else False
    except Exception as e:
        print("Error adding event:", e)
        return False
