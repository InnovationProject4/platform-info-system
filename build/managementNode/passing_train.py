import requests


def get_passing_train(station):
    url = f"https://rata.digitraffic.fi/api/v1/live-trains/station/{station}?arrived_trains=0&arriving_trains=20&departed_trains=0&departing_trains=0&include_nonstopping=true"
    response = requests.get(url)
    passing_trains = []
    if response.ok:
        for train in response.json():
            if "timeTableRows" in train and len(train["timeTableRows"]) > 1:
                for row in train["timeTableRows"]:
                    if row["stationShortCode"] == station and row["type"] == "ARRIVAL" and not row["trainStopping"]:
                        scheduled_time = row["scheduledTime"]
                        live_estimate = row["liveEstimate"] if "liveEstimate" in row else None
                        if live_estimate and live_estimate != scheduled_time:
                            scheduled_time = live_estimate
                        passing_trains.append({
                            "track": row["commercialTrack"] if "commercialTrack" in row else "",
                            "scheduledTime": scheduled_time
                        })
    return passing_trains



