(function(root){
  'use strict';
  const rows=[
    ['T00','Basalto','Mondo basaltico',1,'#858494','#292b37','#b2b5c3','#9da9cc',.025,11,'Fondamenti'],
    ['M01','Terra','Pianeta terrestre',0,'#4f8155','#123855','#c1c7b7','#67bcff',.035,21,'Fondamenti'],
    ['M02','Tellus','Mondo tettonico',2,'#ba7e57','#403b41','#d4b393','#e0aa7e',.023,32,'Fondamenti'],
    ['M03','Iride','Mondo minerale',3,'#3f8d8d','#362557','#c2bfa2','#a0cfe7',.028,43,'Fondamenti'],
    ['M04','Aurea','Gigante gassoso',4,'#b67d44','#4e2b30','#e7d3a1','#f1bc82',.023,54,'Inferenza'],
    ['M05','Pelago','Mondo oceanico',5,'#628f79','#063b65','#e5ddae','#62d2e5',.028,65,'Inferenza'],
    ['M06','Gemina','Due continenti',6,'#9b705b','#183c55','#9caa7c','#a5c5c9',.024,76,'Inferenza'],
    ['M07','Annula','Mondo con anelli',7,'#a78e70','#4b575c','#dad4b5','#d4c5a5',.022,87,'Inferenza'],
    ['M08','Polychroma','Province minerali',8,'#517d6f','#493b59','#bf8c58','#a3b2e8',.026,98,'Modelli'],
    ['M09','Borealis','Mondo glaciale',9,'#b2d6e1','#163b57','#e6edef','#79d8df',.022,109,'Modelli'],
    ['M10','Caerulea','Gigante atmosferico',10,'#4476ac','#142e5a','#9fb9cc','#72abed',.019,120,'Modelli'],
    ['M11','Erg','Mondo desertico',11,'#bc814f','#4a2c27','#e7c18c','#e2aa76',.027,131,'Territorio'],
    ['M12','Ares','Rilievi e bacini',12,'#9f503c','#382b33','#d79d72','#d68d7c',.026,142,'Territorio'],
    ['M13','Strata','Archivi sedimentari',13,'#aa7760','#442f35','#e4c59c','#ddb292',.021,153,'Territorio'],
    ['M14','Ignis','Mondo vulcanico',14,'#35313b','#141820','#e46e20','#e77145',.024,164,'Sintesi'],
    ['M15','Argenta','Osservatorio orbitale',15,'#9dacae','#333b4e','#d8d3ba','#b3d4e5',.022,175,'Sintesi'],
    ['M16','Prisma','Mosaico geologico',16,'#5c8685','#39394d','#b4a27a','#91c5b9',.027,186,'Sintesi']
  ];
  const planets=rows.map((r,i)=>({id:r[0],name:r[1],description:r[2],kind:r[3],land:r[4],deep:r[5],high:r[6],atmosphere:r[7],speed:r[8],seed:r[9],sector:r[10],tilt:[-.24,.28,-.34,.19,.41,-.18,.3,.47,-.2,.35,.2,-.25,.17,-.38,.3,-.2,.24][i],phase:i===1?2.2:i*.71+.4,rings:i===7||i===15,moon:i===6||i===8||i===15}));
  const expeditions={P01:['M05','M07'],P02:['M05','M06'],P03:['M09'],P04:['M07','M10'],P05:['M09','M10'],P06:['M11','M16'],P07:['M12'],P08:['M13'],P09:['M14'],P10:['M15'],P11:['M16']};
  const byId=Object.fromEntries(planets.map(p=>[p.id,p]));
  Object.entries(expeditions).forEach(([id,parents],i)=>{byId[id]={...byId[parents[0]],id,name:'Spedizione '+id,description:'Missione applicativa',parents,seed:230+i*13,phase:.5+i*.6,moon:false,rings:false,expedition:true};});
  root.GeoPlanets=Object.freeze({planets,byId,expeditions,sectors:[...new Set(planets.map(p=>p.sector))]});
})(globalThis);
