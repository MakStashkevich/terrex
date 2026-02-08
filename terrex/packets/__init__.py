# base
from .base import Packet, registry
# packet ids
from .packet_ids import PacketIds

# packets
from .connect import Connect
from .disconnect import Disconnect
from .set_user_slot import SetUserSlot
from .player_info import PlayerInfo
from .player_inventory_slot import PlayerInventorySlot
from .request_world_data import RequestWorldData
from .world_info import WorldInfo
from .request_essential_tiles import RequestEssentialTiles
from .status import Status
from .send_section import PacketSendSection
from .section_tile_frame import SectionTileFrame
from .spawn_player import SpawnPlayer
from .update_player import UpdatePlayer
from .player_active import PlayerActive
from .packet15 import Packet15 # null 15
from .player_hp import PlayerHp
from .modify_tile import ModifyTile
from .time import Time
from .door_toggle import DoorToggle
from .send_tile_square import SendTileSquare
# update item drop 21 (deprecated)
from .update_item_owner import UpdateItemOwner
from .npc_update import NpcUpdate
from .strike_npc import StrikeNpc
# null 25
# null 26
from .projectile_update import ProjectileUpdate
from .npc_strike import NpcStrike
from .destroy_projectile import DestroyProjectile
from .toggle_pvp import TogglePvp
from .open_chest import OpenChest
from .update_chest_item import UpdateChestItem
from .sync_active_chest import SyncActiveChest
from .place_chest import PlaceChest
from .heal_effect import HealEffect
from .player_zone import PlayerZone
from .request_password import RequestPassword
from .send_password import SendPassword
from .remove_item_owner import RemoveItemOwner
from .set_active_npc import SetActiveNpc
from .player_item_animation import PlayerItemAnimation
from .player_mana import PlayerMana
from .mana_effect import ManaEffect
# null 44
from .player_team import PlayerTeam
from .request_sign import RequestSign
from .update_sign import UpdateSign
from .set_liquid import SetLiquid
from .complete_connection_and_spawn import CompleteConnectionAndSpawn
from .update_player_buff import UpdatePlayerBuff
from .special_npc_effect import SpecialNpcEffect
from .unlock import Unlock
from .add_npc_buff import AddNpcBuff
from .update_npc_buff import UpdateNpcBuff
from .add_player_buff import AddPlayerBuff
from .update_npc_name import UpdateNpcName
from .update_good_evil import UpdateGoodEvil
from .play_music_item import PlayMusicItem
from .hit_switch import PacketHitSwitch
from .set_npc_home import PacketSetNpcHome
from .spawn_boss_invasion import SpawnBossInvasion
from .player_dodge import PlayerDodge
from .paint_tile import PaintTile
from .paint_wall import PaintWall
from .player_npc_teleport import PlayerNpcTeleport
from .heal_other_player import HealOtherPlayer
from .placeholder import Placeholder # null on official server, but may be used on TShock
from .client_uuid import ClientUuid
from .get_chest_name import GetChestName
from .catch_npc import CatchNpc
from .release_npc import ReleaseNpc
from .travelling_merchant_inventory import TravellingMerchantInventory
from .teleportation_potion import TeleportationPotion
from .angler_quest import AnglerQuest
from .complete_angler_quest import CompleteAnglerQuest
from .angler_quests import AnglerQuests
from .create_temporary_animation import CreateTemporaryAnimation
from .invasion_progress import InvasionProgress
from .place_object import PlaceObject
from .sync_player_chest_index import SyncPlayerChestIndex
from .create_combat_text import CreateCombatText
from .load_net_module import LoadNetModule
from .set_npc_kill_count import SetNpcKillCount
from .set_player_stealth import SetPlayerStealth
from .force_item_nearest_chest import ForceItemNearestChest
from .update_tile_entity import UpdateTileEntity
from .place_tile_entity import PlaceTileEntity
from .tweak_item import TweakItem
from .place_item_frame import PlaceItemFrame
from .update_item_drop2 import UpdateItemDrop2
from .sync_emote_bubble import SyncEmoteBubble
from .sync_extra_value import SyncExtraValue
# social handshake 93
from .packet94 import Packet94
from .kill_portal import KillPortal
from .player_teleport_portal import PlayerTeleportPortal
from .notify_player_npc_killed import NotifyPlayerNpcKilled
from .notify_player_of_event import NotifyPlayerOfEvent
from .set_minion_target import SetMinionTarget
from .npc_teleport_portal import NpcTeleportPortal
from .update_shield_strengths import UpdateShieldStrengths
from .nebula_level_up import NebulaLevelUp
from .moon_lord_countdown import MoonLordCountdown
from .npc_shop_item import NpcShopItem
from .gem_lock_toggle import GemLockToggle
from .poof_of_smoke import PoofOfSmoke
from .smart_text_message import SmartTextMessage
from .wired_cannon_shot import WiredCannonShot
from .mass_wire import MassWire
from .mass_consume_wire import MassConsumeWire
from .toggle_birthday_party import ToggleBirthdayParty
from .grow_fx import GrowFx
from .crystal_invasion_start import CrystalInvasionStart
from .crystal_invasion_wipe import CrystalInvasionWipe
from .minion_attack_target_update import MinionAttackTargetUpdate
from .crystal_invasion_wait import CrystalInvasionWait
from .player_hurt import PlayerHurt
from .player_death import PlayerDeath
from .combat_text import CombatText
from .emoji import Emoji
from .doll_sync import DollSync
from .interact_tile_entity import InteractTileEntity
from .place_weapon_rack import PlaceWeaponRack
from .hat_rack_sync import HatRackSync
from .sync_tile_picking import SyncTilePicking
from .sync_revenge_marker import SyncRevengeMarker
from .remove_revenge_marker import RemoveRevengeMarker
from .land_golf_ball import LandGolfBall
from .connection_complete import ConnectionComplete
from .fish_out_npc import FishOutNpc
from .tamper_with_npc import TamperWithNpc
from .play_legacy_sound import PlayLegacySound
from .place_food import PlaceFood
from .update_player_luck import UpdatePlayerLuck
from .dead_player import DeadPlayer
from .sync_cavern_monster_type import SyncCavernMonsterType
from .request_npc_debuff import RequestNpcDebuff
from .client_synced_inventory import ClientSyncedInventory
from .set_as_host import SetAsHost
# set misc event values 140


# todo: add all new packets from 1.4.5.0+
# ------
# LucyAxeMove (ClientPacket) 141
# Unknown update data for player (ClientPacket) 142
# AttemptToSkipWaitTime for player (ClientPacket) 143
# HaveDryadDoStardewAnimation for NPC (SyncPacket???) 144
# NPC ShimmerTransformToItem (ServerPacket?) 145
# NPC ShimmerTransformToNPC (ServerPacket?) 146
from .update_player_loadout import UpdatePlayerLoadout
# GetItemUsedLuckyCoin (ClientPacket) 148
# null 149
# SetOrRequestSpectating (SyncPacket) 150
# PickAnItemSlotToSpawnItemOn (ServerPacket) 0-400 151
# PlayerUseSoundSync (SyncPacket???) 152
# NPC ApplyEelWhipDoT (ServerPacket) 153
from .ping import Ping
# SendMaxChestItems (ServerPacket) 155
# DebugPlaceTileEntityKiteAnchorItem (ServerPacket???) (156
# UpdatePlayerTeam (SyncPacket) 157
# null 158
# Control Check Rope Usability (ClientPacket) 159
# SyncItemOnSection (ServerPacket???) 160