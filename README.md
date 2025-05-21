# Battery Notification Script

Get notified when your device's battery reaches a desired charge percentage. This Python script monitors battery status and provides an audible alert.

## Features

*   Set a custom battery percentage for notifications.
*   Audible beep alerts (platform-dependent, with fallbacks).
*   Cross-platform: Designed to work on Windows, Linux (desktop), and Android (via Termux/Pydroid3).
*   Command-line interface for setting the target percentage.

## Supported Platforms

*   **Windows**: Fully supported.
*   **Linux (Desktop)**: Fully supported. (Requires audio libraries for sound, e.g., ALSA or PulseAudio development packages for `beepy`).
*   **Android**: Supported via Termux or Pydroid 3, with specific considerations (see "Running on Android" section).

## Dependencies

This script relies on the following Python libraries:

*   **`psutil`**: For fetching battery status across platforms.
*   **`beepy`**: For playing sound alerts.
    *   Note: `beepy`'s effectiveness, especially on Linux and Android, depends on the availability of system audio libraries and successful compilation of its dependency `simpleaudio`. On Android/Termux, if `beepy` fails, using Termux-API for notifications is a recommended alternative (see "Running on Android").
*   **`argparse`**: For parsing command-line arguments (part of standard Python library, no separate installation needed).

**Installation of Dependencies:**

It's recommended to install these libraries using `pip`:

```bash
pip install psutil beepy
```

(On Linux, you might need to install audio development libraries first, e.g., `sudo apt-get install libasound2-dev python3-dev` on Debian/Ubuntu for `beepy`/`simpleaudio`).

A `requirements.txt` file may be added in the future for easier dependency management.

## Installation and Usage

1.  **Download the Script**:
    *   Clone this repository or download `battery_status.py`.

2.  **Install Dependencies**:
    *   Ensure Python 3 is installed on your system.
    *   Install the required libraries as mentioned in the "Dependencies" section.

3.  **Running the Script**:
    *   Open your terminal or command prompt.
    *   Navigate to the directory where you saved `battery_status.py`.
    *   Execute the script using the `--percent` argument to set your desired notification percentage:

        ```bash
        python battery_status.py --percent 80
        ```
        (Replace `80` with your target percentage, e.g., 90 for 90%).

    *   The script will then run in the background, checking the battery status every 60 seconds.
    *   You will hear a beep and see a console message when the battery reaches or exceeds the specified percentage while charging.

### Platform-Specific Instructions

#### Windows & Linux (Desktop)

*   Follow the general "Running the Script" instructions above.
*   On Linux, ensure you have necessary audio libraries installed for `beepy` to function correctly (e.g., `libasound2-dev`).

#### Android

*   Please refer to the detailed "[Running on Android](#running-on-android)" section below for specific setup instructions using Termux or Pydroid 3, including important notes on battery optimization and potential sound issues.

## Running on Android

Running this script on Android is possible, primarily using an app called Termux, which provides a Linux-like terminal environment. Pydroid 3 is another alternative but might have different steps for package installation.

**Important Considerations for Android:**

*   **Battery Optimization**: Android's aggressive battery optimization will likely terminate background scripts. You **must** disable battery optimization for Termux (or your chosen Python app) for this script to run reliably in the background. Go to Android Settings -> Apps -> Termux -> Battery, and set it to "Unrestricted" or "Allow background activity" (wording varies by Android version).
*   **Wake Lock (Termux)**: To prevent the device from deep sleeping and stopping the script, use Termux's wake lock feature. Install tools: `pkg install termux-tools`. Before running the script, execute `termux-wake-lock` in the Termux session.
*   **Sound (`beepy`) Issues**: The `beepy` library (and its dependency `simpleaudio`) requires compilation and access to system audio libraries. This can be problematic on Android. If `beepy` fails to install or produce sound, an alternative is to use Termux-API for notifications (see below).

### Using Termux (Recommended)

