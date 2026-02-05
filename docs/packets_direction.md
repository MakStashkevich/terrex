# List of Terraria Packet protocol directions

# Packets

## Connect Request [1]

### Client -> Server

## Disconnect [2]

### Server -> Client

## Set User Slot [3]

### Server -> Client

## Player Info [4]

### Server <-> Client (Sync)

## Player Inventory Slot [5]

### Server <-> Client (Sync)

## Request World Data [6]

### Client -> Server

## World Info [7]

### Server -> Client

## Request Essential Tiles [8]

### Client -> Server

## Status [9]

### Server -> Client

## Send Section [10]

### Server -> Client

## Section Tile Frame [11]

### Server -> Client

## Spawn Player [12]

### Client -> Server

## Update Player [13]

### Server <-> Client (Sync)

## Player Active [14]

### Server -> Client

## Null [15]

### Never sent

## Player HP [16]

### Server <-> Client (Sync)

## Modify Tile [17]

### Server <-> Client (Sync)

## Time [18]

### Server -> Client

## Door Toggle [19]

### Server <-> Client (Sync)

## Send Tile Square [20]

### Server <-> Client (Sync)

## Update Item Drop [21]

## Update Item Owner [22]

### Server <-> Client (Sync)

## NPC Update [23]

### Server -> Client

## Strike NPCwith Held Item [24]

### Server <-> Client (Sync)

## Null [25]

### Never sent

## Null [26]

### Never sent

## Projectile Update [27]

### Server <-> Client (Sync)

## NPC Strike [28]

### Server <-> Client (Sync)

## Destroy Projectile [29]

### Server <-> Client (Sync)

## Toggle P V P [30]

### Server <-> Client (Sync)

## Open Chest [31]

### Client -> Server

## Update Chest Item [32]

### Server <-> Client (Sync)

## Sync Active Chest [33]

### Server <-> Client (Sync)

## PlaceChest [34]

### Server <-> Client

## Heal Effect [35]

### Server <-> Client (Sync)

## Player Zone [36]

### Server <-> Client (Sync)

## Request Password [37]

### Server -> Client

## Send Password [38]

### Client -> Server

## Remove Item Owner [39]

### Server -> Client

## Set Active NPC [40]

### Server <-> Client (Sync)

## Player Item Animation [41]

### Server <-> Client (Sync)

## Player Mana [42]

### Server <-> Client (Sync)

## Mana Effect [43]

### Server <-> Client (Sync)

## Null [44]

### Never sent

## Player Team [45]

### Server <-> Client (Sync)

## Request Sign [46]

### Client -> Server

## Update Sign [47]

### Updates sign if sent from client otherwise displays sign to client.

## Set Liquid [48]

### Server <-> Client (Sync)

## Complete Connection and Spawn [49]

### Server -> Client

## Update Player Buff [50]

### Server <-> Client (Sync)

## Special NPC Effect [51]

### Server <-> Client (Sync)

## Unlock [52]

### Server <-> Client (Sync)

## Add NPC Buff [53]

### Server <-> Client (Sync)

## Update NPC Buff [54]

### Server -> Client

## Add Player Buff [55]

### Server <-> Client (Sync)

## Update NPC Name [56]

### Server <-> Client (Sync)

## Update Good Evil [57]

### Server -> Client

## Play Music Item [58]

### Server <-> Client (Sync)

## Hit Switch [59]

### Server <-> Client (Sync)

## NPC Home Update [60]

### Server <-> Client (Sync)

## Spawn Boss Invasion [61]

### Client -> Server

## Player Dodge [62]

### Server <-> Client (Sync)

## Paint Tile [63]

### Server <-> Client (Sync)

## Paint Wall [64]

### Server <-> Client (Sync)

## Player NPC Teleport [65]

### Server <-> Client (Sync)

## Heal Other Player [66]

### Server <-> Client (Sync)

## Placeholder [67]

### Does not exist in the official client. Exists solely for the purpose of being used by custom clients and servers.

## Client UUID [68]

### Client -> Server

## Get Chest Name [69]

### Server <-> Client (Sync)

## Catch NPC [70]

### Client -> Server

## Release NPC [71]

### Client -> Server

## Travelling Merchant Inventory [72]

### Server -> Client

## Teleportation Potion [73]

### Server <-> Client

## Angler Quest [74]

### Server -> Client

## Complete Angler Quest Today [75]

### Client -> Server

## Number Of Angler Quests Completed [76]

### Client -> Server

