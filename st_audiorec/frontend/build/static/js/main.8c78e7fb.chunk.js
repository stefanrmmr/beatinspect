(this.webpackJsonpstreamlit_component_template=this.webpackJsonpstreamlit_component_template||[]).push([[0],{17:function(t,e,a){t.exports=a(28)},28:function(t,e,a){"use strict";a.r(e);var n=a(6),o=a.n(n),r=a(15),s=a.n(r),i=a(0),c=a(1),l=a(2),u=a(3),d=a(8),p=a(11),m=(a(27),function(t){Object(l.a)(a,t);var e=Object(u.a)(a);function a(){var t;Object(c.a)(this,a);for(var n=arguments.length,r=new Array(n),s=0;s<n;s++)r[s]=arguments[s];return(t=e.call.apply(e,[this].concat(r))).state={isFocused:!1,recordState:null,audioDataURL:"",reset:!1,base64data:""},t.render=function(){var e=t.props.theme,a={},n=t.state.recordState;if(e){var r="1px solid ".concat(t.state.isFocused?e.primaryColor:"gray");a.border=r,a.outline=r}return o.a.createElement("span",null,o.a.createElement("div",null,o.a.createElement("button",{id:"record",onClick:t.onClick_start},"Start Recording"),o.a.createElement("button",{id:"stop",onClick:t.onClick_stop},"Stop"),o.a.createElement("button",{id:"reset",onClick:t.onClick_reset},"Reset"),o.a.createElement(p.b,{state:n,onStop:t.onStop_audio,type:"audio/wav",backgroundColor:"rgb(15, 17, 22)",foregroundColor:"rgb(227, 252, 3)",canvasWidth:450,canvasHeight:100}),o.a.createElement("audio",{id:"audio",controls:!0,src:t.state.audioDataURL}),o.a.createElement("button",{id:"continue",onClick:t.onClick_continue},"Continue to Analysis")))},t.onClick_start=function(){t.setState({reset:!1,audioDataURL:"",recordState:p.a.START}),d.a.setComponentValue("")},t.onClick_stop=function(){t.setState({reset:!1,recordState:p.a.STOP})},t.onClick_reset=function(){t.setState({reset:!0,audioDataURL:"",recordState:p.a.STOP}),d.a.setComponentValue("")},t.onClick_continue=function(){""!==t.state.audioDataURL&&d.a.setComponentValue(t.state.base64data)},t.onStop_audio=function(e){if(!0===t.state.reset)t.setState({audioDataURL:""}),d.a.setComponentValue("");else{var a;t.setState({audioDataURL:e.url});var n=new XMLHttpRequest;n.open("GET",e.url,!0),n.responseType="blob",n.onload=function(t){if(200==this.status){var e=this.response,n=new FileReader;n.readAsDataURL(e),n.onloadend=function(){a=n.result}}},n.send(),t.setState({base64data:String(a)})}},t}return Object(i.a)(a)}(d.b)),b=Object(d.c)(m);d.a.setComponentReady(),d.a.setFrameHeight(),s.a.render(o.a.createElement(o.a.StrictMode,null,o.a.createElement(b,null)),document.getElementById("root"))}},[[17,1,2]]]);
//# sourceMappingURL=main.8c78e7fb.chunk.js.map