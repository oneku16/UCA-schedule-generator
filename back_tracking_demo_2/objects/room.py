from back_tracking_demo_2.objects.room_type import LectureRoom, LaboratoryRoom, SportRoom

def get_room(room_id, capacity, room_type, room_name):
    if room_type.lower() == 'laboratory':
        return LaboratoryRoom(room_id=room_id, capacity=capacity, room_name=room_name)
    elif room_type.lower == 'training':
        return SportRoom(room_id=room_id, capacity=capacity, room_name=room_name)
    return LectureRoom(room_id=room_id, capacity=capacity, room_name=room_name)
