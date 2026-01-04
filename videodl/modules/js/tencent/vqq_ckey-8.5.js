// Grabbed from the official VQQ player https://vm.gtimg.cn/thumbplayer/superplayer/1.27.3/superplayer.js

"use strict";

var Zu = Z1;
!function(e, t) {
    for (var o = Z1, i = Z0(); ; )
        try {
            if (581243 == parseInt(o(508)) / 1 + -parseInt(o(510)) / 2 * (-parseInt(o(632)) / 3) + parseInt(o(517)) / 4 + -parseInt(o(593)) / 5 * (-parseInt(o(641)) / 6) + parseInt(o(502)) / 7 + -parseInt(o(583)) / 8 + -parseInt(o(511)) / 9)
                break;
            i.push(i.shift())
        } catch (e) {
            i.push(i.shift())
        }
}();
var t, r, e, n, o, i, s = function(e, t) {
    return (s = Object.setPrototypeOf || {
        __proto__: []
    }instanceof Array && function(e, t) {
        e[Z1(536) + "__"] = t
    }
    || function(e, t) {
        var o = Z1;
        for (var i in t)
            Object[o(589) + "pe"][o(585) + o(561)][o(624)](t, i) && (e[i] = t[i])
    }
    )(e, t)
};
function c(e, t) {
    var o = Z1;
    if ("function" != typeof t && null !== t)
        throw new TypeError("Class e" + o(594) + "value " + String(t) + o(579) + " a constructor" + o(602) + "l");
    function i() {
        var t = o;
        this[t(552) + t(555)] = e
    }
    s(e, t),
    e[o(589) + "pe"] = null === t ? Object.create(t) : (i.prototype = t.prototype,
    new i)
}
"function" == typeof SuppressedError && SuppressedError,
(null === (t = Zu(634) + "ed" != typeof globalThis ? globalThis : void 0) || void 0 === t ? void 0 : t[Zu(515)]) || (null === (r = Zu(634) + "ed" != typeof global ? global : void 0) || void 0 === r ? void 0 : r.crypto) || (null === (e = Zu(634) + "ed" != typeof window ? window : void 0) || void 0 === e ? void 0 : e[Zu(515)]) || (null === (n = Zu(634) + "ed" != typeof self ? self : void 0) || void 0 === n ? void 0 : n.crypto) || null === (i = null === (o = Zu(634) + "ed" != typeof frames ? frames : void 0) || void 0 === o ? void 0 : o[0]) || void 0 === i || i[Zu(515)];
for (var a$1 = function(e) {
    for (var t = [], o = function(e) {
        var t = e
          , o = 987654321
          , i = 4294967295;
        return function() {
            var e = ((o = 36969 * (65535 & o) + (o >> 16) & i) << 16) + (t = 18e3 * (65535 & t) + (t >> 16) & i) & i;
            return e /= 4294967296,
            (e += .5) * (Math.random() > .5 ? 1 : -1)
        }
    }, i = 0, A = void 0; i < e; i += 4) {
        var r = o(4294967296 * (A || Math.random()));
        A = 987654071 * r(),
        t.push(4294967296 * r() | 0)
    }
    return new p(t,e)
}, u = function() {
    var e = Zu;
    function t() {}
    return t.create = function() {
        for (var e = Z1, t = [], o = 0; o < arguments[e(548)]; o++)
            t[o] = arguments[o];
        return new (this.bind.apply(this, function(t, o, i) {
            var A = e;
            if (i || 2 === arguments[A(548)])
                for (var r, n = 0, a = o[A(548)]; n < a; n++)
                    !r && n in o || (r || (r = Array[A(589) + "pe"][A(570)][A(624)](o, 0, n)),
                    r[n] = o[n]);
            return t[A(532)](r || Array[A(589) + "pe"][A(570)][A(624)](o))
        }([void 0], t, !1)))
    }
    ,
    t[e(589) + "pe"][e(604)] = function(t) {
        return Object[e(623)](this, t)
    }
    ,
    t[e(589) + "pe"][e(523)] = function() {
        var t = e
          , o = new (this[t(552) + t(555)]);
        return Object[t(623)](o, this),
        o
    }
    ,
    t
}(), p = function(e) {
    var t = Zu;
    function o(t, o) {
        var i = Z1;
        void 0 === t && (t = []),
        void 0 === o && (o = 4 * t.length);
        var A = e[i(624)](this) || this
          , r = t;
        if (r instanceof ArrayBuffer && (r = new Uint8Array(r)),
        ArrayBuffer[i(595)](r) && (r = new Uint8Array(r[i(633)],r[i(545) + i(509)],r[i(527) + i(505)])),
        r instanceof Uint8Array) {
            for (var n = r[i(527) + "gth"], a = [], s = 0; s < n; s += 1)
                a[s >>> 2] |= r[s] << 24 - s % 4 * 8;
            A[i(562)] = a,
            A[i(612) + "s"] = n
        } else
            A.words = t,
            A.sigBytes = o;
        return A
    }
    return c(o, e),
    o.prototype[t(597) + "g"] = function(e) {
        return void 0 === e && (e = f),
        e[t(567) + "fy"](this)
    }
    ,
    o.prototype[t(532)] = function(e) {
        var o = t
          , i = this[o(562)]
          , A = e[o(562)]
          , r = this[o(612) + "s"]
          , n = e[o(612) + "s"];
        if (this[o(520)](),
        r % 4)
            for (var a = 0; a < n; a += 1) {
                var s = A[a >>> 2] >>> 24 - a % 4 * 8 & 255;
                i[r + a >>> 2] |= s << 24 - (r + a) % 4 * 8
            }
        else
            for (a = 0; a < n; a += 4)
                i[r + a >>> 2] = A[a >>> 2];
        return this[o(612) + "s"] += n,
        this
    }
    ,
    o[t(589) + "pe"].clamp = function() {
        var e = t
          , o = this.words
          , i = this[e(612) + "s"];
        o[i >>> 2] &= 4294967295 << 32 - i % 4 * 8,
        o[e(548)] = Math[e(549)](i / 4)
    }
    ,
    o[t(589) + "pe"][t(523)] = function() {
        var o = t
          , i = e[o(589) + "pe"][o(523)][o(624)](this);
        return i[o(562)] = this[o(562)][o(570)](0),
        i
    }
    ,
    o[t(563)] = a$1,
    o
}(u), f = {
    stringify: function(e) {
        for (var t = Zu, o = e.words, i = e[t(612) + "s"], A = [], r = 0; r < i; r += 1) {
            var n = o[r >>> 2] >>> 24 - r % 4 * 8 & 255;
            A[t(621)]((n >>> 4)[t(597) + "g"](16)),
            A.push((15 & n)[t(597) + "g"](16))
        }
        return A[t(524)]("")
    },
    parse: function(e) {
        for (var t = Zu, o = e[t(548)], i = [], A = 0; A < o; A += 2)
            i[A >>> 3] |= parseInt(e[t(636)](A, 2), 16) << 24 - A % 8 * 4;
        return new p(i,o / 2)
    }
}, h = function(e) {
    for (var t = e[Zu(548)], o = [], i = 0; i < t; i += 1)
        o[i >>> 2] |= (255 & e.charCodeAt(i)) << 24 - i % 4 * 8;
    return new p(o,t)
}, l = function(e) {
    return h(unescape(encodeURIComponent(e)))
}, v = function(e) {
    var t = Zu;
    function o() {
        var t = Z1
          , o = e[t(624)](this) || this;
        return o[t(559) + t(601)] = 0,
        o
    }
    return c(o, e),
    o.prototype.reset = function() {
        var e = Z1;
        this[e(626)] = new p,
        this[e(582) + e(580)] = 0
    }
    ,
    o[t(589) + "pe"][t(534)] = function(e) {
        var o = t
          , i = e;
        o(544) == typeof i && (i = l(i)),
        this[o(626)][o(532)](i),
        this[o(582) + o(580)] += i.sigBytes
    }
    ,
    o[t(589) + "pe"][t(625) + "s"] = function(e) {
        var o, i = t, A = this[i(626)], r = this[i(525) + "ze"], n = A.words, a = A[i(612) + "s"], s = a / (4 * r), g = (s = e ? Math[i(549)](s) : Math[i(645)]((0 | s) - this[i(559) + i(601)], 0)) * r, l = Math[i(647)](4 * g, a);
        if (g) {
            for (var E = 0; E < g; E += r)
                this[i(553) + "essBlock"](n, E);
            o = n[i(504)](0, g),
            A[i(612) + "s"] -= l
        }
        return new p(o,l)
    }
    ,
    o.prototype.clone = function() {
        var o = t
          , i = e[o(589) + "pe"].clone[o(624)](this);
        return i[o(626)] = this[o(626)].clone(),
        i
    }
    ,
    o
}(u), y = function(e) {
    var t = Zu;
    function o(t) {
        var o = Z1
          , i = e.call(this) || this;
        return i[o(525) + "ze"] = 16,
        i[o(615)] = Object[o(623)](new u, t),
        i[o(642)](),
        i
    }
    return c(o, e),
    o[t(513) + t(571)] = function(e) {
        return function(t, o) {
            var i = Z1;
            return new e(o)[i(644) + "e"](t)
        }
    }
    ,
    o.prototype.reset = function() {
        var o = t;
        e[o(589) + "pe"][o(642)].call(this),
        this[o(568) + "t"]()
    }
    ,
    o[t(589) + "pe"][t(605)] = function(e) {
        var o = t;
        return this._append(e),
        this[o(625) + "s"](),
        this
    }
    ,
    o[t(589) + "pe"].finalize = function(e) {
        var o = t;
        return e && this[o(534)](e),
        this[o(587) + o(610)]()
    }
    ,
    o
}(v), d = [], _ = 0; _ < 64; _ += 1)
    d[_] = 4294967296 * Math.abs(Math[Zu(539)](_ + 1)) | 0;
