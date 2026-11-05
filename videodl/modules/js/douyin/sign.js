/*
 * 抖音 a_bogus 签名器（node 版，供 videodl 调用）。
 *
 * 用法：node sign.js "<query_string>" "<post_data>" "<user_agent>"
 *   stdout 输出 a_bogus 字符串。
 *
 * 算法文件按版本存放：a_bogus.<version>.js（入口 get_abogus(query, post, ua)）。
 * 用环境变量 ABOGUS_VERSION 选择版本，默认见 DEFAULT_VERSION。
 *
 * 实现参考：hhy5562877/douyin_mcp（MIT License）。该项目用 py_mini_racer 跑
 * douyin.js；这里改为用 node 内置 vm 模块跑（videodl 已自带 node，无需额外依赖）。
 * 浏览器环境 polyfill 沿用其 sign.py 的 JS_BROWSER_ENV（已与该 douyin.js 验证匹配），
 * 仅把 navigator.userAgent 改成调用方传入的 UA。
 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const DEFAULT_VERSION = '1.0.1.5';

function abogus(query, post, ua) {
  const version = process.env.ABOGUS_VERSION || DEFAULT_VERSION;
  const algoPath = path.join(__dirname, `a_bogus.${version}.js`);
  let algo = fs.readFileSync(algoPath, 'utf8');
  // 剥掉 douyin.js 自带的坏 polyfill：保留从 `window.bdms || function()` 开始的真实算法
  const m = algo.search(/window\.bdms\s*\|\|\s*function/);
  if (m > 0) algo = algo.slice(m);

  const ENV = browserEnv(ua);
  const sandbox = {};
  vm.createContext(sandbox);
  vm.runInContext(ENV, sandbox, { timeout: 8000 });
  vm.runInContext(algo, sandbox, { timeout: 8000 });
  vm.runInContext(
    `var __q=${JSON.stringify(query)},__p=${JSON.stringify(post)},__ua=${JSON.stringify(ua)};`,
    sandbox
  );
  return vm.runInContext('get_abogus(__q, __p, __ua)', sandbox, { timeout: 8000 });
}

// 浏览器环境 polyfill（喂给纯 V8 上下文，让签名算法跑起来）。
function browserEnv(ua) {
  const UA = JSON.stringify(ua || 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36');
  return `
var global = {};
var window = global;
var self = global;
var console = { log:function(){}, warn:function(){}, error:function(){}, info:function(){}, debug:function(){}, trace:function(){} };
var document = {
  cookie:'', domain:'www.douyin.com', referrer:'', title:'', URL:'https://www.douyin.com/', all:[],
  documentElement:{ style:{}, clientWidth:2560, clientHeight:1440 },
  body:null, head:null, hidden:false, visibilityState:'visible', readyState:'complete',
  createElement:function(tag){
    var elem={ tagName:tag?tag.toUpperCase():'DIV', style:{}, attributes:{}, children:[], childNodes:[],
      innerHTML:'', innerText:'', textContent:'', outerHTML:'', src:'', href:'', type:'', id:'', className:'',
      async:false, defer:false, onload:null, onerror:null, onreadystatechange:null, readyState:'complete',
      parentNode:null, parentElement:null, firstChild:null, lastChild:null, nextSibling:null, previousSibling:null,
      nodeType:1, nodeName:tag?tag.toUpperCase():'DIV', ownerDocument:document,
      getAttribute:function(n){return this.attributes[n]||null;}, setAttribute:function(n,v){this.attributes[n]=String(v);},
      removeAttribute:function(n){delete this.attributes[n];}, hasAttribute:function(n){return n in this.attributes;},
      appendChild:function(c){this.children.push(c);this.childNodes.push(c);if(c&&typeof c==='object')c.parentNode=this;return c;},
      removeChild:function(c){var i=this.children.indexOf(c);if(i>-1)this.children.splice(i,1);return c;},
      insertBefore:function(a,b){return a;}, replaceChild:function(a,b){return b;}, cloneNode:function(){return Object.assign({},this);},
      addEventListener:function(){}, removeEventListener:function(){}, dispatchEvent:function(){return true;},
      click:function(){}, focus:function(){}, blur:function(){},
      getBoundingClientRect:function(){return {top:0,left:0,right:0,bottom:0,width:0,height:0,x:0,y:0};},
      getClientRects:function(){return [];}, matches:function(){return false;}, closest:function(){return null;},
      contains:function(){return false;}, querySelector:function(){return null;}, querySelectorAll:function(){return [];},
      getElementsByTagName:function(){return [];}, getElementsByClassName:function(){return [];}
    };
    if(tag&&tag.toLowerCase()==='canvas'){
      elem.width=300; elem.height=150;
      elem.getContext=function(){return {
        fillRect:function(){}, clearRect:function(){},
        getImageData:function(x,y,w,h){return {data:new Uint8ClampedArray((w||1)*(h||1)*4),width:w,height:h};},
        putImageData:function(){}, createImageData:function(w,h){return {data:new Uint8ClampedArray(w*h*4),width:w,height:h};},
        setTransform:function(){}, drawImage:function(){}, save:function(){}, restore:function(){},
        fillText:function(){}, strokeText:function(){}, measureText:function(){return {width:0};},
        arc:function(){}, fill:function(){}, stroke:function(){}, beginPath:function(){}, closePath:function(){},
        moveTo:function(){}, lineTo:function(){}, clip:function(){}, rect:function(){}, scale:function(){},
        rotate:function(){}, translate:function(){}, transform:function(){},
        createLinearGradient:function(){return {addColorStop:function(){}};},
        createRadialGradient:function(){return {addColorStop:function(){}};},
        canvas:elem, fillStyle:'#000000', strokeStyle:'#000000', lineWidth:1, font:'10px sans-serif',
        globalAlpha:1, globalCompositeOperation:'source-over'
      };};
      elem.toDataURL=function(){return 'data:image/png;base64,';};
    }
    return elem;
  },
  createEvent:function(t){return {type:t, initEvent:function(x){this.type=x;}, preventDefault:function(){}, stopPropagation:function(){}};},
  createTextNode:function(t){return {nodeValue:t, textContent:t, nodeType:3, nodeName:'#text', data:t, length:t?t.length:0};},
  createDocumentFragment:function(){return {appendChild:function(c){return c;}, children:[], childNodes:[], nodeType:11, nodeName:'#document-fragment'};},
  getElementById:function(){return null;}, getElementsByTagName:function(){return [];}, getElementsByClassName:function(){return [];},
  querySelector:function(){return null;}, querySelectorAll:function(){return [];},
  addEventListener:function(){}, removeEventListener:function(){}, hasFocus:function(){return true;},
  write:function(){}, writeln:function(){}, open:function(){}, close:function(){}
};
document.body = document.createElement('body');
document.head = document.createElement('head');
var navigator = {
  userAgent: ${UA}, platform:'MacIntel', language:'zh-CN', languages:['zh-CN','zh'], cookieEnabled:true, onLine:true,
  hardwareConcurrency:8, deviceMemory:8, maxTouchPoints:0, vendor:'Google Inc.', appName:'Netscape', appVersion:'5.0',
  product:'Gecko', connection:{effectiveType:'4g',downlink:10,rtt:100}, plugins:{length:0}, mimeTypes:{length:0}
};
var location = { href:'https://www.douyin.com/', protocol:'https:', host:'www.douyin.com', hostname:'www.douyin.com', port:'', pathname:'/', search:'', hash:'', origin:'https://www.douyin.com' };
var screen = { width:2560, height:1440, availWidth:2560, availHeight:1400, colorDepth:24, pixelDepth:24, orientation:{type:'landscape-primary',angle:0} };
var history = { length:1, state:null, pushState:function(){}, replaceState:function(){}, go:function(){}, back:function(){}, forward:function(){} };
var performance = { now:function(){return Date.now();}, timing:{navigationStart:Date.now()} };
var crypto = { getRandomValues:function(a){for(var i=0;i<a.length;i++)a[i]=Math.floor(Math.random()*256);return a;}, subtle:{} };
var XMLHttpRequest = function(){ this.readyState=0; this.status=0; this.statusText=''; this.responseText=''; this.response=''; this.onreadystatechange=null; this.onload=null; this.onerror=null; };
XMLHttpRequest.prototype = { open:function(){}, send:function(){}, abort:function(){}, setRequestHeader:function(){}, getResponseHeader:function(){return null;}, getAllResponseHeaders:function(){return '';}, addEventListener:function(){}, removeEventListener:function(){} };
XMLHttpRequest.UNSENT=0; XMLHttpRequest.OPENED=1; XMLHttpRequest.HEADERS_RECEIVED=2; XMLHttpRequest.LOADING=3; XMLHttpRequest.DONE=4;
var fetch = function(){ return Promise.resolve({ ok:true, status:200, json:function(){return Promise.resolve({});}, text:function(){return Promise.resolve('');} }); };
var Storage = function(){ this._data={}; };
Storage.prototype = { getItem:function(k){return this._data[k]||null;}, setItem:function(k,v){this._data[k]=String(v);}, removeItem:function(k){delete this._data[k];}, clear:function(){this._data={};} };
var localStorage = new Storage();
var sessionStorage = new Storage();
var TextEncoder = function(){ this.encode=function(s){var a=[];for(var i=0;i<s.length;i++){var c=s.charCodeAt(i);if(c<128)a.push(c);else if(c<2048){a.push((c>>6)|192);a.push((c&63)|128);}else{a.push((c>>12)|224);a.push(((c>>6)&63)|128);a.push((c&63)|128);}}return new Uint8Array(a);}; };
var TextDecoder = function(){ this.decode=function(a){var r='';for(var i=0;i<a.length;i++)r+=String.fromCharCode(a[i]);return r;}; };
var atob = function(str){ var chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='; var output=''; str=String(str).replace(/=+$/,''); for(var bc=0,bs,buffer,idx=0; buffer=str.charAt(idx++); ~buffer&&(bs=bc%4?bs*64+buffer:buffer,bc++%4)?output+=String.fromCharCode(255&bs>>(-2*bc&6)):0){buffer=chars.indexOf(buffer);} return output; };
var btoa = function(str){ var chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='; var output=''; for(var block,charCode,idx=0,map=chars; str.charAt(idx|0)||(map='=',idx%1); output+=map.charAt(63&block>>8-idx%1*8)){charCode=str.charCodeAt(idx+=3/4);block=block<<8|charCode;} return output; };
var setTimeout=function(){return 0;}; var setInterval=function(){return 0;}; var clearTimeout=function(){}; var clearInterval=function(){};
var requestAnimationFrame=function(){return 0;}; var cancelAnimationFrame=function(){};
var Event=function(t){this.type=t;}; Event.prototype={preventDefault:function(){}, stopPropagation:function(){}};
var CustomEvent=Event; var MessageEvent=Event;
var Blob=function(){this.size=0;this.type='';}; var File=Blob; var FileReader=function(){}; var FormData=function(){};
var URL=function(u){this.href=u;}; URL.createObjectURL=function(){return 'blob:null';}; URL.revokeObjectURL=function(){};
var Worker=function(){this.postMessage=function(){};this.terminate=function(){};};
var WebSocket=function(){this.send=function(){};this.close=function(){};};
var MutationObserver=function(){this.observe=function(){};this.disconnect=function(){};};
var ResizeObserver=MutationObserver; var IntersectionObserver=MutationObserver;
var Image=function(){this.src='';this.onload=null;}; var Audio=function(){this.play=function(){return Promise.resolve();};};
window.innerWidth=2560; window.innerHeight=1440; window.outerWidth=2560; window.outerHeight=1440;
window.screenX=0; window.screenY=0; window.pageXOffset=0; window.pageYOffset=0; window.scrollX=0; window.scrollY=0; window.devicePixelRatio=1;
window.document=document; window.navigator=navigator; window.location=location; window.screen=screen; window.history=history;
window.performance=performance; window.crypto=crypto; window.localStorage=localStorage; window.sessionStorage=sessionStorage; window.console=console;
window.XMLHttpRequest=XMLHttpRequest; window.fetch=fetch; window.TextEncoder=TextEncoder; window.TextDecoder=TextDecoder; window.atob=atob; window.btoa=btoa;
window.setTimeout=setTimeout; window.setInterval=setInterval; window.clearTimeout=clearTimeout; window.clearInterval=clearInterval;
window.requestAnimationFrame=requestAnimationFrame; window.cancelAnimationFrame=cancelAnimationFrame;
window.Event=Event; window.CustomEvent=CustomEvent; window.Blob=Blob; window.URL=URL; window.Worker=Worker; window.WebSocket=WebSocket;
window.MutationObserver=MutationObserver; window.Image=Image; window.Audio=Audio;
window.getComputedStyle=function(){return {getPropertyValue:function(){return '';}};};
window.matchMedia=function(q){return {matches:false, media:q, addListener:function(){}, removeListener:function(){}};};
window.open=function(){return null;}; window.close=function(){}; window.focus=function(){}; window.blur=function(){};
window.alert=function(){}; window.confirm=function(){return true;}; window.prompt=function(){return null;};
window.addEventListener=function(){}; window.removeEventListener=function(){}; window.dispatchEvent=function(){return true;};
window.postMessage=function(){}; window.scrollTo=function(){}; window.scroll=function(){}; window.scrollBy=function(){};
window._sdkGlueVersionMap={ "sdkGlueVersion":"1.0.0.49", "bdmsVersion":"1.0.1.1", "captchaVersion":"4.0.2" };
`;
}

module.exports = { abogus };

// CLI: node sign.js <query> <post> <ua>
if (require.main === module) {
  const [query, post, ua] = [process.argv[2] || '', process.argv[3] || '', process.argv[4] || ''];
  try {
    const out = abogus(query, post, ua);
    process.stdout.write(String(out || ''));
  } catch (e) {
    process.stderr.write('ABOGUS_ERROR: ' + (e && e.message ? e.message : String(e)));
    process.exit(1);
  }
}
