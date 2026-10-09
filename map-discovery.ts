// Adapted from wa-map-optimizer-vite getMaps (AGPL-3.0).
// Original license: licenses/wa-map-optimizer-vite-AGPL-3.0.txt
import fs from "node:fs";
import { ITiledMap } from "@workadventure/tiled-map-type-guard";

/**
 * Same discovery and schema checks as wa-map-optimizer-vite's getMaps, with
 * only the repository-root archive excluded before recursion. Archived drafts
 * must never become build inputs or fail a production build while being read.
 */
export function getPublishedMaps(mapDirectory = "."): Map<string, ITiledMap> {
    let maps = new Map<string, ITiledMap>();
    for (const file of fs.readdirSync(mapDirectory)) {
        const fullPath = mapDirectory + "/" + file;
        if (mapDirectory === "." && file === "map-mocks") continue;
        if (mapDirectory && fs.lstatSync(fullPath).isDirectory() && file !== "dist" && file !== "node_modules") {
            maps = new Map([...maps, ...getPublishedMaps(fullPath)]);
        } else if (fullPath.endsWith(".tmj")) {
            let object: unknown;
            try {
                object = JSON.parse(fs.readFileSync(fullPath).toString());
            } catch (error) {
                throw new Error(`Error on ${fullPath} map file: ${error}`);
            }
            const map = ITiledMap.safeParse(object);
            if (!map.success) {
                console.error(`${fullPath} is not a compatible map file, the file will be skip`);
                console.error(JSON.stringify(map.error.issues));
                continue;
            }
            maps.set(fullPath, map.data);
        }
    }
    return maps;
}
