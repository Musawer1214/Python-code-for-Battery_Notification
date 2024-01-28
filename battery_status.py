import psutil
import winsound
import time

percentage = int(input("Select percentage for Beep(0-100) :  "))

print("You will be notified when your battery will reach {}%".format(percentage))

def check_battery():
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = battery.percent

    return plugged, percent

def beep():
    frequency = 1500  # Frequency of the beep sound in Hertz
    duration = 1000   # Duration of the beep sound in milliseconds
    winsound.Beep(frequency, duration)

def main():
    while True:
        plugged, percent = check_battery()
        

        if plugged and percent == percentage:
            message = f"Unplug the charger! Battery is {percent}% charged."
            print(message)
            beep()

        time.sleep(60)  # Check battery status every 60 seconds

if __name__ == "__main__":
    main()