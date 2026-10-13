from pathlib import Path
import json,subprocess,numpy as np,math
R=Path(__file__).resolve().parents[1]; report=json.loads((R/'evidence/integrated-native-walkthrough.json').read_text());video=R/'evidence/integrated-native-walkthrough.webm'
data=subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-vn','-af','aresample=async=1:first_pts=0','-ac','1','-ar','24000','-f','f32le','-'])
a=np.frombuffer(data,dtype=np.float32);sr=24000
segments=[]
for i,step in enumerate(report['steps']):
 start=step.get('audioMs',step['ms'])/1000;end=(report['steps'][i+1].get('audioMs',report['steps'][i+1]['ms'])/1000 if i+1<len(report['steps']) else len(a)/sr)
 lo=start+.2;hi=max(lo,end-.1);s=a[int(lo*sr):int(hi*sr)]
 rms=float(np.sqrt(np.mean(s*s))) if len(s) else 0;peak=float(np.max(np.abs(s))) if len(s) else 0
 segments.append({'label':step['text'],'start':start,'end':end,'sampleCount':len(s),'rmsDbFS':20*math.log10(max(rms,1e-12)),'peakDbFS':20*math.log10(max(peak,1e-12))})
quiet=[s for s in segments if s['label'].startswith(('V2 source review','Native mute','Quiet again'))]
result={'scope':'Encoded QA capture signal analysis, not human listening or physical-device acceptance','durationSeconds':len(a)/sr,'peakDbFS':20*math.log10(max(float(np.max(np.abs(a))),1e-12)),'segments':segments,'expectedQuietSegments':quiet,'quietSegmentsPass':all(s['sampleCount']>0 and s['peakDbFS'] < -65 for s in quiet),'hasAudibleWaterSignal':any(s['rmsDbFS'] > -65 for s in segments),'masterNormalizationApplied':False,'timing':'AudioContext clock plus encoded audio packet timestamps; timestamp gaps decoded as silence, no synthesized or replaced water'}
(R/'evidence/integrated-walkthrough-signal.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
