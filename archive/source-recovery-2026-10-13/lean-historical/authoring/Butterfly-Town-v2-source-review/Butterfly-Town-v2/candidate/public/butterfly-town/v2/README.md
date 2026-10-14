# Butterfly Town v2 review candidate

One self-contained 144×96 TMJ at 32px tiles. A monumental gate leads to a separate town with local roof reveals for StudentHub, Lantern Café and Atlas Archive. Permanent collisions never disappear when art layers change.

Install this entire folder only as `public/butterfly-town/v2/`; keep v1 and unrelated maps unchanged. Entry: `butterfly-town.tmj`. No WAM import, backend change or paid service is required. This is a local review candidate, not published.

Audio implementation and water assets are included, but `ENABLE_NATIVE_AUDIO` in `scripts/town.js` remains false until compatible native PR712 is deployed and device/listening acceptance passes. The implementation uses the existing native playAudio/audioVolume/audioLoop properties. Do not activate an independent player. See the source package's AUDIO-INTEGRATION.md.

The source package includes reproducible generators, original artwork, frozen v1 comparison, QA and stage-specific reports. Source-harness tests are not full hosted Universe/two-client/physical-phone acceptance. The one corrected desk/chair arrangement is a standing-workspace proposal, not an implemented sitting interaction or a claim of independently Y-sorted furniture.
