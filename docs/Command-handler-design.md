# Command handler design

The commands modules consists of multiple commands and a command parser. The command parser is responsible for parsing the commands from the user. The command parser contains the list of commands that can be accessed by an anonymous/authenticated user.

```plantuml
@startuml

!theme spacelab
left to right direction
skinparam linetype polyline


abstract class Command {
   +is_valid_command(command: str) -> bool
   +parse(command: str) -> GameEngineEvent, dict
}

class ConnectCommand
class DirectionCommand
class HelpCommand
class LogoutCommand
class LookCommand
class RegisterCommand
class MoveCommand
class SayCommand

ConnectCommand --|> Command
DirectionCommand --|> Command
HelpCommand --|> Command
LogoutCommand --|> Command
LookCommand --|> Command
RegisterCommand --|> Command
SayCommand --|> Command
MoveCommand --|> Command

class CommandParser {
   +parse(command: str, is_user_authenticated : bool) -> GameEngineEvent, dict
   +get_commands(is_user_authenticated : bool) -> list
}

CommandParser "1" *-- "many" Command : contains
@enduml


@enduml
```
