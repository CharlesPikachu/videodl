// Adapted from https://raw.githubusercontent.com/ZSAIm/iqiyi-parser/master/js/tencent.js

var document = {
    URL: "",
    referrer: ""
}

var window = {
    document: document,
    navigator: {
        userAgent: "Mozilla/5.0 (Linux; U; Android 9; zh-cn) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Safari/537.36",
        appCodeName: "Mozilla",
        appName: "Netscape",
        platform: "Linux"
    },
};


function w() {
    Fa = new Int8Array(Ea),
        Ha = new Int16Array(Ea),
        Ja = new Int32Array(Ea),
        Ga = new Uint8Array(Ea),
        Ia = new Uint16Array(Ea),
        Ka = new Uint32Array(Ea),
        La = new Float32Array(Ea),
        Ma = new Float64Array(Ea);
}

function d(a) {
    var b = Oa;
    return Oa = Oa + a + 15 & -16,
        b
}

function e(a, b) {
    b || (b = Da);
    var c = a = Math.ceil(a / b) * b;
    return c
}

function i(a, b, c, d, e){
    function f(a) {
        return "string" === b ? k(a) : "boolean" === b ? Boolean(a) : a
    }
    var i = wasmobject.exports._getckey //h(a)
        , j = []
        , l = 0;
    // if (g("array" !== b, 'Return type should not be "array".'),
    //     d)
    if (d)
        for (var m = 0; m < d.length; m++) {
            var n = $a[c[m]];
            // n ? (0 === l && (l = Ub()),
            n ? (0 === l && (l = Ub()),
                j[m] = n(d[m])) : j[m] = d[m]
        }
    var o = i.apply(null, j);
    return o = f(o),
    0 !== l && Tb(l),
        o

}

function k(a, b) {
    if (0 === b || !a)
        return "";
    for (var c, d = 0, e = 0; ; ) {
        // if (g(a + e < db),
        if (
            c = Ga[a + e >> 0],
                d |= c,
            0 == c && !b)
            break;
        if (e++,
        b && e == b)
            break
    }
    b || (b = e);
    var f = "";
    if (d < 128) {
        for (var h, i = 1024; b > 0; )
            h = String.fromCharCode.apply(String, Ga.subarray(a, a + Math.min(b, i))),
                f = f ? f + h : h,
                a += i,
                b -= i;
        return f
    }
    return m(a)
}

function o(a, b, c) {
    return n(a, Ga, b, c)
}

function n(a, b, c, d) {
    if (!(d > 0))
        return 0;
    for (var e = c, f = c + d - 1, g = 0; g < a.length; ++g) {
        var h = a.charCodeAt(g);
        if (h >= 55296 && h <= 57343) {
            var i = a.charCodeAt(++g);
            h = 65536 + ((1023 & h) << 10) | 1023 & i
        }
        if (h <= 127) {
            if (c >= f)
                break;
            b[c++] = h
        } else if (h <= 2047) {
            if (c + 1 >= f)
                break;
            b[c++] = 192 | h >> 6,
                b[c++] = 128 | 63 & h
        } else if (h <= 65535) {
            if (c + 2 >= f)
                break;
            b[c++] = 224 | h >> 12,
                b[c++] = 128 | h >> 6 & 63,
                b[c++] = 128 | 63 & h
        } else if (h <= 2097151) {
            if (c + 3 >= f)
                break;
            b[c++] = 240 | h >> 18,
                b[c++] = 128 | h >> 12 & 63,
                b[c++] = 128 | h >> 6 & 63,
                b[c++] = 128 | 63 & h
        } else if (h <= 67108863) {
            if (c + 4 >= f)
                break;
            b[c++] = 248 | h >> 24,
                b[c++] = 128 | h >> 18 & 63,
                b[c++] = 128 | h >> 12 & 63,
                b[c++] = 128 | h >> 6 & 63,
                b[c++] = 128 | 63 & h
        } else {
            if (c + 5 >= f)
                break;
            b[c++] = 252 | h >> 30,
                b[c++] = 128 | h >> 24 & 63,
                b[c++] = 128 | h >> 18 & 63,
                b[c++] = 128 | h >> 12 & 63,
                b[c++] = 128 | h >> 6 & 63,
                b[c++] = 128 | 63 & h
        }
    }
    return b[c] = 0,
    c - e
}

