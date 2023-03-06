import messaging.ratatraffic as ratatraffic
import time

'''
    connection to rata.digitraffic via https/api
'''


# Multiple API  requests
def batchRequest():
    live_trains = ratatraffic.Batch()

    live_trains.get('live-trains/station/KKN', payload={
        'arrived_trains': 0,
        'arriving_trains': 5,
        'departing_trains': 0,
        'departed_trains': 0,
        'include_nonstopping': 'true'
    }, onSuccess= lambda res, status, data : (
        print("success #1"), print(res.json())

    )).get('live-trains/station/KNN', payload={
        'arrived_trains': 0,
        'arriving_trains': 5,
        'departing_trains': 0,
        'departed_trains': 0,
        'include_nonstopping': 'true'
    }, onSuccess= lambda res, status, data : (
        print("success #2"), print(res.json())
    ))

    return live_trains


# Single API request
def singleRequest():

    live_trains = ratatraffic.Simple('live-trains/station/KKN').get(payload={
        'arrived_trains': 0,
        'arriving_trains': 5,
        'departing_trains': 0,
        'departed_trains': 0,
        'include_nonstopping': 'true'
    }).onSuccess(lambda response, status, data : (
        print("successful fetching"), 
        print(response.json())

    )).onFailure(lambda response, status, data : (
        print(f"Error: {status}") if status == 400 else print(f"Internal Error: {status}"),
        str(data)

    ))

    return live_trains



if __name__ == '__main__':
    get_live_trains = singleRequest()

    while True:
        get_live_trains.send()
        time.sleep(30)