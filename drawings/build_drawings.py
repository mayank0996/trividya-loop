import os, math, zipfile
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, FancyArrowPatch, Arc
from matplotlib.backends.backend_pdf import PdfPages

HERE=os.path.dirname(os.path.abspath(__file__)); OUT=HERE; os.makedirs(OUT+'/png',exist_ok=True)
PDF=OUT+'/Trividya-engineering-drawings-v1.pdf'
INK='#251f21'; INK2='#585254'; HAIR='#d9d5d2'; SAND='#f4efec'; TEAL='#3f8175'; RED='#d92b3a'; BLUE='#386a8c'; AMBER='#c98d21'; WHITE='#ffffff'; OBS='#251f21'; EST='#2d73a5'; PROP='#a76022'
W,H=16.54,11.69

def setup(code,title,subtitle):
 fig,ax=plt.subplots(figsize=(W,H)); fig.patch.set_facecolor(SAND); ax.set_facecolor(WHITE); ax.set_xlim(0,160); ax.set_ylim(0,105); ax.axis('off')
 ax.add_patch(Rectangle((3,3),154,99,facecolor=WHITE,edgecolor=INK,lw=1.1))
 ax.text(7,97,title,fontsize=23,color=INK,va='top'); ax.text(7,91.5,subtitle,fontsize=10.5,color=INK2,va='top')
 # legend
 ax.add_patch(Rectangle((104,91),3,3,facecolor=OBS,edgecolor='none')); ax.text(108,92.5,'OBSERVED',fontsize=8.5,va='center',color=INK)
 ax.add_patch(Rectangle((123,91),3,3,facecolor=EST,edgecolor='none')); ax.text(127,92.5,'ESTIMATED',fontsize=8.5,va='center',color=INK)
 ax.add_patch(Rectangle((143,91),3,3,facecolor=PROP,edgecolor='none')); ax.text(147,92.5,'PROPOSED',fontsize=8.5,va='center',color=INK)
 ax.plot([6,154],[9,9],color=INK,lw=.8); ax.text(7,6.2,'TRIVIDYA-LOOP | EXPLORATORY DESIGN STUDY',fontsize=8.5,color=INK)
 ax.text(152,6.2,code,fontsize=9,color=INK,ha='right',weight='bold')
 return fig,ax

def save(fig,code):
 fig.savefig(f'{OUT}/png/{code}.png',dpi=160,bbox_inches='tight',facecolor=fig.get_facecolor())
 pdf.savefig(fig,bbox_inches='tight',facecolor=fig.get_facecolor()); plt.close(fig)

def dim(ax,p1,p2,label,offset=(0,0),color=EST):
 x1,y1=p1; x2,y2=p2; ox,oy=offset; p1=(x1+ox,y1+oy); p2=(x2+ox,y2+oy)
 ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle='<->',mutation_scale=10,color=color,lw=1))
 ax.text((p1[0]+p2[0])/2,(p1[1]+p2[1])/2+1,label,color=color,fontsize=8,ha='center',bbox=dict(facecolor=WHITE,edgecolor='none',pad=1))

def note(ax,x,y,status,title,text,w=34):
 col={'OBSERVED':OBS,'ESTIMATED':EST,'PROPOSED':PROP}[status]
 ax.add_patch(Rectangle((x,y),w,9,facecolor='#faf9f8',edgecolor=HAIR,lw=.8)); ax.add_patch(Rectangle((x,y),2,9,facecolor=col,edgecolor='none'))
 ax.text(x+3,y+6.4,title,fontsize=8.5,color=INK,weight='bold'); ax.text(x+3,y+2.1,text,fontsize=7,color=INK2,wrap=True)

