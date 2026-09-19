"""Original schematic cover art; deliberately illustrative, never presented as build photos."""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
def circle(x,y,r,**attrs):return f'<circle cx="{x}" cy="{y}" r="{r}" '+ ' '.join(f'{k}="{v}"' for k,v in attrs.items())+'/>'
def gear(x,y,r,n=12):
 s=circle(x,y,r)+circle(x,y,r*.7)+circle(x,y,r*.17)
 for i in range(n):
  a=i*2*math.pi/n;s+=f'<path d="M{x+r*.94*math.cos(a):.1f} {y+r*.94*math.sin(a):.1f}l{r*.2*math.cos(a):.1f} {r*.2*math.sin(a):.1f}"/>'
 return s
car='''<path d="M130 295l52-80 193-18 99 76-21 50-257 32zM182 215l54 46 238 12M236 261l-40 94M375 197l-35 64M130 295l106-34M265 211l51-4 37 32-55 5z"/><path d="M173 228l47 44-20 43-48-28M385 228l43 32M239 307l162-10"/><ellipse cx="182" cy="332" rx="27" ry="38" transform="rotate(-20 182 332)"/><ellipse cx="182" cy="332" rx="13" ry="20" transform="rotate(-20 182 332)"/><ellipse cx="432" cy="304" rx="25" ry="37" transform="rotate(-20 432 304)"/><ellipse cx="432" cy="304" rx="12" ry="18" transform="rotate(-20 432 304)"/>'''
rover='''<path d="M175 250l117-55 142 49-105 60zM175 250v54l154 49 105-56v-53M329 304v49M250 234v-40l37-16 43 16v39M287 178v-62l30-8 23 12-28 10-25-14M312 130v24M220 305l-30 38M274 325l-2 34M365 331l39 1M392 285l39 18M226 230l51 17 68-31"/>'''+''.join(f'<ellipse cx="{x}" cy="{y}" rx="22" ry="30" transform="rotate(-15 {x} {y})"/>' for x,y in [(172,345),(268,371),(404,348),(444,309)])
clock=gear(262,233,59)+gear(355,278,39)+gear(354,197,31)+'''<path d="M188 133h225v242H188zM218 154v171M218 325v71M204 396h28v29h-28zM353 318v83"/><circle cx="353" cy="411" r="23"/><path d="M244 139v-28h100v28M233 355h112"/>'''
plane='''<path d="M119 299l133-43 42-133 18-10 5 129 182-43 20 12-200 68-8 73 50 23v12l-65-8-54 23-8-9 52-45-3-58-146 24zM317 242l2 37M286 288l33-9"/><path d="M133 334l-30 10M473 268l28-8M247 174l6-20" stroke-dasharray="4 6"/>'''
boat='''<path d="M128 330l89-36 253 7-68 54-205 5zM128 330l35 44 214 5 25-24M470 301l-15 45-78 33M199 296V170h88v126M199 190h88M211 170v108M228 170v108M245 170v108M262 170v108M279 170v108M337 296V161h88v136M337 181h88M349 161v110M366 161v110M383 161v110M400 161v110M417 161v110"/><path d="M194 142q45-39 90 0M332 133q45-39 90 0M174 405q35-10 70 0t70 0t70 0" stroke-dasharray="5 7"/>'''
plant='''<path d="M175 118v291M422 118v291M158 214h280M158 339h280M170 220l15 43h225l17-43M170 345l15 38h225l17-38M192 119h210M192 142h210"/>'''
for y in [214,339]:
 for x in [217,279,341,393]:plant+=f'<path d="M{x} {y}v-35q-29 0-22-23 24 0 22 23 25-27 28-3-8 12-28 3"/>'
plant+='<path d="M455 273v115h-37M166 283h-37v66"/>'
chip='''<rect x="220" y="170" width="160" height="160" rx="9"/><rect x="246" y="196" width="108" height="108" rx="2"/><path d="M263 248l24 24 47-49"/>'''
for i in range(7):
 x=235+i*22;chip+=f'<path d="M{x} 150v20M{x} 330v20M200 {x-45}h20M380 {x-45}h20"/>'
