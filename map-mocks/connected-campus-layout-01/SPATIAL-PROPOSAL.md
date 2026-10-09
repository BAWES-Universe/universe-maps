# One home, one town

## Decision

Use a single StudentHub workplace for the small team, immediately beyond reception. The four main work chairs in the latest painted proof are sufficient for the first slice. Do not add a building, doorway, carpet island or extra workstation merely to represent another software integration. Operations, Sales, Research, Media and Design are roles and shared tools within this same home.

The overview is a complete-campus spatial proposal, not a finished render. It gives the painted arrival/workplace study a clear place in the larger plan. Surrounding extensions are not built. All silhouettes and positions in the overview are schematic, not a pixel-exact trace of the painting. The detailed six-seat diagram is an earlier dimensioned alternative, retained as an internal planning study; do not present it as the current painted floor plan.

## Arrival and navigation

1. Monumental gate: a protected arrival forecourt with the giant doorway as the vertical landmark. Keep waterfalls, light and vegetation around the walkable center rather than over its silhouette.
2. Lantern avenue: a short, continuous, 4–6-tile-wide axis. The newcomer should see the next destination immediately after the gate reveal.
3. Fountain court: the fountain sits just off the axis. A clear route passes its right side toward the StudentHub door; a slower circular route gives public visitors a natural meeting point.
4. StudentHub: one warmly lit door and one recognizable roofline. Reception is beside the entrance, where the daily work group and colleague sprites are visible. The main walking line is a rug/stone runner, not a row of tiny signs.
5. Branches: a public cloister runs left to teaching/events, right to the portal garden. The market is a pair of shallow frontage rows beside the avenue, without obstructing the arrival view.

## Complete program without department silos

- Shared team core: four everyday work chairs in the first painted study. Future growth can use six seats in the same room if a native-scale collision/clearance proof passes. Reception → first desk should take roughly 4–7 clear tiles. All everyday desks should fit into one normal desktop camera view.
- Operations command / Sales CRM: a shared wall console or two adjacent work surfaces, visible from the team room. A dashboard is a tool destination; it is not a reason for a separate building. CRM content should remain under the appropriate account permissions.
- Research lab: a recognizable book/sample/tool bench on the same perimeter, shared by the team. Larger experiments can use a later portal room.
- Media / Imagine / music / design: a shared creator surface and asset-review wall. An acoustically isolated music/recording room may be an expansion; regular media/design work still happens beside the team.
- Meeting rooms: one visible glass room within the first workplace. An attached east meeting gallery later provides two small quiet rooms and a flexible conference area. It remains part of the same architectural shell, reached by a short glazed passage. Door access can distinguish visitors from team-only rooms.
- Indoor lounge: one compact sofa arrangement on one carpet, visibly associated with reception and the team. Maintain individual furniture contact shadows and convincing chair/table proximity.
- Outdoor commons: one sheltered larger couch-and-carpet group beside the fountain. Keep circulation outside the seating conversation circle.
- Teaching: a public classroom within a civic pavilion off the left cloister, with teacher position, board/front, facing student desks, rear entry and visible central aisle. Classroom teaching should not use the team's quiet desk zone.
- Events: the lower part of that same civic pavilion is a great hall with a stage, podium, front-facing audience, clear center aisle and rear/side entry. It supports presentations, conference sessions and public events without turning the everyday office into an auditorium.
- Market: four coherent sheltered storefronts/booths. Give each a standing/service approach and a waiting position offset from the avenue. Future guide, recruitment, shop or service bot positions can be reserved here; no active commerce, recruitment or bots are claimed.
- Portals: a garden off the public court can extend to larger classrooms, creator rooms, specialist labs or event worlds. Portal expansion should not be necessary to find a coworker in the normal small-team office.

## Public and quieter routes

Public route: gate → market edge → fountain → public cloister → classroom / great hall / portal garden. Visitors can reach public functions without crossing daily desks.

