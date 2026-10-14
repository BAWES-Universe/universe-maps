var PathTileType = /*#__PURE__*/ function(PathTileType) {
    PathTileType[PathTileType["Walkable"] = 0] = "Walkable";
    PathTileType[PathTileType["Collider"] = 1] = "Collider";
    PathTileType[PathTileType["Exit"] = 2] = "Exit";
    PathTileType[PathTileType["Start"] = 3] = "Start";
    return PathTileType;
}(PathTileType || {});
class PathfindingManager {
    easyStar;
    grid;
    tileDimensions;
    currentPathfindingInstanceId = null;
    pathfindingTimeout = null;
    pathfindingRequestId = 0;
    resolveCancelledPath;
    constructor(collisionsGrid, tileDimensions){
        this.easyStar = new EasyStar.js();
        this.easyStar.enableDiagonals();
        this.easyStar.disableCornerCutting();
        this.easyStar.setTileCost(2, 100);
        this.easyStar.setIterationsPerCalculation(1000);
        this.grid = collisionsGrid;
        this.tileDimensions = tileDimensions;
        this.setEasyStarGrid(collisionsGrid);
    }
    setCollisionGrid(collisionGrid) {
        this.setEasyStarGrid(collisionGrid);
    }
    cleanup() {
        this.pathfindingRequestId++;
        this.cancelCurrentPathfinding();
    }
    async findPathFromGameCoordinates(start, end, tryFindingNearestAvailable = false) {
        const requestId = ++this.pathfindingRequestId;
        this.cancelCurrentPathfinding();
        const startTile = this.mapPixelsToTileUnits(this.clampToMap(start));
        const clampedEnd = this.clampToMap(end);
        const endTile = this.mapPixelsToTileUnits(clampedEnd);
        const result = await this.findPath(startTile, endTile, tryFindingNearestAvailable, requestId);
        const path = result.path;
        if (path.length > 1) {
            path[0] = {
                x: start.x,
                y: start.y + this.tileDimensions.height * 0.5
            };
        }
        if (path.length > 0 && result.isExactTarget) {
            path[path.length - 1] = this.fitBodyWithinTile(clampedEnd.x, clampedEnd.y, this.tileDimensions.width, this.tileDimensions.height);
        }
        return path;
    }
    fitBodyWithinTile(x, y, tileWidth, tileHeight) {
        const xMod = x % tileWidth;
        const yMod = y % tileHeight;
        if (yMod < CHARACTER_BODY_HEIGHT / 2 + CHARACTER_BODY_OFFSET_Y) {
            y -= yMod;
            y += CHARACTER_BODY_HEIGHT / 2 + CHARACTER_BODY_OFFSET_Y;
        }
        if (xMod < CHARACTER_BODY_HEIGHT / 2 + CHARACTER_BODY_OFFSET_X) {
            x -= xMod;
            x += CHARACTER_BODY_HEIGHT / 2 + CHARACTER_BODY_OFFSET_X;
        }
        if (yMod > tileHeight - CHARACTER_BODY_HEIGHT / 2 + CHARACTER_BODY_OFFSET_Y) {
            y -= yMod;
            y += tileHeight - CHARACTER_BODY_HEIGHT / 2 + CHARACTER_BODY_OFFSET_Y;
        }
        if (xMod > tileWidth - CHARACTER_BODY_HEIGHT / 2 + CHARACTER_BODY_OFFSET_X) {
            x -= xMod;
            x += tileWidth - CHARACTER_BODY_HEIGHT / 2 + CHARACTER_BODY_OFFSET_X;
        }
        return {
            x,
            y
        };
    }
    async findPath(start, end, tryFindingNearestAvailable, requestId) {
        let isExactTarget = true;
        let endPoints = [
            end
        ];
        if (tryFindingNearestAvailable) {
            endPoints = [
                end,
                ...this.getNeighbouringTiles(end).sort((a, b)=>{
                    const aDist = MathUtils.distanceBetween(a, start, false);
                    const bDist = MathUtils.distanceBetween(b, start, false);
                    if (aDist > bDist) {
                        return 1;
                    }
                    if (aDist < bDist) {
                        return -1;
                    }
                    return 0;
                })
            ];
        }
        let path = [];
        while(endPoints.length > 0){
            const endPoint = endPoints.shift();
            if (!endPoint) {
                return {
                    path: [],
                    isExactTarget: false
                };
            }
            path = await this.getPath(start, endPoint).catch();
            if (requestId !== this.pathfindingRequestId) {
                return {
                    path: [],
                    isExactTarget: false
                };
            }
            if (path && path.length > 0) {
                return {
                    path: this.mapTileUnitsToPixels(path),
                    isExactTarget
                };
            }
            isExactTarget = false;
        }
        return {
            path: [],
            isExactTarget: false
        };
    }
    mapTileUnitsToPixels(path) {
        return path.map(this.mapTileUnitToPixels.bind(this));
    }
    mapTileUnitToPixels(tilePosition) {
        return {
            x: tilePosition.x * this.tileDimensions.width + this.tileDimensions.width * 0.5,
            y: tilePosition.y * this.tileDimensions.height + this.tileDimensions.height * 0.5
        };
    }
    mapPixelsToTileUnits(position) {
        return {
            x: Math.floor(position.x / this.tileDimensions.width),
            y: Math.floor(position.y / this.tileDimensions.height)
        };
    }
    getNeighbouringTiles(tile) {
        const xOffsets = [
            -1,
            0,
            1,
            1,
            1,
            0,
            -1,
            -1
        ];
        const yOffsets = [
            -1,
            -1,
            -1,
            0,
            1,
            1,
            1,
            0
        ];
        const neighbours = [];
        for(let i = 0; i < 8; i += 1){
            const tileToCheck = {
                x: tile.x + xOffsets[i],
                y: tile.y + yOffsets[i]
            };
            if (this.isTileWithinMap(tileToCheck)) {
                neighbours.push(tileToCheck);
            }
        }
        return neighbours;
    }
    isTileWithinMap(tile) {
        const mapHeight = this.grid.length ?? 0;
        const mapWidth = this.grid[0]?.length ?? 0;
        return MathUtils.isBetween(tile.x, 0, mapWidth) && MathUtils.isBetween(tile.y, 0, mapHeight);
    }
    clampToMap(position) {
        let x = position.x;
        let y = position.y;
        const mapHeight = this.grid.length;
        const mapWidth = this.grid[0].length;
        if (x < 0) {
            x = 0;
        }
        if (y < 0) {
            y = 0;
        }
        if (x >= mapWidth * this.tileDimensions.width) {
            x = mapWidth * this.tileDimensions.width - 1;
        }
        if (y >= mapHeight * this.tileDimensions.height) {
            y = mapHeight * this.tileDimensions.height - 1;
        }
        return {
            x,
            y
        };
    }
    async getPath(start, end) {
        if (start.x === end.x && start.y === end.y) {
            const tile = this.grid[end.y]?.[end.x];
            return tile === 0 || tile === 2 || tile === 3 ? [
                {
                    ...end
                }
            ] : [];
        }
        return new Promise((resolve)=>{
            let pathFound = false;
            this.resolveCancelledPath = ()=>{
                pathFound = true;
                resolve([]);
            };
            let calculationCount = 0;
            const maxCalculations = 50;
            const maxTimeMs = 3000;
            const startTime = Date.now();
            this.currentPathfindingInstanceId = this.easyStar.findPath(start.x, start.y, end.x, end.y, (path)=>{
                if (pathFound) return;
                pathFound = true;
                this.resolveCancelledPath = undefined;
                this.clearPathfindingTimeout();
                this.currentPathfindingInstanceId = null;
                if (path === null) {
                    resolve([]);
                } else {
                    resolve(path);
                }
            });
            const performCalculation = ()=>{
                if (pathFound) return;
                const currentTime = Date.now();
                if (currentTime - startTime > maxTimeMs) {
                    this.cancelCurrentPathfinding();
                    console.warn("Pathfinding timeout reached, returning empty path");
                    resolve([]);
                    return;
                }
                calculationCount++;
                if (calculationCount > maxCalculations) {
                    this.cancelCurrentPathfinding();
                    console.warn("Pathfinding max calculations reached, returning empty path");
                    resolve([]);
                    return;
                }
                this.easyStar.calculate();
                if (!pathFound) {
                    this.pathfindingTimeout = window.setTimeout(performCalculation, 10);
                }
            };
            performCalculation();
        });
    }
    cancelCurrentPathfinding() {
        this.resolveCancelledPath?.();
        this.resolveCancelledPath = undefined;
        if (this.currentPathfindingInstanceId !== null) {
            this.easyStar.cancelPath(this.currentPathfindingInstanceId);
            this.currentPathfindingInstanceId = null;
        }
        this.clearPathfindingTimeout();
    }
    clearPathfindingTimeout() {
        if (this.pathfindingTimeout !== null) {
            clearTimeout(this.pathfindingTimeout);
            this.pathfindingTimeout = null;
        }
    }
    setEasyStarGrid(grid) {
        this.grid = grid;
        this.easyStar.setGrid(grid);
        this.easyStar.setAcceptableTiles([
            0,
            2,
            3
        ]);
    }
}
class NativeMath {
    static isBetween(value, min, max) {
        return value >= min && value <= max;
    }
    static isOverlappingWithRectangle(p, r) {
        return this.isBetween(p.x, r.x, r.x + r.width) && this.isBetween(p.y, r.y, r.y + r.height);
    }
    static distanceBetween(p1, p2, squared = true) {
        const distance = Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2);
        return squared ? Math.sqrt(distance) : distance;
    }
}
class NativePlayer {
    async setPathToFollow(path, speed) {
        this.getBody().setDirectControl(true);
        const isPreviousPathInProgress = this.pathToFollow !== undefined && this.pathToFollow.length > 0;
        this.pathToFollow = this.adjustPathToFollowToColliderBounds(path);
        this.pathToFollow.unshift({
            x: this.x,
            y: this.y
        });
        this.pathWalkingSpeed = speed;
        this.currentPathSegmentDistanceFromStart = 0;
        return new Promise((resolve)=>{
            this.followingPathPromiseResolve?.call(this, {
                x: this.x,
                y: this.y,
                cancelled: isPreviousPathInProgress
            });
            this.followingPathPromiseResolve = resolve;
        });
    }
    getCurrentPathDestinationPoint(coordinates = "sprite") {
        if (!this.pathToFollow) {
            return undefined;
        }
        const destination = this.pathToFollow[this.pathToFollow.length - 1];
        if (destination && coordinates === "floor") {
            const body = this.getBody();
            return {
                x: destination.x,
                y: destination.y + body.height / 2 + body.offset.y
            };
        }
        return destination;
    }
    finishFollowingPath(cancelled = false) {
        let wasFollowing = false;
        if (this.pathToFollow || this.followingPathPromiseResolve) {
            wasFollowing = true;
        }
        this.pathToFollow = undefined;
        this.pathWalkingSpeed = undefined;
        this.currentPathSegmentDistanceFromStart = 0;
        this.stop();
        this.followingPathPromiseResolve?.call(this, {
            x: this.x,
            y: this.y,
            cancelled
        });
        this.getBody().setDirectControl(false);
        if (wasFollowing) {
            this.emit(hasMovedEventName, {
                moving: false,
                direction: this._lastDirection,
                x: this.x,
                y: this.y
            });
        }
    }
    deduceSpeed(speedUp, followMode) {
        return this.pathWalkingSpeed ? this.pathWalkingSpeed : speedUp && !followMode ? 2.5 * WOKA_SPEED : WOKA_SPEED;
    }
    adjustPathToFollowToColliderBounds(path) {
        return path.map((step)=>{
            return {
                x: step.x,
                y: step.y - this.getBody().height / 2 - this.getBody().offset.y
            };
        });
    }
    followPath(delta) {
        if (this.pathToFollow !== undefined && this.pathToFollow.length === 1) {
            this.finishFollowingPath();
        }
        if (!this.pathToFollow) {
            return;
        }
        let segmentStartPos = this.pathToFollow[0];
        let segmentEndPos = this.pathToFollow[1];
        let xDistance = segmentEndPos.x - segmentStartPos.x;
        let yDistance = segmentEndPos.y - segmentStartPos.y;
        let pathSegmentLength = Math.sqrt(Math.pow(xDistance, 2) + Math.pow(yDistance, 2));
        this.currentPathSegmentDistanceFromStart += this.deduceSpeed(false, false) * delta * 20 / 1000;
        while(this.currentPathSegmentDistanceFromStart >= pathSegmentLength){
            this.currentPathSegmentDistanceFromStart -= pathSegmentLength;
            this.pathToFollow.shift();
            if (this.pathToFollow.length === 1) {
                this.x = this.pathToFollow[0].x;
                this.y = this.pathToFollow[0].y;
                this.finishFollowingPath();
                return;
            }
            segmentStartPos = this.pathToFollow[0];
            segmentEndPos = this.pathToFollow[1];
            xDistance = segmentEndPos.x - segmentStartPos.x;
            yDistance = segmentEndPos.y - segmentStartPos.y;
            pathSegmentLength = Math.sqrt(Math.pow(xDistance, 2) + Math.pow(yDistance, 2));
        }
        const newX = segmentStartPos.x + this.currentPathSegmentDistanceFromStart / pathSegmentLength * (segmentEndPos.x - segmentStartPos.x);
        const newY = segmentStartPos.y + this.currentPathSegmentDistanceFromStart / pathSegmentLength * (segmentEndPos.y - segmentStartPos.y);
        this.moveToPos(newX, newY);
        this.emit(hasMovedEventName, {
            moving: true,
            direction: this._lastDirection,
            x: this.x,
            y: this.y
        });
        this.scene.markDirty();
    }
    moveToPos(x, y) {
        const oldX = this.x;
        const oldY = this.y;
        this.x = x;
        this.y = y;
        if (Math.abs(x - oldX) > Math.abs((y - oldY) * 1.1)) {
            if (x < oldX) {
                this._lastDirection = PositionMessage_Direction.LEFT;
            } else if (x > oldX) {
                this._lastDirection = PositionMessage_Direction.RIGHT;
            }
        } else {
            if (y < oldY) {
                this._lastDirection = PositionMessage_Direction.UP;
            } else if (y > oldY) {
                this._lastDirection = PositionMessage_Direction.DOWN;
            }
        }
        passStatusToOnline();
        this.playAnimation(this._lastDirection, true);
        this.setDepth(this.y + 16);
        if (this.companion) {
            this.companion.setTarget(this.x, this.y, this._lastDirection);
        }
    }
}
class NativeScene {
    async moveTo(position, tryFindingNearestAvailable = false, speed = undefined) {
        const request = {
            position: {
                ...position
            },
            speed,
            tryFindingNearestAvailable
        };
        this.pendingMoveTo = request;
        try {
            const path = await this.getPathfindingManager().findPathFromGameCoordinates({
                x: this.CurrentPlayer.x,
                y: this.CurrentPlayer.y
            }, request.position, tryFindingNearestAvailable);
            if (this.pendingMoveTo !== request) {
                return {
                    x: this.CurrentPlayer.x,
                    y: this.CurrentPlayer.y,
                    cancelled: true
                };
            }
            if (path.length === 0) throw new Error("No path found");
            return this.CurrentPlayer.setPathToFollow(path, speed ?? this.CurrentPlayer.walkingSpeed);
        } finally{
            if (this.pendingMoveTo === request) {
                this.pendingMoveTo = undefined;
            }
        }
    }
    subscribeToGameMapChanged() {
        this.gameMapChangedSubscription?.unsubscribe();
        this.gameMapChangedSubscription = this.gameMapFrontWrapper.getMapChangedObservable().subscribe((collisionGrid)=>{
            this.pathfindingManager.setCollisionGrid(collisionGrid);
            this.markDirty();
            const pendingMove = this.pendingMoveTo;
            if (pendingMove) {
                this.moveTo(pendingMove.position, pendingMove.tryFindingNearestAvailable, pendingMove.speed).catch((reason)=>console.warn(reason));
                return;
            }
            const playerDestination = this.CurrentPlayer.getCurrentPathDestinationPoint("floor");
            if (playerDestination) {
                this.moveTo(playerDestination, true).catch((reason)=>console.warn(reason));
            }
        });
    }
}
class NativeWrapper {
    setLayerVisibility(layerName, visible) {
        const phaserLayer = this.findPhaserLayer(layerName);
        if (phaserLayer != undefined) {
            phaserLayer.setVisible(visible);
            phaserLayer.setCollisionByProperty({
                collides: true
            }, visible);
            this.updateCollisionGrid(phaserLayer);
        } else {
            const phaserLayers = this.findPhaserLayers(layerName + "/");
            if (phaserLayers.length === 0) {
                console.warn('Could not find layer with name that contains "' + layerName + '" when calling WA.hideLayer / WA.showLayer');
                return;
            }
            for(let i = 0; i < phaserLayers.length; i++){
                phaserLayers[i].setVisible(visible);
                phaserLayers[i].setCollisionByProperty({
                    collides: true
                }, visible);
            }
            this.updateCollisionGrid(undefined, false);
        }
    }
    findPhaserLayer(layerName) {
        return this.phaserLayers.find((layer)=>layer.layer.name === layerName);
    }
    findPhaserLayers(groupName) {
        return this.phaserLayers.filter((l)=>l.layer.name.includes(groupName));
    }
    getLayerCollisionGrid(layer) {
        let isExitLayer = false;
        const isStartLayer = layer.layer.name === "start";
        for (const property of layer.layer.properties){
            if (property.name && property.name === "exitUrl") {
                isExitLayer = true;
            }
        }
        return layer.layer.data.map((row)=>row.map((tile)=>tile.properties?.[GameMapProperties.COLLIDES] ? 1 : isExitLayer && tile.index !== -1 || tile.properties?.[GameMapProperties.EXIT_URL] || tile.properties?.[GameMapProperties.EXIT_SCENE_URL] ? 2 : isStartLayer && tile.index !== -1 || tile.properties?.[GameMapProperties.START] || tile.properties?.[GameMapProperties.START_LAYER] ? 3 : 0));
    }
    updateCollisionGrid(modifiedLayer, useCache = true) {
        const map = this.gameMap.getMap();
        if (map.height === undefined || map.width === undefined) {
            this.collisionGrid = [];
            return;
        }
        const grid = Array.from(Array(map.height), (_)=>Array(map.width).fill(0));
        if (modifiedLayer) {
            this.perLayerCollisionGridCache.set(modifiedLayer.layerIndex, this.getLayerCollisionGrid(modifiedLayer));
        }
        for (const layer of this.phaserLayers){
            if (!layer.visible && layer !== this.entitiesCollisionLayer && layer !== this.areasCollisionLayer) {
                continue;
            }
            if (!useCache) {
                this.perLayerCollisionGridCache.set(layer.layerIndex, this.getLayerCollisionGrid(layer));
            }
            const cachedLayer = this.perLayerCollisionGridCache.get(layer.layerIndex);
            if (!cachedLayer) {
                this.perLayerCollisionGridCache.set(layer.layerIndex, this.getLayerCollisionGrid(layer));
            } else {
                for(let y = 0; y < map.height; y += 1){
                    for(let x = 0; x < map.width; x += 1){
                        if (grid[y][x] === 2 && cachedLayer[y][x] === 1) {
                            grid[y][x] = cachedLayer[y][x];
                            continue;
                        }
                        if (grid[y][x] === 3 && cachedLayer[y][x] === 1) {
                            grid[y][x] = cachedLayer[y][x];
                            continue;
                        }
                        if (grid[y][x] !== 0) {
                            continue;
                        }
                        grid[y][x] = cachedLayer[y][x];
                    }
                }
            }
        }
        this.collisionGrid = grid;
        this.mapChangedSubject.next(this.collisionGrid);
    }
}
class NativePointer {
    handlePointerUpEvent(pointer, gameObjects) {
        if (get(mapEditorToolbarInUseStore)) {
            return;
        }
        if (pointer.wasTouch || pointer.leftButtonReleased()) {
            for (const object of gameObjects){
                if (isActivatable(object)) {
                    if (object instanceof RemotePlayer && get(botEditorToolActiveStore)) {
                        return;
                    }
                    this.gameScene.getActivatablesManager().handlePointerDownEvent(object);
                    return;
                }
            }
            if (!get(botEditorToolActiveStore) && this.gameScene.userInputManager.isControlsEnabled && isQuickTap(pointer) && gameObjects.includes(this.gameScene.CurrentPlayer)) {
                toggleMyCard(localUserStore.getLocalUser()?.uuid);
                return;
            }
        }
        if (!pointer.wasTouch && pointer.leftButtonReleased() || pointer.getDuration() > 250) {
            return;
        }
        if (!this.gameScene.userInputManager.isControlsEnabled) {
            return;
        }
        if (!this.gameScene.userInputManager.isRightClickEnabled) {
            return;
        }
        for (const object of gameObjects){
            if (object instanceof Player || object instanceof RemotePlayer) {
                return;
            }
        }
        const camera = this.gameScene.getCameraManager().getCamera();
        this.gameScene.moveTo({
            x: pointer.x + camera.scrollX,
            y: pointer.y + camera.scrollY
        }, true).catch((reason)=>{
            console.warn(reason);
        });
    }
}
globalThis.classes = {
    PathfindingManager,
    NativeMath,
    NativePlayer,
    NativeScene,
    NativeWrapper,
    NativePointer
};
