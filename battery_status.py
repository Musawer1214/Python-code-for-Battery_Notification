#!/usr/bin/env python3
import psutil
import beepy
import time
import sys
import argparse

def get_target_percentage():
    parser = argparse.ArgumentParser(description="Battery monitor script.")
    parser.add_argument("--percent", type=int, help="Target battery percentage (0-100).")
    args = parser.parse_args()

    percentage_val = -1

    if args.percent is not None:
        percentage_val = args.percent
    else:
        print("No --percent argument provided. Attempting to read from input.", file=sys.stderr)
        try:
            percentage_str = input("Select percentage for Beep (0-100): ")
            percentage_val = int(percentage_str)
        except EOFError:
            print("Error: EOFError. Cannot read from input. Please run with --percent <value>.", file=sys.stderr)
            sys.exit(1)
        except ValueError:
            print("Error: Invalid numeric input.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error during input: {e}", file=sys.stderr)
            sys.exit(1)
            
    if not (0 <= percentage_val <= 100):
        print(f"Error: Percentage '{percentage_val}' must be 0-100.", file=sys.stderr)
        sys.exit(1)
    
    print(f"Monitoring: Notify when battery reaches {percentage_val}%.")
    return percentage_val

def check_battery():
    try:
        battery = psutil.sensors_battery()
        if battery is None: return None, None
        plugged = getattr(battery, 'power_plugged', None)
        percent = getattr(battery, 'percent', None)
        if plugged is None or percent is None: return None, None
        return plugged, percent
    except Exception as e:
        return None, None

def play_alert_sound():
    try:
        beepy.beep(sound=1)
    except Exception as e:
        print("BEEP! (Sound alert failed or sound system not available)", file=sys.stderr)

def main():
    target_percentage = get_target_percentage()
    print(f"Starting battery monitor for {target_percentage}%. Press Ctrl+C to exit.")
    notified_while_charging = False
    
    try:
        while True:
            plugged, current_percent = check_battery()
            if plugged is not None and current_percent is not None:
                if plugged and current_percent >= target_percentage:
                    if not notified_while_charging:
                        print(f"Battery at {current_percent}%. Please unplug the charger.")
                        play_alert_sound()
                        notified_while_charging = True
                elif plugged:
                    notified_while_charging = False
                else: 
                    notified_while_charging = False
            else:
                pass 
            time.sleep(60) # Set to 60 seconds for normal operation
    except KeyboardInterrupt:
        print("\nExiting battery monitor.")
    except Exception as e:
        print(f"An unexpected error occurred in main loop: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