1.  **Install Termux**:
    *   It is highly recommended to install Termux from [F-Droid](https://f-droid.org/en/packages/com.termux/) or [GitHub](https://github.com/termux/termux-app#installation) as the Google Play Store version is outdated and no longer supported.

2.  **Initial Setup & Update**:
    *   Open Termux and run:
        ```bash
        pkg update && pkg upgrade -y
        ```

3.  **Install Python and Build Tools**:
    *   ```bash
        pkg install python build-essential python-dev libandroid-support-dev clang -y
        ```
    *   (Note: `libandroid-support-dev` provides general NDK support. For audio, `simpleaudio` might also need `opensles`, try `pkg install libopensles-dev` or `opensles-toolchain` if `beepy` installation fails later).

4.  **Install Script Dependencies**:
    *   Install `psutil`:
        ```bash
        pip install psutil
        ```
    *   Install `beepy`:
        ```bash
        pip install beepy
        ```
    *   **If `beepy` installation fails**: This is often due to `simpleaudio` compilation issues. Android's audio system is different from desktop Linux. You might need to search for specific solutions or use the Termux-API alternative for sound (see "Alternative for Sound" below).

5.  **Download/Transfer the Script**:
    *   Download `battery_status.py` to your device.
    *   In Termux, navigate to where you saved it (e.g., in internal storage, often accessible via `/sdcard/Download` or by setting up Termux storage access with `termux-setup-storage`).
        ```bash
        cd /sdcard/Download # Example path
        ```

6.  **Run the Script**:
    *   Remember to acquire a wake lock first: `termux-wake-lock`
    *   Then run the script:
        ```bash
        python battery_status.py --percent 80
        ```
        (Replace `80` with your desired percentage).

7.  **Alternative for Sound/Notification (if `beepy` fails)**:
    *   Install Termux-API:
        ```bash
        pkg install termux-api
        ```
    *   You will also need to install the Termux:API app from F-Droid or GitHub.
    *   Modify `battery_status.py`. Change the `play_alert_sound` function to:
        ```python
        import os # Ensure os is imported at the top of the script

        def play_alert_sound():
            try:
                # This command creates a notification and plays the default notification sound.
                # The {current_percent} variable would need to be passed into this function or accessed globally.
                # For simplicity, a generic message is used here.
                os.system('termux-notification -t "Battery Alert" --content "Battery at target! Unplug charger." --id "battery-alert" --priority max --sound')
                # For spoken alerts (Text-To-Speech):
                # os.system('termux-tts-speak "Battery at target, please unplug your charger."')
            except Exception as e:
                print(f"Termux-API notification/TTS failed: {e}", file=sys.stderr)
        ```
    * This provides a reliable way to get notified even if `beepy` doesn't work.

### Using Pydroid 3

1.  **Install Pydroid 3**: Get it from the Google Play Store.
2.  **Install Dependencies**:
    *   Open Pydroid 3, go to the "PIP" tab.
    *   Search for and install `psutil`.
    *   Search for and install `beepy`. (Success for `beepy` depends on Pydroid's build environment and included libraries, similar to Termux).
3.  **Run the Script**:
    *   Open `battery_status.py` in Pydroid 3.
    *   Run it. You might need to provide command-line arguments if Pydroid 3 supports it, or modify the script to set the percentage directly if not.
4.  **Battery Optimization & Background**:
    *   Like Termux, you **must** disable battery optimization for Pydroid 3 in Android settings.
    *   Pydroid 3 may have its own settings related to background execution; consult its documentation.
    *   If `beepy` fails, a generic Python library for Android notifications would be needed, which is outside the scope of this script's direct dependencies.

**General Android Notes:**
*   The script checks battery status every 60 seconds.
*   Ensure your Android device does not aggressively kill background processes or network connections if you are running this for extended periods.
*   Permissions for accessing battery status are usually handled by `psutil` leveraging the permissions granted to the host app (Termux or Pydroid 3).

## Contributing

Contributions are welcome and encouraged! If you'd like to contribute to this project:

1.  **Fork the repository** on GitHub.
2.  **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name` or `bugfix/your-bug-fix`.
3.  **Make your changes** and commit them with clear, descriptive messages.
4.  **Push your branch** to your forked repository.
5.  **Submit a pull request** to the main repository, detailing the changes you've made.

Please ensure your code is well-formatted and tested if possible.

## License

This project is licensed under the **MIT License**.

(A `LICENSE` file should be added to the repository containing the full MIT License text in a future step).
