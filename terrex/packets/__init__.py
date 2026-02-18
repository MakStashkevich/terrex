# fmt: off
# ruff: noqa

# base
from .base import Packet as Packet, packet_registry as packet_registry

# packets
from .hello import Hello as Hello
from .kick import Kick as Kick
from .player_info import PlayerInfo as PlayerInfo
from .sync_player import SyncPlayer as SyncPlayer
from .sync_equipment import SyncEquipment as SyncEquipment
from .request_world_data import RequestWorldData as RequestWorldData
from .world_data import WorldData as WorldData
from .spawn_tile_data import SpawnTileData as SpawnTileData
from .status_text_size import StatusTextSize as StatusTextSize
from .tile_section import TileSection as TileSection
from .tile_frame_section import TileFrameSection as TileFrameSection
from .player_spawn import PlayerSpawn as PlayerSpawn
from .player_controls import PlayerControls as PlayerControls
from .player_active import PlayerActive as PlayerActive
from .unknown15 import Unknown15 as Unknown15 # null 15
from .player_life_mana import PlayerLifeMana as PlayerLifeMana
from .tile_manipulation import TileManipulation as TileManipulation
from .set_time import SetTime as SetTime
from .toggle_door_state import ToggleDoorState as ToggleDoorState
from .area_tile_change import AreaTileChange as AreaTileChange
from .sync_item import SyncItem as SyncItem
from .item_owner import ItemOwner as ItemOwner
from .sync_npc import SyncNPC as SyncNPC
from .unused_melee_strike import UnusedMeleeStrike as UnusedMeleeStrike
# null 25
# null 26
from .sync_projectile import SyncProjectile as SyncProjectile
from .damage_npc import DamageNPC as DamageNPC
from .kill_projectile import KillProjectile as KillProjectile
from .toggle_pvp import TogglePvp as TogglePvp
from .request_chest_open import RequestChestOpen as RequestChestOpen
from .sync_chest_item import SyncChestItem as SyncChestItem
from .sync_player_chest import SyncPlayerChest as SyncPlayerChest
from .chest_updates import ChestUpdates as ChestUpdates
from .player_heal import PlayerHeal as PlayerHeal
from .sync_player_zone import SyncPlayerZone as SyncPlayerZone
from .request_password import RequestPassword as RequestPassword
from .send_password import SendPassword as SendPassword
from .release_item_ownership import ReleaseItemOwnership as ReleaseItemOwnership
from .sync_talk_npc import SyncTalkNPC as SyncTalkNPC
from .item_rotation_and_animation import ItemRotationAndAnimation as ItemRotationAndAnimation
from .player_mana import PlayerMana as PlayerMana
from .mana_effect import ManaEffect as ManaEffect
# null 44
from .team_change import TeamChange as TeamChange
from .open_sign_request import OpenSignRequest as OpenSignRequest
from .open_sign_response import OpenSignResponse as OpenSignResponse
from .liquid_update import LiquidUpdate as LiquidUpdate
from .initial_spawn import InitialSpawn as InitialSpawn
from .player_buffs import PlayerBuffs as PlayerBuffs
from .special_fx import SpecialFX as SpecialFX
from .lock_and_unlock import LockAndUnlock as LockAndUnlock
from .add_npc_buff import AddNPCBuff as AddNPCBuff
from .npc_buffs import NPCBuffs as NPCBuffs
from .add_player_buff_pvp import AddPlayerBuffPvP as AddPlayerBuffPvP
from .unique_town_npc_info_sync_request import UniqueTownNPCInfoSyncRequest as UniqueTownNPCInfoSyncRequest
from .update_good_evil import UpdateGoodEvil as UpdateGoodEvil
from .instrument_sound import InstrumentSound as InstrumentSound
from .hit_switch import HitSwitch as HitSwitch
from .update_home_npc import UpdateHomeNPC as UpdateHomeNPC
from .spawn_boss_use_license_start_event import SpawnBossUseLicenseStartEvent as SpawnBossUseLicenseStartEvent
from .player_dodge import PlayerDodge as PlayerDodge
from .sync_tile_paint_or_coating import SyncTilePaintOrCoating as SyncTilePaintOrCoating
from .sync_wall_paint_or_coating import SyncWallPaintOrCoating as SyncWallPaintOrCoating
from .teleport_entity import TeleportEntity as TeleportEntity
from .heal_other_player import HealOtherPlayer as HealOtherPlayer
from .tshock_placeholder import TShockPlaceholder as TShockPlaceholder # null on official server, but may be used on TShock
from .client_uuid import ClientUUID as ClientUUID
from .chest_name import ChestName as ChestName
from .bug_catching import BugCatching as BugCatching
from .bug_releasing import BugReleasing as BugReleasing
from .travel_merchant_items import TravelMerchantItems as TravelMerchantItems
from .request_teleportation_by_server import RequestTeleportationByServer as RequestTeleportationByServer
from .angler_quest import AnglerQuest as AnglerQuest
from .angler_quest_finished import AnglerQuestFinished as AnglerQuestFinished
from .quests_count_sync import QuestsCountSync as QuestsCountSync
from .temporary_animation import TemporaryAnimation as TemporaryAnimation
from .invasion_progress_report import InvasionProgressReport as InvasionProgressReport
from .place_object import PlaceObject as PlaceObject
from .sync_player_chest_index import SyncPlayerChestIndex as SyncPlayerChestIndex
from .combat_text_int import CombatTextInt as CombatTextInt
from .net_modules import NetModules as NetModules
from .unused83 import Unused83 as Unused83
from .player_stealth import PlayerStealth as PlayerStealth
from .quick_stack_chests import QuickStackChests as QuickStackChests
from .tile_entity_sharing import TileEntitySharing as TileEntitySharing
from .tile_entity_placement import TileEntityPlacement as TileEntityPlacement
from .item_tweaker import ItemTweaker as ItemTweaker
from .item_frame_try_placing import ItemFrameTryPlacing as ItemFrameTryPlacing
# from .InstancedItem import InstancedItem
from .sync_emote_bubble import SyncEmoteBubble as SyncEmoteBubble
from .sync_extra_value import SyncExtraValue as SyncExtraValue
# social handshake 93
from .dev_commands import DevCommands as DevCommands
from .murder_someone_elses_portal import MurderSomeoneElsesPortal as MurderSomeoneElsesPortal
from .teleport_player_through_portal import TeleportPlayerThroughPortal as TeleportPlayerThroughPortal
from .achievement_message_npc_killed import AchievementMessageNPCKilled as AchievementMessageNPCKilled
from .achievement_message_event_happened import AchievementMessageEventHappened as AchievementMessageEventHappened
from .minion_rest_target_update import MinionRestTargetUpdate as MinionRestTargetUpdate
from .teleport_npc_through_portal import TeleportNPCThroughPortal as TeleportNPCThroughPortal
from .update_tower_shield_strengths import UpdateTowerShieldStrengths as UpdateTowerShieldStrengths
from .nebula_levelup_request import NebulaLevelupRequest as NebulaLevelupRequest
from .moonlord_horror import MoonlordHorror as MoonlordHorror
from .shop_override import ShopOverride as ShopOverride
from .gem_lock_toggle import GemLockToggle as GemLockToggle
from .poof_of_smoke import PoofOfSmoke as PoofOfSmoke
from .smart_text_message import SmartTextMessage as SmartTextMessage
from .wired_cannon_shot import WiredCannonShot as WiredCannonShot
from .mass_wire_operation import MassWireOperation as MassWireOperation
from .mass_wire_operation_pay import MassWireOperationPay as MassWireOperationPay
from .toggle_party import ToggleParty as ToggleParty
from .special_fx import SpecialFX as SpecialFX
from .crystal_invasion_start import CrystalInvasionStart as CrystalInvasionStart
from .crystal_invasion_wipe_all_the_thingsss import CrystalInvasionWipeAllTheThingsss as CrystalInvasionWipeAllTheThingsss
from .minion_attack_target_update import MinionAttackTargetUpdate as MinionAttackTargetUpdate
from .crystal_invasion_send_wait_time import CrystalInvasionSendWaitTime as CrystalInvasionSendWaitTime
from .player_hurt_v2 import PlayerHurtV2 as PlayerHurtV2
from .player_death_v2 import PlayerDeathV2 as PlayerDeathV2
from .combat_text_string import CombatTextString as CombatTextString
from .emoji import Emoji as Emoji
from .te_display_doll_data_sync import TEDisplayDollDataSync as TEDisplayDollDataSync
from .request_tile_entity_interaction import RequestTileEntityInteraction as RequestTileEntityInteraction
from .weapons_rack_try_placing import WeaponsRackTryPlacing as WeaponsRackTryPlacing
from .te_hat_rack_item_sync import TEHatRackItemSync as TEHatRackItemSync
from .sync_tile_picking import SyncTilePicking as SyncTilePicking
from .sync_revenge_marker import SyncRevengeMarker as SyncRevengeMarker
from .remove_revenge_marker import RemoveRevengeMarker as RemoveRevengeMarker
from .land_golf_ball_in_cup import LandGolfBallInCup as LandGolfBallInCup
from .finished_connecting_to_server import FinishedConnectingToServer as FinishedConnectingToServer
from .fish_out_npc import FishOutNpc as FishOutNpc
from .tamper_with_npc import TamperWithNPC as TamperWithNPC
from .play_legacy_sound import PlayLegacySound as PlayLegacySound
from .food_platter_try_placing import FoodPlatterTryPlacing as FoodPlatterTryPlacing
from .update_player_luck_factors import UpdatePlayerLuckFactors as UpdatePlayerLuckFactors
from .dead_player import DeadPlayer as DeadPlayer
from .sync_cavern_monster_type import SyncCavernMonsterType as SyncCavernMonsterType
from .request_npc_buff_removal import RequestNPCBuffRemoval as RequestNPCBuffRemoval
from .client_synced_inventory import ClientSyncedInventory as ClientSyncedInventory
from .set_counts_as_host_for_gameplay import SetCountsAsHostForGameplay as SetCountsAsHostForGameplay
# SetMiscEventValues 140


# todo: add all new packets from 1.4.5.0+
# ------
# LucyAxeMove (ClientPacket) 141
# Unknown update data for player (ClientPacket) 142
# AttemptToSkipWaitTime for player (ClientPacket) 143
# HaveDryadDoStardewAnimation for NPC (SyncPacket???) 144
# NPC ShimmerTransformToItem (ServerPacket?) 145
# NPC ShimmerTransformToNPC (ServerPacket?) 146
from .sync_loadout import SyncLoadout as SyncLoadout
# GetItemUsedLuckyCoin (ClientPacket) 148
# null 149
# SetOrRequestSpectating (SyncPacket) 150
# PickAnItemSlotToSpawnItemOn (ServerPacket) 0-400 151
# PlayerUseSoundSync (SyncPacket???) 152
# NPC ApplyEelWhipDoT (ServerPacket) 153
from .ping import Ping as Ping
# SendMaxChestItems (ServerPacket) 155
# DebugPlaceTileEntityKiteAnchorItem (ServerPacket???) (156
# UpdatePlayerTeam (SyncPacket) 157
# null 158
# Control Check Rope Usability (ClientPacket) 159
# SyncItemOnSection (ServerPacket???) 160

# fmt: on
