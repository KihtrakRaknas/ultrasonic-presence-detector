from time import sleep
import network
import urequests
from picozero import DistanceSensor
import config

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(config.SSID, config.PASSWORD)
while not wlan.isconnected():
    sleep(1)
print("Connected:", wlan.ifconfig())


ultrasonic_sensor = DistanceSensor(
    trigger=config.ULTRASONIC_TRIGGER_PIN,
    echo=config.ULTRASONIC_ECHO_PIN,
    max_distance=config.DOOR_HALLWAY_WIDTH / 100,
)


def presence_detected():
    try:
        print("REQUEST")
        urequests.post(
            config.WEBHOOK_URL,
            json=(
                {"history": distance_history}
                if config.DISTANCE_HISTORY_LENGTH > 0
                else None
            ),
            timeout=10,
        ).close()
    except Exception as e:
        print("Error sending presence detection:", e)


presence = False
inactive_time = 0
active_loops = 0
distance_history = []
count_down_to_presence_detected = -1
try:
    while True:
        dist = (ultrasonic_sensor.distance or 0) * 100
        active = dist < config.DOOR_HALLWAY_WIDTH

        distance_history.append(dist)
        if len(distance_history) > config.DISTANCE_HISTORY_LENGTH:
            distance_history.pop(0)

        if not presence:
            if active:
                active_loops += 1
                if active_loops >= config.ACTIVE_LOOP_THRESHOLD:
                    presence = True
                    inactive_time = 0
                    # presence_detected()
                    count_down_to_presence_detected = max(
                        config.DISTANCE_HISTORY_LENGTH - config.ACTIVE_LOOP_THRESHOLD, 0
                    )
            else:
                active_loops = 0
        elif presence and not active:
            inactive_time += config.LOOP_DELAY
            if inactive_time >= config.ACTIVE_RESET_PERIOD:
                presence = False

        if count_down_to_presence_detected == 0:
            presence_detected()
        if count_down_to_presence_detected > -1:
            count_down_to_presence_detected -= 1

        sleep(config.LOOP_DELAY)
except KeyboardInterrupt:
    print("Stopped.")
