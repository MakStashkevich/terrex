# Packets structure for the Terraria multiplayer game

All packages described here are implemented in Terrex through reverse engineering and proxy and are relevant for the latest version of Terraria.

The package names and their data types are as close as possible to the original ones. 

**Attention!** If you find outdated packages, let I know by [making a new general discussion](https://github.com/MakStashkevich/terrex/discussions/new?category=general) with label "bug" or email me personally on [makstashkevich@gmail.com](mailto:makstashkevich@gmail.com?subject=Terrex%20Bug%20Report&body=Please%20describe%20the%20issue)


## NeverCalled [0]
### Unknown Direction

> It will never be implemented.
## [Hello](../terrex/packets/hello.py) [1]

### Client -> Server


    It is used for the first request and comparison by the server of the Terraria version with the client version.
    
    In case of an error, the server sends a Kick [2] packet and terminates the connection.
    

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| ? | Version | string | 'Terraria123' where 123 is protocol version number |


## [Kick](../terrex/packets/kick.py) [2]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 8 | reason | NetworkText.read() | - |


## [PlayerInfo](../terrex/packets/player_info.py) [3]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 1 | is_server | bool | - |


## [SyncPlayer](../terrex/packets/sync_player.py) [4]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 1 | skin_variant | uint8 | - |
| 1 | voice_variant | uint8 | - |
| 4 | voice_pitch_offset | float32 | - |
| 1 | hair | uint8 | - |
| ? | name | string | - |
| 1 | hair_dye | uint8 | - |
| 2 | accessory_visibility | uint16 | - |
| 1 | hide_misc | bool | - |
| 8 | hair_color | Rgb.read() | - |
| 8 | skin_color | Rgb.read() | - |
| 8 | eye_color | Rgb.read() | - |
| 8 | shirt_color | Rgb.read() | - |
| 8 | under_shirt_color | Rgb.read() | - |
| 8 | pants_color | Rgb.read() | - |
| 8 | shoe_color | Rgb.read() | - |
| 1 | difficulty_flags | uint8 | - |
| 1 | biome_torch_flags | uint8 | - |
| 1 | consumables_flags | uint8 | - |


## [SyncEquipment](../terrex/packets/sync_equipment.py) [5]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 2 | slot_id | int16 | - |
| 2 | stack | int16 | - |
| 1 | prefix | uint8 | - |
| 2 | item_netid | uint16 | - |


## [RequestWorldData](../terrex/packets/request_world_data.py) [6]

### Client -> Server

> This packet not contains any data.

## [WorldData](../terrex/packets/world_data.py) [7]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 4 | time | int32 | - |
| 1 | day_info | uint8 | - |
| 1 | moon_phase | uint8 | - |
| 2 | max_tiles_x | int16 | - |
| 2 | max_tiles_y | int16 | - |
| 2 | spawn_x | int16 | - |
| 2 | spawn_y | int16 | - |
| 2 | world_surface | int16 | - |
| 2 | rock_layer | int16 | - |
| 4 | world_id | int32 | - |
| ? | world_name | string | - |
| 1 | game_mode | uint8 | - |
| 1 | moon_type | uint8 | - |
| 1 | tree_background | uint8 | - |
| 1 | corruption_background | uint8 | - |
| 1 | jungle_background | uint8 | - |
| 1 | snow_background | uint8 | - |
| 1 | hallow_background | uint8 | - |
| 1 | crimson_background | uint8 | - |
| 1 | desert_background | uint8 | - |
| 1 | ocean_background | uint8 | - |
| 1 | ice_back_style | uint8 | - |
| 1 | jungle_back_style | uint8 | - |
| 1 | hell_back_style | uint8 | - |
| 4 | wind_speed_set | float32 | - |
| 1 | cloud_number | uint8 | - |
| 1 | corruption_tree_top_style | uint8 | - |
| 1 | jungle_tree_top_style | uint8 | - |
| 1 | snow_tree_top_style | uint8 | - |
| 1 | hallow_tree_top_style | uint8 | - |
| 1 | crimson_tree_top_style | uint8 | - |
| 1 | desert_tree_top_style | uint8 | - |
| 1 | ocean_tree_top_style | uint8 | - |
| 1 | glowing_mushroom_tree_top_style | uint8 | - |
| 1 | underworld_tree_top_style | uint8 | - |
| 4 | rain | float32 | - |
| 8 | event_info | uint64 | - |
| 1 | invasion_type | int8 | - |
| 8 | lobby_id | uint64 | - |
| 4 | sandstorm_severity | float32 | - |


## [SpawnTileData](../terrex/packets/spawn_tile_data.py) [8]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | spawn_x | int16 | - |
| 2 | spawn_y | int16 | - |


## [StatusTextSize](../terrex/packets/status_text_size.py) [9]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 4 | status_id | int32 | - |
| 8 | text | NetworkText.read() | - |
| 1 | flags | uint8 | - |


## [TileSection](../terrex/packets/tile_section.py) [10]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| ? | Compressed | raw deflate | Contains the following fields after decompression |
| 4 | x_start | int32 | - |
| 4 | y_start | int32 | - |
| 2 | width | int16 | - |
| 2 | height | int16 | - |
| ? | tiles | Tile[y][x] | - |
| ? | chests | Chest[] | - |
| ? | signs | Sign[] | - |
| ? | tile_entities | TileEntity[] | - |


## [TileFrameSection](../terrex/packets/tile_frame_section.py) [11]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | start_x | int16 | - |
| 2 | start_y | int16 | - |
| 2 | end_x | int16 | - |
| 2 | end_y | int16 | - |


## [PlayerSpawn](../terrex/packets/player_spawn.py) [12]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 4 | spawn_x | float32 | - |
| 4 | spawn_y | float32 | - |
| 4 | respawn_time_remaining | int32 | - |
| 1 | player_spawn_context | uint8 | - |


## [PlayerControls](../terrex/packets/player_controls.py) [13]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 1 | keys | uint8 | - |
| 1 | pulley | uint8 | - |
| 1 | action | uint8 | - |
| 1 | sleep_info | uint8 | - |
| 1 | selected_item | uint8 | - |
| 8 | pos | Vec2.read() | - |
| 8 | vel | Vec2.read() | - |


## [PlayerActive](../terrex/packets/player_active.py) [14]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 1 | active | bool | - |


## [Unknown15](../terrex/packets/unknown15.py) [15]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | pkt_id | int16 | - |
| ? | version | string | - |


## [PlayerLifeMana](../terrex/packets/player_life_mana.py) [16]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 2 | hp | uint16 | - |
| 2 | max_hp | uint16 | - |


## [TileManipulation](../terrex/packets/tile_manipulation.py) [17]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | action | uint8 | - |
| 2 | tile_x | int16 | - |
| 2 | tile_y | int16 | - |
| 2 | extra | int16 | - |
| 1 | style | uint8 | - |


## [SetTime](../terrex/packets/set_time.py) [18]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | day_time | bool | - |
| 4 | time | int32 | - |
| 2 | sun_mod_y | int16 | - |
| 2 | moon_mod_y | int16 | - |


## [ToggleDoorState](../terrex/packets/toggle_door_state.py) [19]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 8 | action | DoorAction.read() | - |
| 2 | tile_x | int16 | - |
| 2 | tile_y | int16 | - |
| 1 | direction | int8 | - |


## [AreaTileChange](../terrex/packets/area_tile_change.py) [20]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | tile_y | int16 | - |
| 2 | tile_x | int16 | - |
| 1 | height | uint8 | - |
| 1 | width | uint8 | - |
| 8 | change_type | ChangeType.read() | - |


## [SyncItem](../terrex/packets/sync_item.py) [21]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | item_id | int16 | - |
| 8 | pos | Vec2.read() | - |
| 8 | vel | Vec2.read() | - |
| 2 | stack_size | int16 | - |
| 1 | prefix | uint8 | - |
| 1 | no_delay | uint8 | - |
| 2 | item_net_id | int16 | - |


## [ItemOwner](../terrex/packets/item_owner.py) [22]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | item_id | int16 | - |
| 1 | player_id | uint8 | - |


## [SyncNPC](../terrex/packets/sync_npc.py) [23]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | npc_id | int16 | - |
| 8 | pos | Vec2.read() | - |
| 8 | vel | Vec2.read() | - |
| 2 | target | uint16 | - |
| 2 | npc_net_id | int16 | - |
| 1 | player_count_scale | uint8 | - |
| 4 | strength_multiplier | float32 | - |
| 1 | life_size | uint8 | - |
| 1 | life | int8 | - |
| 2 | life | int16 | - |
| 4 | life | int32 | - |
| 1 | release_owner | uint8 | - |


## [UnusedMeleeStrike](../terrex/packets/unused_melee_strike.py) [24]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | npc_id | int16 | - |
| 1 | player_id | uint8 | - |


## Unused25 [25]
### Unknown Direction

> The packet has not been implemented yet.
## Unused26 [26]
### Unknown Direction

> The packet has not been implemented yet.
## [SyncProjectile](../terrex/packets/sync_projectile.py) [27]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | projectile_id | int16 | - |
| 8 | pos | Vec2.read() | - |
| 8 | vel | Vec2.read() | - |
| 1 | owner | uint8 | - |
| 2 | ty | int16 | - |
| 1 | flags | uint8 | - |
| 2 | damage | int16 | - |
| 4 | knockback | float32 | - |
| 2 | original_damage | int16 | - |
| 2 | proj_uuid | int16 | - |


## [DamageNPC](../terrex/packets/damage_npc.py) [28]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | npc_id | int16 | - |
| 2 | damage | int16 | - |
| 4 | knockback | float32 | - |
| 1 | hit_direction | uint8 | - |
| 1 | crit | bool | - |


## [KillProjectile](../terrex/packets/kill_projectile.py) [29]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | projectile_id | int16 | - |
| 1 | owner | uint8 | - |


## [TogglePvp](../terrex/packets/toggle_pvp.py) [30]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 1 | pvp_enabled | bool | - |


## [RequestChestOpen](../terrex/packets/request_chest_open.py) [31]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | tile_x | int16 | - |
| 2 | tile_y | int16 | - |


## [SyncChestItem](../terrex/packets/sync_chest_item.py) [32]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | chest_id | int16 | - |
| 1 | item_slot | uint8 | - |
| 2 | stack | int16 | - |
| 1 | prefix | uint8 | - |
| 2 | item_net_id | int16 | - |


## [SyncPlayerChest](../terrex/packets/sync_player_chest.py) [33]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | chest_id | int16 | - |
| 2 | x | int16 | - |
| 2 | y | int16 | - |
| ? | name | string | - |


## [ChestUpdates](../terrex/packets/chest_updates.py) [34]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 8 | action | ChestAction.read() | - |
| 2 | tile_x | int16 | - |
| 2 | tile_y | int16 | - |
| 2 | style | int16 | - |
| 2 | chest_id_to_destroy | int16 | - |


## [PlayerHeal](../terrex/packets/player_heal.py) [35]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 2 | heal_amount | int16 | - |


## [SyncPlayerZone](../terrex/packets/sync_player_zone.py) [36]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 4 | flags | int32 | - |


## [RequestPassword](../terrex/packets/request_password.py) [37]

### Server -> Client

> This packet not contains any data.

## [SendPassword](../terrex/packets/send_password.py) [38]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| ? | password | string | - |


## [ReleaseItemOwnership](../terrex/packets/release_item_ownership.py) [39]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | item_index | uint16 | - |


## [SyncTalkNPC](../terrex/packets/sync_talk_npc.py) [40]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 2 | npc_talk_target | int16 | - |


## [ItemRotationAndAnimation](../terrex/packets/item_rotation_and_animation.py) [41]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 4 | item_rotation | float32 | - |
| 2 | item_animation | int16 | - |


## [PlayerMana](../terrex/packets/player_mana.py) [42]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 2 | mana | int16 | - |
| 2 | max_mana | int16 | - |


## [ManaEffect](../terrex/packets/mana_effect.py) [43]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 2 | mana_amount | int16 | - |


## Unknown44 [44]
### Unknown Direction

> The packet has not been implemented yet.
## [TeamChange](../terrex/packets/team_change.py) [45]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 1 | team | uint8 | - |


## [OpenSignRequest](../terrex/packets/open_sign_request.py) [46]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | x | int16 | - |
| 2 | y | int16 | - |


## [OpenSignResponse](../terrex/packets/open_sign_response.py) [47]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | sign_id | int16 | - |
| 2 | x | int16 | - |
| 2 | y | int16 | - |
| ? | text | string | - |
| 1 | player_id | uint8 | - |
| 1 | flags | uint8 | - |


## [LiquidUpdate](../terrex/packets/liquid_update.py) [48]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | x | int16 | - |
| 2 | y | int16 | - |
| 1 | liquid | uint8 | - |
| 1 | liquid_type | uint8 | - |


## [InitialSpawn](../terrex/packets/initial_spawn.py) [49]

### Server -> Client

> This packet not contains any data.

## [PlayerBuffs](../terrex/packets/player_buffs.py) [50]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |


## MiscDataSync [51]
### Unknown Direction

> The packet has not been implemented yet.
## [LockAndUnlock](../terrex/packets/lock_and_unlock.py) [52]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | x | int16 | - |
| 2 | y | int16 | - |


## [AddNPCBuff](../terrex/packets/add_npc_buff.py) [53]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | npc_id | int16 | - |
| 2 | buff | uint16 | - |
| 2 | time | int16 | - |


## [NPCBuffs](../terrex/packets/npc_buffs.py) [54]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | npc_id | int16 | - |


## [AddPlayerBuffPvP](../terrex/packets/add_player_buff_pvp.py) [55]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 2 | buff | uint16 | - |
| 4 | time | int32 | - |


## [UniqueTownNPCInfoSyncRequest](../terrex/packets/unique_town_npc_info_sync_request.py) [56]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | npc_id | int16 | - |
| ? | name | string | - |
| 4 | town_npc_variation_idx | int32 | - |


## [Unknown57](../terrex/packets/unknown57.py) [57]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | good | uint8 | - |
| 1 | evil | uint8 | - |
| 1 | crimson | uint8 | - |


## [InstrumentSound](../terrex/packets/instrument_sound.py) [58]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 4 | note | float32 | - |


## [HitSwitch](../terrex/packets/hit_switch.py) [59]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 8 | data | HitSwitchData.read() | - |


## [Unknown60](../terrex/packets/unknown60.py) [60]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 8 | data | SetNpcHome.read() | - |


## [SpawnBossUseLicenseStartEvent](../terrex/packets/spawn_boss_use_license_start_event.py) [61]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | player_id | int16 | - |
| 2 | invasion_type | int16 | - |


## [Unknown62](../terrex/packets/player_dodge.py) [62]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |


## [SyncTilePaintOrCoating](../terrex/packets/sync_tile_paint_or_coating.py) [63]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | x | int16 | - |
| 2 | y | int16 | - |
| 1 | color | uint8 | - |


## [SyncWallPaintOrCoating](../terrex/packets/sync_wall_paint_or_coating.py) [64]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | x | int16 | - |
| 2 | y | int16 | - |
| 1 | color | uint8 | - |


## [TeleportEntity](../terrex/packets/teleport_entity.py) [65]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | flags | uint8 | - |
| 2 | target_id | int16 | - |
| 1 | style | uint8 | - |
| 4 | extra_info | int32 | - |


## [Unknown66](../terrex/packets/unknown66.py) [66]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 2 | heal_amount | int16 | - |


## [Unknown67](../terrex/packets/unknown67.py) [67]

### Server <-> Client (Sync)

> This packet not contains any data.

## [Unknown68](../terrex/packets/unknown68.py) [68]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| ? | uuid4 | string | - |


## [ChestName](../terrex/packets/chest_name.py) [69]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | chest_id | int16 | - |
| 2 | x | int16 | - |
| 2 | y | int16 | - |
| ? | name | string | - |


## [BugCatching](../terrex/packets/bug_catching.py) [70]

### Client -> Server

> This packet not contains any data.

## [BugReleasing](../terrex/packets/bug_releasing.py) [71]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | npc_type | int16 | - |
| 1 | style | uint8 | - |


## [TravelMerchantItems](../terrex/packets/travel_merchant_items.py) [72]

### Server -> Client

> This packet not contains any data.

## [RequestTeleportationByServer](../terrex/packets/request_teleportation_by_server.py) [73]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | packet_type | uint8 | - |


## [AnglerQuest](../terrex/packets/angler_quest.py) [74]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | quest | uint8 | - |
| 1 | completed | bool | - |


## [AnglerQuestFinished](../terrex/packets/angler_quest_finished.py) [75]

### Client -> Server

> This packet not contains any data.

## [QuestsCountSync](../terrex/packets/quests_count_sync.py) [76]

### Client -> Server

> This packet not contains any data.

## [TemporaryAnimation](../terrex/packets/temporary_animation.py) [77]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | animation_type | int16 | - |
| 2 | tile_type | uint16 | - |
| 2 | x | int16 | - |
| 2 | y | int16 | - |


## [InvasionProgressReport](../terrex/packets/invasion_progress_report.py) [78]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 4 | progress | int32 | - |
| 4 | max_progress | int32 | - |
| 1 | icon | uint8 | - |
| 1 | wave | uint8 | - |


## [PlaceObject](../terrex/packets/place_object.py) [79]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | x | int16 | - |
| 2 | y | int16 | - |
| 2 | ty | int16 | - |
| 2 | style | int16 | - |
| 1 | alternate | uint8 | - |
| 1 | random | int8 | - |
| 1 | direction | bool | - |


## [SyncPlayerChestIndex](../terrex/packets/sync_player_chest_index.py) [80]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 2 | chest_id | int16 | - |


## [CombatTextInt](../terrex/packets/combat_text_int.py) [81]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 8 | pos | Vec2.read() | - |
| 8 | color | Rgb.read() | - |
| 4 | heal_amount | int32 | - |


## [NetModules](../terrex/packets/net_modules.py) [82]

### Server <-> Client (Sync)

> This packet not contains any data.

## [Unused83](../terrex/packets/unused83.py) [83]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | npc_type | int16 | - |
| 4 | kill_count | int32 | - |


## [PlayerStealth](../terrex/packets/player_stealth.py) [84]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player | uint8 | - |
| 4 | stealth | float32 | - |


## [QuickStackChests](../terrex/packets/quick_stack_chests.py) [85]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | inventory_slot | uint8 | - |


## [TileEntitySharing](../terrex/packets/tile_entity_sharing.py) [86]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 4 | tile_entity_id | int32 | - |
| 1 | update_flag | bool | - |
| 1 | tile_entity_type | uint8 | - |
| 2 | x | int16 | - |
| 2 | y | int16 | - |


## [TileEntityPlacement](../terrex/packets/tile_entity_placement.py) [87]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | x | int16 | - |
| 2 | y | int16 | - |
| 8 | tile_entity_type | TileEntityType.read() | - |


## [ItemTweaker](../terrex/packets/item_tweaker.py) [88]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | item_index | int16 | - |
| 1 | flags1 | uint8 | - |
| 4 | packed_color | int32 | - |
| 2 | damage | uint16 | - |
| 4 | knockback | float32 | - |
| 2 | use_animation | uint16 | - |
| 2 | use_time | uint16 | - |
| 2 | shoot | int16 | - |
| 4 | shoot_speed | float32 | - |
| 1 | flags2 | uint8 | - |
| 2 | width | int16 | - |
| 2 | height | int16 | - |
| 4 | scale | float32 | - |
| 2 | ammo | int16 | - |
| 2 | use_ammo | int16 | - |
| 1 | not_ammo | bool | - |


## [ItemFrameTryPlacing](../terrex/packets/item_frame_try_placing.py) [89]

### Client -> Server

> This packet not contains any data.

## InstancedItem [90]
### Unknown Direction

> The packet has not been implemented yet.
## [SyncEmoteBubble](../terrex/packets/sync_emote_bubble.py) [91]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 4 | emote_id | int32 | - |
| 1 | anchor_type | uint8 | - |
| 2 | player_id | uint16 | - |
| 2 | emote_lifetime | uint16 | - |
| 1 | emote | uint8 | - |
| 2 | emote_metadata | int16 | - |


## [SyncExtraValue](../terrex/packets/sync_extra_value.py) [92]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | npc_index | uint16 | - |
| 4 | extra_value | int32 | - |
| 8 | pos | Vec2.read() | - |


## SocialHandshake [93]
### Unknown Direction

> The packet has not been implemented yet.
## [DevCommands](../terrex/packets/dev_commands.py) [94]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| ? | buf | remaining | - |


## [MurderSomeoneElsesPortal](../terrex/packets/murder_someone_elses_portal.py) [95]

### Client -> Server

> This packet not contains any data.

## [TeleportPlayerThroughPortal](../terrex/packets/teleport_player_through_portal.py) [96]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 2 | portal_color_index | int16 | - |
| 4 | new_pos_x | float32 | - |
| 4 | new_pos_y | float32 | - |
| 4 | vel_x | float32 | - |
| 4 | vel_y | float32 | - |


## [AchievementMessageNPCKilled](../terrex/packets/achievement_message_npc_killed.py) [97]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | npc_id | int16 | - |


## [AchievementMessageEventHappened](../terrex/packets/achievement_message_event_happened.py) [98]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | event_id | int16 | - |


## [MinionRestTargetUpdate](../terrex/packets/minion_rest_target_update.py) [99]

### Client -> Server

> This packet not contains any data.

## [TeleportNPCThroughPortal](../terrex/packets/teleport_npc_through_portal.py) [100]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | npc_id | uint16 | - |
| 2 | portal_color_index | uint16 | - |
| 8 | pos | Vec2.read() | - |
| 8 | vel | Vec2.read() | - |


## [UpdateTowerShieldStrengths](../terrex/packets/update_tower_shield_strengths.py) [101]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | solar_tower | uint16 | - |
| 2 | vortex_tower | uint16 | - |
| 2 | nebula_tower | uint16 | - |
| 2 | stardust_tower | uint16 | - |


## [NebulaLevelupRequest](../terrex/packets/nebula_levelup_request.py) [102]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 2 | level_up_type | uint16 | - |
| 8 | origin | Vec2.read() | - |


## [MoonlordHorror](../terrex/packets/moonlord_horror.py) [103]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 4 | countdown | int32 | - |


## [ShopOverride](../terrex/packets/shop_override.py) [104]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | slot | uint8 | - |
| 2 | item_type | int16 | - |
| 2 | stack | int16 | - |
| 1 | prefix | uint8 | - |
| 4 | value | int32 | - |
| 1 | buy_once | bool | - |


## [GemLockToggle](../terrex/packets/gem_lock_toggle.py) [105]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | x | int16 | - |
| 2 | y | int16 | - |
| 1 | on | bool | - |


## [PoofOfSmoke](../terrex/packets/poof_of_smoke.py) [106]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | x | int16 | - |
| 2 | y | int16 | - |


## [SmartTextMessage](../terrex/packets/smart_text_message.py) [107]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 8 | color | Rgb.read() | - |
| 8 | message | NetworkText.read() | - |
| 2 | message_length | int16 | - |


## [WiredCannonShot](../terrex/packets/wired_cannon_shot.py) [108]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | damage | int16 | - |
| 4 | knockback | float32 | - |
| 2 | x | int16 | - |
| 2 | y | int16 | - |
| 2 | angle | int16 | - |
| 2 | ammo | int16 | - |
| 1 | player_id | uint8 | - |


## [MassWireOperation](../terrex/packets/mass_wire_operation.py) [109]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | start_x | int16 | - |
| 2 | start_y | int16 | - |
| 2 | end_x | int16 | - |
| 2 | end_y | int16 | - |
| 8 | tool_mode | ToolMode.read() | - |


## [MassWireOperationPay](../terrex/packets/mass_wire_operation_pay.py) [110]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | item_type | int16 | - |
| 2 | quantity | int16 | - |
| 1 | player_id | uint8 | - |


## [ToggleParty](../terrex/packets/toggle_party.py) [111]

### Client -> Server

> This packet not contains any data.

## [SpecialFX](../terrex/packets/special_fx.py) [112]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 1 | effect_type | uint8 | - |


## [CrystalInvasionStart](../terrex/packets/crystal_invasion_start.py) [113]

### Client -> Server

> This packet not contains any data.

## [CrystalInvasionWipeAllTheThingsss](../terrex/packets/crystal_invasion_wipe_all_the_thingsss.py) [114]

### Server -> Client

> This packet not contains any data.

## [MinionAttackTargetUpdate](../terrex/packets/minion_attack_target_update.py) [115]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 2 | minion_target | int16 | - |


## [CrystalInvasionSendWaitTime](../terrex/packets/crystal_invasion_send_wait_time.py) [116]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 4 | time_until_next_wave | int32 | - |


## [PlayerHurtV2](../terrex/packets/player_hurt_v2.py) [117]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 8 | reason | PlayerDeathReason.read() | - |
| 2 | damage | int16 | - |
| 1 | hit_direction | uint8 | - |
| 1 | flags | uint8 | - |
| 1 | cooldown_counter | int8 | - |


## [PlayerDeathV2](../terrex/packets/player_death_v2.py) [118]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 8 | reason | PlayerDeathReason.read() | - |
| 2 | damage | int16 | - |
| 1 | hit_direction | uint8 | - |
| 1 | pvp | bool | - |


## [CombatTextString](../terrex/packets/combat_text_string.py) [119]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 8 | pos | Vec2.read() | - |
| 8 | color | Rgb.read() | - |
| 8 | combat_text | NetworkText.read() | - |


## [Emoji](../terrex/packets/emoji.py) [120]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 1 | emoticon | uint8 | - |


## [TEDisplayDollDataSync](../terrex/packets/te_display_doll_data_sync.py) [121]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 4 | tile_entity_id | int32 | - |
| 1 | item_index | uint8 | - |
| 2 | item_id | uint16 | - |
| 2 | stack | uint16 | - |
| 1 | prefix | uint8 | - |


## [RequestTileEntityInteraction](../terrex/packets/request_tile_entity_interaction.py) [122]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 4 | tile_entity_id | int32 | - |
| 1 | player_id | uint8 | - |


## [WeaponsRackTryPlacing](../terrex/packets/weapons_rack_try_placing.py) [123]

### Client -> Server

> This packet not contains any data.

## [TEHatRackItemSync](../terrex/packets/te_hat_rack_item_sync.py) [124]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 4 | tile_entity_id | int32 | - |
| 1 | item_index | uint8 | - |
| 2 | item_id | uint16 | - |
| 2 | stack | uint16 | - |
| 1 | prefix | uint8 | - |


## [SyncTilePicking](../terrex/packets/sync_tile_picking.py) [125]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 2 | x | int16 | - |
| 2 | y | int16 | - |
| 1 | pick_damage | uint8 | - |


## [SyncRevengeMarker](../terrex/packets/sync_revenge_marker.py) [126]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 4 | unique_id | int32 | - |
| 4 | x | float32 | - |
| 4 | y | float32 | - |
| 4 | npc_id | int32 | - |
| 4 | npc_hp_percent | float32 | - |
| 4 | npc_type | int32 | - |
| 4 | npc_ai | int32 | - |
| 4 | coin_value | int32 | - |
| 4 | base_value | float32 | - |
| 1 | spawned_from_statue | bool | - |


## [RemoveRevengeMarker](../terrex/packets/remove_revenge_marker.py) [127]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 4 | unique_id | int32 | - |


## [LandGolfBallInCup](../terrex/packets/land_golf_ball_in_cup.py) [128]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 2 | x | int16 | - |
| 2 | y | int16 | - |
| 2 | number_of_hits | uint16 | - |
| 2 | proj_id | uint16 | - |


## [FinishedConnectingToServer](../terrex/packets/finished_connecting_to_server.py) [129]

### Server -> Client

> This packet not contains any data.

## [FishOutNpc](../terrex/packets/fish_out_npc.py) [130]

### Client -> Server

> This packet not contains any data.

## [TamperWithNPC](../terrex/packets/tamper_with_npc.py) [131]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 2 | npc_id | uint16 | - |
| 4 | immunity_time | int32 | - |
| 2 | immunity_player_id | int16 | - |


## [PlayLegacySound](../terrex/packets/play_legacy_sound.py) [132]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 8 | pos | Vec2.read() | - |
| 2 | sound_id | uint16 | - |


## [FoodPlatterTryPlacing](../terrex/packets/food_platter_try_placing.py) [133]

### Client -> Server

> This packet not contains any data.

## [UpdatePlayerLuckFactors](../terrex/packets/update_player_luck_factors.py) [134]

### Server <-> Client (Sync)

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 4 | ladybug_luck_time_left | int32 | - |
| 4 | torch_luck | float32 | - |
| 1 | luck_potion | uint8 | - |
| 1 | has_garden_gnome_nearby | bool | - |
| 1 | broken_mirror_bad_luck | bool | - |
| 4 | equipment_based_luck_bonus | float32 | - |
| 4 | coin_luck | float32 | - |
| 1 | kite_luck_level | uint8 | - |


## [DeadPlayer](../terrex/packets/dead_player.py) [135]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |


## [SyncCavernMonsterType](../terrex/packets/sync_cavern_monster_type.py) [136]

### Server <-> Client (Sync)

> This packet not contains any data.

## [RequestNPCBuffRemoval](../terrex/packets/request_npc_buff_removal.py) [137]

### Client -> Server

> This packet not contains any data.

## [ClientSyncedInventory](../terrex/packets/client_synced_inventory.py) [138]

### Client -> Server

> This packet not contains any data.

## [SetCountsAsHostForGameplay](../terrex/packets/set_counts_as_host_for_gameplay.py) [139]

### Server -> Client

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 1 | host | bool | - |


## SetMiscEventValues [140]
### Unknown Direction

> The packet has not been implemented yet.

<div align="center">
<h1>[ i ] Packets 141-161 have been added on versions 1.4.5.x</h1>
</div>

## RequestLucyPopup [141]
### Unknown Direction

> The packet has not been implemented yet.
## SyncProjectileTrackers [142]
### Unknown Direction

> The packet has not been implemented yet.
## CrystalInvasionRequestedToSkipWaitTime [143]
### Unknown Direction

> The packet has not been implemented yet.
## RequestQuestEffect [144]
### Unknown Direction

> The packet has not been implemented yet.
## SyncItemsWithShimmer [145]
### Unknown Direction

> The packet has not been implemented yet.
## ShimmerActions [146]
### Unknown Direction

> The packet has not been implemented yet.
## [SyncLoadout](../terrex/packets/sync_loadout.py) [147]

### Client -> Server

| Size (bytes) | Description | Type | Notes |
| --- | --- | --- | --- |
| 1 | player_id | uint8 | - |
| 1 | loadout_index | uint8 | - |
| 2 | accessory_visibility | uint16 | - |


## SyncItemCannotBeTakenByEnemies [148]
### Unknown Direction

> The packet has not been implemented yet.
## DeadCellsDisplayJarTryPlacing [149]
### Unknown Direction

> The packet has not been implemented yet.
## SpectatePlayer [150]
### Unknown Direction

> The packet has not been implemented yet.
## SyncItemDespawn [151]
### Unknown Direction

> The packet has not been implemented yet.
## ItemUseSound [152]
### Unknown Direction

> The packet has not been implemented yet.
## NPCDebuffDamage [153]
### Unknown Direction

> The packet has not been implemented yet.
## [Ping](../terrex/packets/ping.py) [154]

### Server <-> Client (Sync)

> This packet not contains any data.

## SyncChestSize [155]
### Unknown Direction

> The packet has not been implemented yet.
## TELeashedEntityAnchorPlaceItem [156]
### Unknown Direction

> The packet has not been implemented yet.
## TeamChangeFromUI [157]
### Unknown Direction

> The packet has not been implemented yet.
## ExtraSpawnSectionLoaded [158]
### Unknown Direction

> The packet has not been implemented yet.
## RequestSection [159]
### Unknown Direction

> The packet has not been implemented yet.
## ItemPosition [160]
### Unknown Direction

> The packet has not been implemented yet.
## HostToken [161]
### Unknown Direction

> The packet has not been implemented yet.
