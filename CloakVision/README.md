# CloakVision - AI-Powered Invisible Cloak

CloakVision is a real-time computer vision application that creates the illusion of invisibility. When a person covers themselves with a pure white cloth, the application detects the white region in every video frame and replaces that region with the previously captured background, making it appear as though the covered body part has disappeared.

The project uses image processing techniques (HSV color segmentation, morphological operations, blurring) rather than generative AI.

## Features

- **Real-Time Invisibility**: Replace white cloth with a clean background.
- **Modern GUI**: Built with CustomTkinter.
- **Adjustable HSV Calibration**: Sliders to fine-tune white detection based on your lighting.
- **Noise Filtering & Smoothing**: Sliders for opening, closing, and blurring.
- **Optional MediaPipe Pose Integration**: If installed, MediaPipe can restrict the invisibility effect strictly to the person's body, ignoring white objects elsewhere in the background.
- **Camera Selection**: Choose between multiple available webcams.
- **Media**: Save screenshots and record videos of the invisibility effect.

## Setup Instructions

1.  **Clone the repository** (or download the files).
2.  **Navigate** to the project directory:
    ```bash
    cd CloakVision
    ```
3.  **Install dependencies**:
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Run the application:
    ```bash
    python app.py
    ```
2.  Click **Start Camera**.
3.  Click **Capture Background**. You will have 5 seconds to step out of the frame.
4.  Once the background is captured, wear a white cloth and step back in.
5.  Click **Start Invisibility**.
6.  Adjust the HSV Calibration and Smoothing sliders until the effect looks perfect!

## Keyboard Shortcuts
- `F11`: Toggle Fullscreen

## Troubleshooting
- If the cloak is not fully disappearing, adjust the **Value Lower** and **Sat Upper** sliders.
- If other white objects in the room are disappearing, enable **MediaPipe Pose** in the Advanced Features tab (requires the `mediapipe` library to be installed).
- Ensure your background is relatively static and lighting remains consistent.
