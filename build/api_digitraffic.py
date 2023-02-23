from messaging.request import rata
import timeç‹

'''
    connection to rata.digitraffic via https/api
'''

def initialize():
    live_trains = rata('live-trains/station/KKN').get(payload={
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
    get_live_trains = initialize()

    while True:
        get_live_trains.send()
        time.sleep(30)