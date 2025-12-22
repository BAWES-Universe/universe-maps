/// <reference types="@workadventure/iframe-api-typings" />

import { bootstrapExtra } from "@workadventure/scripting-api-extra";

console.log('Script started successfully');

// Waiting for the API to be ready
WA.onInit().then(() => {
    console.log('Scripting API ready');
    console.log('Player tags: ',WA.player.tags)

    // Lighting Zone Handler
    WA.room.area.onEnter("stage-focus").subscribe(() => {
        WA.room.showLayer("stage-glow-2");
        WA.room.showLayer("stage-glow-1");
    });

    WA.room.area.onLeave("stage-focus").subscribe(() => {
        WA.room.hideLayer("stage-glow-2");
        WA.room.hideLayer("stage-glow-1");
    });

    // The line below bootstraps the Scripting API Extra library that adds a number of advanced properties/features to WorkAdventure
    bootstrapExtra().then(() => {
        console.log('Scripting API Extra ready');
    }).catch(e => console.error(e));

}).catch(e => console.error(e));

export {};
