(this.webpackJsonpstreamlit_component_template=this.webpackJsonpstreamlit_component_template||[]).push([[0],{17:function(t,e,a){t.exports=a(28)},28:function(t,e,a){"use strict";a.r(e);var o=a(6),n=a.n(o),r=a(15),c=a.n(r),i=a(0),l=a(1),s=a(2),u=a(3),d=a(8),p=a(11),m=(a(27),function(t){Object(s.a)(a,t);var e=Object(u.a)(a);function a(){var t;Object(l.a)(this,a);for(var o=arguments.length,r=new Array(o),c=0;c<o;c++)r[c]=arguments[c];return(t=e.call.apply(e,[this].concat(r))).state={isFocused:!1,recordState:null,audioDataUrl:"",reset:!1},t.render=function(){var e=t.props.theme,a={},o=t.state.recordState;if(e){var r="1px solid ".concat(t.state.isFocused?e.primaryColor:"gray");a.border=r,a.outline=r}return n.a.createElement("span",null,n.a.createElement("div",null,n.a.createElement("button",{id:"record",onClick:t.onClick_start},"Start Recording"),n.a.createElement("button",{id:"stop",onClick:t.onClick_stop},"Stop"),n.a.createElement("button",{id:"reset",onClick:t.onClick_reset},"Reset"),n.a.createElement(p.b,{state:o,onStop:t.onStop_audio,backgroundColor:"rgb(15, 17, 22)",foregroundColor:"rgb(227, 252, 3)",canvasWidth:450,canvasHeight:150}),n.a.createElement("audio",{id:"audio",controls:!0,src:t.state.audioDataUrl}),n.a.createElement("button",{id:"continue",onClick:t.onClick_continue},"Continue to Analysis")))},t.onClick_start=function(){t.setState({reset:!1,audioDataUrl:"",recordState:p.a.START}),d.a.setComponentValue("")},t.onClick_stop=function(){t.setState({reset:!1,recordState:p.a.STOP})},t.onClick_reset=function(){t.setState({reset:!0,audioDataUrl:"",recordState:p.a.STOP}),d.a.setComponentValue("")},t.onClick_continue=function(){""!==t.state.audioDataUrl&&d.a.setComponentValue(t.state.audioDataUrl)},t.onStop_audio=function(e){!0===t.state.reset?(t.setState({audioDataUrl:""}),d.a.setComponentValue("")):t.setState({audioDataUrl:e.url})},t}return Object(i.a)(a)}(d.b)),C=Object(d.c)(m);d.a.setComponentReady(),d.a.setFrameHeight(),c.a.render(n.a.createElement(n.a.StrictMode,null,n.a.createElement(C,null)),document.getElementById("root"))}},[[17,1,2]]]);
//# sourceMappingURL=main.f1f93a3c.chunk.js.map