from threading import Lock

class RoomBookingSystem:
    def __init__(self):
        self.availableRooms = {} # meeting room objects
        self.lock = Lock()
        self.users = {1: UserFactory().createUser("root", 1, "admin")}

    def search(self, minCapacity, timeSlot):
        results = []

        for roomId in self.availableRooms:
            room = self.getRoomById(roomId)
            if room.capacity >= minCapacity:
                if room.checkAvailability(timeSlot):
                    results.append(room)
        return results

    def addRoom(self, user, roomId, roomName, capacity):
        if user.permissionLevel < 2:
            return "not enough permsision"

        room = MeetingRoom(roomId, roomName, capacity)
        self.lock.acquire()
        self.availableRooms[roomId] = room
        self.lock.release()
        return "done"

    def addUser(self, user, employeeId, userName, permissionLevel):
        if user.permissionLevel < 2:
            return "not enough permission"

        userObejct = User(userName, employeeId, permissionLevel)
        self.lock.acquire()
        self.users[employeeId] = userObejct
        self.lock.release()

    def removeRoom(self, user, roomId):
        if user.permissionLevel < 2:
            return "not enough permissions"
        room = self.getRoomById(roomId)
        del room
        self.lock.acquire()
        del self.availableRooms[roomId]
        self.lock.release()

    def getRoomById(self, roomId):
        result = None
        self.lock.acquire()
        if roomId in self.availableRooms:
            result = self.availableRooms[roomId]
        self.lock.release()
        return result

    def bookRoom(self, roomId, fromTime, toTime):
        room = self.getRoomById(roomId)
        timeSlot = TimeSlot(fromTime, toTime)
        return room.bookRoom(timeSlot)

    def changeRoomCapacity(self, user, roomId, newCapacity):
        if user.permissionLevel < 2:
            return "not enough permsision"
        room = self.getRoomById(roomId)
        if room == None:
            return "room doesnt exist"
        room.changeCapacity = newCapacity

    def mainInterface(self):
        root = self.users[1]
        for i in range(2):
            self.addRoom(root, i, "cara {}".format(i), 3)
        for i in range(2, 5):
            self.addRoom(root, i, "zor {}".format(i), 5)

        results = self.search(3, timeSlot=TimeSlot(5, 15))
        for res in results:
            print(res.roomId, res.roomName, res.capacity, res.availability)

        print(self.bookRoom(2, 5, 15))
        results = self.search(3, timeSlot=TimeSlot(10, 20))
        for res in results:
            print(res.roomId, res.roomName, res.capacity, res.availability)



class MeetingRoom:
    def __init__(self, roomId, roomName, capacity):
        self.roomId = roomId
        self.roomName = roomName
        self.capacity = capacity
        self.availability = {i:True for i in range(48)} # 30 minute time slots in a 24 hour clock
        self.seats = [Seating("featherlite")] * self.capacity
        self.lock = Lock()

    def checkAvailability(self, timeSlot):
        isAvailable = True
        for time in range(timeSlot.fromTime, timeSlot.toTime + 1):
            if not self.availability[time]:
                isAvailable = False
        return isAvailable

    def changeCapacity(self, capacity):
        self.lock.acquire()
        self.capacity = capacity
        self.lock.release()

    def bookRoom(self, timeSlot):
        self.lock.acquire()
        isAvailable = self.checkAvailability(timeSlot)
        if not isAvailable:
            self.lock.release()
            return "unavailable"
        for time in range(timeSlot.fromTime, timeSlot.toTime + 1):
            self.availability[time] = False
        self.lock.release()
        return "booked"




class Seating:
    def __init__(self, brand):
        self.seatingBrand = brand

class Hardware:
    def __init__(self):
        pass

class TimeSlot:
    def __init__(self, fromTime, toTime):
        self.fromTime = fromTime
        self.toTime = toTime

class Booking:
    def __init__(self, meetingRoom, timeSlot):
        self.room = meetingRoom
        self.timeSlot = timeSlot

class User:
    def __init__(self, name, employeeId, permissionLevel=1):
        self.name = name
        self.employeeId = employeeId
        self.permissionLevel = permissionLevel

class UserFactory:
    def __init__(self):
        pass

    def createUser(self, name, employeeId, level="user"):
        if level == "user":
            return User(name, employeeId, permissionLevel=1)
        if level == "admin":
            return User(name, employeeId, permissionLevel=2)

if __name__ == "__main__":
    system = RoomBookingSystem()
    system.mainInterface()