chip+='<path d="M150 152h55v-35h131M156 330v46h149M437 174v-40h-41M420 333h33v47h-75"/>'
wave='<path d="M150 325h300M174 325v-45h54v-65h62v-59h61v-35h63"/>'
for i in range(4):wave+=f'<path d="M{210+i*20} {332+i*2}q{90-i*18} {-220+i*42} {180-i*36} 0"/>'
drone='''<path d="M265 238l-68-59M334 238l67-59M264 281l-63 56M334 281l65 56M266 227h68l21 29-21 34h-68l-22-34z"/>'''+''.join(f'<ellipse cx="{x}" cy="{y}" rx="62" ry="24"/><circle cx="{x}" cy="{y}" r="8"/>' for x,y in [(191,171),(407,171),(195,345),(405,345)])
arcade='''<path d="M226 122h154l25 49-22 101 34 24-15 116H203l-13-118 28-29-10-94zM226 122l-18 49h197M218 185h164l-15 74H228zM218 265l165 7M190 294h227M213 323h182M248 341h103v52H248zM238 287v-17M339 284h19M369 285h18"/><circle cx="238" cy="268" r="8"/><path d="M270 205l10 7-10 7zM325 240l10 7-10 7z"/>'''
vacuum='''<ellipse cx="300" cy="309" rx="126" ry="54"/><path d="M174 309v42c0 76 252 76 252 0v-42M239 287v-77h123v77M239 210q60-34 123 0M251 231l98 40M252 260l74 25M276 190v-24h46v24M201 365v26M399 365v26"/><ellipse cx="300" cy="209" rx="61" ry="19"/>'''
rocket='''<path d="M275 263V151l25-55 25 55v112zM275 245l-37 55 37-8M325 245l37 55-37-8M275 270h50M300 285v32M245 324l55-15 55 15v46l-55 16-55-16zM245 324l55 17 55-17M300 341v45M263 377l-26 45M337 377l26 45"/><ellipse cx="300" cy="292" rx="58" ry="19"/><path d="M234 292h-26M366 292h26"/>'''
shapes={'cybertruck-go-kart':car,'hurc-mars-rover':rover,'mechanical-clock':clock,'low-cost-rc-plane':plane,'ion-thruster-boat':boat,'hydroponic-farm':plant,'ai-parts-database':chip,'transducer-phased-array':wave,'micro-swarming-drone':drone,'arcade-cabinet':arcade,'industrial-robotic-vacuum':vacuum,'gimbaling-tvc':rocket,'hybrid-rc-car':car,'remote-control-hot-wheels':car,'geophone-vibration-tester':wave,'custom-drives':gear(300,250,91,18),'vacuum-tube-power-supply':chip}
colors={'Robotics':('#e8eee8','#314e40'),'Electronics':('#e7ebeb','#344c4e'),'Mechanisms':('#eee8de','#655442'),'Fabrication':('#e9e5df','#655444'),'Research':('#e7e8ee','#494e6a'),'Software':('#e6e9ed','#3c5367'),'Coursework':('#ece9e4','#6a635a')}
for i,p in enumerate(json.loads((ROOT/'content/projects.json').read_text())):
 bg,fg=colors[p['category']];shape=shapes.get(p['slug'],gear(268,249,70)+gear(383,272,37))
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 460" fill="none"><defs><pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0v30" stroke="{fg}" opacity=".075"/></pattern></defs><path fill="{bg}" d="M0 0h600v460H0z"/><path fill="url(#grid)" d="M0 0h600v460H0z"/><g stroke="{fg}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round">{shape}</g><g stroke="{fg}" opacity=".35"><path d="M95 90v305M87 100h16M87 385h16M140 422h328M150 414v16M458 414v16"/><path d="M300 56v25M288 68h24M507 260h25M519 248v24"/></g><g font-family="monospace" font-size="9" letter-spacing="1.5" fill="{fg}"><text x="30" y="36">GK / PROJECT {i+1:02}</text><text x="570" y="36" text-anchor="end">{p['category'].upper()}</text><text x="30" y="441" opacity=".7">CONCEPTUAL ILLUSTRATION</text></g><circle cx="546" cy="420" r="4" fill="#c75834"/></svg>'''
 (ROOT/'assets/illustrations'/f"{p['slug']}.svg").write_text(svg)
print('Created original project cover illustrations.')