## Create Temporary Animation [77]

### Server -> Client

## Report Invasion Progress [78]

### Server -> Client

## Place Object [79]

### Server <-> Client

## Sync Player Chest Index [80]

### Server -> Client

## Create Combat Text [81]

### Server -> Client

## Load Net Module [82]

### Server <-> Client

## Set NPC Kill Count [83]

### Server -> Client

## Set Player Stealth [84]

### Server <-> Client (Sync)

## Force Item Into Nearest Chest [85]

### Client -> Server

## Update Tile Entity [86]

### Server -> Client

## Place Tile Entity [87]

### Client -> Server

## Tweak Item (FKA. Alter Item Drop) [88]

### Server -> Client

## Place Item Frame [89]

### Client -> Server

## Update Item Drop 2 [90]

### Server <-> Client (Sync)

## Sync Emote Bubble [91]

### Server -> Client

## Sync Extra Value [92]

### Server <-> Client (Sync)

## Social Handshake [93]

### Not used

## Deprecated [94]

### Not used

## Kill Portal [95]

### Client -> Server

## Player Teleport Portal [96]

### Server <-> Client

## Notify Player NPC Killed [97]

### Server -> Client

## Notify Player Of Event [98]

### Server -> Client

## Update Minion Target [99]

### Server <-> Client (Sync)

## NPC Teleport Portal [100]

### Server <-> Client

## Update Shield Strengths [101]

### Server -> Client

## Nebula Level Up [102]

### Server <-> Client (Sync)

## Moon Lord Countdown [103]

### Server -> Client

## NPC Shop Item [104]

### Server -> Client

## Gem Lock Toggle [105]

### Client -> Server

## Poof of Smoke [106]

### Server -> Client

## Smart Text Message (FKA. Chat Message v2) [107]

### Server -> Client

## Wired Cannon Shot [108]

### Server -> Client

## Mass Wire Operation [109]

### Client -> Server

## Mass Wire Operation Consume [110]

### Server -> Client

## Toggle Birthday Party [111]

### Client -> Server

## GrowFX [112]

### Server <-> Client (Sync)

## CrystalInvasionStart [113]

### Client -> Server

## CrystalInvasionWipeAll [114]

### Server -> Client

## MinionAttackTargetUpdate [115]

### Client -> Server

## CrystalInvasionSendWaitTime [116]

### Server -> Client

## PlayerHurtV2 [117]

### Client -> Server

## PlayerDeathV2 [118]

### Client -> Server

## CombatTextString [119]

### Client <-> Server

## Emoji [120]

### Client -> Server

## TEDisplayDollItemSync [121]

### Client <-> Server

## RequestTileEntityInteraction [122]

### Client <-> Server

## WeaponsRackTryPlacing [123]

### Client -> Server

## TEHatRackItemSync [124]

### Client <-> Server

## SyncTilePicking [125]

### Client <-> Server

## SyncRevengeMarker [126]

### Server -> Client

## RemoveRevengeMarker [127]

### Server -> Client

## LandGolfBallInCup [128]

### Client <-> Server

## FinishedConnectingToServer [129]

### Server -> Client

## FishOutNPC [130]

### Client -> Server

## TamperWithNPC [131]

### Server -> Client

## PlayLegacySound [132]

### Server -> Client

## FoodPlatterTryPlacing [133]

### Client -> Server

## UpdatePlayerLuckFactors [134]

### Client <-> Server

## DeadPlayer [135]

### Server -> Client

## SyncCavernMonsterType [136]

### Client <-> Server

## RequestNPCBuffRemoval [137]

### Client -> Server

## ClientFinishedInventoryChangesOnThisTick (formerly ClientSyncedInventory) [138]

### Client -> Server

## SetCountsAsHostForGameplay [139]

### Server -> Client

## SetMiscEventValues [140]

### Server -> Client

---

# Net Modules

## Net Module Format (packet within a packet)

## Liquid [0]

### Server -> Client

## Text [1]

### Server <-> Client (Sync)

## Ping [2]

### Server <-> Client (Sync)

## Ambience [3]

### Server -> Client

## Bestiary [4]

### Server -> Client

## CreativeUnlocks [5]

### Server -> Client

## CreativePowers [6]

### Server <-> Client (Sync)

## CreativeUnlocksPlayerReport [7]

### Client -> Server

## TeleportPylon [8]

### Server <-> Client (Sync)

## Particles [9]

### Server <-> Client (Sync)

## CreativePowerPermissions [10]

### Server -> Client

