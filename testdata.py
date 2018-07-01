test1 = {
   "hotel": [
      {
         "id": "abc",
         "foods": [
            {
               "id": "123",
               "name": "food1"
            }
         ]
      }
   ]
}
sol1 = {'hotel': [{'id': 'abc'}], 'hotel_food': [{'id': ['abc', '123'], 'name': 'food1'}]}

test2 = {
    "donuts": [
        {
            "batter": {
                "types": [
                    {
                        "type": "Regular"
                    },
                    {
                        "type": "Chocolate"
                    },
                    {
                        "type": "Blueberry"
                    },
                    {
                        "type": "Devil's Food"
                    }
                ]
            },
            "calories": 550,
            "id": "1",
            "name": "chocolate frosted",
            "toppings": [
                {
                    "type": "None"
                },
                {
                    "type": "Glazed"
                },
                {
                    "type": "Sugar"
                },
                {
                    "type": "Powdered Sugar"
                },
                {
                    "type": "Chocolate with Sprinkles"
                },
                {
                    "type": "Chocolate"
                },
                {
                    "type": "Maple"
                }
            ],
            "type": "donut"
        }
    ]
}
sol2 ={
   "donut": [
      {
         "id": "1",
         "calories": 550,
         "name": "chocolate frosted",
         "type": "donut"
      }
   ],
   "donut_batter": [
      {
         "id": "1"
      }
   ],
   "donut_batter_type": [
      {
         "id": "1",
         "__index": '0',
         "type": "Regular"
      },
      {
         "id": "1",
         "__index": '1',
         "type": "Chocolate"
      },
      {
         "id": "1",
         "__index": '2',
         "type": "Blueberry"
      },
      {
         "id": "1",
         "__index": '3',
         "type": "Devil's Food"
      }
   ],
   "donut_topping": [
      {
         "id": "1",
         "__index": '0',
         "type": "None"
      },
      {
         "id": "1",
         "__index": '1',
         "type": "Glazed"
      },
      {
         "id": "1",
         "__index": '2',
         "type": "Sugar"
      },
      {
         "id": "1",
         "__index": '3',
         "type": "Powdered Sugar"
      },
      {
         "id": "1",
         "__index": '4',
         "type": "Chocolate with Sprinkles"
      },
      {
         "id": "1",
         "__index": '5',
         "type": "Chocolate"
      },
      {
         "id": "1",
         "__index": '6',
         "type": "Maple"
      }
   ]
}

test3 = {
    "accounts": [
        {
            "id": "1",
            "account_number": "ABC15797531",
            "description": "Industrial Cleaning Supply Company",
            "name": "Xytrex Co."
        }
    ]
}

sol3 = {
   "account": [
      {
         "id": "1",
         "account_number": "ABC15797531",
         "description": "Industrial Cleaning Supply Company",
         "name": "Xytrex Co."
      }
   ]
}
