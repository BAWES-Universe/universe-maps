from pathlib import Path
import difflib, json, hashlib
ROOT=Path(__file__).resolve().parent
PIN=ROOT/'pinned-source'
OUT=ROOT/'engine-patch'
PATHS={'CameraManager.ts':'play/src/front/Phaser/Game/CameraManager.ts','GameScene.ts':'play/src/front/Phaser/Game/GameScene.ts','camera.ts':'play/src/front/Api/Iframe/camera.ts','IframeListener.ts':'play/src/front/Api/IframeListener.ts','IframeEvent.ts':'play/src/front/Api/Events/IframeEvent.ts'}
sources={name:(PIN/name).read_text() for name in PATHS}
modified=dict(sources)
modified['CameraManager.ts']=modified['CameraManager.ts'].replace('    private cameraLocked: boolean;','    private cameraLocked: boolean;\n    private viewportUpdatePending = false;\n    private viewportAutomationDisabled = false;\n    private readonly emitViewportUpdate = (): void => {\n        this.viewportUpdatePending = false;\n        this.emit(CameraManagerEvent.CameraUpdate, this.getCameraUpdateEventData());\n    };')
modified['CameraManager.ts']=modified['CameraManager.ts'].replace('        this.unsubscribeMapEditorModeStore();','        this.scene.events.off(Phaser.Scenes.Events.RENDER, this.emitViewportUpdate);\n        this.viewportUpdatePending = false;\n        this.unsubscribeMapEditorModeStore();')
modified['CameraManager.ts']=modified['CameraManager.ts'].replace('    public zoomByFactor(zoomFactor: number, smooth: boolean): void {','    public zoomByFactor(zoomFactor: number, smooth: boolean): void {\n        this.viewportAutomationDisabled = true;')
modified['CameraManager.ts']=modified['CameraManager.ts'].replace('    public setExplorationMode(): void {','    public setExplorationMode(): void {\n        this.viewportAutomationDisabled = true;')
marker='    public getCamera(): Phaser.Cameras.Scene2D.Camera {'
method='''    /** Fit a world-space viewport while preserving the native Follow target and camera offset.
     * Ignores focus, exploration and zoom-lock modes so a map cannot reclaim a user's camera.
     * Legacy setPosition/enterFocusMode/leaveFocusMode behavior is unchanged.
     */
    public setViewport(width: number, height: number, smooth = false): void {
        if (this.cameraMode !== CameraMode.Follow || this.isZoomLocked() || this.viewportAutomationDisabled) return;
        if (!Number.isFinite(width) || !Number.isFinite(height) || width < 1 || height < 1 || width > 1_000_000 || height > 1_000_000) return;
        const nextZoom = this.waScaleManager.getTargetZoomModifierFor(width, height);
        if (!Number.isFinite(nextZoom) || nextZoom <= 0) return;
        if (smooth) {
            this.animateToZoomLevel(nextZoom);
            return;
        }
        this.targetZoomModifier = undefined;
        if (Math.abs(nextZoom - this.waScaleManager.zoomModifier) < 1e-9) return;
        this.waScaleManager.zoomModifier = nextZoom;
        // worldView is stale until Phaser renders after its native scale resize.
        if (!this.viewportUpdatePending) {
            this.viewportUpdatePending = true;
            this.scene.events.once(Phaser.Scenes.Events.RENDER, this.emitViewportUpdate);
        }
        this.scene.markDirty();
    }

'''
assert marker in modified['CameraManager.ts'];modified['CameraManager.ts']=modified['CameraManager.ts'].replace(marker,method+marker)
marker='''        this.iframeSubscriptionList.push(
            iframeListener.cameraSetStream.subscribe((cameraSetEvent) => {'''