function Tb(){
    return wasmobject.exports.stackRestore.apply(null, arguments)

}

function Ub(){
    return wasmobject.exports.stackSave.apply(null, arguments)

}

function Sb(){
    return wasmobject.exports.stackAlloc.apply(null, arguments)

}

function Pb(){
    return wasmobject.exports._malloc.apply(null, arguments)
}

function P() {      // function 20( )
    function p(a) {
        for (var b = 0, c = 0; c < a.length; ++c) {
            var d = a.charCodeAt(c);
            d >= 55296 && d <= 57343 && (d = 65536 + ((1023 & d) << 10) | 1023 & a.charCodeAt(++c)),
                d <= 127 ? ++b : b += d <= 2047 ? 2 : d <= 65535 ? 3 : d <= 2097151 ? 4 : d <= 67108863 ? 5 : 6
        }
        return b
    }
    function a(a) {
        return a ? a.length > 48 ? a.substr(0, 48) : a : ""
    }
    function b() {
        var b = document.URL
            , c = window.navigator.userAgent.toLowerCase()
            , d = "";
        document.referrer.length > 0 && (d = document.referrer);
        try {
            0 == d.length && opener.location.href.length > 0 && (d = opener.location.href)
        } catch (e) {}
        var f = window.navigator.appCodeName
            , g = window.navigator.appName
            , h = window.navigator.platform;
        return b = a(b),
            d = a(d),
            c = a(c),
        b + "|" + c + "|" + d + "|" + f + "|" + g + "|" + h
    }
    var c = b()
        , d = p(c) + 1
        , e = Pb(d);
    return o(c, e, d + 1),
        e
}

function C() {
    return db
}

var $a = {
    string: function(a) {
        var b = 0;
        if (null !== a && void 0 !== a && 0 !== a) {
            var c = (a.length << 2) + 1;
            b = Sb(c),
                o(a, b, c)
        }
        return b
    },
    array: function(a) {
        var b = Sb(a.length);
        return K(a, b),
            b
    },
};


//////////////////////////////// init global var

var Da = 16;

var Ea, Fa, Ga, Ha, Ia, Ja, Ka, La, Ma, Na, Oa, Pa, Qa, Ra, Sa, Ta, Ua, Va = {
    "f64-rem": function(a, b) {
        return a % b
    },
    "debugger": function() {}
}, Wa = (new Array(0), 1024) ;

Na = Oa = Qa = Ra = Sa = Ta = Ua = 0,
    Pa = !1;
var cb = 5242880 , db = 16777216, ab = 65536;


var wasmMemory = new WebAssembly.Memory({
    initial: db / ab,
    maximum: db / ab
});
Ea = wasmMemory.buffer;

w();
Ja[0] = 1668509029;
Ha[1] = 25459;

var eb = []
    , fb = []
    , gb = []
    , hb = []
    , ib = !1
    , jb = !1;

Na = Wa,
    Oa = Na + 6928,
    fb.push();

Oa += 16;

Ua = d(4),
Qa = Ra = e(Oa),
Sa = Qa + cb,
Ta = e(Sa),
Ja[Ua >> 2] = Ta,
Pa = !0;

////////////////////////////////// wasm env ///////////////////////////////////////

var fun_ = function(){};

