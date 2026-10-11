const fs=require('node:fs'),{stripTypeScriptTypes}=require('node:module');
const repo=process.env.ENGINE_AUDIT_REPO||'/workspace/shared/native32-replan-fix';
let s=fs.readFileSync(__dirname+'/source/types.ts','utf8').split('export const mapCustomEntityDirectionToDirection')[0].replace('import { CustomEntityDirection } from "@workadventure/messages";','').replace('from "zod"','from "'+repo+'/node_modules/zod/index.js"');
fs.writeFileSync(__dirname+'/schema.mjs',stripTypeScriptTypes(s,{mode:'transform'}));
s=fs.readFileSync(__dirname+'/source/WamFileMigration.ts','utf8').replace('from "../types"','from "./schema.mjs"');fs.writeFileSync(__dirname+'/migration.mjs',stripTypeScriptTypes(s,{mode:'transform'}));
