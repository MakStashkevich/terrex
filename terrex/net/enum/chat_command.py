from enum import Enum


class ChatCommand(str, Enum):
    SayChat = "Say"
    Roll = "Roll"
    RockPaperScissors = "RPS"
    PVPDeath = "PVPDeath"
    PartyChat = "Party"
    ListPlayers = "Playing"
    Help = "Help"
    Emote = "Emote"
    Emoji = "Emoji"
    Death = "Death"
    BossDamage = "BossDamage"
    AllPVPDeath = "AllPVPDeath"
    AllDeath = "AllDeath"