Welcomed office route: fountain → StudentHub doorway → reception → shared team floor. Meeting invitations can use a controlled reception/gallery route.

Quiet route: reception → glazed side passage → meeting gallery. The short distance preserves team connection while giving calls and focused work a separate boundary.

These are proposed spatial access boundaries. A glass wall or room label does not provide audio privacy, meeting permissions, account authorization, live bot services, broadcast settings or CRM security. Those capabilities require configuration and real-client tests.

## Scale contract

- Keep the original 32 px Woka and 32 px tile contract unchanged.
- Painted study envelope: 1024 × 1024 native pixels, 32 × 32 tiles.
- Initial main-shell target was x160..864, y96..512. The actual painted master differs: room approximately x112..937, y40..417; entrance center x512 with threshold extending to y538; main court route approximately x460..574 to the bottom; fountain center approximately (280, 718), radius 120. The art lead supplied these measured bounds after rendering. They are guidance, not a verified collision map.
- Actual painted furniture: four dedicated desks in two close pairs, four glass-meeting chairs, a couch group and reception counter approximately x610..753, y329..386. Customer approach should be west of the counter, around (590, 350), not in the narrow strip between counter and front wall. A team/reception spawn should use this clear interior welcome area.
- Do not label six built stations or transfer the earlier diagram’s native coordinates onto the actual painting.
- Daily-team design envelope: approximately 576 × 352 px before allocating the east glass room. Do not describe this as 576 px of clear desks plus the meeting room; the meeting room occupies part of it.
- Individual desk: about 64 px wide. Chair: 24–32 px. Main routes and door openings: at least 96 px clear. Short chair approaches/pullback: at least 32 px, verified with the actual sprite collider.
- Main campus proposal: about 72 × 74 tiles including generous arrival and future public functions; the player's normal view is much closer than the overview.
- This is an outline for one connected ground plane, not a collection of isolated department islands.

## Roof, glass and spatial legibility

Exterior state must preserve the building as one coherent object with a roof ridge, clerestory/dormers, arched entrance, walls and grounded planting.

Interior state should fade/remove only obstructing roof planes. Retain the structural perimeter, low front wall, wall tops/rim, entrance piers, glass frames and selected columns so the room keeps its shape. High north walls can remain; foreground walls should be low or selectively transparent. Window and roof reveal must be local to the player and must never change physical collision.

Glass should have restrained tinted reflections and readable framing. It is not a pale opaque rectangle and should not erase the meeting table, chairs or Woka. Preserve furniture depth and a small contact shadow on the player in both states.

## Art and acceptance

What v1 gets right: a cohesive stone material, warm pools of light, colored roof silhouettes, integrated gardens, a prominent fountain and a few readable destinations. The newer rejected layout inflated the route network and repeated nearly identical floors/furniture, making departments feel disconnected and furniture float as stickers.

The new painted proof is a strong return to cohesive world-building: architectural framing, deliberately paired desks, dense peripheral greenery, curved planter edges, a visible interior, textured floor and integrated lighting. Preserve those qualities while separating the actual paint into useful rendering layers; do not replace the composition with generic boxes or pasted room sprites.

Before approving playable implementation, verify: 1:1 Woka and furniture scale; one uninterrupted reception-to-desk path; no canopy/plant obstruction at threshold; true glass visibility; coherent exterior roof and interior cutaway; passable audience/classroom aisles; reachable booth fronts; permanent collision independent of reveal; reduced-motion lighting/water state; no false live-service claims.

## Deliverables

- 01-connected-campus-concept.png / .svg: reviewed full-campus planning overview, appropriate to show beside the painted proof.
- 02-studenthub-core-concept.png / .svg: earlier six-seat dimensioned alternative, internal planning only; not the current painted floorplan.
- render_layout.py: reproducible code-native schematic source.

Only this proposal folder was edited. Existing map, engine, painted art and archived v1 were not changed.
