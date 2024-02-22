import{b as G,i as v,m as O,G as j,l as A}from"./layout-ue_8KlME.js";import{i as M,u as _,s as H,a as V,b as U,p as D,c as W,d as Y,e as q,f as z,g as L,h as C}from"./edges-5ec2587c-mED27liZ.js";import{l as i,o as N,c as S}from"./mermaid-JzgFY9bh.js";import{c as K}from"./createText-a48a4c90-c10_cUgP.js";import{af as T}from"./index-Pz--jxPk.js";var Q=4;function Z(e){return G(e,Q)}function x(e){var t={options:{directed:e.isDirected(),multigraph:e.isMultigraph(),compound:e.isCompound()},nodes:I(e),edges:tt(e)};return v(e.graph())||(t.value=Z(e.graph())),t}function I(e){return O(e.nodes(),function(t){var n=e.node(t),r=e.parent(t),s={v:t};return v(n)||(s.value=n),v(r)||(s.parent=r),s})}function tt(e){return O(e.edges(),function(t){var n=e.edge(t),r={v:t.v,w:t.w};return v(t.name)||(r.name=t.name),v(n)||(r.value=n),r})}let f={},g={},J={};const et=()=>{g={},J={},f={}},X=(e,t)=>(i.trace("In isDecendant",t," ",e," = ",g[t].includes(e)),!!g[t].includes(e)),nt=(e,t)=>(i.info("Decendants of ",t," is ",g[t]),i.info("Edge is ",e),e.v===t||e.w===t?!1:g[t]?g[t].includes(e.v)||X(e.v,t)||X(e.w,t)||g[t].includes(e.w):(i.debug("Tilt, ",t,",not in decendants"),!1)),R=(e,t,n,r)=>{i.warn("Copying children of ",e,"root",r,"data",t.node(e),r);const s=t.children(e)||[];e!==r&&s.push(e),i.warn("Copying (nodes) clusterId",e,"nodes",s),s.forEach(c=>{if(t.children(c).length>0)R(c,t,n,r);else{const d=t.node(c);i.info("cp ",c," to ",r," with parent ",e),n.setNode(c,d),r!==t.parent(c)&&(i.warn("Setting parent",c,t.parent(c)),n.setParent(c,t.parent(c))),e!==r&&c!==e?(i.debug("Setting parent",c,e),n.setParent(c,e)):(i.info("In copy ",e,"root",r,"data",t.node(e),r),i.debug("Not Setting parent for node=",c,"cluster!==rootId",e!==r,"node!==clusterId",c!==e));const l=t.edges(c);i.debug("Copying Edges",l),l.forEach(u=>{i.info("Edge",u);const h=t.edge(u.v,u.w,u.name);i.info("Edge data",h,r);try{nt(u,r)?(i.info("Copying as ",u.v,u.w,h,u.name),n.setEdge(u.v,u.w,h,u.name),i.info("newGraph edges ",n.edges(),n.edge(n.edges()[0]))):i.info("Skipping copy of edge ",u.v,"-->",u.w," rootId: ",r," clusterId:",e)}catch(w){i.error(w)}})}i.debug("Removing node",c),t.removeNode(c)})},p=(e,t)=>{const n=t.children(e);let r=[...n];for(const s of n)J[s]=e,r=[...r,...p(s,t)];return r},b=(e,t)=>{i.trace("Searching",e);const n=t.children(e);if(i.trace("Searching children of id ",e,n),n.length<1)return i.trace("This is a valid node",e),e;for(const r of n){const s=b(r,t);if(s)return i.trace("Found replacement for",e," => ",s),s}},E=e=>!f[e]||!f[e].externalConnections?e:f[e]?f[e].id:e,it=(e,t)=>{if(!e||t>10){i.debug("Opting out, no graph ");return}else i.debug("Opting in, graph ");e.nodes().forEach(function(n){e.children(n).length>0&&(i.warn("Cluster identified",n," Replacement id in edges: ",b(n,e)),g[n]=p(n,e),f[n]={id:b(n,e),clusterData:e.node(n)})}),e.nodes().forEach(function(n){const r=e.children(n),s=e.edges();r.length>0?(i.debug("Cluster identified",n,g),s.forEach(c=>{if(c.v!==n&&c.w!==n){const d=X(c.v,n),l=X(c.w,n);d^l&&(i.warn("Edge: ",c," leaves cluster ",n),i.warn("Decendants of XXX ",n,": ",g[n]),f[n].externalConnections=!0)}})):i.debug("Not a cluster ",n,g)}),e.edges().forEach(function(n){const r=e.edge(n);i.warn("Edge "+n.v+" -> "+n.w+": "+JSON.stringify(n)),i.warn("Edge "+n.v+" -> "+n.w+": "+JSON.stringify(e.edge(n)));let s=n.v,c=n.w;if(i.warn("Fix XXX",f,"ids:",n.v,n.w,"Translating: ",f[n.v]," --- ",f[n.w]),f[n.v]&&f[n.w]&&f[n.v]===f[n.w]){i.warn("Fixing and trixing link to self - removing XXX",n.v,n.w,n.name),i.warn("Fixing and trixing - removing XXX",n.v,n.w,n.name),s=E(n.v),c=E(n.w),e.removeEdge(n.v,n.w,n.name);const d=n.w+"---"+n.v;e.setNode(d,{domId:d,id:d,labelStyle:"",labelText:r.label,padding:0,shape:"labelRect",style:""});const l=structuredClone(r),u=structuredClone(r);l.label="",l.arrowTypeEnd="none",u.label="",l.fromCluster=n.v,u.toCluster=n.v,e.setEdge(s,d,l,n.name+"-cyclic-special"),e.setEdge(d,c,u,n.name+"-cyclic-special")}else(f[n.v]||f[n.w])&&(i.warn("Fixing and trixing - removing XXX",n.v,n.w,n.name),s=E(n.v),c=E(n.w),e.removeEdge(n.v,n.w,n.name),s!==n.v&&(r.fromCluster=n.v),c!==n.w&&(r.toCluster=n.w),i.warn("Fix Replacing with XXX",s,c,n.name),e.setEdge(s,c,r,n.name))}),i.warn("Adjusted Graph",x(e)),P(e,0),i.trace(f)},P=(e,t)=>{if(i.warn("extractor - ",t,x(e),e.children("D")),t>10){i.error("Bailing out");return}let n=e.nodes(),r=!1;for(const s of n){const c=e.children(s);r=r||c.length>0}if(!r){i.debug("Done, no node has children",e.nodes());return}i.debug("Nodes = ",n,t);for(const s of n)if(i.debug("Extracting node",s,f,f[s]&&!f[s].externalConnections,!e.parent(s),e.node(s),e.children("D")," Depth ",t),!f[s])i.debug("Not a cluster",s,t);else if(!f[s].externalConnections&&e.children(s)&&e.children(s).length>0){i.warn("Cluster without external connections, without a parent and with children",s,t);let d=e.graph().rankdir==="TB"?"LR":"TB";f[s]&&f[s].clusterData&&f[s].clusterData.dir&&(d=f[s].clusterData.dir,i.warn("Fixing dir",f[s].clusterData.dir,d));const l=new j({multigraph:!0,compound:!0}).setGraph({rankdir:d,nodesep:50,ranksep:50,marginx:8,marginy:8}).setDefaultEdgeLabel(function(){return{}});i.warn("Old graph before copy",x(e)),R(s,e,l,s),e.setNode(s,{clusterNode:!0,id:s,clusterData:f[s].clusterData,labelText:f[s].labelText,graph:l}),i.warn("New graph after copy node: (",s,")",x(l)),i.debug("Old graph after copy",x(e))}else i.warn("Cluster ** ",s," **not meeting the criteria !externalConnections:",!f[s].externalConnections," no parent: ",!e.parent(s)," children ",e.children(s)&&e.children(s).length>0,e.children("D"),t),i.debug(f);n=e.nodes(),i.warn("New list of nodes",n);for(const s of n){const c=e.node(s);i.warn(" Now next level",s,c),c.clusterNode&&P(c.graph,t+1)}},F=(e,t)=>{if(t.length===0)return[];let n=Object.assign(t);return t.forEach(r=>{const s=e.children(r),c=F(e,s);n=[...n,...c]}),n},st=e=>F(e,e.children()),rt=(e,t)=>{i.info("Creating subgraph rect for ",t.id,t);const n=e.insert("g").attr("class","cluster"+(t.class?" "+t.class:"")).attr("id",t.id),r=n.insert("rect",":first-child"),s=N(S().flowchart.htmlLabels),c=n.insert("g").attr("class","cluster-label"),d=t.labelType==="markdown"?K(c,t.labelText,{style:t.labelStyle,useHtmlLabels:s}):c.node().appendChild(L(t.labelText,t.labelStyle,void 0,!0));let l=d.getBBox();if(N(S().flowchart.htmlLabels)){const a=d.children[0],o=T(d);l=a.getBoundingClientRect(),o.attr("width",l.width),o.attr("height",l.height)}const u=0*t.padding,h=u/2,w=t.width<=l.width+u?l.width+u:t.width;t.width<=l.width+u?t.diff=(l.width-t.width)/2-t.padding/2:t.diff=-t.padding/2,i.trace("Data ",t,JSON.stringify(t)),r.attr("style",t.style).attr("rx",t.rx).attr("ry",t.ry).attr("x",t.x-w/2).attr("y",t.y-t.height/2-h).attr("width",w).attr("height",t.height+u),s?c.attr("transform","translate("+(t.x-l.width/2)+", "+(t.y-t.height/2)+")"):c.attr("transform","translate("+t.x+", "+(t.y-t.height/2)+")");const m=r.node().getBBox();return t.width=m.width,t.height=m.height,t.intersect=function(a){return C(t,a)},n},at=(e,t)=>{const n=e.insert("g").attr("class","note-cluster").attr("id",t.id),r=n.insert("rect",":first-child"),s=0*t.padding,c=s/2;r.attr("rx",t.rx).attr("ry",t.ry).attr("x",t.x-t.width/2-c).attr("y",t.y-t.height/2-c).attr("width",t.width+s).attr("height",t.height+s).attr("fill","none");const d=r.node().getBBox();return t.width=d.width,t.height=d.height,t.intersect=function(l){return C(t,l)},n},ct=(e,t)=>{const n=e.insert("g").attr("class",t.classes).attr("id",t.id),r=n.insert("rect",":first-child"),s=n.insert("g").attr("class","cluster-label"),c=n.append("rect"),d=s.node().appendChild(L(t.labelText,t.labelStyle,void 0,!0));let l=d.getBBox();if(N(S().flowchart.htmlLabels)){const a=d.children[0],o=T(d);l=a.getBoundingClientRect(),o.attr("width",l.width),o.attr("height",l.height)}l=d.getBBox();const u=0*t.padding,h=u/2,w=t.width<=l.width+t.padding?l.width+t.padding:t.width;t.width<=l.width+t.padding?t.diff=(l.width+t.padding*0-t.width)/2:t.diff=-t.padding/2,r.attr("class","outer").attr("x",t.x-w/2-h).attr("y",t.y-t.height/2-h).attr("width",w+u).attr("height",t.height+u),c.attr("class","inner").attr("x",t.x-w/2-h).attr("y",t.y-t.height/2-h+l.height-1).attr("width",w+u).attr("height",t.height+u-l.height-3),s.attr("transform","translate("+(t.x-l.width/2)+", "+(t.y-t.height/2-t.padding/3+(N(S().flowchart.htmlLabels)?5:3))+")");const m=r.node().getBBox();return t.height=m.height,t.intersect=function(a){return C(t,a)},n},ot=(e,t)=>{const n=e.insert("g").attr("class",t.classes).attr("id",t.id),r=n.insert("rect",":first-child"),s=0*t.padding,c=s/2;r.attr("class","divider").attr("x",t.x-t.width/2-c).attr("y",t.y-t.height/2).attr("width",t.width+s).attr("height",t.height+s);const d=r.node().getBBox();return t.width=d.width,t.height=d.height,t.diff=-t.padding/2,t.intersect=function(l){return C(t,l)},n},lt={rect:rt,roundedWithTitle:ct,noteGroup:at,divider:ot};let k={};const ft=(e,t)=>{i.trace("Inserting cluster");const n=t.shape||"rect";k[t.id]=lt[n](e,t)},dt=()=>{k={}},$=async(e,t,n,r,s)=>{i.info("Graph in recursive render: XXX",x(t),s);const c=t.graph().rankdir;i.trace("Dir in recursive render - dir:",c);const d=e.insert("g").attr("class","root");t.nodes()?i.info("Recursive render XXX",t.nodes()):i.info("No nodes found for",t),t.edges().length>0&&i.trace("Recursive edges",t.edge(t.edges()[0]));const l=d.insert("g").attr("class","clusters"),u=d.insert("g").attr("class","edgePaths"),h=d.insert("g").attr("class","edgeLabels"),w=d.insert("g").attr("class","nodes");await Promise.all(t.nodes().map(async function(a){const o=t.node(a);if(s!==void 0){const y=JSON.parse(JSON.stringify(s.clusterData));i.info("Setting data for cluster XXX (",a,") ",y,s),t.setNode(s.id,y),t.parent(a)||(i.trace("Setting parent",a,s.id),t.setParent(a,s.id,y))}if(i.info("(Insert) Node XXX"+a+": "+JSON.stringify(t.node(a))),o&&o.clusterNode){i.info("Cluster identified",a,o.width,t.node(a));const y=await $(w,o.graph,n,r,t.node(a)),B=y.elem;_(o,B),o.diff=y.diff||0,i.info("Node bounds (abc123)",a,o,o.width,o.x,o.y),H(B,o),i.warn("Recursive render complete ",B,o)}else t.children(a).length>0?(i.info("Cluster - the non recursive path XXX",a,o.id,o,t),i.info(b(o.id,t)),f[o.id]={id:b(o.id,t),node:o}):(i.info("Node - the non recursive path",a,o.id,o),await V(w,t.node(a),c))})),t.edges().forEach(function(a){const o=t.edge(a.v,a.w,a.name);i.info("Edge "+a.v+" -> "+a.w+": "+JSON.stringify(a)),i.info("Edge "+a.v+" -> "+a.w+": ",a," ",JSON.stringify(t.edge(a))),i.info("Fix",f,"ids:",a.v,a.w,"Translateing: ",f[a.v],f[a.w]),U(h,o)}),t.edges().forEach(function(a){i.info("Edge "+a.v+" -> "+a.w+": "+JSON.stringify(a))}),i.info("#############################################"),i.info("###                Layout                 ###"),i.info("#############################################"),i.info(t),A(t),i.info("Graph after layout:",x(t));let m=0;return st(t).forEach(function(a){const o=t.node(a);i.info("Position "+a+": "+JSON.stringify(t.node(a))),i.info("Position "+a+": ("+o.x,","+o.y,") width: ",o.width," height: ",o.height),o&&o.clusterNode?D(o):t.children(a).length>0?(ft(l,o),f[o.id].node=o):D(o)}),t.edges().forEach(function(a){const o=t.edge(a);i.info("Edge "+a.v+" -> "+a.w+": "+JSON.stringify(o),o);const y=W(u,a,o,f,n,t,r);Y(o,y)}),t.nodes().forEach(function(a){const o=t.node(a);i.info(a,o.type,o.diff),o.type==="group"&&(m=o.diff)}),{elem:d,diff:m}},yt=async(e,t,n,r,s)=>{M(e,n,r,s),q(),z(),dt(),et(),i.warn("Graph at first:",JSON.stringify(x(t))),it(t),i.warn("Graph after:",JSON.stringify(x(t))),await $(e,t,r,s)};export{yt as r};
