(this.webpackJsonpstreamlit_component_template=this.webpackJsonpstreamlit_component_template||[]).push([[0],{15:function(e,t,n){e.exports=n(16)},16:function(e,t,n){"use strict";n.r(t);var o=n(0),a=n(1),r=n(2),c=n(3),i=n(10),s=n(6),d=n.n(s),l=n(13),p=(s.Component,document.body.appendChild(document.createElement("span"))),m=p.appendChild(document.createTextNode("")),u=p.appendChild(document.createElement("button"));u.textContent="Click Me!";var C=0,h=!1;u.onclick=function(){C+=1,i.a.setComponentValue(C)},u.onfocus=function(){h=!0},u.onblur=function(){h=!1},i.a.events.addEventListener(i.a.RENDER_EVENT,(function(e){var t=e.detail;if(t.theme){var n="1px solid var(".concat(h?"--primary-color":"gray",")");u.style.border=n,u.style.outline=n}u.disabled=t.disabled;var o=t.args.name;m.textContent="Hello, ".concat(o,"! ")+String.fromCharCode(160),i.a.setFrameHeight()})),i.a.setComponentReady(),i.a.setFrameHeight()}},[[15,1,2]]]);
//# sourceMappingURL=main.009c69af.chunk.js.map