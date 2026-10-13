"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.PathfindingManager = exports.PathTileType = void 0;
var PathTileType;
(function (PathTileType) {
    PathTileType[PathTileType["Walkable"] = 0] = "Walkable";
    PathTileType[PathTileType["Collider"] = 1] = "Collider";
    PathTileType[PathTileType["Exit"] = 2] = "Exit";
    PathTileType[PathTileType["Start"] = 3] = "Start";
})(PathTileType || (exports.PathTileType = PathTileType = {}));
class PathfindingManager {
    easyStar;
    grid;
    tileDimensions;
    currentPathfindingInstanceId = null;
    pathfindingTimeout = null;
    pathfindingRequestId = 0;
    resolveCancelledPath;
    constructor(collisionsGrid, tileDimensions) {
        this.easyStar = new EasyStar.js();
        this.easyStar.enableDiagonals();
        this.easyStar.disableCornerCutting();
        this.easyStar.setTileCost(PathTileType.Exit, 100);
        this.easyStar.setIterationsPerCalculation(1000);
        this.grid = collisionsGrid;
        this.tileDimensions = tileDimensions;
        this.setEasyStarGrid(collisionsGrid);
        //this.logGridToTheConsole(collisionsGrid);
    }
    setCollisionGrid(collisionGrid) {
        this.setEasyStarGrid(collisionGrid);
    }
    /**
     * Clean up any ongoing pathfinding operations
     */
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
            // Replace the first element of the path with the actual start position
            path[0] = { x: start.x, y: start.y + this.tileDimensions.height * 0.5 }; // We need to add half of the tile height to get the bottom center of the tile as long as the player origin is centered
        }
        if (path.length > 0 && result.isExactTarget) {
            // Let's put back the exact position.
            // Actually, we are not targeting always the absolutely exact pixel-perfect position.
            // Indeed, we want the hitbox of the sprite to be completely inside the tile.
            // Otherwise, the hitbox of the sprite could overflow a collide tile, so the player could use
            // his keyboard to move the sprite inside the wall.
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
        return { x, y };
    }
    async findPath(start, end, tryFindingNearestAvailable, requestId) {
        let isExactTarget = true;
        let endPoints = [end];
        if (tryFindingNearestAvailable) {
            endPoints = [
                end,
                ...this.getNeighbouringTiles(end).sort((a, b) => {
                    const aDist = MathUtils.distanceBetween(a, start, false);
                    const bDist = MathUtils.distanceBetween(b, start, false);
                    if (aDist > bDist) {
                        return 1;
                    }
                    if (aDist < bDist) {
                        return -1;
                    }
                    return 0;
                }),
            ];
        }
        let path = [];
        while (endPoints.length > 0) {
            const endPoint = endPoints.shift();
            if (!endPoint) {
                return { path: [], isExactTarget: false };
            }
            // rejected Promise will return undefined for path
            // eslint-disable-next-line no-await-in-loop
            path = await this.getPath(start, endPoint).catch();
            // A cancelled request must not try another neighbour or cancel the newer request.
            if (requestId !== this.pathfindingRequestId) {
                return { path: [], isExactTarget: false };
            }
            if (path && path.length > 0) {
                return { path: this.mapTileUnitsToPixels(path), isExactTarget };
            }
            isExactTarget = false;
        }
        return { path: [], isExactTarget: false };
    }
    mapTileUnitsToPixels(path) {
        return path.map(this.mapTileUnitToPixels.bind(this));
    }
    mapTileUnitToPixels(tilePosition) {
        return {
            x: tilePosition.x * this.tileDimensions.width + this.tileDimensions.width * 0.5,
            y: tilePosition.y * this.tileDimensions.height + this.tileDimensions.height * 0.5,
        };
    }
    mapPixelsToTileUnits(position) {
        return {
            x: Math.floor(position.x / this.tileDimensions.width),
            y: Math.floor(position.y / this.tileDimensions.height),
        };
    }
    getNeighbouringTiles(tile) {
        const xOffsets = [-1, 0, 1, 1, 1, 0, -1, -1];
        const yOffsets = [-1, -1, -1, 0, 1, 1, 1, 0];
        const neighbours = [];
        for (let i = 0; i < 8; i += 1) {
            const tileToCheck = { x: tile.x + xOffsets[i], y: tile.y + yOffsets[i] };
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
    /**
     * Takes a position in pixels and returns it.
     * It the position is out of the bounds of the map, takes the closest position within the map.
     */
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
        return { x, y };
    }
    /**
     * Returns empty array if path was not found
     */
    async getPath(start, end) {
        // EasyStar returns [] for start=end, even on a blocked tile. A walkable same-tile
        // destination is a valid path; keep one point so the exact within-tile fit is applied.
        if (start.x === end.x && start.y === end.y) {
            const tile = this.grid[end.y]?.[end.x];
            return tile === PathTileType.Walkable || tile === PathTileType.Exit || tile === PathTileType.Start
                ? [{ ...end }]
                : [];
        }
        return new Promise((resolve) => {
            let pathFound = false;
            this.resolveCancelledPath = () => {
                pathFound = true;
                resolve([]);
            };
            let calculationCount = 0;
            const maxCalculations = 50; // Maximum number of calculate() iterations
            const maxTimeMs = 3000; // Maximum time in milliseconds (3 seconds)
            const startTime = Date.now();
            // Store the instance ID for potential cancellation
            this.currentPathfindingInstanceId = this.easyStar.findPath(start.x, start.y, end.x, end.y, (path) => {
                if (pathFound)
                    return; // Already resolved
                pathFound = true;
                this.resolveCancelledPath = undefined;
                this.clearPathfindingTimeout();
                this.currentPathfindingInstanceId = null;
                if (path === null) {
                    resolve([]);
                }
                else {
                    resolve(path);
                }
            });
            // Function to perform calculation with retry logic
            const performCalculation = () => {
                if (pathFound)
                    return; // Path already found
                const currentTime = Date.now();
                if (currentTime - startTime > maxTimeMs) {
                    // Timeout reached
                    this.cancelCurrentPathfinding();
                    console.warn("Pathfinding timeout reached, returning empty path");
                    resolve([]);
                    return;
                }
                calculationCount++;
                if (calculationCount > maxCalculations) {
                    // Too many calculations, probably no path exists
                    this.cancelCurrentPathfinding();
                    console.warn("Pathfinding max calculations reached, returning empty path");
                    resolve([]);
                    return;
                }
                // Perform one iteration of pathfinding calculation
                this.easyStar.calculate();
                // If no path found yet, schedule next calculation
                if (!pathFound) {
                    this.pathfindingTimeout = window.setTimeout(performCalculation, 10); // 10ms delay between calculations
                }
            };
            // Start the calculation process
            performCalculation();
        });
    }
    /**
     * Cancel the current pathfinding operation if one is in progress
     */
    cancelCurrentPathfinding() {
        this.resolveCancelledPath?.();
        this.resolveCancelledPath = undefined;
        if (this.currentPathfindingInstanceId !== null) {
            this.easyStar.cancelPath(this.currentPathfindingInstanceId);
            this.currentPathfindingInstanceId = null;
        }
        this.clearPathfindingTimeout();
    }
    /**
     * Clear the pathfinding timeout
     */
    clearPathfindingTimeout() {
        if (this.pathfindingTimeout !== null) {
            clearTimeout(this.pathfindingTimeout);
            this.pathfindingTimeout = null;
        }
    }
    setEasyStarGrid(grid) {
        this.grid = grid;
        this.easyStar.setGrid(grid);
        this.easyStar.setAcceptableTiles([PathTileType.Walkable, PathTileType.Exit, PathTileType.Start]);
    }
}
exports.PathfindingManager = PathfindingManager;
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
        // take collider offset into consideration
        this.pathToFollow = this.adjustPathToFollowToColliderBounds(path);
        this.pathToFollow.unshift({ x: this.x, y: this.y });
        this.pathWalkingSpeed = speed;
        this.currentPathSegmentDistanceFromStart = 0;
        return new Promise((resolve) => {
            this.followingPathPromiseResolve?.call(this, { x: this.x, y: this.y, cancelled: isPreviousPathInProgress });
            this.followingPathPromiseResolve = resolve;
        });
    }
    getCurrentPathDestinationPoint(coordinates = "sprite") {
        if (!this.pathToFollow) {
            return undefined;
        }
        const destination = this.pathToFollow[this.pathToFollow.length - 1];
        if (destination && coordinates === "floor") {
            // Reverse adjustPathToFollowToColliderBounds for GameScene.moveTo.
            const body = this.getBody();
            return { x: destination.x, y: destination.y + body.height / 2 + body.offset.y };
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
        this.followingPathPromiseResolve?.call(this, { x: this.x, y: this.y, cancelled });
        this.getBody().setDirectControl(false);
        if (wasFollowing) {
            this.emit(hasMovedEventName, { moving: false, direction: this._lastDirection, x: this.x, y: this.y });
        }
    }
    deduceSpeed(speedUp, followMode) {
        return this.pathWalkingSpeed ? this.pathWalkingSpeed : speedUp && !followMode ? 2.5 * WOKA_SPEED : WOKA_SPEED;
    }
    adjustPathToFollowToColliderBounds(path) {
        return path.map((step) => {
            return { x: step.x, y: step.y - this.getBody().height / 2 - this.getBody().offset.y };
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
        // Compute movement direction
        let xDistance = segmentEndPos.x - segmentStartPos.x;
        let yDistance = segmentEndPos.y - segmentStartPos.y;
        let pathSegmentLength = Math.sqrt(Math.pow(xDistance, 2) + Math.pow(yDistance, 2));
        this.currentPathSegmentDistanceFromStart += (this.deduceSpeed(false, false) * delta * 20) / 1000;
        while (this.currentPathSegmentDistanceFromStart >= pathSegmentLength) {
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
            // Compute movement direction
            xDistance = segmentEndPos.x - segmentStartPos.x;
            yDistance = segmentEndPos.y - segmentStartPos.y;
            pathSegmentLength = Math.sqrt(Math.pow(xDistance, 2) + Math.pow(yDistance, 2));
        }
        const newX = segmentStartPos.x +
            (this.currentPathSegmentDistanceFromStart / pathSegmentLength) * (segmentEndPos.x - segmentStartPos.x);
        const newY = segmentStartPos.y +
            (this.currentPathSegmentDistanceFromStart / pathSegmentLength) * (segmentEndPos.y - segmentStartPos.y);
        this.moveToPos(newX, newY);
        this.emit(hasMovedEventName, { moving: true, direction: this._lastDirection, x: this.x, y: this.y });
        this.scene.markDirty();
        /*if (distance < 200) {
            this.pathToFollow.shift();
        }
        return this.getMovementDirection(xDistance, yDistance, distance);*/
    }
    moveToPos(x, y) {
        const oldX = this.x;
        const oldY = this.y;
        this.x = x;
        this.y = y;
        // The 1.1 ratio to y is applied here because in path finding mode, the player often moves in diagonal.
        // In diagonal, the amount of x and y are almost equal. This produces a graphical glitch where on one frame,
        // the player goes left, and on the next frame, the player goes up. This is because the x and y are almost equal.
        // To fix this, we apply a ratio of 1.1 to y to make sure that the player goes up/down when the y and x are almost equal.
        if (Math.abs(x - oldX) > Math.abs((y - oldY) * 1.1)) {
            if (x < oldX) {
                this._lastDirection = PositionMessage_Direction.LEFT;
            }
            else if (x > oldX) {
                this._lastDirection = PositionMessage_Direction.RIGHT;
            }
        }
        else {
            if (y < oldY) {
                this._lastDirection = PositionMessage_Direction.UP;
            }
            else if (y > oldY) {
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
        const request = { position: { ...position }, speed, tryFindingNearestAvailable };
        this.pendingMoveTo = request;
        try {
            const path = await this.getPathfindingManager().findPathFromGameCoordinates({
                x: this.CurrentPlayer.x,
                y: this.CurrentPlayer.y,
            }, request.position, tryFindingNearestAvailable);
            if (this.pendingMoveTo !== request) {
                return { x: this.CurrentPlayer.x, y: this.CurrentPlayer.y, cancelled: true };
            }
            if (path.length === 0)
                throw new Error("No path found");
            return this.CurrentPlayer.setPathToFollow(path, speed ?? this.CurrentPlayer.walkingSpeed);
        }
        finally {
            if (this.pendingMoveTo === request) {
                this.pendingMoveTo = undefined;
            }
        }
    }
    subscribeToGameMapChanged() {
        this.gameMapChangedSubscription?.unsubscribe();
        this.gameMapChangedSubscription = this.gameMapFrontWrapper
            .getMapChangedObservable()
            .subscribe((collisionGrid) => {
            this.pathfindingManager.setCollisionGrid(collisionGrid);
            this.markDirty();
            // A newer click may still be calculating while the previous path is being followed.
            const pendingMove = this.pendingMoveTo;
            if (pendingMove) {
                this.moveTo(pendingMove.position, pendingMove.tryFindingNearestAvailable, pendingMove.speed).catch((reason) => console.warn(reason));
                return;
            }
            const playerDestination = this.CurrentPlayer.getCurrentPathDestinationPoint("floor");
            if (playerDestination) {
                this.moveTo(playerDestination, true).catch((reason) => console.warn(reason));
            }
        });
    }
}
class NativeWrapper {
    setLayerVisibility(layerName, visible) {
        const phaserLayer = this.findPhaserLayer(layerName);
        if (phaserLayer != undefined) {
            phaserLayer.setVisible(visible);
            phaserLayer.setCollisionByProperty({ collides: true }, visible);
            this.updateCollisionGrid(phaserLayer);
        }
        else {
            const phaserLayers = this.findPhaserLayers(layerName + "/");
            if (phaserLayers.length === 0) {
                console.warn('Could not find layer with name that contains "' +
                    layerName +
                    '" when calling WA.hideLayer / WA.showLayer');
                return;
            }
            for (let i = 0; i < phaserLayers.length; i++) {
                phaserLayers[i].setVisible(visible);
                phaserLayers[i].setCollisionByProperty({ collides: true }, visible);
            }
            this.updateCollisionGrid(undefined, false);
        }
    }
    findPhaserLayer(layerName) {
        return this.phaserLayers.find((layer) => layer.layer.name === layerName);
    }
    findPhaserLayers(groupName) {
        return this.phaserLayers.filter((l) => l.layer.name.includes(groupName));
    }
    getLayerCollisionGrid(layer) {
        let isExitLayer = false;
        const isStartLayer = layer.layer.name === "start";
        for (const property of layer.layer.properties) {
            if (property.name && property.name === "exitUrl") {
                isExitLayer = true;
            }
        }
        return layer.layer.data.map((row) => row.map((tile) => tile.properties?.[GameMapProperties.COLLIDES]
            ? 1
            : (isExitLayer && tile.index !== -1) ||
                tile.properties?.[GameMapProperties.EXIT_URL] ||
                tile.properties?.[GameMapProperties.EXIT_SCENE_URL]
                ? 2
                : (isStartLayer && tile.index !== -1) ||
                    tile.properties?.[GameMapProperties.START] ||
                    tile.properties?.[GameMapProperties.START_LAYER]
                    ? 3
                    : 0));
    }
    updateCollisionGrid(modifiedLayer, useCache = true) {
        const map = this.gameMap.getMap();
        // initialize collision grid to write on
        if (map.height === undefined || map.width === undefined) {
            this.collisionGrid = [];
            return;
        }
        const grid = Array.from(Array(map.height), (_) => Array(map.width).fill(PathTileType.Walkable));
        if (modifiedLayer) {
            // recalculate cache for certain layer if needed
            this.perLayerCollisionGridCache.set(modifiedLayer.layerIndex, this.getLayerCollisionGrid(modifiedLayer));
        }
        // go through all tilemap layers on map. Maintain order
        for (const layer of this.phaserLayers) {
            if (!layer.visible && layer !== this.entitiesCollisionLayer && layer !== this.areasCollisionLayer) {
                continue;
            }
            if (!useCache) {
                this.perLayerCollisionGridCache.set(layer.layerIndex, this.getLayerCollisionGrid(layer));
            }
            const cachedLayer = this.perLayerCollisionGridCache.get(layer.layerIndex);
            if (!cachedLayer) {
                // no cache, calculate collision grid for this layer
                this.perLayerCollisionGridCache.set(layer.layerIndex, this.getLayerCollisionGrid(layer));
            }
            else {
                for (let y = 0; y < map.height; y += 1) {
                    for (let x = 0; x < map.width; x += 1) {
                        // currently no case where we can make tile non-collidable with collidable object beneath, skip position
                        if (grid[y][x] === PathTileType.Exit && cachedLayer[y][x] === PathTileType.Collider) {
                            grid[y][x] = cachedLayer[y][x];
                            continue;
                        }
                        if (grid[y][x] === PathTileType.Start && cachedLayer[y][x] === PathTileType.Collider) {
                            grid[y][x] = cachedLayer[y][x];
                            continue;
                        }
                        if (grid[y][x] !== PathTileType.Walkable) {
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
    getDynamicAreasOnPosition(position, offsetY = 16) {
        const overlappedDynamicAreas = [];
        for (const dynamicArea of this.dynamicAreas.values()) {
            if (MathUtils.isOverlappingWithRectangle({ x: position.x, y: position.y + offsetY }, { x: dynamicArea.x, y: dynamicArea.y, width: dynamicArea.width, height: dynamicArea.height })) {
                overlappedDynamicAreas.push(dynamicArea);
            }
        }
        return overlappedDynamicAreas;
    }
    triggerDynamicAreasChange(oldPosition, position) {
        const areasByOldPosition = oldPosition ? this.getDynamicAreasOnPosition(oldPosition) : [];
        const areasByNewPosition = position ? this.getDynamicAreasOnPosition(position) : [];
        const enterAreas = new Set(areasByNewPosition);
        const leaveAreas = new Set(areasByOldPosition);
        enterAreas.forEach((area) => {
            if (leaveAreas.has(area)) {
                leaveAreas.delete(area);
                enterAreas.delete(area);
            }
        });
        let areasChange = false;
        if (enterAreas.size > 0) {
            const areasArray = Array.from(enterAreas);
            for (const callback of this.enterDynamicAreaCallbacks) {
                callback(areasArray, areasByNewPosition);
            }
            areasChange = true;
        }
        if (leaveAreas.size > 0) {
            const areasArray = Array.from(leaveAreas);
            for (const callback of this.leaveDynamicAreaCallbacks) {
                callback(areasArray, areasByNewPosition);
            }
            areasChange = true;
        }
        return areasChange;
    }
}
class NativePointer {
    handlePointerUpEvent(pointer, gameObjects) {
        // While editing the room, a tap on the map is for the editor (place, select, pan): it never walks you there.
        // Looking around is not editing: a tap on someone still opens their card, as it always did.
        if (get(mapEditorToolbarInUseStore)) {
            return;
        }
        if (pointer.wasTouch || pointer.leftButtonReleased()) {
            for (const object of gameObjects) {
                if (isActivatable(object)) {
                    // While the bot editor is open, clicks on the map are for placing and moving bots:
                    // don't open an avatar's card over the editor (your own card is skipped below).
                    if (object instanceof RemotePlayer && get(botEditorToolActiveStore)) {
                        return;
                    }
                    this.gameScene.getActivatablesManager().handlePointerDownEvent(object);
                    return;
                }
            }
            // Your own avatar: a quick tap or click opens your card (a hold or a joystick drag from it doesn't),
            // except while the bot editor is open.
            if (!get(botEditorToolActiveStore) &&
                this.gameScene.userInputManager.isControlsEnabled &&
                isQuickTap(pointer) &&
                gameObjects.includes(this.gameScene.CurrentPlayer)) {
                toggleMyCard(localUserStore.getLocalUser()?.uuid);
                return;
            }
        }
        if ((!pointer.wasTouch && pointer.leftButtonReleased()) || pointer.getDuration() > 250) {
            return;
        }
        if (!this.gameScene.userInputManager.isControlsEnabled) {
            return;
        }
        // If right click is disabled, we don't want to move the player
        if (!this.gameScene.userInputManager.isRightClickEnabled) {
            return;
        }
        for (const object of gameObjects) {
            if (object instanceof Player || object instanceof RemotePlayer) {
                return;
            }
        }
        const camera = this.gameScene.getCameraManager().getCamera();
        this.gameScene
            .moveTo({
            x: pointer.x + camera.scrollX,
            y: pointer.y + camera.scrollY,
        }, true)
            .catch((reason) => {
            console.warn(reason);
        });
    }
}
class NativeCamera {
    enterFocusMode(focusOn, margin = 0, duration = 1000, 
    // False when going back to a focus a drag left: the zoom saved on the way in is still the one to go back to.
    saveZoom = true) {
        this.dragFocus = undefined;
        this.freedByDrag = false;
        this.clearDragListener();
        this.focusMargin = margin;
        this.setCameraMode(CameraMode.Focus);
        this.followedRemotePlayerUuid = undefined;
        if (saveZoom) {
            this.waScaleManager.saveZoom();
        }
        this.waScaleManager.setFocusTarget(focusOn);
        this.cameraLocked = false;
        this.zoomLocked = false;
        this.restoreZoomTween?.stop();
        this.startFollowTween?.stop();
        //Set the camera to focus on the given point
        const focusPoint = {
            x: focusOn.x,
            y: focusOn.y,
        };
        this.camera.startFollow(focusPoint, true);
        this.playerToFollow = undefined;
        const currentZoomModifier = this.waScaleManager.zoomModifier;
        const zoomModifierChange = this.getZoomModifierChange(focusOn.width, focusOn.height, 1 + margin);
        if (duration === 0) {
            this.waScaleManager.zoomModifier = currentZoomModifier + zoomModifierChange;
            this.camera.centerOn(focusOn.x, focusOn.y);
            this.emit(CameraManagerEvent.CameraUpdate, this.getCameraUpdateEventData());
            return;
        }
        this.stopPan();
        this.camera.pan(focusOn.x, focusOn.y, duration, Easing.SineEaseOut, true, (camera, progress, x, y) => {
            if (zoomModifierChange) {
                this.waScaleManager.zoomModifier = currentZoomModifier + progress * zoomModifierChange;
            }
            if (progress === 1) {
                // NOTE: Making sure the last action will be centering after zoom change
                this.camera.centerOn(focusOn.x, focusOn.y);
            }
            this.emit(CameraManagerEvent.CameraUpdate, this.getCameraUpdateEventData());
        });
    }
    leaveFocusMode(player, duration = 0) {
        this.waScaleManager.setFocusTarget();
        this.unlockCameraWithDelay(duration);
        this.startFollowPlayer(player, duration);
        this.restoreZoom(duration);
    }
    getZoomModifierChange(width, height, multiplier = 1) {
        if (!width || !height) {
            return 0;
        }
        const targetZoomModifier = this.waScaleManager.getTargetZoomModifierFor(width * multiplier, height * multiplier);
        const currentZoomModifier = this.waScaleManager.zoomModifier;
        return targetZoomModifier - currentZoomModifier;
    }
    restoreZoom(duration = 0) {
        if (duration === 0) {
            this.waScaleManager.zoomModifier = this.waScaleManager.getSaveZoom();
            return;
        }
        this.animationInProgress = true;
        this.restoreZoomTween?.stop();
        this.restoreZoomTween = this.scene.tweens.addCounter({
            from: this.waScaleManager.zoomModifier,
            to: this.waScaleManager.getSaveZoom(),
            duration,
            ease: Easing.SineEaseOut,
            onUpdate: (tween) => {
                this.waScaleManager.zoomModifier = tween.getValue() ?? 0;
                this.emit(CameraManagerEvent.CameraUpdate, this.getCameraUpdateEventData());
            },
            onComplete: () => {
                this.animationInProgress = false;
            },
        });
    }
}
globalThis.classes = { PathfindingManager, NativePlayer, NativeScene, NativeWrapper, NativePointer, NativeCamera, NativeMath };
