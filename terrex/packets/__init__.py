# base
from .achievement_message_event_happened import AchievementMessageEventHappened
from .achievement_message_npc_killed import AchievementMessageNPCKilled
from .add_npc_buff import AddNPCBuff
from .add_player_buff_pvp import AddPlayerBuffPvP
from .angler_quest import AnglerQuest
from .angler_quest_finished import AnglerQuestFinished
from .area_tile_change import AreaTileChange
from .base import Packet, packet_registry
from .bug_catching import BugCatching
from .bug_releasing import BugReleasing
from .chest_name import ChestName
from .chest_updates import ChestUpdates
from .client_synced_inventory import ClientSyncedInventory
from .combat_text_int import CombatTextInt
from .combat_text_string import CombatTextString
from .crystal_invasion_send_wait_time import CrystalInvasionSendWaitTime
from .crystal_invasion_start import CrystalInvasionStart
from .crystal_invasion_wipe_all_the_thingsss import CrystalInvasionWipeAllTheThingsss
from .damage_npc import DamageNPC
from .dead_player import DeadPlayer

# social handshake 93
from .dev_commands import DevCommands
from .emoji import Emoji
from .finished_connecting_to_server import FinishedConnectingToServer
from .fish_out_npc import FishOutNpc
from .food_platter_try_placing import FoodPlatterTryPlacing
from .gem_lock_toggle import GemLockToggle

# packet ids
# packets
from .hello import Hello
from .hit_switch import HitSwitch
from .initial_spawn import InitialSpawn
from .instrument_sound import InstrumentSound
from .invasion_progress_report import InvasionProgressReport
from .item_frame_try_placing import ItemFrameTryPlacing
from .item_owner import ItemOwner
from .item_rotation_and_animation import ItemRotationAndAnimation
from .item_tweaker import ItemTweaker
from .kick import Kick
from .kill_projectile import KillProjectile
from .land_golf_ball_in_cup import LandGolfBallInCup
from .liquid_update import LiquidUpdate
from .lock_and_unlock import LockAndUnlock
from .mana_effect import ManaEffect
from .mass_wire_operation import MassWireOperation
from .mass_wire_operation_pay import MassWireOperationPay
from .minion_attack_target_update import MinionAttackTargetUpdate
from .minion_rest_target_update import MinionRestTargetUpdate
from .moonlord_horror import MoonlordHorror
from .murder_someone_elses_portal import MurderSomeoneElsesPortal
from .nebula_levelup_request import NebulaLevelupRequest
from .net_modules import NetModules
from .npc_buffs import NPCBuffs
from .open_sign_request import OpenSignRequest
from .open_sign_response import OpenSignResponse

# GetItemUsedLuckyCoin (ClientPacket) 148
# null 149
# SetOrRequestSpectating (SyncPacket) 150
# PickAnItemSlotToSpawnItemOn (ServerPacket) 0-400 151
# PlayerUseSoundSync (SyncPacket???) 152
# NPC ApplyEelWhipDoT (ServerPacket) 153
from .ping import Ping
from .place_object import PlaceObject
from .play_legacy_sound import PlayLegacySound
from .player_active import PlayerActive
from .player_buffs import PlayerBuffs
from .player_controls import PlayerControls
from .player_death_v2 import PlayerDeathV2
from .player_dodge import PlayerDodge
from .player_heal import PlayerHeal
from .player_hurt_v2 import PlayerHurtV2
from .player_info import PlayerInfo
from .player_life_mana import PlayerLifeMana
from .player_mana import PlayerMana
from .player_spawn import PlayerSpawn
from .player_stealth import PlayerStealth
from .poof_of_smoke import PoofOfSmoke
from .quests_count_sync import QuestsCountSync
from .quick_stack_chests import QuickStackChests
from .release_item_ownership import ReleaseItemOwnership
from .remove_revenge_marker import RemoveRevengeMarker
from .request_chest_open import RequestChestOpen
from .request_npc_buff_removal import RequestNPCBuffRemoval
from .request_password import RequestPassword
from .request_teleportation_by_server import RequestTeleportationByServer
from .request_tile_entity_interaction import RequestTileEntityInteraction
from .request_world_data import RequestWorldData
from .send_password import SendPassword
from .set_counts_as_host_for_gameplay import SetCountsAsHostForGameplay
from .set_time import SetTime
from .shop_override import ShopOverride
from .smart_text_message import SmartTextMessage
from .spawn_boss_use_license_start_event import SpawnBossUseLicenseStartEvent
from .spawn_tile_data import SpawnTileData
from .special_fx import SpecialFX
from .status_text_size import StatusTextSize
from .sync_cavern_monster_type import SyncCavernMonsterType
from .sync_chest_item import SyncChestItem