def mock_side(ax,x,y,s=1,status='OBSERVED'):
 col={'OBSERVED':OBS,'ESTIMATED':EST,'PROPOSED':PROP}[status]
 pts=np.array([[0,0],[1,24],[6,38],[16,51],[43,52],[48,2]])*s+[x,y]
 ax.add_patch(Polygon(pts,closed=True,fill=False,edgecolor=col,lw=1.8))
 can=np.array([[2,3],[3,24],[8,37],[18,48],[38,49],[42,45],[32,37],[23,24],[17,5]])*s+[x,y]
 ax.add_patch(Polygon(can,closed=True,facecolor=INK,edgecolor=col,lw=1))
 ax.add_patch(Polygon((np.array([[17,39],[27,40],[25,34],[18,33]])*s+[x,y]),closed=True,facecolor=BLUE,edgecolor=col,lw=1))
 ax.add_patch(Rectangle((x+6*s,y+0*s),36*s,4*s,facecolor='none',edgecolor=col,lw=1))
 ax.add_patch(Rectangle((x-3*s,y+54*s),55*s,4*s,facecolor='none',edgecolor=col,lw=1.5))
 ax.plot([x+9*s,x+9*s],[y+50*s,y+54*s],color=col,lw=2); ax.plot([x+41*s,x+41*s],[y+50*s,y+54*s],color=col,lw=2)

def mock_front(ax,x,y,s=1):
 ax.add_patch(Polygon(np.array([[0,0],[2,36],[9,53],[33,53],[40,36],[42,0]])*s+[x,y],closed=True,fill=False,edgecolor=OBS,lw=1.7))
 ax.add_patch(Polygon(np.array([[4,2],[5,30],[11,47],[31,47],[37,30],[38,2]])*s+[x,y],closed=True,facecolor=INK,edgecolor=OBS,lw=1))
 ax.add_patch(Polygon(np.array([[14,38],[28,38],[26,32],[15,32]])*s+[x,y],closed=True,facecolor=BLUE,edgecolor=EST,lw=1))
 ax.add_patch(Rectangle((x-5*s,y+56*s),52*s,4*s,fill=False,edgecolor=OBS,lw=1.6)); ax.plot([x+8*s,x+8*s],[y+53*s,y+56*s],color=OBS,lw=2); ax.plot([x+34*s,x+34*s],[y+53*s,y+56*s],color=OBS,lw=2)

def mock_rear(ax,x,y,s=1):
 ax.add_patch(Rectangle((x,y),42*s,48*s,fill=False,edgecolor=OBS,lw=1.7))
 ax.add_patch(Rectangle((x+4*s,y+28*s),34*s,12*s,fill=False,edgecolor=OBS,lw=1.2)); ax.add_patch(Rectangle((x+9*s,y+6*s),24*s,15*s,fill=False,edgecolor=OBS,lw=1.2))
 ax.add_patch(Rectangle((x+1*s,y+44*s),40*s,7*s,facecolor=INK,edgecolor=OBS,lw=1));
 for cx in [11,21,31]: ax.add_patch(Circle((x+cx*s,y+47.5*s),2.2*s,fill=False,edgecolor=EST,lw=1))
 ax.add_patch(Rectangle((x-5*s,y+55*s),52*s,4*s,fill=False,edgecolor=OBS,lw=1.6)); ax.plot([x+9*s,x+9*s],[y+51*s,y+55*s],color=OBS,lw=2); ax.plot([x+33*s,x+33*s],[y+51*s,y+55*s],color=OBS,lw=2)

def tube(ax,cx,cy,r,prop=True):
 col=PROP if prop else OBS; ax.add_patch(Circle((cx,cy),r,fill=False,edgecolor=col,lw=2)); ax.add_patch(Circle((cx,cy),r*.83,fill=False,edgecolor=col,lw=1));

