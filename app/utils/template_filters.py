from flask import current_app
from datetime import datetime, timezone

@current_app.template_filter("timeago")
def timeago_filter(dt):
    if not dt:
        return ""
    
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    diff = now - dt
    seconds = diff.total_seconds()
    
    if seconds < 10:
        return "now"
    elif seconds < 60:
        return f"{int(seconds)}s ago"
    elif seconds < 3600:
        return f"{int(seconds//60)}m ago"
    elif seconds < 86400:
        return f"{int(seconds//3600)}h ago"
    elif seconds < 604800:
        return f"{int(seconds//86400)}d ago"
    elif seconds < 2419200:
        return f"{int(seconds//604800)}w ago"
    else:
        return dt.strf("%B%d%Y")
    
        
    
    