# from .InstancedItem import InstancedItem
from .sync_emote_bubble import SyncEmoteBubble
from .sync_equipment import SyncEquipment
from .sync_extra_value import SyncExtraValue
from .sync_item import SyncItem

# SetMiscEventValues 140
# todo: add all new packets from 1.4.5.0+
# ------
# LucyAxeMove (ClientPacket) 141
# Unknown update data for player (ClientPacket) 142
# AttemptToSkipWaitTime for player (ClientPacket) 143
# HaveDryadDoStardewAnimation for NPC (SyncPacket???) 144
# NPC ShimmerTransformToItem (ServerPacket?) 145
# NPC ShimmerTransformToNPC (ServerPacket?) 146
from .sync_loadout import SyncLoadout
from .sync_npc import SyncNPC
from .sync_player import SyncPlayer
from .sync_player_chest import SyncPlayerChest
from .sync_player_chest_index import SyncPlayerChestIndex
from .sync_player_zone import SyncPlayerZone

# null 25
# null 26
from .sync_projectile import SyncProjectile
from .sync_revenge_marker import SyncRevengeMarker
from .sync_talk_npc import SyncTalkNPC
from .sync_tile_paint_or_coating import SyncTilePaintOrCoating
from .sync_tile_picking import SyncTilePicking
from .sync_wall_paint_or_coating import SyncWallPaintOrCoating
from .tamper_with_npc import TamperWithNPC
from .te_display_doll_data_sync import TEDisplayDollDataSync
from .te_hat_rack_item_sync import TEHatRackItemSync

# null 44
from .team_change import TeamChange
from .teleport_entity import TeleportEntity
from .teleport_npc_through_portal import TeleportNPCThroughPortal
from .teleport_player_through_portal import TeleportPlayerThroughPortal
from .temporary_animation import TemporaryAnimation
from .tile_entity_placement import TileEntityPlacement
from .tile_entity_sharing import TileEntitySharing
from .tile_frame_section import TileFrameSection
from .tile_manipulation import TileManipulation
from .tile_section import TileSection
from .toggle_door_state import ToggleDoorState
from .toggle_party import ToggleParty
from .toggle_pvp import TogglePvp
from .travel_merchant_items import TravelMerchantItems
from .unique_town_npc_info_sync_request import UniqueTownNPCInfoSyncRequest
from .unknown15 import Unknown15  # null 15
from .unknown57 import Unknown57
from .unknown60 import Unknown60
from .unknown66 import Unknown66
from .unknown67 import Unknown67  # null on official server, but may be used on TShock
from .unknown68 import Unknown68
from .unused83 import Unused83
from .unused_melee_strike import UnusedMeleeStrike
from .update_player_luck_factors import UpdatePlayerLuckFactors
from .update_tower_shield_strengths import UpdateTowerShieldStrengths
from .weapons_rack_try_placing import WeaponsRackTryPlacing
from .wired_cannon_shot import WiredCannonShot
from .world_data import WorldData

# SendMaxChestItems (ServerPacket) 155
# DebugPlaceTileEntityKiteAnchorItem (ServerPacket???) (156
# UpdatePlayerTeam (SyncPacket) 157
# null 158
# Control Check Rope Usability (ClientPacket) 159
# SyncItemOnSection (ServerPacket???) 160
