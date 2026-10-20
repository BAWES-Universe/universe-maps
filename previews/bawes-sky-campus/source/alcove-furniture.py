"""Native furniture within the bounded stone conversation recess."""
# Replace only the previous lower west table; keep the northern landing setting.
# Close the bowl perimeter and open its real inner floor and eastern stairs.
rectwalk((1952,3152,384,224),0)
for ty in range(3152//16,3376//16):
 for tx in range(1984//16,2336//16):
  cx=tx*16+8-(LX+184);cy=ty*16+8-(LY+120)
  if (cx/126)**2+(cy/62)**2<1:rectwalk((tx*16,ty*16,16,16))
rectwalk((2240,3232,96,64))
item('out-cafe-curve',2048,3184,(2048,3184,144,16))
for dx in (40,72,104):seats.append(dict(x=2048+dx,y=3216,group='conservatory-lounge',facing='down'))
im=sprites['out-table-cups'];small=im.resize((48,48),Image.Resampling.LANCZOS);sprites['alcove-table']=small
item('alcove-table',2160,3264,(2160,3280,48,16))
im=sprites['out-cafe-curve'].copy();a=np.array(im);a[:46,:,3]=0;alcove_foreground.alpha_composite(Image.fromarray(a),(2048-LX,3184-LY))