var g = function(e, t, o, i, A, r, n) {
    var a = e + (t & o | ~t & i) + A + n;
    return (a << r | a >>> 32 - r) + t
}
  , w = function(e, t, o, i, A, r, n) {
    var a = e + (t & i | o & ~i) + A + n;
    return (a << r | a >>> 32 - r) + t
}
  , B = function(e, t, o, i, A, r, n) {
    var a = e + (t ^ o ^ i) + A + n;
    return (a << r | a >>> 32 - r) + t
}
  , m = function(e, t, o, i, A, r, n) {
    var a = e + (o ^ (t | ~i)) + A + n;
    return (a << r | a >>> 32 - r) + t
}
  , k = function(e) {
    var t = Zu;
    function o() {
        var t = Z1;
        return null !== e && e[t(556)](this, arguments) || this
    }
    return c(o, e),
    o[t(589) + "pe"][t(568) + "t"] = function() {
        this[t(537)] = new p([1732584193, 4023233417, 2562383102, 271733878])
    }
    ,
    o.prototype[t(553) + t(530) + "k"] = function(e, o) {
        for (var i = t, A = e, r = 0; r < 16; r += 1) {
            var n = o + r
              , a = e[n];
            A[n] = 16711935 & (a << 8 | a >>> 24) | 4278255360 & (a << 24 | a >>> 8)
        }
        var s = this[i(537)][i(562)]
          , l = A[o + 0]
          , E = A[o + 1]
          , c = A[o + 2]
          , u = A[o + 3]
          , p = A[o + 4]
          , h = A[o + 5]
          , I = A[o + 6]
          , _ = A[o + 7]
          , f = A[o + 8]
          , C = A[o + 9]
          , y = A[o + 10]
          , v = A[o + 11]
          , T = A[o + 12]
          , Q = A[o + 13]
          , S = A[o + 14]
          , D = A[o + 15]
          , R = s[0]
          , O = s[1]
          , F = s[2]
          , N = s[3];
        R = g(R, O, F, N, l, 7, d[0]),
        N = g(N, R, O, F, E, 12, d[1]),
        F = g(F, N, R, O, c, 17, d[2]),
        O = g(O, F, N, R, u, 22, d[3]),
        R = g(R, O, F, N, p, 7, d[4]),
        N = g(N, R, O, F, h, 12, d[5]),
        F = g(F, N, R, O, I, 17, d[6]),
        O = g(O, F, N, R, _, 22, d[7]),
        R = g(R, O, F, N, f, 7, d[8]),
        N = g(N, R, O, F, C, 12, d[9]),
        F = g(F, N, R, O, y, 17, d[10]),
        O = g(O, F, N, R, v, 22, d[11]),
        R = g(R, O, F, N, T, 7, d[12]),
        N = g(N, R, O, F, Q, 12, d[13]),
        F = g(F, N, R, O, S, 17, d[14]),
        O = g(O, F, N, R, D, 22, d[15]),
        R = w(R, O, F, N, E, 5, d[16]),
        N = w(N, R, O, F, I, 9, d[17]),
        F = w(F, N, R, O, v, 14, d[18]),
        O = w(O, F, N, R, l, 20, d[19]),
        R = w(R, O, F, N, h, 5, d[20]),
        N = w(N, R, O, F, y, 9, d[21]),
        F = w(F, N, R, O, D, 14, d[22]),
        O = w(O, F, N, R, p, 20, d[23]),
        R = w(R, O, F, N, C, 5, d[24]),
        N = w(N, R, O, F, S, 9, d[25]),
        F = w(F, N, R, O, u, 14, d[26]),
        O = w(O, F, N, R, f, 20, d[27]),
        R = w(R, O, F, N, Q, 5, d[28]),
        N = w(N, R, O, F, c, 9, d[29]),
        F = w(F, N, R, O, _, 14, d[30]),
        O = w(O, F, N, R, T, 20, d[31]),
        R = B(R, O, F, N, h, 4, d[32]),
        N = B(N, R, O, F, f, 11, d[33]),
        F = B(F, N, R, O, v, 16, d[34]),
        O = B(O, F, N, R, S, 23, d[35]),
        R = B(R, O, F, N, E, 4, d[36]),
        N = B(N, R, O, F, p, 11, d[37]),
        F = B(F, N, R, O, _, 16, d[38]),
        O = B(O, F, N, R, y, 23, d[39]),
        R = B(R, O, F, N, Q, 4, d[40]),
        N = B(N, R, O, F, l, 11, d[41]),
        F = B(F, N, R, O, u, 16, d[42]),
        O = B(O, F, N, R, I, 23, d[43]),
        R = B(R, O, F, N, C, 4, d[44]),
        N = B(N, R, O, F, T, 11, d[45]),
        F = B(F, N, R, O, D, 16, d[46]),
        O = B(O, F, N, R, c, 23, d[47]),
        R = m(R, O, F, N, l, 6, d[48]),
        N = m(N, R, O, F, _, 10, d[49]),
        F = m(F, N, R, O, S, 15, d[50]),
        O = m(O, F, N, R, h, 21, d[51]),
        R = m(R, O, F, N, T, 6, d[52]),
        N = m(N, R, O, F, u, 10, d[53]),
        F = m(F, N, R, O, y, 15, d[54]),
        O = m(O, F, N, R, E, 21, d[55]),
        R = m(R, O, F, N, f, 6, d[56]),
        N = m(N, R, O, F, D, 10, d[57]),
        F = m(F, N, R, O, I, 15, d[58]),
        O = m(O, F, N, R, Q, 21, d[59]),
        R = m(R, O, F, N, p, 6, d[60]),
        N = m(N, R, O, F, v, 10, d[61]),
        F = m(F, N, R, O, c, 15, d[62]),
        O = m(O, F, N, R, C, 21, d[63]),
        s[0] = s[0] + R | 0,
        s[1] = s[1] + O | 0,
        s[2] = s[2] + F | 0,
        s[3] = s[3] + N | 0
    }
    ,
    o.prototype[t(587) + t(610)] = function() {
        var e = t
          , o = this[e(626)]
          , i = o[e(562)]
          , A = 8 * this[e(582) + e(580)]
          , r = 8 * o.sigBytes;
        i[r >>> 5] |= 128 << 24 - r % 32;
        var n = Math[e(618)](A / 4294967296)
          , a = A;
        i[15 + (r + 64 >>> 9 << 4)] = 16711935 & (n << 8 | n >>> 24) | 4278255360 & (n << 24 | n >>> 8),
        i[14 + (r + 64 >>> 9 << 4)] = 16711935 & (a << 8 | a >>> 24) | 4278255360 & (a << 24 | a >>> 8),
        o.sigBytes = 4 * (i[e(548)] + 1),
        this[e(625) + "s"]();
        for (var s = this[e(537)], g = s[e(562)], l = 0; l < 4; l += 1) {
            var E = g[l];
            g[l] = 16711935 & (E << 8 | E >>> 24) | 4278255360 & (E << 24 | E >>> 8)
        }
        return s
    }
    ,
    o[t(589) + "pe"].clone = function() {
        var o = t
          , i = e[o(589) + "pe"][o(523)][o(624)](this);
        return i[o(537)] = this[o(537)].clone(),
        i
    }
    ,
    o
}(y)
  , b$1 = y[Zu(513) + Zu(571)](k)
  , S = {
    stringify: function(e) {
        var t = Zu
          , o = e[t(562)]
          , i = e[t(612) + "s"]
          , A = this[t(640)];
        e.clamp();
        for (var r = [], n = 0; n < i; n += 3)
            for (var a = (o[n >>> 2] >>> 24 - n % 4 * 8 & 255) << 16 | (o[n + 1 >>> 2] >>> 24 - (n + 1) % 4 * 8 & 255) << 8 | o[n + 2 >>> 2] >>> 24 - (n + 2) % 4 * 8 & 255, s = 0; s < 4 && n + .75 * s < i; s += 1)
                r[t(621)](A.charAt(a >>> 6 * (3 - s) & 63));
        var g = A.charAt(64);
        if (g)
            for (; r[t(548)] % 4; )
                r[t(621)](g);
        return r.join("")
    },
    parse: function(e) {
        var t = Zu
          , o = e[t(548)]
          , i = this._map
          , A = this[t(535) + "eMap"];
        if (!A) {
            this[t(535) + t(499)] = [],
            A = this["_revers" + t(499)];
            for (var r = 0; r < i[t(548)]; r += 1)
                A[i[t(588) + t(578)](r)] = r
        }
        var n = i.charAt(64);
        if (n) {
            var a = e.indexOf(n);
            -1 !== a && (o = a)
        }
        return function(e, o, i) {
            for (var A = t, r = [], n = 0, a = 0; a < o; a += 1)
                if (a % 4) {
                    var s = i[e.charCodeAt(a - 1)] << a % 4 * 2 | i[e[A(588) + A(578)](a)] >>> 6 - a % 4 * 2;
                    r[n >>> 2] |= s << 24 - n % 4 * 8,
                    n += 1
                }
            return p[A(541)](r, n)
        }(e, o, A)
    },
    _map: Zu(630) + Zu(629) + Zu(554) + Zu(500) + "cdefghi" + Zu(501) + "qrstuvwxyz0123" + Zu(565) + "/="
}
  , O = function(e) {
    var t = Zu;
    function o(t, o, i) {
        var A = Z1
          , r = e[A(624)](this) || this;
        return r[A(615)] = Object.assign(new u, i),
        r._xformMode = t,
        r[A(519)] = o,
        r[A(642)](),
        r
    }
    return c(o, e),
    o["createE" + t(506) + "r"] = function(e, o) {
        var i = t;
        return this[i(541)](this[i(617) + i(564) + "E"], e, o)
    }
    ,
    o[t(577) + t(607) + "r"] = function(e, t) {
        return this.create(this._DEC_XFORM_MODE, e, t)
    }
    ,
    o[t(513) + "Helper"] = function(e) {
        var t = function(e) {
            return R
        };
        return {
            encrypt: function(o, i, A) {
                var r = Z1;
                return t()[r(538)](e, o, i, A)
            },
            decrypt: function(o, i, A) {
                var r = Z1;
                return t()[r(603)](e, o, i, A)
            }
        }
    }
    ,
    o[t(589) + "pe"][t(642)] = function() {
        var o = t;
        e.prototype[o(642)][o(624)](this),
        this[o(568) + "t"]()
    }
    ,
    o[t(589) + "pe"][t(503)] = function(e) {
        var o = t;
        return this[o(534)](e),
        this[o(625) + "s"]()
    }
    ,
    o[t(589) + "pe"][t(644) + "e"] = function(e) {
        var o = t;
        return e && this[o(534)](e),
        this[o(587) + o(610)]()
    }
    ,
    o
}(v);
function M(e, t, o) {
    var i, A = Zu, r = e, n = this[A(531)];
    n ? (i = n,
    this._iv = void 0) : i = this["_prevBl" + A(529)];
    for (var a = 0; a < o; a += 1)
        r[t + a] ^= i[a]
}
O[Zu(617) + Zu(564) + "E"] = 1,
O[Zu(543) + Zu(564) + "E"] = 2,
O.keySize = 4,
O.ivSize = 4;
var A = function(e) {
    function t() {
        return null !== e && e.apply(this, arguments) || this
    }
    return c(t, e),
    t
}(function(e) {
    var t = Zu;
    function o(t, o) {
        var i = Z1
          , A = e[i(624)](this) || this;
        return A._cipher = t,
        A[i(531)] = o,
        A
    }
    return c(o, e),
    o[t(497) + t(506) + "r"] = function(e, o) {
        var i = t;
        return this[i(619) + "or"][i(541)](e, o)
    }
    ,
    o.createDecryptor = function(e, o) {
        return this[t(596) + "or"].create(e, o)
    }
    ,
    o
}(u));
A.Encryptor = function(e) {
    var t = Zu;
    function o() {
        var t = Z1;
        return null !== e && e[t(556)](this, arguments) || this
    }
    return c(o, e),
    o[t(589) + "pe"][t(503) + t(600)] = function(e, o) {
        var i = t
          , A = this._cipher
          , r = A[i(525) + "ze"];
        M.call(this, e, o, r),
        A[i(538) + i(600)](e, o),
        this[i(512) + i(529)] = e[i(570)](o, o + r)
    }
    ,
    o
}(A),
A[Zu(596) + "or"] = function(e) {
    var t = Zu;
    function o() {
        var t = Z1;
        return null !== e && e[t(556)](this, arguments) || this
    }
    return c(o, e),
    o.prototype[t(503) + "Block"] = function(e, o) {
        var i = t
          , A = this[i(590)]
          , r = A[i(525) + "ze"]
          , n = e[i(570)](o, o + r);
        A[i(603) + i(600)](e, o),
        M[i(624)](this, e, o, r),
        this["_prevBl" + i(529)] = n
    }
    ,
    o
}(A);
var z = {
    pad: function(e, t) {
        for (var o = Zu, i = 4 * t, A = i - e[o(612) + "s"] % i, r = A << 24 | A << 16 | A << 8 | A, n = [], a = 0; a < A; a += 4)
            n[o(621)](r);
        var s = p[o(541)](n, A);
        e.concat(s)
    },
    unpad: function(e) {
        var t = e
          , o = 255 & t[Zu(562)][t.sigBytes - 1 >>> 2];
        t.sigBytes -= o
    }
}
  , E = function(e) {
    var t = Zu;
    function o(t, o, i) {
        var r = Z1
          , n = e[r(624)](this, t, o, Object[r(623)]({
            mode: A,
            padding: z
        }, i)) || this;
        return n[r(525) + "ze"] = 4,
        n
    }
    return c(o, e),
    o.prototype[t(642)] = function() {
        var o, i = t;
        e[i(589) + "pe"][i(642)][i(624)](this);
        var A = this.cfg
          , r = A.iv
          , n = A[i(599)];
        this["_xformM" + i(622)] === this["constru" + i(555)][i(617) + i(564) + "E"] ? o = n[i(497) + i(506) + "r"] : (o = n[i(577) + i(607) + "r"],
        this[i(559) + "ferSize"] = 1),
        this._mode = o.call(n, this, null == r ? void 0 : r.words),
        this._mode[i(498) + "or"] = o
    }
    ,
    o[t(589) + "pe"][t(553) + t(530) + "k"] = function(e, o) {
        var i = t;
        this[i(533)][i(503) + i(600)](e, o)
    }
    ,
    o[t(589) + "pe"][t(587) + t(610)] = function() {
        var e, o = t, i = this[o(615)][o(569)];
        return this[o(591) + o(622)] === this[o(552) + "ctor"]["_ENC_XF" + o(564) + "E"] ? (i[o(627)](this[o(626)], this[o(525) + "ze"]),
        e = this[o(625) + "s"](!0)) : (e = this[o(625) + "s"](!0),
        i[o(631)](e)),
        e
    }
    ,
    o
}(O)
  , C = function(e) {
    var t = Zu;
    function o(t) {
        var o = Z1
          , i = e.call(this) || this;
        return i[o(604)](t),
        i
    }
    return c(o, e),
    o[t(589) + "pe"][t(597) + "g"] = function(e) {
        var o = t;
        return (e || this[o(573) + "er"])[o(567) + "fy"](this)
    }
    ,
    o
}(u)
  , D = {
    stringify: function(e) {
        var t = Zu
          , o = e[t(516) + "ext"]
          , i = e[t(557)];
        return (i ? p.create([1398893684, 1701076831])[t(532)](i)[t(532)](o) : o)[t(597) + "g"](S)
    },
    parse: function(e) {
        var t, o = Zu, i = S.parse(e), A = i.words;
        return 1398893684 === A[0] && 1701076831 === A[1] && (t = p[o(541)](A.slice(2, 4)),
        A[o(504)](0, 4),
        i[o(612) + "s"] -= 16),
        C[o(541)]({
            ciphertext: i,
            salt: t
        })
    }
}
  , R = function(e) {
    var t = Zu;
    function o() {
        var t = Z1;
        return null !== e && e[t(556)](this, arguments) || this
    }
    return c(o, e),
    o[t(538)] = function(e, o, i, A) {
        var r = t
          , n = Object.assign(new u, this[r(615)], A)
          , a = e[r(497) + "ncryptor"](i, n)
          , s = a[r(644) + "e"](o)
          , g = a[r(615)];
        return C[r(541)]({
            ciphertext: s,
            key: i,
            iv: g.iv,
            algorithm: e,
            mode: g[r(599)],
            padding: g[r(569)],
            blockSize: a.blockSize,
            formatter: n.format
        })
    }
    ,
    o[t(603)] = function(e, o, i, A) {
        var r = t
          , n = o
          , a = Object[r(623)](new u, this[r(615)], A);
        return n = this[r(584)](n, a[r(576)]),
        e[r(577) + r(607) + "r"](i, a)[r(644) + "e"](n[r(516) + r(643)])
    }
    ,
    o[t(584)] = function(e, o) {
        var i = t;
        return i(544) == typeof e ? o[i(522)](e, this) : e
    }
    ,
    o
}(u);
R[Zu(615)] = Object[Zu(623)](new u, {
    format: D
});
var j = []
  , x = []
  , F = []
  , N = []
  , P = []
  , X = []
  , H = []
  , I = []
  , J = []
  , U = [];
