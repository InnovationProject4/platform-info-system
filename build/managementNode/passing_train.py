import requests


def get_passing_train(station):
    url = f"https://rata.digitraffic.fi/api/v1/live-trains/station/{station}?arrived_trains=0&arriving_trains=20&departed_trains=0&departing_trains=0&include_nonstopping=true"
    response = requests.get(url)
    passing_trains = []
    if response.ok:
        for train in response.json():
            # Check if the train contains timetable information
            if "timeTableRows" in train and len(train["timeTableRows"]) > 1:
                for row in train["timeTableRows"]:
                    # Checks if the row corresponds to an arriving train at the specified station
                    if row["stationShortCode"] == station and row["type"] == "ARRIVAL" and not row["trainStopping"]:
                        # Extract the scheduled arrival time and live estimate (if available) from the row
                        scheduled_time = row["scheduledTime"]
                        live_estimate = row["liveEstimate"] if "liveEstimate" in row else None
                        # If there is a live estimate available and it differs from the scheduled time, use the live estimate instead
                        if live_estimate and live_estimate != scheduled_time:
                            scheduled_time = live_estimate
                        # Add the train's track number and scheduled arrival time to the passing_trains list
                        passing_trains.append({
                            "track": row["commercialTrack"] if "commercialTrack" in row else "",
                            "scheduledTime": scheduled_time
                        })
    # Sorts the passing_trains list by scheduled arrival time
    sorted_passing_trains = sorted(passing_trains, key=lambda train: train["scheduledTime"])
    return sorted_passing_trains



