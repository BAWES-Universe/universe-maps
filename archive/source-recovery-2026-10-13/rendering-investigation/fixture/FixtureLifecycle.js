// Latest request wins; a replacement never starts before the previous game is destroyed.
export function createFixtureController({ start, destroy, onWaiting, onError }) {
    let generation = 0;
    let active = null;
    let queue = Promise.resolve();
    const isCurrent = record => active === record && record.id === generation && !record.obsolete;
    function request() {
        const id = ++generation;
        if (active) active.obsolete = true;
        queue = queue.then(async () => {
            if (id !== generation) return;
            if (active) {
                const previous = active;
                onWaiting(previous);
                await destroy(previous);
                if (active === previous) active = null;
            }
            if (id !== generation) return;
            const record = { id, obsolete: false, game: null, removeErrorListeners: () => {} };
            active = record;
            start(record, () => isCurrent(record));
        }).catch(error => onError(error));
        return queue;
    }
    return { request, isCurrent, get active() { return active; } };
}
