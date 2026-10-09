/* Source-extracted primitives: Universe bae18306. No engine logic rewritten. */
const DEPTH_OVERLAY_INDEX=1000000;
const fork={
 buildLayers:function(phaserMap,terrains){
        let depth = -2;
        for (const layer of this.gameMap.flatLayers) {
            if (layer.type === "tilelayer") {
                const phaserLayer = phaserMap.createLayer(
                    layer.name,
                    terrains,
                    (layer.x || 0) * 32,
                    (layer.y || 0) * 32
                );
                if (phaserLayer) {
                    this.phaserLayers.push(
                        phaserLayer
                            .setDepth(depth)
                            .setScrollFactor(layer.parallaxx ?? 1, layer.parallaxy ?? 1)
                            .setAlpha(layer.opacity)
                            .setVisible(layer.visible)
                            .setSize(layer.width, layer.height)
                    );
                }
            }
            if (layer.type === "objectgroup" && layer.name === "floorLayer") {
                depth = DEPTH_OVERLAY_INDEX;
            }
        }


},
 setLayerVisibility:function(layerName,visible){
        const phaserLayer = this.findPhaserLayer(layerName);
        if (phaserLayer != undefined) {
            phaserLayer.setVisible(visible);
            phaserLayer.setCollisionByProperty({ collides: true }, visible);
            this.updateCollisionGrid(phaserLayer);
        } else {
            const phaserLayers = this.findPhaserLayers(layerName + "/");
            if (phaserLayers.length === 0) {
                console.warn(
                    'Could not find layer with name that contains "' +
                        layerName +
                        '" when calling WA.hideLayer / WA.showLayer'
                );
                return;
            }
            for (let i = 0; i < phaserLayers.length; i++) {
                phaserLayers[i].setVisible(visible);
                phaserLayers[i].setCollisionByProperty({ collides: true }, visible);
            }
            this.updateCollisionGrid(undefined, false);
        }

},
 entityDepth:function(){return this.y + this.displayHeight + (this.prefab.depthOffset ?? 0);},
 characterDepth:function(){return this.y + 16;},
 configureBody:function(){
        this.scene.physics.world.enableBody(this);
        this.getBody().setImmovable(true);
        this.getBody().setCollideWorldBounds(true);
        this.setSize(CHARACTER_BODY_WIDTH, CHARACTER_BODY_HEIGHT);
        this.getBody().setSize(CHARACTER_BODY_WIDTH, CHARACTER_BODY_HEIGHT); //edit the hitbox to better match the character model
        this.getBody().setOffset(CHARACTER_BODY_OFFSET_X, CHARACTER_BODY_OFFSET_Y);
        this.setDepth(this.y + 16);
}
};
const CHARACTER_BODY_WIDTH=16,CHARACTER_BODY_HEIGHT=16,CHARACTER_BODY_OFFSET_X=0,CHARACTER_BODY_OFFSET_Y=8;

fork.modifyToCollisionsLayer=function(x,y,name,collisionGrid,withGridUpdate=true){
        const coords = this.entitiesCollisionLayer.worldToTileXY(x, y, true);
        for (let y = 0; y < collisionGrid.length; y += 1) {
            for (let x = 0; x < collisionGrid[y].length; x += 1) {
                // add tiles
                if (collisionGrid[y][x] === 1) {
                    const tile = this.entitiesCollisionLayer.putTileAt(
                        this.existingTileIndex,
                        coords.x + x,
                        coords.y + y
                    );
                    if (tile !== null) {
                        tile.properties["collides"] = true;
                    }
                    continue;
                }
                // remove tiles
                if (collisionGrid[y][x] === -1) {
                    this.entitiesCollisionLayer.removeTileAt(coords.x + x, coords.y + y, false);
                }
            }
        }
        this.entitiesCollisionLayer.setCollisionByProperty({ collides: true });
        if (withGridUpdate) {
            this.updateCollisionGrid(this.entitiesCollisionLayer, false);
        }

};
