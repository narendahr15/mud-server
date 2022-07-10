# Game profile design

All the game profiles derive from the base class Profile which is inherited from the Model class.

The PlayerProfile class is the profile of the player. The PlayerProfile class is responsible for storing the player's room id. It has one to one association with the User class.

Can be extended to store the player's inventory, room data, etc.

```plantuml
@startuml

!theme plain
left to right direction
skinparam linetype ortho

class Model
class User

class Profile {
    location:int
}

class PlayerProfile {
    user:User
    name:str
    is_authenticated: bool
}

Profile --> Model
PlayerProfile --|> Profile
PlayerProfile ||-- User
@enduml
```
