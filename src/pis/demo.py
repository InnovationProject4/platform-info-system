import utils.BinaryTree as Trees

data = [
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'IC11': [
          {
            'trainNumber': 11,
            'trainType': 'IC',
            'trainCategory': 'Long-distance',
            'commuterLineID': '',
            'timetable': [
              {
                'destination': 'Joensuu asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:35:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '4',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              }
            ]
          }
        ],
        'S89': [
          {
            'trainNumber': 89,
            'trainType': 'S',
            'trainCategory': 'Long-distance',
            'commuterLineID': '',
            'timetable': [
              {
                'destination': 'Jyväskylä',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:09:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '4',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              }
            ]
          }
        ],
        'IC111': [
          {
            'trainNumber': 111,
            'trainType': 'IC',
            'trainCategory': 'Long-distance',
            'commuterLineID': '',
            'timetable': [
              {
                'destination': 'Imatra asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:25:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '4',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'IC24': [
          {
            'trainNumber': 24,
            'trainType': 'IC ',
            'trainCategory': 'Long-distance',
            'commuterLineID': '',
            'timetable': [
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:30:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimate Time': '2023-04-03T14:30:18.000Z',
                'commercialTrack': '5',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ],
        'IC68': [
          {
            'trainNumber': 68,
            'trainType': 'IC',
            'trainCategory': 'Long-distance',
            'commuterLineID': '',
            'timetable': [
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:35:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T15:35:13.000Z',
                'commercialTrack': '5',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ],
        'IC86': [
          {
            'trainNumber': 86,
            'trainType': 'IC',
            'trainCategory': 'Long-distance',
            'commuterLineID': '',
            'timetable': [
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTUR E',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:49:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T14:49:13.000Z',
                'commercialTrack': '5',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'IC29': [
          {
            'trainNumber': 29,
            'trainType': 'IC',
            'trainCategory': 'Long-distance',
            'commuterLineID': '',
            'timetable': [
              {
                'destination': 'Oulu asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:30:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '3',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              }
            ]
          }
        ],
        'IC49': [
          {
            'trainNumber': 49,
            'trainType': 'IC',
            'trainCategory': 'Long-distance',
            'commuterLineID': '',
            'timetable': [
              {
                'destination': 'Vaasa',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:30:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '3',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              }
            ]
          }
        ],
        'IC177': [
          {
            'trainNumber': 177,
            'trainType': 'IC',
            'trainCategory': 'Long-distance',
            'commuterLineID': '',
            'timetable': [
              {
                'destination': 'Tampere asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:09:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime ': None,
                'commercialTrack': '3',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'IC50': [
          {
            'trainNumber': 50,
            'trainType': 'IC',
            'trainCategory': 'Long-distance',
            'commuterLineID': '',
            'timetable': [
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:30:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateT ime': '2023-04-03T15:30:13.000Z',
                'commercialTrack': '6',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'IC962': [
          {
            'trainNumber': 962,
            'trainType': 'IC',
            'trainCategory': 'Long-distance',
            'commuterLineID': '',
            'timetable': [
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:18:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': ' 2023-04-03T14:18:23.000Z',
                'commercialTrack': '9',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ],
        'IC964': [
          {
            'trainNumber': 964,
            'trainType': 'IC',
            'trainCategory': 'Long-distance',
            'commuterLineID': '',
            'timetable': [
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:18:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T15:18:00.000Z',
                'commercialTrack': '9',
                'trainSto pping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'IC963': [
          {
            'trainNumber': 963,
            'trainType': 'IC',
            'trainCategory': 'Long-distance',
            'commuterLineID': '',
            'timetable': [
              {
                'destination': 'Kupittaa',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:42:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '8',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              }
            ]
          }
        ],
        'IC965': [
          {
            'trainNumber': 965,
            'trainType': 'IC',
            'trainCategory': 'Long-distance',
            'commuterLineID': '',
            'timetable': [
              {
                'destination': 'Kupittaa',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:42:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '8',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'H elsinki Kivihaka',
                  'Huopalahti'
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'A': [
          {
            'trainNumber': 8171,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'A',
            'timetable': [
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T13:58:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T13:58:00.000Z',
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'st op_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:08:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:18:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:28:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:38:00.000Z ',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:48:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:58:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:08:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:18:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:28:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:38:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ],
        'I': [
          {
            'trainNumber': 8933,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'I',
            'timetable': [
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:03:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T14:03:04.000Z',
                'commercialTrack': '10',
                'trainStopping': True,
                'cause ': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:13:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T14:13:04.000Z',
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:23:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T14:23:05.000Z',
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:33:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T14:33:36.000Z',
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:43:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T14:43:04.000Z',
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:53:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:03:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:13:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTr ack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:23:00.000Z',
                'differenceInMinutes': None,
                'liveEstimat eTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:33:00.000Z',
                'differenceInM inutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:43:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:53:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:03:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:33:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:13:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:23:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'tra inStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:43:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'A': [
          {
            'trainNumber': 8171,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'A',
            'timetable': [
              {
                'destination': 'Leppävaara',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T13:57:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T13:57:22.000Z',
                'commercialTrack': '11',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              },
              {
                'destination': 'Leppävaara',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:07:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '11',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              },
              {
                'destination': 'Leppävaara',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:17:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '11',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              },
              {
                'destination': 'Leppävaara',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:27:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '11',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              },
              {
                'destination': 'Leppävaara',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:37:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '11',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              },
              {
                'destination': 'Leppävaara',
                'type': 'DEP ARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:47:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '11',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'He lsinki Kivihaka',
                  'Huopalahti'
                ]
              },
              {
                'destination': 'Leppävaara',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:57:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '11',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              },
              {
                'destination': 'Leppävaara',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:07:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '11',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              },
              {
                'destination': 'Leppävaara',
                'type': 'DEPARTU RE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:37:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '11',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsin ki Kivihaka',
                  'Huopalahti'
                ]
              }
            ]
          }
        ],
        'P': [
          {
            'trainNumber': 8711,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'P',
            'timetable': [
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:56:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelle d': False,
                'scheduledTime': '2023-04-03T15:06:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'typ e': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:16:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destin ation': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:26:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_o n_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:36:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:46:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:56:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime ': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:06:00.000Z',
                'differenceInMinutes ': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:16:00.0 00Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:26:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancel led': False,
                'scheduledTime': '2023-04-03T16:36:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:46:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'E': [
          {
            'trainNumber': 8371,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'E',
            'timetable': [
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T13:59:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T13:59:12.000Z',
                'commercialTrack': '9',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Hel sinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:29:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '9',
                'trainStopping': True,
                'cause': None,
                'stop_on_statio ns': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:59:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '9',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:29:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '9',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ],
        'U': [
          {
            'trainNumber': 8489,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'U',
            'timetable': [
              {
                'destination': 'Helsinki asema',
                'type': 'DEP ARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:13:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T14:13:12.000Z',
                'commercialTrack': '9',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:43:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '9',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:13:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '9',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:43:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '9',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ],
        'Y': [
          {
            'trainNumber': 8581,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'Y',
            'timetable': [
              {
                'destination': 'Helsin ki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:04:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T14:04:12.000Z',
                'commercialTrack': '9',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:04:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '9',
                'trainS topping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'E': [
          {
            'trainNumber': 8371,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'E',
            'timetable': [
              {
                'destination': 'Kauklahti asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:01:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '8',
                'trainStopping': True,
                'cause': None,
                ' stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              },
              {
                'destination': 'Kauklahti asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:31:00.000Z',
                'differenceInMinutes': None,
                'liveEsti mateTime': None,
                'commercialTrack': '8',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              },
              {
                'destination': 'Kauklahti asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:01:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '8',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              },
              {
                'destination': 'Kauklahti asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:31:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '8',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              }
            ]
          }
        ],
        'U': [
          {
            'trainNumber': 8489,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'U',
            'timetable': [
              {
                'destination': 'Kirkkonummi',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:16:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '8',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asem a',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              },
              {
                'destination': 'Kirkkonummi',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:46:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '8',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              },
              {
                'destination': 'Kirkkonummi',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:16:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '8',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              },
              {
                'destination': 'Kirkkonummi',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:46:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '8',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              }
            ]
          }
        ],
        'Y': [
          {
            'trainNumber': 8581,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'Y',
            'timetable': [
              {
                'destination': 'Siuntio',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:27:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '8',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Ilmala asema',
                  'Helsinki Kivihaka',
                  'Huopalahti'
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'P': [
          {
            'trainNumber': 8711,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'P',
            'timetable': [
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T13:56:00.000Z',
                'differenceInMinutes': 2,
                'liveEstimateTime': '2023-04-03T13:58:01.000Z',
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Hels inki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:06:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T14:06:06.000Z',
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:16:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T14:16:06.000Z',
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:26:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimate Time': '2023-04-03T14:26:06.000Z',
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:36:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T14:36:06.000Z',
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:46:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T14:46:06.000Z',
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Len toasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:56:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:06:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:16:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:26:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:36:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:46:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:56:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:06:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPAR TURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:16:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'L entoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:26:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations ': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:36:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause ': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:46:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ],
        'K': [
          {
            'trainNumber': 9357,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'K',
            'timetable': [
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:01:00.000Z',
                'differenceInMinutes': 2,
                'liveEstimateTime': '2023-04-03T14:03:38.000Z',
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'desti nation': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:11:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T14:11:06.000Z',
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:21:00.000Z',
                'differenceInMinutes': 1,
                'liveEstimateTime': '2023-04-03T14:22:51.000 Z',
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:31:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:41:0 0.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:51:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTUR E',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:01:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Hels inki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:11:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_station s': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:21:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                ' cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:31:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:41:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:51:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '1',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'I': [
          {
            'trainNumber': 8933,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'I',
            'timetable': [
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:53:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:03:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:13:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:23:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:33:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:43:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:53:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                's top_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:03:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:33:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercial Track': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:13:00.000Z',
                'differenceInMinutes': None,
                'liveEstim ateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:23:00.000Z',
                'differenceI nMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Lentoasema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T16:43:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '10',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ],
        'K': [
          {
            'trainNumber': 9357,
            'trainType': 'HL',
            'trainCategory': 'Commut er',
            'commuterLineID': 'K',
            'timetable': [
              {
                'destination': 'Kerava asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:05:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '2',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              },
              {
                'destination': 'Kerava asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:15:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '2',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              },
              {
                'destination': 'Kerava asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:25:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '2',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              },
              {
                'destination': 'Kerava asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:35:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '2',
                'trainStopping': True,
                'cause': None,
                ' stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              },
              {
                'destination': 'Kerava asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:45:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '2',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              },
              {
                'destination': 'Kerava asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:55:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '2',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              },
              {
                'destination': 'Kerava asema',
                'type': 'DEPARTURE ',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:05:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '2',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pu kinmäki'
                ]
              },
              {
                'destination': 'Kerava asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:15:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '2',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              },
              {
                'destination': 'Kerava asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:35:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '2',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              },
              {
                'destination': 'Kerava asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:45:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '2',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              },
              {
                'destination': 'Kerava asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:25:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '2',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              },
              {
                'destination': 'Kerava asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:55:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '2',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'R': [
          {
            'trainNumber': 9711,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'R',
            'timetable': [
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:14:00.000Z',
                'differenceInMinutes': 1,
                'liveEstimateTime': '2023-04-03T14:15:26.000Z',
                'commercialTrack': '5',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:44:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '5',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:14:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '5',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:44:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T15:44:09.000Z',
                'commercialTrack': '5',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'R': [
          {
            'trainNumber': 9711,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'R',
            'timetable': [
              {
                'destination': 'Tampere asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:15:0 0.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '3',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              },
              {
                'destination': 'Riihimäki asema',
                'type': 'DEP ARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:45:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '3',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä ',
                  'Pukinmäki'
                ]
              },
              {
                'destination': 'Riihimäki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:15:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '3',
                'trainStopping ': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              },
              {
                'destination': 'Riihimäki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:45:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '3',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'Z': [
          {
            'trainNumber': 9863,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'Z',
            'timetable': [
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:19:00.000Z',
                'differenceInMinutes': 0,
                'liveEstimateTime': '2023-04-03T14:19:09.000Z',
                'commercialTrack': '6',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              },
              {
                'destination': 'Helsinki asema',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:19:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '6',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    'stationFullname': 'Pasila asema',
    'schedule': [
      {
        'Z': [
          {
            'trainNumber': 9863,
            'trainType': 'HL',
            'trainCategory': 'Commuter',
            'commuterLineID': 'Z',
            'timetable': [
              {
                'destination': 'Lahti',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T14:40:00.000Z',
                'differenceInMinutes ': None,
                'liveEstimateTime': None,
                'commercialTrack': '4',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              },
              {
                'destination': 'Lahti',
                'type': 'DEPARTURE',
                'cancelled': False,
                'scheduledTime': '2023-04-03T15:40:00.000Z',
                'differenceInMinutes': None,
                'liveEstimateTime': None,
                'commercialTrack': '4',
                'trainStopping': True,
                'cause': None,
                'stop_on_stations': [
                  'Käpylä',
                  'Oulunkylä',
                  'Pukinmäki'
                ]
              }
            ]
          }
        ]
      }
    ]
  }
]






if __name__ == "__main__":
    
    root = Trees.TupledBST(lambda x, y : (
        
    ) )
    
  
    for item in data:
        #print(item)
        print()
        for t in item["schedule"]:
            for train, schedule in t.items():
                #print(train)
                #print(schedule)
                print()
                for tr in schedule:
                    #print(tr["timetable"])
                    for timetable in tr["timetable"]:
                       # print(train)
                        #print(timetable)
                        #print(timetable["scheduledTime"])
                        print()
                        
                        timetable["id"] =  tr["trainNumber"]
                        
                        root.insert((timetable["scheduledTime"],  tr["trainNumber"]), timetable)
                        
                        
    x = root.get_sorted_data(lambda x: (
       True
    ), lambda x : x["scheduledTime"])
    
    
    print(x)    
                        

               
        
               
    
    
    
    pass