with PdfPages(PDF) as pdf:
 # A01 orthographic
 fig,ax=setup('A01','Physical mockup orthographic views','Seven supplied photos. Geometry in black is observed; blue dimensions are photo-derived estimates.')
 mock_front(ax,12,26,.9); ax.text(31,20,'FRONT',ha='center',fontsize=9,color=INK)
 mock_side(ax,62,28,.84); ax.text(82,20,'SIDE',ha='center',fontsize=9,color=INK)
 mock_rear(ax,113,28,.9); ax.text(132,20,'REAR',ha='center',fontsize=9,color=INK)
 # top
 ax.add_patch(Polygon([[65,75],[73,84],[104,84],[112,75],[108,68],[69,68]],closed=True,fill=False,edgecolor=OBS,lw=1.7)); ax.add_patch(Rectangle((61,86),56,4,fill=False,edgecolor=OBS,lw=1.6)); ax.text(89,64,'TOP',ha='center',fontsize=9,color=INK)
 note(ax,8,12,'OBSERVED','Source geometry','Shell, canopy, window, top bridge, rear bays, vents and service doors.',43); note(ax,57,12,'ESTIMATED','No measurement scale','Proportions inferred across seven uncalibrated images.',43); note(ax,106,12,'PROPOSED','None on A01','This sheet avoids tube, guideway and clinical overlays.',43)
 save(fig,'A01')
 # A02 dimensions
 fig,ax=setup('A02','Estimated replica dimensions','Visual reconstruction envelope and primary features. All dimensions require confirmation on the physical mockup.')
 mock_side(ax,25,21,1.15,'OBSERVED'); dim(ax,(25,18),(80,18),'2050 mm overall length (EST.)'); dim(ax,(19,21),(19,88),'2235 mm to bridge (EST.)');
 mock_front(ax,101,25,1.05); dim(ax,(96,21),(150,21),'1500 mm overall width (EST.)'); dim(ax,(108,65),(137,65),'470 mm window (EST.)')
 ax.text(8,80,'DIMENSION BASIS',fontsize=11,color=INK,weight='bold'); ax.text(8,75,'No ruler, tape, photogrammetry target, known component size or camera calibration was supplied.',fontsize=8.5,color=INK2)
 note(ax,8,63,'ESTIMATED','Main body','1830 L x 1200 W x 1900 H mm.',42); note(ax,8,51,'ESTIMATED','Top bridge','1500 W x 430 D x 65 T mm.',42); note(ax,8,39,'ESTIMATED','Fan / pod sizes','Rear fan 156 mm dia; side pod 150 mm dia.',42)
 save(fig,'A02')
 # A03 sections
 fig,ax=setup('A03','Key sections and construction reading','Observed shell interpreted as plywood skins/panels around an open service volume. Thicknesses are estimated.')
 ax.text(12,82,'SECTION A-A | TRANSVERSE',fontsize=10,color=INK,weight='bold'); ax.add_patch(Polygon([[18,28],[20,60],[31,81],[61,81],[72,60],[74,28]],closed=True,fill=False,edgecolor=OBS,lw=2)); ax.add_patch(Polygon([[23,31],[24,58],[34,74],[58,74],[68,58],[69,31]],closed=True,fill=False,edgecolor=EST,lw=1)); ax.add_patch(Rectangle((30,28),32,23,fill=False,edgecolor=PROP,lw=1.2,linestyle='--')); ax.text(46,42,'service / cabin\nvolume',ha='center',fontsize=9,color=PROP)
 ax.text(91,82,'SECTION B-B | LONGITUDINAL',fontsize=10,color=INK,weight='bold'); mock_side(ax,96,27,.95); ax.plot([100,141],[38,38],color=PROP,lw=1.2,ls='--'); ax.text(122,34,'PROPOSED floor datum',ha='center',fontsize=8,color=PROP)
 note(ax,12,14,'OBSERVED','Outer shell','Plywood-colored side skins and black canopy.',43); note(ax,59,14,'ESTIMATED','Panel thickness','Plywood 30 mm; canopy skin 18 mm.',43); note(ax,106,14,'PROPOSED','Cabin datum','Flat interior datum for later ambulance integration.',43)
 save(fig,'A03')
 # A04 exploded
 fig,ax=setup('A04','Exploded physical assembly','Subsystem decomposition matches the editable STL package. Arrow direction is illustrative, not an assembly sequence.')
 centers=[(22,53,'1 Shell +\nwhite panels'),(48,62,'2 Canopy +\nwindow'),(76,70,'3 Top bridge\n+ supports'),(105,60,'4 Rear bays\n+ fans'),(134,48,'5 Service doors\n+ handles')]
 shapes=[]
 ax.add_patch(Polygon([[10,35],[13,64],[22,78],[34,68],[38,37]],closed=True,fill=False,edgecolor=OBS,lw=1.8))
 ax.add_patch(Polygon([[43,42],[45,65],[52,77],[61,66],[63,44]],closed=True,facecolor=INK,edgecolor=OBS,lw=1.2))
 ax.add_patch(Rectangle((67,73),25,4,fill=False,edgecolor=OBS,lw=1.7)); ax.plot([72,72],[62,73],color=OBS,lw=2); ax.plot([87,87],[62,73],color=OBS,lw=2)
 ax.add_patch(Rectangle((98,55),25,8,facecolor=INK,edgecolor=OBS)); [ax.add_patch(Circle((103+i*7,51),2.3,fill=False,edgecolor=OBS)) for i in range(3)]
 ax.add_patch(Rectangle((130,35),18,28,fill=False,edgecolor=OBS,lw=1.5)); ax.add_patch(Rectangle((133,51),12,7,fill=False,edgecolor=OBS)); ax.add_patch(Rectangle((135,39),8,7,fill=False,edgecolor=OBS))
 for a,b in [((38,56),(43,56)),((63,64),(67,70)),((92,70),(98,61)),((123,56),(130,51))]: ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',color=EST,mutation_scale=12,lw=1.2))
 for x,y,t in centers: ax.text(x,y-27,t,ha='center',fontsize=9,color=INK)
 note(ax,10,13,'OBSERVED','Decomposition','Features grouped from visible construction seams and housings.',45); note(ax,58,13,'ESTIMATED','Interfaces','Exact fasteners, hinges, panel overlaps and wiring are unknown.',45); note(ax,106,13,'PROPOSED','Assembly use','Subsystem STLs support independent edits in Tinkercad.',45)
 save(fig,'A04')
 # B01 interior
 fig,ax=setup('B01','Proposed ambulance pod interior layout','Concept-only clinical layout inside a future pod envelope. Not validated for medical workflow, accessibility or regulation.')
 # plan pod
 ax.add_patch(Rectangle((13,24),103,55,fill=False,edgecolor=PROP,lw=2)); ax.add_patch(Arc((13,51.5),20,55,theta1=90,theta2=270,color=PROP,lw=2)); ax.add_patch(Rectangle((28,39),55,16,facecolor='#e7f1ee',edgecolor=PROP,lw=1.5)); ax.text(55.5,47,'PATIENT / STRETCHER',ha='center',va='center',fontsize=10,color=INK)
 ax.add_patch(Rectangle((88,58),22,13,fill=False,edgecolor=PROP,lw=1.2)); ax.text(99,64.5,'EQUIPMENT\nRACK',ha='center',fontsize=8,color=INK)
 ax.add_patch(Rectangle((88,28),22,13,fill=False,edgecolor=PROP,lw=1.2)); ax.text(99,34.5,'OXYGEN +\nSUCTION',ha='center',fontsize=8,color=INK)
 ax.add_patch(Circle((69,65),5,fill=False,edgecolor=PROP,lw=1.2)); ax.text(69,65,'C',ha='center',va='center',fontsize=9,color=INK); ax.add_patch(Circle((69,31),5,fill=False,edgecolor=PROP,lw=1.2)); ax.text(69,31,'A',ha='center',va='center',fontsize=9,color=INK)
 ax.add_patch(Rectangle((15,43),6,17,fill=False,edgecolor=RED,lw=1.5)); ax.text(18,51.5,'DOOR',rotation=90,ha='center',va='center',fontsize=7,color=RED)
 # side info
 ax.text(123,75,'WORKING ZONES',fontsize=10,color=INK,weight='bold');
 for i,(c,t) in enumerate([(TEAL,'Patient transfer path'),(PROP,'Clinician reach zone'),(RED,'Primary emergency exit'),(BLUE,'Clinical equipment')]): ax.add_patch(Rectangle((123,67-i*9),4,4,facecolor=c,edgecolor='none')); ax.text(129,69-i*9,t,fontsize=8,color=INK,va='center')
 note(ax,12,12,'PROPOSED','Interior baseline','Stretcher centerline, clinician at side/head, assistant opposite.',44); note(ax,60,12,'PROPOSED','Systems','Monitoring, oxygen, suction, storage and crash-rated restraints.',44); note(ax,108,12,'PROPOSED','Validation needed','Human factors, infection control, EMC, fire and evacuation.',44)
 save(fig,'B01')
 # B02 tube/guideway
 fig,ax=setup('B02','Proposed tube and guideway interface','Concept section showing the ambulance pod inside a low-pressure transport tube. Interface dimensions remain open.')
 tube(ax,58,52,34); ax.add_patch(Rectangle((31,20),54,5,facecolor='#efe5db',edgecolor=PROP,lw=1)); ax.add_patch(Rectangle((38,25),40,4,facecolor=PROP,alpha=.35,edgecolor=PROP)); mock_front(ax,43,31,.72)
 for x in [37,79]: ax.add_patch(Rectangle((x,28),4,10,facecolor=TEAL,edgecolor=PROP)); ax.text(x+2,26,'guide rail',ha='center',fontsize=7,color=PROP)
 dim(ax,(24,14),(92,14),'Tube ID 3600 mm (PROPOSED)',color=PROP); dim(ax,(39,83),(77,83),'Pod width 1800 mm (PROPOSED)',color=PROP)
 ax.text(104,76,'INTERFACE ZONES',fontsize=10,color=INK,weight='bold');
 for yy,t in [(67,'Pod primary structure'),(57,'Levitation air gap / guide reaction'),(47,'Linear propulsion reaction rail'),(37,'Service / rescue walkway'),(27,'Tube pressure boundary')]: ax.plot([104,111],[yy,yy],color=PROP,lw=4); ax.text(114,yy,t,fontsize=8.5,color=INK,va='center')
 note(ax,103,13,'PROPOSED','Open engineering questions','Gap control, vacuum loads, rail tolerance, thermal growth, rescue access and debris protection.',47)
 save(fig,'B02')
 # B03 propulsion
 fig,ax=setup('B03','Levitation and propulsion zone diagram','Functional architecture only. Magnet topology, force, power, air gap and control laws are not specified.')
 ax.add_patch(Rectangle((20,50),115,10,facecolor='#e8e6e5',edgecolor=PROP,lw=1.5)); ax.text(77.5,55,'POD UNDERSIDE / REACTION STRUCTURE',ha='center',va='center',fontsize=10,color=INK)
 for x in np.linspace(28,127,8): ax.add_patch(Rectangle((x,39),7,7,facecolor=TEAL,edgecolor=PROP,lw=.8))
 ax.add_patch(Rectangle((20,29),115,7,facecolor='#efe5db',edgecolor=PROP,lw=1.2)); ax.text(77.5,32.5,'GUIDEWAY PROPULSION STATOR / REACTION RAIL',ha='center',va='center',fontsize=9,color=INK)
 for x in [35,60,85,110]: ax.add_patch(FancyArrowPatch((x,39),(x,49),arrowstyle='<->',color=EST,mutation_scale=12)); ax.text(x+2,44,'gap',fontsize=7,color=EST)
 ax.add_patch(FancyArrowPatch((38,66),(120,66),arrowstyle='-|>',color=PROP,mutation_scale=18,lw=2)); ax.text(79,69,'thrust direction',ha='center',fontsize=9,color=PROP)
 for x,y,t in [(18,81,'LEVITATION'),(67,81,'LATERAL GUIDANCE'),(116,81,'PROPULSION')]: ax.add_patch(Rectangle((x,y),34,7,fill=False,edgecolor=PROP,lw=1)); ax.text(x+17,y+3.5,t,ha='center',va='center',fontsize=8,color=INK)
 note(ax,16,13,'PROPOSED','Control loop','Gap sensors -> vehicle controller -> levitation current.',40); note(ax,60,13,'PROPOSED','Power','Segmented wayside power and isolated emergency coast/brake mode.',40); note(ax,104,13,'PROPOSED','Fail-safe work','Define passive support, braking, thermal and fault containment.',40)
 save(fig,'B03')
 # B04 sensors/egress
 fig,ax=setup('B04','Sensor placement and emergency egress','Proposed placement map with two independent egress directions. Final placement depends on structure and certification.')
 mock_side(ax,17,25,1.05,'OBSERVED')
 sensors=[(27,70,'CAM'),(45,76,'IMU'),(62,63,'GAP'),(30,39,'TEMP'),(52,33,'SMOKE')]
 for x,y,t in sensors: ax.add_patch(Circle((x,y),2.8,facecolor=TEAL,edgecolor=PROP)); ax.text(x,y,t,fontsize=5.5,ha='center',va='center',color=WHITE)
 ax.add_patch(FancyArrowPatch((42,42),(9,42),arrowstyle='-|>',mutation_scale=18,color=RED,lw=2)); ax.text(8,46,'PRIMARY SIDE EGRESS',fontsize=8,color=RED)
 ax.add_patch(FancyArrowPatch((57,55),(93,55),arrowstyle='-|>',mutation_scale=18,color=RED,lw=2)); ax.text(94,55,'REAR SERVICE EGRESS',fontsize=8,color=RED,va='center')
 ax.text(102,79,'SENSOR SET',fontsize=10,color=INK,weight='bold')
 entries=[('CAM','forward/rear visual'),('IMU','motion state'),('GAP','levitation clearance'),('TEMP','equipment thermal'),('SMOKE','fire detection'),('PRESS','cabin/tube pressure'),('BIO','patient monitor gateway')]
 for i,(a,b) in enumerate(entries): ax.add_patch(Circle((106,71-i*7),2,facecolor=TEAL,edgecolor='none')); ax.text(111,71-i*7,a,fontsize=8,weight='bold',color=INK,va='center'); ax.text(122,71-i*7,b,fontsize=8,color=INK2,va='center')
 note(ax,14,12,'PROPOSED','Emergency principle','Manual release, photoluminescent path, independent power and clear rescue interface.',61); note(ax,79,12,'PROPOSED','Verification','Egress time, door force, tunnel clearance, smoke spread and remote rescue.',68)
 save(fig,'B04')
 # B05 data flow
 fig,ax=setup('B05','Clinical and vehicle data-flow schematic','Logical separation between clinical data, safety control and transport operations. Cybersecurity boundaries are proposed.')
 cols=[(12,'CLINICAL EDGE',TEAL),(56,'POD SAFETY',RED),(100,'WAYSIDE / HOSPITAL',PROP)]
 for x,title,c in cols:
  ax.add_patch(Rectangle((x,24),40,58,fill=False,edgecolor=c,lw=1.5)); ax.text(x+20,78,title,ha='center',fontsize=10,color=INK,weight='bold')
 boxes=[(16,65,'Patient monitor',TEAL),(16,53,'Clinician console',TEAL),(16,41,'Camera / audio',TEAL),(60,65,'Vehicle controller',RED),(60,53,'Safety PLC',RED),(60,41,'Event recorder',RED),(104,65,'Wayside control',PROP),(104,53,'Hospital gateway',PROP),(104,41,'Emergency services',PROP)]
 for x,y,t,c in boxes: ax.add_patch(Rectangle((x,y),32,8,facecolor='#faf9f8',edgecolor=c,lw=1)); ax.text(x+16,y+4,t,ha='center',va='center',fontsize=8,color=INK)
 arrows=[((48,69),(60,69)),((48,57),(60,57)),((92,69),(104,69)),((92,57),(104,57)),((92,45),(104,45)),((32,41),(76,41))]
 for a,b in arrows: ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=12,color=INK2,lw=1))
 ax.text(80,34,'SIGNED EVENTS + TIME SYNC',ha='center',fontsize=8,color=INK2); ax.plot([20,144],[31,31],color=HAIR,lw=1)
 note(ax,13,12,'PROPOSED','Privacy boundary','Minimum necessary patient data; encrypted transport; role-based access.',43); note(ax,60,12,'PROPOSED','Safety separation','Clinical services cannot command levitation, propulsion or braking.',43); note(ax,107,12,'PROPOSED','Continuity','Offline local care remains available during network loss.',43)
 save(fig,'B05')
 # B06 index
 fig,ax=setup('B06','Integrated artifact index and revision map','Public artifact index for the mockup reconstruction, baseline concept model and this drawing set.')
 ax.text(12,81,'3D MODEL 01 | BASELINE CONCEPT',fontsize=11,color=INK,weight='bold'); ax.text(12,76,'Tube, guideway and engineering overlays. Existing 1:30 package.',fontsize=8.5,color=INK2)
 ax.text(12,65,'3D MODEL 02 | PHYSICAL MOCKUP REPLICA',fontsize=11,color=INK,weight='bold'); ax.text(12,60,'Observed shell-focused 1:10 package. Merged STL, grouped OBJ/MTL, subsystem STLs, specs and previews.',fontsize=8.5,color=INK2)
 ax.text(12,49,'2D ENGINEERING DRAWING SET',fontsize=11,color=INK,weight='bold'); ax.text(12,44,'A01-A04 physical replica; B01-B05 proposed ambulance-hyperloop systems; B06 index.',fontsize=8.5,color=INK2)
 ax.add_patch(Rectangle((104,37),42,43,fill=False,edgecolor=INK,lw=1.2)); ax.text(125,74,'STATUS KEY',ha='center',fontsize=10,color=INK,weight='bold')
 for i,(c,a,b) in enumerate([(OBS,'OBSERVED','Directly visible geometry'),(EST,'ESTIMATED','Photo-derived dimension'),(PROP,'PROPOSED','Engineering concept')]): ax.add_patch(Rectangle((109,64-i*10),4,4,facecolor=c)); ax.text(116,66-i*10,a,fontsize=8,weight='bold',color=INK,va='center'); ax.text(116,62.5-i*10,b,fontsize=7,color=INK2)
 note(ax,12,18,'ESTIMATED','Measurement revision','Replace photo-derived values after measuring W/L/H, window, bridge, bays, fans and doors.',64); note(ax,80,18,'PROPOSED','Engineering revision','Carry requirements into CAD only after clinical, safety, tube and propulsion reviews.',66)
 save(fig,'B06')

