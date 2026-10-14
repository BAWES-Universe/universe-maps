from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1];r=json.loads((R/'evidence/scenery-after-video.json').read_text());m=json.loads((R/'evidence/scenery-video-timeline.json').read_text());hidden=m['foregroundHidden'];restored=m['foregroundRestored'];water=m['waterStart']
f=(f"[0:v]fps=30,scale=660:420,tpad=stop_mode=clone:stop_duration=12,drawtext=text='V1 - BEFORE':fontcolor=white:fontsize=24:x=20:y=20:box=1:boxcolor=black@0.6[a];"
   f"[1:v]fps=30,split=2[c][w];[c]trim=end={water},setpts=PTS-STARTPTS,scale=660:420,drawtext=text='V2 - CORRECTED':fontcolor=white:fontsize=24:x=20:y=20:box=1:boxcolor=black@0.6,"
   f"drawtext=text='Foreground hidden for comparison':enable='between(t,{hidden},{restored})':fontcolor=white:fontsize=20:x=12:y=385:box=1:boxcolor=black@0.7,"
   f"drawtext=text='Foreground restored - Greg is behind the tree':enable='gte(t,{restored})':fontcolor=white:fontsize=18:x=12:y=385:box=1:boxcolor=black@0.7[b];"
   f"[a][b]hstack=inputs=2:shortest=1,pad=1320:840:0:210:color=0x071322,drawtext=text='Same starting positions and walking inputs':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=100[comparison];"
   f"[w]trim=start={water},setpts=PTS-STARTPTS,scale=1320:840,drawtext=text='V2 - FOUNTAIN MOTION RESTORED':fontcolor=white:fontsize=28:x=24:y=24:box=1:boxcolor=black@0.65[water];"
   f"[comparison][water]concat=n=2:v=1:a=0[v]")
cmd=['ffmpeg','-y','-i',str(R/'evidence/scenery-before.webm'),'-i',str(R/'evidence/scenery-after-water.webm'),'-filter_complex',f,'-map','[v]','-an','-c:v','libx264','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(R/'Butterfly-Town-v2-scenery-comparison.mp4')]
with (R/'evidence/scenery-video-encode.log').open('w') as out:subprocess.run(cmd,check=True,stdout=out,stderr=out)
print('Encoded comparison plus uncut fountain hold.')