for (_ = 0; _ < 256; _ += 1)
    U[_] = _ < 128 ? _ << 1 : _ << 1 ^ 283;
var V = 0
  , T = 0;
for (_ = 0; _ < 256; _ += 1) {
    var K = T ^ T << 1 ^ T << 2 ^ T << 3 ^ T << 4;
    K = K >>> 8 ^ 255 & K ^ 99,
    j[V] = K;
    var L = U[V]
      , q = U[L]
      , G = U[q]
      , Q = 257 * U[K] ^ 16843008 * K;
    x[V] = Q << 24 | Q >>> 8,
    F[V] = Q << 16 | Q >>> 16,
    N[V] = Q << 8 | Q >>> 24,
    P[V] = Q,
    Q = 16843009 * G ^ 65537 * q ^ 257 * L ^ 16843008 * V,
    X[K] = Q << 24 | Q >>> 8,
    H[K] = Q << 16 | Q >>> 16,
    I[K] = Q << 8 | Q >>> 24,
    J[K] = Q,
    V ? (V = L ^ U[U[U[G ^ L]]],
    T ^= U[U[T]]) : V = T = 1
}
var W = [0, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54]
  , Y = function(e) {
    var t = Zu;
    function o() {
        return null !== e && e.apply(this, arguments) || this
    }
    return c(o, e),
    o[t(589) + "pe"][t(568) + "t"] = function() {
        var e, o = t;
        if (!this._nRounds || this[o(614) + o(638)] !== this[o(519)]) {
            this[o(614) + o(638)] = this[o(519)];
            var i = this[o(614) + o(638)]
              , A = i[o(562)]
              , r = i[o(612) + "s"] / 4;
            this._nRounds = r + 6;
            var n = 4 * (this[o(547) + "s"] + 1);
            this._keySchedule = [];
            for (var a = this[o(646) + o(592)], s = 0; s < n; s += 1)
                s < r ? a[s] = A[s] : (e = a[s - 1],
                s % r ? r > 6 && s % r == 4 && (e = j[e >>> 24] << 24 | j[e >>> 16 & 255] << 16 | j[e >>> 8 & 255] << 8 | j[255 & e]) : (e = j[(e = e << 8 | e >>> 24) >>> 24] << 24 | j[e >>> 16 & 255] << 16 | j[e >>> 8 & 255] << 8 | j[255 & e],
                e ^= W[s / r | 0] << 24),
                a[s] = a[s - r] ^ e);
            this[o(628) + "Schedule"] = [];
            for (var g = this[o(628) + o(521) + "e"], l = 0; l < n; l += 1)
                s = n - l,
                e = l % 4 ? a[s] : a[s - 4],
                g[l] = l < 4 || s <= 4 ? e : X[j[e >>> 24]] ^ H[j[e >>> 16 & 255]] ^ I[j[e >>> 8 & 255]] ^ J[j[255 & e]]
        }
    }
    ,
    o[t(589) + "pe"]["encrypt" + t(600)] = function(e, o) {
        var i = t;
        this[i(518) + i(637)](e, o, this[i(646) + i(592)], x, F, N, P, j)
    }
    ,
    o.prototype[t(518) + t(637)] = function(e, o, i, A, r, n, a, s) {
        for (var g = e, l = this[t(547) + "s"], E = g[o] ^ i[0], c = g[o + 1] ^ i[1], d = g[o + 2] ^ i[2], u = g[o + 3] ^ i[3], p = 4, B = 1; B < l; B += 1) {
            var h = A[E >>> 24] ^ r[c >>> 16 & 255] ^ n[d >>> 8 & 255] ^ a[255 & u] ^ i[p];
            p += 1;
            var I = A[c >>> 24] ^ r[d >>> 16 & 255] ^ n[u >>> 8 & 255] ^ a[255 & E] ^ i[p];
            p += 1;
            var _ = A[d >>> 24] ^ r[u >>> 16 & 255] ^ n[E >>> 8 & 255] ^ a[255 & c] ^ i[p];
            p += 1;
            var f = A[u >>> 24] ^ r[E >>> 16 & 255] ^ n[c >>> 8 & 255] ^ a[255 & d] ^ i[p];
            p += 1,
            E = h,
            c = I,
            d = _,
            u = f
        }
        var C = (s[E >>> 24] << 24 | s[c >>> 16 & 255] << 16 | s[d >>> 8 & 255] << 8 | s[255 & u]) ^ i[p];
        p += 1;
        var y = (s[c >>> 24] << 24 | s[d >>> 16 & 255] << 16 | s[u >>> 8 & 255] << 8 | s[255 & E]) ^ i[p];
        p += 1;
        var m = (s[d >>> 24] << 24 | s[u >>> 16 & 255] << 16 | s[E >>> 8 & 255] << 8 | s[255 & c]) ^ i[p];
        p += 1;
        var v = (s[u >>> 24] << 24 | s[E >>> 16 & 255] << 16 | s[c >>> 8 & 255] << 8 | s[255 & d]) ^ i[p];
        p += 1,
        g[o] = C,
        g[o + 1] = y,
        g[o + 2] = m,
        g[o + 3] = v
    }
    ,
    o
}(E);
function Z0() {
    var e = ["zgvJCNLWDa", "BwL4sw4", "DxbKyxrL", "Dg9vChbLCG", "zwnYExb0BW", "mZm1ma", "q0zbqZiXnG", "BgL6zq", "ms4WlJe", "C2LNqNL0zq", "y2HHCKf0", "x2TLEvbYAq", "y2zN", "uvjtvfzxwa", "x0voq19yrG", "zMXVB3i", "rw5JCNLWDa", "EhOWmti0nG", "ChvZAa", "B2rL", "yxnZAwDU", "y2fSBa", "x3bYB2nLCW", "x2rHDge", "CgfK", "x2LUDKTLEq", "seLks0XntG", "qujdrevgrW", "Dw5Wywq", "ndy0nZy2v05fAxn2", "yNvMzMvY", "Dw5KzwzPBG", "z3vPza", "C3vIC3rY", "DejSB2nR", "B3jszxnLDa", "ls0Wmq", "x21HCa", "mtu2v01bueTf", "CMvZzxq", "zxH0", "zMLUywXPEG", "Bwf4", "x2TLEvnJAa", "BwLU", "y3jLyxrLrq", "x19JCMvHDa", "zu1HCa", "vLDywvPHyG", "AMTSBw5VCa", "mtK5nJyXmenlBerOua", "ChjVy2vZCW", "C3bSAwnL", "z3rO", "BMnYExb0BW", "BM9Uy2u", "ody3ntu1Aw1JtwLi", "C2v0", "ngLJEfvODa", "mtu3ntGZndnwuLPJwLy", "x3bYzxzcBa", "x2nYzwf0zq", "ndqZnZCZqq", "y3j5ChrV", "y2LWAgvYDa", "nde2odG5nND1DuztyW", "x2rVq3j5Ca", "x2TLEq", "y2XHBxa", "u2nOzwr1Ba", "CgfYC2u", "y2XVBMu", "AM9PBG", "yMXVy2TtAq", "yNvZsLnptG", "yNL0zuXLBG", "mKe1que2ma", "B2nR", "zxnZqMXVyW", "x2L2", "y29Uy2f0", "x21Vzgu", "x2fWCgvUza", "x3jLDMvYCW", "x19WCM90BW", "x2HHC2G", "zw5JCNLWDa", "C2LU", "nJaXmZu3nq", "y3jLyxrL", "C2vJsLnptG", "x0rfq19yrG", "C3rYAw5N", "yNL0zu9MzG", "qujdruzhsa", "x25sB3vUza", "BgvUz3rO", "y2vPBa", "DMLK", "C3vIC3rYAq", "y29UC3rYDq", "x2rVuhjVyW", "t1bruLnuvq", "y3rVCG", "yxbWBhK", "C2fSDa", "CMfUza", "x21PBKj1zG", "mtC4que2qW", "CM9Wzxj0Eq", "D29Yzhm", "CMfUzg9T", "t1jnx01pra", "ndu2nZG5kW", "wvPHyMnLzG", "C3rYAw5NAq", "x2rVuMvZzq", "CgfKzgLUzW", "C2XPy2u", "sgvSCgvY", "nKm0rq", "zM9YBwf0Da", "C2rRvMvY", "Adm4", "zM9YBwf0", "y3jLyxrLra", "zuf0", "igLZig5VDa", "ExrLCW", "ChfYC3v2DW", "x25eyxrHqG", "nJGXndqYnevYvKPQtG", "x3bHCNnL", "AgfZt3DUua", "z2LQA2XTBG", "x2rVrMLUyq", "y2HHCKnVza", "ChjVDg90Eq", "x2nPCgHLCG", "x3HMB3jTtq", "zwr1Bgu", "mtmWnJaWvKXdrhfd", "EhrLBMrZia", "AxnwAwv3", "rgvJCNLWDa", "Dg9tDhjPBG", "CgXHDgzVCG", "Bw9Kzq", "qMXVy2S", "zMvYu2L6zq", "ig9Yig51Ba"];
    return (Z0 = function() {
        return e
    }
    )()
}
function Z1(e, t) {
    var o = Z0();
    return Z1 = function(t, i) {
        var A = o[t -= 497];
        if (void 0 === Z1.FikNlj) {
            var r = function(e) {
                for (var t, o, i = "", A = "", r = 0, n = 0; o = e.charAt(n++); ~o && (t = r % 4 ? 64 * t + o : o,
                r++ % 4) ? i += String.fromCharCode(255 & t >> (-2 * r & 6)) : 0)
                    o = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=".indexOf(o);
                for (var a = 0, s = i.length; a < s; a++)
                    A += "%" + ("00" + i.charCodeAt(a).toString(16)).slice(-2);
                return decodeURIComponent(A)
            };
            Z1.kyqcpm = r,
            e = arguments,
            Z1.FikNlj = !0
        }
        var n = o[0]
          , a = t + n
          , s = e[a];
        return s ? A = s : (A = Z1.kyqcpm(A),
        e[a] = A),
        A
    }
    ,
    Z1(e, t)
}
Y.keySize = 8;
var Z = E[Zu(513) + Zu(571)](Y);


