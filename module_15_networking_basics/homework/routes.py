import json
from typing import List

from flask import Flask, request, Response

from models import init_db, insert_room, get_all_rooms, get_rooms, get_room_from_db, update_room, Room


app: Flask = Flask(__name__)


@app.route('/add-room', methods=['POST'])
def add_room() -> Response:
    data = json.loads(request.data)
    insert_room(data['floor'], data['beds'], data['guestNum'], data['price'])
    return Response(status=200)


@app.route('/room', methods=['GET'])
def get_room() -> str:
    if request.args:
        check_in = request.args.get('checkIn')
        check_out = request.args.get('checkOut')
        guest_num = int(request.args.get('guestsNum'))
        check_in = '{}-{}-{}'.format(check_in[:4], check_in[4:6], check_in[6:])
        check_out = '{}-{}-{}'.format(check_out[:4], check_out[4:6], check_out[6:])
        rooms: List[Room] = get_rooms(guest_num, check_in, check_out)
    else:
        rooms = get_all_rooms()
    return json.dumps({
        "rooms": [
            {
                "roomId": room.id,
                "floor": room.floor,
                "guestNum": room.guest_num,
                "beds": room.beds,
                "price": room.price
            }
            for room in rooms]
    })


@app.route('/booking', methods=['POST'])
def booking() -> Response:
    data = json.loads(request.data)

    check_in = '{}-{}-{}'.format(str(data['bookingDates']['checkIn'])[:4],
                                 str(data['bookingDates']['checkIn'])[4:6],
                                 str(data['bookingDates']['checkIn'])[6:])

    check_out = '{}-{}-{}'.format(str(data['bookingDates']['checkOut'])[:4],
                                  str(data['bookingDates']['checkOut'])[4:6],
                                  str(data['bookingDates']['checkOut'])[6:])

    room: Room = get_room_from_db(data['roomId'])
    if not room.lastname:
        update_room(check_in, check_out, data['firstName'], data['lastName'], data['roomId'])
        return Response(status=200)
    return Response(status=409)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
