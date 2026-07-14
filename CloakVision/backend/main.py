from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import json

from cloak_detector import CloakDetector

app = FastAPI(title="CloakVision API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "ok", "service": "CloakVision Backend"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time invisible cloak processing.

    Binary message protocol (first byte = type):
      Client → Server:
        0x00 + JPEG bytes  → regular video frame (server returns processed frame)
        0x01 + JPEG bytes  → capture this frame as the background

      Server → Client:
        0x02 + JPEG bytes  → processed / output frame

    JSON message protocol:
      Client → Server:
        { "command": "toggle_invisibility" }
        { "command": "update_hsv", "h": int, "s": int, "v": int }
        { "command": "update_proc", "open_k": int, "close_k": int, "blur_k": int }

      Server → Client:
        { "type": "status", "active": bool, "bg_ready": bool }
    """
    await websocket.accept()

    detector = CloakDetector()
    background = None
    invisibility_active = False

    try:
        while True:
            message = await websocket.receive()

            # ── JSON command ──────────────────────────────────────────────────
            if "text" in message and message["text"]:
                try:
                    data = json.loads(message["text"])
                except json.JSONDecodeError:
                    continue

                command = data.get("command")

                if command == "toggle_invisibility":
                    if background is not None:
                        invisibility_active = not invisibility_active
                    await websocket.send_json({
                        "type": "status",
                        "active": invisibility_active,
                        "bg_ready": background is not None,
                    })

                elif command == "update_hsv":
                    detector.update_hsv_thresholds(
                        [0, 0, int(data.get("v", 180))],
                        [int(data.get("h", 180)), int(data.get("s", 40)), 255],
                    )

                elif command == "update_proc":
                    detector.update_filter_params(
                        int(data.get("open_k", 3)),
                        int(data.get("close_k", 3)),
                        int(data.get("blur_k", 5)),
                    )

            # ── Binary frame ──────────────────────────────────────────────────
            elif "bytes" in message and message["bytes"]:
                raw = message["bytes"]
                if not raw or len(raw) < 2:
                    continue

                msg_type = raw[0]
                frame_bytes = bytes(raw[1:])

                nparr = np.frombuffer(frame_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if frame is None:
                    continue

                # type 0x01 → set background
                if msg_type == 1:
                    background = frame.copy()
                    await websocket.send_json({
                        "type": "status",
                        "bg_ready": True,
                        "active": invisibility_active,
                    })
                    continue

                # type 0x00 → process frame and return
                if invisibility_active and background is not None:
                    bg = background
                    if bg.shape != frame.shape:
                        bg = cv2.resize(bg, (frame.shape[1], frame.shape[0]))
                    display_frame = detector.apply_cloak(frame, bg)
                else:
                    display_frame = frame

                ret, buffer = cv2.imencode(
                    ".jpg", display_frame, [cv2.IMWRITE_JPEG_QUALITY, 80]
                )
                if ret:
                    # Prefix with type byte 0x02
                    await websocket.send_bytes(bytes([2]) + buffer.tobytes())

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")