// encryptVer = "8.5"
// signature: getCkey({vid: "videoId", ts: "timeStamp", appVer: "1.27.2", guid: "guid", platform: "10201", h38: "qimeiH38"})
function getCkey(e) {
        var t = Zu
          , o = function(e) {
            var t = Z1;
            void 0 === e && (e = 32);
            for (var o = t(546) + "IJKLNOP" + t(616) + t(566) + t(586) + t(581) + t(620) + "79", i = "", A = 0; A < e; A += 1)
                i += o[t(613)](Math[t(618)](Math[t(563)]() * o[t(548)]));
            return i
        }(11)
          , i = e[t(550)]
          , r = e.ts
          , n = e.appVer
          , a = e[t(635)]
          , s = e[t(598) + "m"]
          , g = e.h38
          , l = void 0 === g ? "" : g
          , E = e[t(542)]
          , c = void 0 === E ? "" : E
          , d = e[t(526)]
          , u = void 0 === d ? "" : d
          , p = {};
        p.vid = i,
        p[t(574)] = t(611),
        p[t(507)] = o,
        p[t(558)] = b$1(""[t(532)](o, "1234"))[t(597) + "g"]()[t(551) + "ng"](0, 8),
        p.appVer = n,
        p[t(635)] = a,
        p.platform = s,
        p.ts = r,
        p[t(575)] = l,
        p.sj = c,
        p.bj = u,
        p.os = JSON[t(567) + "fy"]({});
        var B = {};
        B.iv = f[t(522)](t(609) + "FAA2D39" + t(540) + "D4055C6" + t(608)),
        B.mode = A,
        B[t(569)] = z;
        var h = Z.encrypt(JSON[t(567) + "fy"](p), f[t(522)](t(528) + t(560) + "8DA662E" + t(514) + t(572)), B);
        return t(639).concat(h[t(516) + "ext"][t(597) + "g"]()[t(606) + "Case"]())
}

function createGUID(e) {
    void 0 === e && (e = 32);
    for (var t = e || 32, o = "", i = 1; i <= t; i++) {
        o += Math.floor(16 * Math.random()).toString(16)
    }
    return o
}

/////////////////////////

async function processRequest(recordLine) {
    var req = recordLine.trim().split(' ');  // Input Record Format: < platform appVer vid vURL referrer >

    await delay((Math.floor(Math.random() * 2) + 1) * 1000);  // sleep for 1 or 2s
    var tm = Math.floor(Date.now() / 1000).toString();

    var reqParams = {
        vid: req[2],
        ts: tm,
        appVer: req[1],
        guid: guid,
        platform: req[0],
        h38: playerid
    };
    var cKey = getCkey(reqParams);

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

var guid = createGUID(16);
var flowid = createGUID(32);
var playerid = createGUID(38);

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
