import re
from flask import Blueprint, request, jsonify
from models import db, Reservation
from middlewares.auth_middleware import auth_required
from datetime import datetime

reservation_bp = Blueprint('reservation', __name__, url_prefix='/api/reservation')

@reservation_bp.route('', methods=['GET'])
@auth_required
def get_reservations():
    user_id = request.user_id
    reservations = Reservation.query.filter_by(user_id=user_id).all()

    result = []
    for r in reservations:
        result.append({
            "id": r.id,
            "date": r.date,
            "room": r.room,
            "hour": r.hour
        })

    return jsonify(result)


@reservation_bp.route('', methods=['POST'])
@auth_required
def create_reservation():
    data = request.json

    date = data.get('date')
    room = data.get('room')
    hour = data.get('hour')

    if not date or not room or not hour:
        return jsonify({
            "message": "Los campos 'fecha', 'sala' y 'hora' son obligatorios"
        }), 400

    try:
        datetime.strptime(date, "%d/%m/%Y")
    except ValueError:
        return jsonify({
            "message": "Formato de fecha inválido. Use DD/MM/YYYY"
        }), 400
    
    hour_format = r"^(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$"
    if not re.match(hour_format, hour):
        return jsonify({
            "message": "Formato de hora inválido. Use HH:MM AM/PM (ej: 09:30 AM)"
        }), 400
    
    valid_rooms = ['A', 'B', 'C']
    if room not in valid_rooms:
        return jsonify({
            "message": f"Sala inválida. Solo se permiten: {', '.join(valid_rooms)}"
        }), 400

    reservation = Reservation(
        date=date,
        room=room,
        hour=hour,
        user_id=request.user_id
    )

    db.session.add(reservation)
    db.session.commit()

    return jsonify({"message": "Reserva creada"}), 201


@reservation_bp.route('/<uuid:id>', methods=['DELETE'])
@auth_required
def delete_reservation(id):
    reservation = Reservation.query.get(id)

    if not reservation:
        return jsonify({"message": "No se pudo encontrar la reserva"}), 404

    if reservation.user_id != request.user_id:
        return jsonify({"message": "No está autorizado para eliminar esta reserva"}), 403

    db.session.delete(reservation)
    db.session.commit()

    return jsonify({"message": "Reserva eliminada"})