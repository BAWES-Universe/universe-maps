"""Encode actual-client captures at recorded file-write intervals, without speeding up animation."""
from pathlib import Path
import subprocess,json
r=Path(__file__).resolve().parents[2]
for name in ['gate','beverage']:
 frames=sorted((r/'review/interaction-frames').glob(name+'-*.png'))
 times=[p.stat().st_mtime for p in frames]
 manifest=r/'review/interaction-frames'/f'{name}.txt'
 lines=[]
 for i,p in enumerate(frames):
  duration=times[i+1]-times[i] if i+1<len(times) else .3
  lines += [f"file '{p}'",f'duration {duration:.6f}']
 lines += [f"file '{frames[-1]}'"]
 manifest.write_text('\n'.join(lines)+'\n')
 subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(manifest),'-vf','fps=15','-c:v','libx264','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(r/'review'/f'{name}-interaction.mp4')],check=True)
 (r/'review'/f'{name}-capture-timing.json').write_text(json.dumps({'method':'actual screenshot completion timestamps; encoded at recorded intervals','durationSeconds':times[-1]-times[0]+.3,'frameCount':len(frames)},indent=2)+'\n')
