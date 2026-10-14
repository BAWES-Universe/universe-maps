export class HdpiManager {
    /**
     *
     * @param minRecommendedGamePixelsNumber The minimum number of pixels we want to display "by default" to the user
     * @param absoluteMinPixelNumber The very minimum of game pixels to display. Below, we forbid zooming more
     */
    constructor(minRecommendedGamePixelsNumber, absoluteMinPixelNumber) {
        this.minRecommendedGamePixelsNumber = minRecommendedGamePixelsNumber;
        this.absoluteMinPixelNumber = absoluteMinPixelNumber;
        this._zoomModifier = 1;
        this._maxZoomOut = 1;
        this._optimalZoomLevel = 1;
        this._maxZoomInReached = false;
    }
    /**
     * Returns the optimal size in "game pixels" based on the screen size in "real pixels".
     *
     * Note: the function is returning the optimal size in "game pixels" in the "game" property,
     * but also recommends resizing the "real" pixel screen size of the canvas.
     * The proposed new real size is a few pixels bigger than the real size available (if the size is not a multiple of the pixel size) and should overflow.
     *
     * @param realPixelScreenSize
     */
    getOptimalGameSize(realPixelScreenSize) {
        this._maxZoomInReached = false;
        const realPixelNumber = realPixelScreenSize.width * realPixelScreenSize.height;
        // If the screen has not a definition small enough to match the minimum number of pixels we want to display,
        // let's make the canvas the size of the screen (in real pixels)
        if (realPixelNumber <= this.minRecommendedGamePixelsNumber) {
            return {
                game: realPixelScreenSize,
                real: realPixelScreenSize,
            };
        }
        this._optimalZoomLevel = this.getOptimalZoomLevel(realPixelNumber);
        // Has the canvas more pixels than the screen? This is forbidden
        if (this.isMaximumZoomReached) {
            // Let's reset the zoom modifier (WARNING this is a SIDE EFFECT in a getter)
            this._zoomModifier = Math.min(this._maxZoomOut / this._optimalZoomLevel, this._zoomOutPastMapFit ?? Number.POSITIVE_INFINITY);
            const maxGameWidth = Math.ceil(realPixelScreenSize.width / this._optimalZoomLevel / this._zoomModifier);
            const maxGameHeight = Math.ceil(realPixelScreenSize.height / this._optimalZoomLevel / this._zoomModifier);
            return {
                game: {
                    width: maxGameWidth,
                    height: maxGameHeight,
                },
                real: realPixelScreenSize,
            };
        }
        const gameWidth = Math.ceil(realPixelScreenSize.width / this._optimalZoomLevel / this._zoomModifier);
        const gameHeight = Math.ceil(realPixelScreenSize.height / this._optimalZoomLevel / this._zoomModifier);
        // Let's ensure we display a minimum of pixels, even if crazily zoomed in.
        if (gameWidth * gameHeight < this.absoluteMinPixelNumber) {
            this._maxZoomInReached = true;
            const minGameHeight = Math.sqrt((this.absoluteMinPixelNumber * realPixelScreenSize.height) / realPixelScreenSize.width);
            const minGameWidth = Math.sqrt((this.absoluteMinPixelNumber * realPixelScreenSize.width) / realPixelScreenSize.height);
            // Let's reset the zoom modifier (WARNING this is a SIDE EFFECT in a getter)
            this._zoomModifier = realPixelScreenSize.width / minGameWidth / this._optimalZoomLevel;
            return {
                game: {
                    width: minGameWidth,
                    height: minGameHeight,
                },
                real: realPixelScreenSize,
            };
        }
        return {
            game: {
                width: gameWidth,
                height: gameHeight,
            },
            real: {
                width: Math.ceil(realPixelScreenSize.width / this._optimalZoomLevel) * this._optimalZoomLevel,
                height: Math.ceil(realPixelScreenSize.height / this._optimalZoomLevel) * this._optimalZoomLevel,
            },
        };
    }
    /**
     * We only accept integer but we make an exception for 1.5
     */
    getOptimalZoomLevel(realPixelNumber) {
        const result = Math.sqrt(realPixelNumber / this.minRecommendedGamePixelsNumber);
        if (1.5 <= result && result < 2) {
            return 1.5;
        }
        else {
            return Math.floor(result);
        }
    }
    get zoomModifier() {
        return this._zoomModifier;
    }
    set zoomModifier(zoomModifier) {
        this._zoomModifier = zoomModifier;
    }
    set maxZoomOut(maxZoomOut) {
        this._maxZoomOut = maxZoomOut;
    }
    get maxZoomOut() {
        return this._maxZoomOut;
    }
    /**
     * How far zooming out may go past the point where the whole map fits (a zoom modifier); undefined stops there.
     * Scrolling out in play has to get through to "Look around", even on a map small enough to fit the screen first.
     */
    set zoomOutPastMapFit(zoomModifier) {
        this._zoomOutPastMapFit = zoomModifier;
    }
    get isMaximumZoomReached() {
        const mapFits = this._optimalZoomLevel * this._zoomModifier <= this._maxZoomOut;
        if (this._zoomOutPastMapFit === undefined)
            return mapFits;
        return mapFits && this._zoomModifier <= this._zoomOutPastMapFit;
    }
    get isMaximumZoomInReached() {
        return this._maxZoomInReached;
    }
}