replacement='''        this.iframeSubscriptionList.push(
            iframeListener.cameraViewportStream.subscribe(({ width, height, smooth }) => {
                this.cameraManager.setViewport(width, height, smooth);
            })
        );

'''+marker
assert modified['GameScene.ts'].count(marker)==1;modified['GameScene.ts']=modified['GameScene.ts'].replace(marker,replacement)
modified['IframeListener.ts']=modified['IframeListener.ts'].replace('import type { CameraSetEvent } from "./Events/CameraSetEvent";','import type { CameraSetEvent } from "./Events/CameraSetEvent";\nimport type { CameraViewportEvent } from "./Events/CameraViewportEvent";')
modified['IframeListener.ts']=modified['IframeListener.ts'].replace('    private readonly _cameraSetStream:', '    private readonly _cameraViewportStream: Subject<CameraViewportEvent> = new Subject();\n    public readonly cameraViewportStream = this._cameraViewportStream.asObservable();\n\n    private readonly _cameraSetStream:')
modified['IframeListener.ts']=modified['IframeListener.ts'].replace('                    } else if (iframeEvent.type === "cameraSet") {','                    } else if (iframeEvent.type === "cameraViewport") {\n                        this._cameraViewportStream.next(iframeEvent.data);\n                    } else if (iframeEvent.type === "cameraSet") {')
modified['IframeEvent.ts']='import { isCameraViewportEvent } from "./CameraViewportEvent";\n'+modified['IframeEvent.ts']
modified['IframeEvent.ts']=modified['IframeEvent.ts'].replace('''    z.object({
        type: z.literal("cameraSet"),''','''    z.object({
        type: z.literal("cameraViewport"),
        data: isCameraViewportEvent,
    }),
    z.object({
        type: z.literal("cameraSet"),''')
marker='''    /**
     * Listens to updates of the camera viewport.'''
method='''    /** Fit a world-space viewport without recentering or interrupting native player follow.
     * No effect while the user is exploring, focusing elsewhere, or has locked zoom.
     * Requires a client that supports the cameraViewport event; legacy clients ignore it.
     */
    public setViewport(width: number, height: number, smooth = false): void {
        if (!Number.isFinite(width) || !Number.isFinite(height) || width < 1 || height < 1 || width > 1_000_000 || height > 1_000_000) {
            throw new RangeError("Camera viewport dimensions must be finite and between 1 and 1,000,000 world pixels.");
        }
        sendToWorkadventure({
            type: "cameraViewport",
            data: { width, height, smooth },
        });
    }

'''
assert marker in modified['camera.ts'];modified['camera.ts']=modified['camera.ts'].replace(marker,method+marker)
PATHS['CameraViewportEvent.ts']='play/src/front/Api/Events/CameraViewportEvent.ts'
sources['CameraViewportEvent.ts']=''
modified['CameraViewportEvent.ts']='''import { z } from "zod";

export const isCameraViewportEvent = z.object({
    width: z.number().finite().min(1).max(1_000_000),
    height: z.number().finite().min(1).max(1_000_000),
    smooth: z.boolean().optional(),
});

/** Fit a world-space viewport while keeping the native Follow target. */
export type CameraViewportEvent = z.infer<typeof isCameraViewportEvent>;
'''
patch=[]
for name,path in PATHS.items():
 target=OUT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(modified[name])
 patch.extend(difflib.unified_diff(sources[name].splitlines(True),modified[name].splitlines(True),fromfile='a/'+path,tofile='b/'+path))
(ROOT/'PRESERVE-NATIVE-FOLLOW.patch').write_text(''.join(patch))
manifest={'stage':'local-only-not-published','baseCommit':'f00b3482f23c51976b4b339d7a891cad683d6498','files':[{'path':path,'baseSha256':hashlib.sha256(sources[name].encode()).hexdigest(),'candidateSha256':hashlib.sha256(modified[name].encode()).hexdigest()} for name,path in PATHS.items()]}
(ROOT/'ENGINE-PATCH-MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Prepared six-file local native Follow-preserving framing API patch.')
