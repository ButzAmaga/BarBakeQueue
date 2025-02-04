from django.http import StreamingHttpResponse
import time
import asyncio

    

async def notification_stream(request):
    """Asynchronous SSE event generator."""
    print("Response")
    for i in range(1, 99):
        yield f'event: counter\ndata: <p>{i} notification</p>\n\n'
    
        await asyncio.sleep(2)  # Non-blocking delay for async stream
    

def NotificationView(request):
    """Handles SSE connection."""
    response = StreamingHttpResponse(notification_stream(request=request), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["Connection"] = "keep-alive"
    return response

    