wasm_env = {
    abort: fun_,
    assert: fun_,
    enlargeMemory: fun_,
    getTotalMemory: C,
    abortOnCannotGrowMemory: fun_,
    abortStackOverflow: fun_,
    nullFunc_ii: fun_,
    nullFunc_iiii: fun_,
    nullFunc_v: fun_,
    nullFunc_vi: fun_,
    nullFunc_viiii: fun_,
    nullFunc_viiiii: fun_,
    nullFunc_viiiiii: fun_,
    invoke_ii: fun_,
    invoke_iiii: fun_,
    invoke_v: fun_,
    invoke_vi: fun_,
    invoke_viiii: fun_,
    invoke_viiiii: fun_,
    invoke_viiiiii: fun_,
    __ZSt18uncaught_exceptionv: fun_,
    ___cxa_find_matching_catch: fun_,
    ___gxx_personality_v0: fun_,
    ___lock: fun_,
    ___resumeException: fun_,
    ___setErrNo: fun_,
    ___syscall140: fun_,
    ___syscall146: fun_,
    ___syscall54: fun_,
    ___syscall6: fun_,
    ___unlock: fun_,
    _abort: fun_,
    _emscripten_memcpy_big: fun_,
    _get_unicode_str: P,              // function 20( ) => P( )
    flush_NO_FILESYSTEM: fun_,
    DYNAMICTOP_PTR: 7968,               //Ua
    tempDoublePtr: 7952,                //rb
    STACKTOP: 7984,                     //Ra
    STACK_MAX: 5250864,                 //Sa

    memoryBase: 1024,
    tableBase: 0,
    memory: wasmMemory,
    table: new WebAssembly.Table({
        initial: 99,
        maximum: 99,
        element: "anyfunc"
    })
};

var importObject = {
    'env': wasm_env,
    'asm2wasm': {
        "f64-rem": function(a, b) {
            return a % b
        },
        "debugger": function() {}
    },
    'global': {
        NaN: NaN,
        Infinity: 1 / 0
    },
    "global.Math": Math,
    // "parent": {};

};


///////////////////////////////// load wasm ///////////////////////////////////////
const path = require('path');
const ckey_wasm = path.resolve(__dirname, './ckey.wasm');

const fs = require('fs');
var wasm_data = fs.readFileSync(ckey_wasm);
var buffer = new Uint8Array(wasm_data);

var wasmobject = new WebAssembly.Instance(new WebAssembly.Module(buffer), importObject);


// function setnavigator(userAgent, appCodeName, appName, platform){
//     navigator = {
//         userAgent: userAgent,
//         appCodeName: appCodeName,
//         appName: appName,
//         platform: platform
//     };
//
//     window.navigator = navigator;
// }


function setDocument(URL, referrer){
    document.URL = URL;
    document.referrer = referrer;
}

// encryptVer = "9.1"
function getCkey(platform, appVer, vid, empty_str="", guid, tm){
    var _args = [platform, appVer, vid, empty_str="", guid, tm];
    var c = ['number', 'string', 'string', 'string', 'string', 'number'];
    return i('getckey', 'string', c, _args, undefined);

}


//  playerID, guid
function createGUID(a) {
    a = a || 32;
    for (var b = "", c = 1; c <= a; c++) {
        var d = Math.floor(16 * Math.random()).toString(16);
        b += d;
    }
    return b;
}

/////////////////////////

async function processRequest(recordLine) {
    var req = recordLine.trim().split(' ');  // Input Record Format: < platform appVer vid vURL referrer >
    setDocument(req[3], req[4]);
    var flowid = flowGuid + "_" + req[0];

    await delay((Math.floor(Math.random() * 2) + 1) * 1000);  // sleep for 1 or 2s
    var tm = Math.floor(Date.now() / 1000);
    var cKey = getCkey(req[0], req[1], req[2], "", guid, tm);

    var resp = [cKey, tm, guid, flowid];
    process.stdout.write(resp.join(' '));  // Output Record Format: < cKey tm guid flowid >
    process.stdout.write('\n');
}

async function delay(millis) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve();
        }, millis);
    });
}

var guid = createGUID();
var flowGuid = createGUID();  // + "_" + platform

process.stdin.setEncoding('utf8');
process.stdout.setEncoding('utf8');

process.stdin.on('readable', () => {
    // read one record line fitting in the pipe buffer
    var line, chunk, chunks=[];
    while ((chunk = process.stdin.read()) !== null) {
        chunks.push(chunk);
    }
    line = chunks.join('').trim();
    if (line) processRequest(line);
});
