# Перенос пакетов Terraria Protocol в TerreX

## Статус переноса

### Реализованные пакеты (по файлам .py и ID)

- `connect.py` (0x01 Connect)
- `player_info.py` (0x04 PlayerInfo)
- `client_uuid.py` (0x44 ClientUuid)
- `player_hp.py` (0x10 PlayerHp)
- `player_mana.py` (0x2A PlayerMana)
- `update_player_buff.py` (0x32 UpdatePlayerBuff)
- `player_inventory_slot.py` (0x05 PlayerInventorySlot)
- `request_world_data.py` (0x06 RequestWorldData)
- `request_essential_tiles.py` (0x08 RequestEssentialTiles)
- `spawn_player.py` (0x0C SpawnPlayer)
- `disconnect.py` (0x02 Disconnect)
- `set_user_slot.py` (0x03 SetUserSlot)
- `status.py` (0x09 Status)
- `world_info.py` (0x07 WorldInfo)
- `player_active.py` (0x0E PlayerActive)
- `section_tile_frame.py` (0x0B SectionTileFrame)
- `time.py` (0x12 Time)
- `door_toggle.py` (0x13 DoorToggle)
- `destroy_projectile.py` (0x1D DestroyProjectile)
- `npc_strike.py` (0x1C NpcStrike)
- `npc_update.py` (0x17 NpcUpdate)
- `strike_npc.py` (0x18 StrikeNpcHeldItem)
- `projectile_update.py` (0x1B ProjectileUpdate)
- `toggle_pvp.py` (0x1E TogglePvp)
- `open_chest.py` (0x1F OpenChest)
- `place_chest.py` (0x22 PlaceChest)
- `heal_effect.py` (0x23 HealEffect)
- `mana_effect.py` (0x2B ManaEffect)
- `player_zone.py` (0x24 PlayerZone)
- `request_password.py` (0x25 RequestPassword)
- `send_password.py` (0x26 SendPassword)
- `remove_item_owner.py` (0x27 RemoveItemOwner)
- `set_active_npc.py` (0x28 SetActiveNpc)
- `player_item_animation.py` (0x29 PlayerItemAnimation)
- `player_team.py` (0x2D PlayerTeam)
- `set_liquid.py` (0x30 SetLiquid)
- `complete_connection_and_spawn.py` (0x31 CompleteConnectionSpawn)
- `sync_active_chest.py` (0x21 SyncActiveChest)
- `update_chest_item.py` (0x20 UpdateChestItem)
- `update_item_owner.py` (0x16 UpdateItemOwner)
- `update_item_drop2.py` (0x5A UpdateItemDrop2)
- `update_sign.py` (0x2F UpdateSign)
- `request_sign.py` (0x2E RequestSign)
- `send_tile_square.py` (0x14 SendTileSquare)
- `update_player.py` (0x0D UpdatePlayer)
- `modify_tile.py` (0x11 ModifyTile)
- `packet15.py` (0x0F Packet15)
- `update_npc_name.py` (0x38 UpdateNpcName)
- `play_music_item.py` (0x3A PlayMusicItem)
- `send_section.py` (0x0A SendSection)
- `hit_switch.py` (0x3B HitSwitch)
- `set_npc_home.py` (0x3C NpcHomeUpdate)

**Примечание:** Все пакеты из handshake.py перенесены в отдельные файлы. player_mana.py больше не дублирует.

Старые `packet*.py` удалены.
handshake.py удален.

### Недостающие пакеты (примеры простых сначала)

Простые (packet_struct! с базовыми типами):
- 0x19 Null25
- 0x1A Null26
- 0x2C Null44
- и многие другие (см полный список в terraria-protocol/src/packets/*.rs и [PacketIds](packet_ids.py))

Полный список .rs файлов в terraria-protocol/src/packets (из list_files):
add_npc_buff.rs, add_player_buff.rs, angler_quest.rs, ... (всего ~150)

### Следующие шаги
1. Реализовать простые пакеты (следующие: null25.py (0x19), null26.py (0x1A), null44.py (0x2C), и т.д.)
2. Затем сложные пакеты как place_object.py, update_tile_entity.py и остальные из terraria-protocol/src/packets/*.rs
2. Для каждого: прочитать .rs, создать класс Packet с read/write по serde
3. Использовать terrex.structures для Tile, Chest и т.д. (уже есть некоторые)
4. Вызвать .register() в конце файла
5. Тестировать в client.py или examples

**Цель:** Полностью перенести все пакеты.
