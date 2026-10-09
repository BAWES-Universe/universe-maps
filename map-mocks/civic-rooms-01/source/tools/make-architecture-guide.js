const fs=require('fs'),sharp=require('sharp'),R='../universe-civic-rooms';
const s=`<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="2304" viewBox="0 0 640 1152">
<rect x="32" y="32" width="576" height="1088" rx="8" fill="#d3be90" stroke="#886a3d" stroke-width="8"/>
<rect x="64" y="64" width="512" height="448" fill="#b78d58"/>
<path d="M64 64H576V160H64Z" fill="#d2bd8c"/><path d="M64 512H576V544H64Z" fill="#ead7a9"/>
<rect x="192" y="76" width="256" height="32" rx="4" fill="#215557" stroke="#b79243" stroke-width="7"/>
<rect x="80" y="78" width="64" height="48" fill="#725033"/><rect x="512" y="78" width="48" height="64" fill="#725033"/>
<path d="M48 344H624V424H48Z" fill="#d3be90"/><path d="M64 344H576V424H64Z" fill="#b78d58"/>
<path d="M588 344H640V424H588Z" fill="#d3be90"/>
<rect x="48" y="536" width="544" height="32" fill="#9c7d4e"/>
<rect x="64" y="576" width="512" height="512" fill="#c5ad80"/>
<rect x="96" y="600" width="448" height="136" rx="4" fill="#a97745" stroke="#79512d" stroke-width="4"/>
<rect x="160" y="736" width="320" height="20" fill="#79522e"/>
<path d="M96 736H160V772H96ZM480 736H544V772H480Z" fill="#b48956" stroke="#7d582f" stroke-width="2"/>
<path d="M96 746H160M96 758H160M480 746H544M480 758H544" stroke="#74532f" stroke-width="2"/>
<rect x="304" y="780" width="64" height="288" fill="#69877f"/>
<path d="M588 952H640V1032H588Z" fill="#d3be90"/>
<g fill="#1e5356" stroke="#b8994d" stroke-width="4"><path d="M33 160H55V224H33ZM33 280H55V328H33ZM33 432H55V496H33ZM33 624H55V688H33ZM33 800H55V864H33ZM33 952H55V1016H33ZM584 160H606V224H584ZM584 264H606V320H584ZM584 448H606V496H584ZM584 624H606V688H584ZM584 800H606V864H584ZM584 1048H606V1080H584Z"/></g>
<g fill="#497652"><circle cx="80" cy="172" r="16"/><circle cx="560" cy="172" r="16"/><circle cx="80" cy="492" r="16"/><circle cx="560" cy="492" r="16"/><circle cx="80" cy="804" r="16"/><circle cx="560" cy="804" r="16"/><circle cx="80" cy="1064" r="16"/><circle cx="560" cy="1064" r="16"/></g>
</svg>`;
fs.writeFileSync(R+'/art-source/architecture-geometry-guide.svg',s);sharp(Buffer.from(s)).png().toFile(R+'/art-source/architecture-geometry-guide.png');