# README/source manifest
with open(OUT+'/README.md','w') as f:
 f.write('''# Trividya ambulance-hyperloop 2D engineering drawing set v1\n\nTen-sheet digital drawing set created as an exploratory, public design study.\n\n## Status language\n- **OBSERVED**: geometry directly visible in seven supplied photos.\n- **ESTIMATED**: proportions or dimensions inferred from uncalibrated photos; not measured.\n- **PROPOSED**: future ambulance-hyperloop engineering concept, not built or validated.\n\n## Sheets\n- A01 Physical mockup orthographic views\n- A02 Estimated replica dimensions\n- A03 Key sections and construction reading\n- A04 Exploded physical assembly\n- B01 Proposed ambulance pod interior layout\n- B02 Proposed tube and guideway interface\n- B03 Levitation and propulsion zone diagram\n- B04 Sensor placement and emergency egress\n- B05 Clinical and vehicle data-flow schematic\n- B06 Integrated artifact index and revision map\n\nPDF and PNG exports are accompanied by the Python/Matplotlib source. These are design-study drawings, not fabrication, clinical, safety or regulatory documents.\n''')
# Source file is already stored beside the generated files.
zip_path=os.path.join(HERE,'Trividya-2D-engineering-drawing-set-v1.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for root,dirs,files in os.walk(OUT):
  for fn in files:
   p=os.path.join(root,fn); z.write(p,os.path.relpath(p,OUT))
print(PDF); print(zip_path)
