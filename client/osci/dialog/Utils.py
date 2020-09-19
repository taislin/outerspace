

def enableConstruction(client):
    enabled1 = 0
    enabled2 = 0
    player = client.getPlayer()
    for techID in player.techs:
        tech = client.getTechInfo(techID)
        if tech.isShipHull:
            enabled1 = 1
            if enabled2: break
        elif tech.isShipEquip and tech.subtype == "seq_ctrl":
            enabled2 = 1
            if enabled1: break

    return enabled1 and enabled2
