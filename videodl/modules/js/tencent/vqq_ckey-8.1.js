// Grabbed from the official VQQ player https://vm.gtimg.cn/thumbplayer/superplayer/1.15.22/superplayer.js

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


// encryptVer = "8.1"
// signature: getCkey(vid, tm, appVer, guid, platform)
var getCkey = function () {
    var e, t, o, r, n, i = -8290, a = -496, s = s || function (e, t) {
        var o = {}, r = o.a = {}, n = function () {
        }, a = r.b = {
            c: function (e) {
                for (var t = "", o = 0; o < "ॅूॅक़".length; o++) t += String.fromCharCode(2348 ^ "ॅूॅक़".charCodeAt(o));
                n.prototype = this;
                var r = new n;
                return e && r.d(e), r.hasOwnProperty(t) || (r.init = function () {
                    r.$super.init.apply(this, arguments)
                }), r.init.prototype = r, r.$super = this, r
            }, create: function () {
                var e = this.c();
                return e.init.apply(e, arguments), e
            }, init: function () {
            }, d: function (e) {
                for (var t = "", o = 0; o < ";͙ͥ;͸ͣͤͭ".length; o++) t += String.fromCharCode(778 ^ ";͙ͥ;͸ͣͤͭ".charCodeAt(o));
                for (var r in e) e.hasOwnProperty(r) && (this[r] = e[r]);
                e.hasOwnProperty(t) && (this.toString = e.toString)
            }, e: function () {
                return this.init.prototype.c(this)
            }
        }, s = r.f = a.c({
            init: function (e, t) {
                e = this.g = e || [], this.h = null != t ? t : (-2630 + i + 10924) * e.length
            }, toString: function (e) {
                return (e || c).i(this)
            }, concat: function (e) {
                var t = this.g, o = e.g, r = this.h;
                if (e = e.h, this.j(), r % 4) for (var n = 0; n < e; n++) t[r + n >>> 2] |= (o[n >>> 2] >>> 24 - n % 4 * 8 & 255) << 24 - (r + n) % 4 * 8; else if (65535 < o.length) for (n = 0; n < e; n += 4) t[r + n >>> 2] = o[n >>> 2]; else t.push.apply(t, o);
                return this.h += e, this
            }, j: function () {
                var t = this.g, o = this.h;
                t[o >>> 2] &= 4294967295 << 32 - o % 4 * 8, t.length = e.ceil(o / 4)
            }, e: function () {
                var e = a.e.call(this);
                return e.g = this.g.slice(0), e
            }, random: function (t) {
                for (var o = [], r = 0; r < t; r += 4) o.push(4294967296 * e.random() | 0);
                return new s.init(o, t)
            }
        }), l = o.k = {}, c = l.l = {
            i: function (e) {
                for (var t = "", o = 0; o < "".length; o++) t += String.fromCharCode(368 ^ "".charCodeAt(o));
                var r = e.g;
                e = e.h;
                for (var n = [], i = 0; i < e; i++) {
                    var a = r[i >>> 2] >>> 24 - i % 4 * 8 & 255;
                    n.push((a >>> 4).toString(16)), n.push((15 & a).toString(16))
                }
                return n.join(t)
            }, parse: function (e) {
                for (var t = e.length, o = [], r = 0; r < t; r += 2) o[r >>> 3] |= parseInt(e.substr(r, 2), 16) << 24 - r % 8 * 4;
                return new s.init(o, t / 2)
            }
        }, p = l.m = {
            i: function (e) {
                for (var t = "", o = 0; o < "".length; o++) t += String.fromCharCode(2238 ^ "".charCodeAt(o));
                var r = e.g;
                e = e.h;
                for (var n = [], i = 0; i < e; i++) n.push(String.fromCharCode(r[i >>> 2] >>> 24 - i % 4 * 8 & 255));
                return n.join(t)
            }, parse: function (e) {
                for (var t = e.length, o = [], r = 0; r < t; r++) o[r >>> 2] |= (255 & e.charCodeAt(r)) << 24 - r % 4 * 8;
                return new s.init(o, t)
            }
        }, d = l.n = {
            i: function (e) {
                for (var t = "", o = 0, r = "ØôùóúçøðñµÀÁÓ¸­µñôáô"; o < r.length; o++) t += String.fromCharCode(149 ^ r.charCodeAt(o));
                try {
                    return decodeURIComponent(escape(p.i(e)))
                } catch (e) {
                    throw Error(t)
                }
            }, parse: function (e) {
                return p.parse(unescape(encodeURIComponent(e)))
            }
        }, u = r.o = a.c({
            p: function () {
                this.q = new s.init, this.r = 0
            }, s: function (e) {
                for (var t = "", o = 0; o < "ྦྷྠྦ྽ྺླ".length; o++) t += String.fromCharCode(4052 ^ "ྦྷྠྦ྽ྺླ".charCodeAt(o));
                t == typeof e && (e = d.parse(e)), this.q.concat(e), this.r += e.h
            }, t: function (t) {
                var o = this.q, r = o.g, n = o.h, i = this.u, a = n / (4 * i);
                if (t = (a = t ? e.ceil(a) : e.max((0 | a) - this.v, 0)) * i, n = e.min(4 * t, n), t) {
                    for (var l = 0; l < t; l += i) this.w(r, l);
                    l = r.splice(0, t), o.h -= n
                }
                return new s.init(l, n)
            }, e: function () {
                var e = a.e.call(this);
                return e.q = this.q.e(), e
            }, v: 0
        });
        r.x = u.c({
            y: a.c(), init: function (e) {
                this.y = this.y.c(e), this.p()
            }, p: function () {
                u.p.call(this), this.z()
            }, A: function (e) {
                return this.s(e), this.t(), this
            }, B: function (e) {
                return e && this.s(e), this.C()
            }, u: 16, D: function (e) {
                return function (t, o) {
                    return new e.init(o).B(t)
                }
            }, F: function (e) {
                return function (t, o) {
                    return new A.HMAC.init(e, o).B(t)
                }
            }
        });
        var A = o.G = {};
        return o
    }(Math);

    function l(e) {
        return c.call(this, 2, e)
    }

    function c(e) {
        for (var t = "", o = 0; o < "ऊ".length; o++) t += String.fromCharCode(2422 ^ "ऊ".charCodeAt(o));
        for (var r = "", n = 0; n < "ޭ".length; n++) r += String.fromCharCode(2001 ^ "ޭ".charCodeAt(n));
        for (var p = "", d = 0; d < "Ҡ".length; d++) p += String.fromCharCode(1244 ^ "Ҡ".charCodeAt(d));
        for (var u = "", A = 0; A < "ഇ".length; A++) u += String.fromCharCode(3451 ^ "ഇ".charCodeAt(A));
        for (var _ = "", E = 0; E < "׿".length; E++) _ += String.fromCharCode(1411 ^ "׿".charCodeAt(E));
        for (var g = "", f = 0; f < "ࢨ".length; f++) g += String.fromCharCode(2260 ^ "ࢨ".charCodeAt(f));
        for (var h = "", v = 0; v < "ଶ".length; v++) h += String.fromCharCode(2890 ^ "ଶ".charCodeAt(v));
        for (var y = "", m = 0; m < "ƨƢǶƦǶƧǵǱƧƤ".length; m++) y += String.fromCharCode(453 ^ "ƨƢǶƦǶƧǵǱƧƤ".charCodeAt(m));
        for (var T = "", C = 0; C < "੸".length; C++) T += String.fromCharCode(2564 ^ "੸".charCodeAt(C));
        for (var I = "", P = 0; P < "ࡌ".length; P++) I += String.fromCharCode(2096 ^ "ࡌ".charCodeAt(P));
        for (var S = "", N = 0; N < "ٶ".length; N++) S += String.fromCharCode(1546 ^ "ٶ".charCodeAt(N));
        for (var D = "", O = 0; O < "ઈ".length; O++) D += String.fromCharCode(2804 ^ "ઈ".charCodeAt(O));
        for (var x = "", R = 0; R < "ȧ".length; R++) x += String.fromCharCode(603 ^ "ȧ".charCodeAt(R));
        for (var b = "", L = 0; L < "о".length; L++) b += String.fromCharCode(1090 ^ "о".charCodeAt(L));
        for (var w = "", M = 0; M < "ߡ".length; M++) w += String.fromCharCode(1949 ^ "ߡ".charCodeAt(M));
        for (var V = "", k = 0; k < "̅".length; k++) V += String.fromCharCode(889 ^ "̅".charCodeAt(k));
        for (var B = "", K = 0; K < "".length; K++) B += String.fromCharCode(3568 ^ "".charCodeAt(K));
        for (var Y = "", F = 0; F < "".length; F++) Y += String.fromCharCode(777 ^ "".charCodeAt(F));
        for (var U = "", Q = 0; Q < "".length; Q++) U += String.fromCharCode(2613 ^ "".charCodeAt(Q));
        for (var H = "", $ = 0; $ < "´¹²¯".length; $++) H += String.fromCharCode(214 ^ "´¹²¯".charCodeAt($));
        for (var G = "", q = 0; q < "ۘە۞ۃ".length; q++) G += String.fromCharCode(1722 ^ "ۘە۞ۃ".charCodeAt(q));
        for (var j = "", W = 0; W < "٨٩٨٣".length; W++) j += String.fromCharCode(1542 ^ "٨٩٨٣".charCodeAt(W));
        for (var z = "", X = 0; X < "ÁÌ".length; X++) z += String.fromCharCode(168 ^ "ÁÌ".charCodeAt(X));
        for (var J = "", Z = 0; Z < "ۆۋ۔".length; Z++) J += String.fromCharCode(1698 ^ "ۆۋ۔".charCodeAt(Z));
        for (var ee = "", te = 0, oe = "ଶଋ୑୞ଈ଍଍୑୙ଶ"; te < oe.length; te++) ee += String.fromCharCode(2921 ^ oe.charCodeAt(te));
        for (var re = "", ne = 0; ne < "יׇ׀׊ׁי".length; ne++) re += String.fromCharCode(1454 ^ "יׇ׀׊ׁי".charCodeAt(ne));
        switch (e) {
            case 0:
                // var ie = [];
                // window[re] === window ? ie.push(0) : ie.push(1);
                // try {
                //     var ae = ee + Math.floor(1e7 * Math.random()), se = document.createElement(J);
                //     se.setAttribute(z, ae), se.style.La = j, (document.body || document.getElementsByTagName(G)[0]).appendChild(se), document.getElementById(ae) ? ie.push(0) : ie.push(1), (document.body || document.getElementsByTagName(H)[0]).removeChild(se)
                // } catch (e) {
                //     ie.push(1)
                // }
                // return ie.join(U);
                return "00";
            case 1:
                var le = arguments[1], ce = new s.a.f.init([1332468387, -1641050960, 2136896045, -1629555948], 16),
                    pe = new s.a.f.init([22039283, 1457920463, 776125350, -1941999367], 16);
                return s.Ga.$(le, ce, {ra: pe, ba: s.ba.la, qa: s.na.ma}).xa.toString().toUpperCase();
            case 2:
                return (fe = arguments[1]) ? fe.length > 48 ? fe.substr(0, 48) : fe : Y;
            case 3:
                var de = window.document.URL, ue = window.navigator.userAgent.toLowerCase(), Ae = B;
                window.document.referrer.length > 0 && (Ae = window.document.referrer);
                try {
                    0 == Ae.length && opener.location.href.length > 0 && (Ae = opener.location.href)
                } catch (e) {
                }
                var _e = window.navigator.appCodeName, Ee = window.navigator.appName,
                    ge = window.navigator.platform;
                return de = l(de), Ae = l(Ae), de + V + (ue = l(ue)) + w + Ae + b + _e + x + Ee + D + ge;
            case 4:
                var fe = arguments[1], he = 0;
                if (0 == fe.length) return he;
                for (i = 0; i < fe.length; i++) {
                    var ve = fe.charCodeAt(i);
                    he = (he = (he << 5) - he + ve) & he
                }
                return he;
            case 5:
                var ye = S + arguments[a + i + 8787] + I + arguments[2] + T + y + h + arguments[3] + g + arguments[4] + _ + arguments[5] + u + function () {
                    return c.call(this, 3)
                }() + p + function () {
                    return c.call(this, 0)
                }() + r;
                return function (e) {
                    return c.call(this, 1, e)
                }(t + (he = function (e) {
                    return c.call(this, 4, e)
                }(ye)) + ye)
        }
    }

    return function () {
        for (var e = "", t = 0, o = "±²³´µ¶·¸¹º»¼½¾¿ ¡¢£¤¥¦§¨©ªàáâãäåæçèéûÿí"; t < o.length; t++) e += String.fromCharCode(208 ^ o.charCodeAt(t));
        var r = s, n = r.a.f;
        r.k.H = {
            i: function (e) {
                for (var t = "", o = 0; o < "".length; o++) t += String.fromCharCode(4077 ^ "".charCodeAt(o));
                var r = e.g, n = e.h, i = this.I;
                e.j(), e = [];
                for (var a = 0; a < n; a += 3) for (var s = (r[a >>> 2] >>> 24 - a % 4 * 8 & 255) << 16 | (r[a + 1 >>> 2] >>> 24 - (a + 1) % 4 * 8 & 255) << 8 | r[a + 2 >>> 2] >>> 24 - (a + 2) % 4 * 8 & 255, l = 0; 4 > l && a + .75 * l < n; l++) e.push(i.charAt(s >>> 6 * (3 - l) & 63));
                if (r = i.charAt(64)) for (; e.length % 4;) e.push(r);
                return e.join(t)
            }, parse: function (e) {
                var t = e.length, o = this.I;
                (r = o.charAt(64)) && -1 != (r = e.indexOf(r)) && (t = r);
                for (var r = [], i = 0, a = 0; a < t; a++) if (a % 4) {
                    var s = o.indexOf(e.charAt(a - 1)) << a % 4 * 2, l = o.indexOf(e.charAt(a)) >>> 6 - a % 4 * 2;
                    r[i >>> 2] |= (s | l) << 24 - i % 4 * 8, i++
                }
                return n.create(r, i)
            }, I: e
        }
    }(), function (e) {
        function t(e, t, o, r, n, i, a) {
            return u.call(this, 0, e, t, o, r, n, i, a)
        }

        function o(e, t, o, r, n, i, a) {
            return u.call(this, 1, e, t, o, r, n, i, a)
        }

        function r(e, t, o, r, n, i, a) {
            return u.call(this, 2, e, t, o, r, n, i, a)
        }

        function n(e, t, o, r, n, i, a) {
            return u.call(this, 3, e, t, o, r, n, i, a)
        }

        for (var i = s, a = (c = i.a).f, l = c.x, c = i.G, p = [], d = 0; 64 > d; d++) p[d] = 4294967296 * e.abs(e.sin(d + 1)) | 0;

        function u(e) {
            switch (e) {
                case 0:
                    var t = arguments[1], o = arguments[2], r = arguments[3], n = arguments[4], i = arguments[5],
                        a = arguments[6];
                    return ((t = t + (o & r | ~o & n) + i + arguments[7]) << a | t >>> 32 - a) + o;
                case 1:
                    return ((t = (t = arguments[1]) + ((o = arguments[2]) & (n = arguments[4]) | (r = arguments[3]) & ~n) + (i = arguments[5]) + arguments[7]) << (a = arguments[6]) | t >>> 32 - a) + o;
                case 2:
                    return ((t = (t = arguments[1]) + ((o = arguments[2]) ^ (r = arguments[3]) ^ (n = arguments[4])) + (i = arguments[5]) + arguments[7]) << (a = arguments[6]) | t >>> 32 - a) + o;
                case 3:
                    return ((t = (t = arguments[1]) + ((r = arguments[3]) ^ ((o = arguments[2]) | ~(n = arguments[4]))) + (i = arguments[5]) + arguments[7]) << (a = arguments[6]) | t >>> 32 - a) + o
            }
        }

        c = c.J = l.c({
            z: function () {
                this.K = new a.init([1732584193, 4023233417, 2562383102, 271733878])
            }, w: function (e, i) {
                for (var a = 0; 16 > a; a++) {
                    var s = e[d = i + a];
                    e[d] = 16711935 & (s << 8 | s >>> 24) | 4278255360 & (s << 24 | s >>> 8)
                }
                a = this.K.g;
                var l, c, d = e[i + 0], u = (s = e[i + 1], e[i + 2]), A = e[i + 3], _ = e[i + 4], E = e[i + 5],
                    g = e[i + 6], f = e[i + 7], h = e[i + 8], v = e[i + 9], y = e[i + 10], m = e[i + 11],
                    T = e[i + 12], C = e[i + 13], I = e[i + 14], P = e[i + 15], S = a[0],
                    N = n(N = n(N = n(N = n(N = r(N = r(N = r(N = r(N = o(N = o(N = o(N = o(N = t(N = t(N = t(N = t(N = a[1], c = t(c = a[2], l = t(l = a[3], S = t(S, N, c, l, d, 7, p[0]), N, c, s, 12, p[1]), S, N, u, 17, p[2]), l, S, A, 22, p[3]), c = t(c, l = t(l, S = t(S, N, c, l, _, 7, p[4]), N, c, E, 12, p[5]), S, N, g, 17, p[6]), l, S, f, 22, p[7]), c = t(c, l = t(l, S = t(S, N, c, l, h, 7, p[8]), N, c, v, 12, p[9]), S, N, y, 17, p[10]), l, S, m, 22, p[11]), c = t(c, l = t(l, S = t(S, N, c, l, T, 7, p[12]), N, c, C, 12, p[13]), S, N, I, 17, p[14]), l, S, P, 22, p[15]), c = o(c, l = o(l, S = o(S, N, c, l, s, 5, p[16]), N, c, g, 9, p[17]), S, N, m, 14, p[18]), l, S, d, 20, p[19]), c = o(c, l = o(l, S = o(S, N, c, l, E, 5, p[20]), N, c, y, 9, p[21]), S, N, P, 14, p[22]), l, S, _, 20, p[23]), c = o(c, l = o(l, S = o(S, N, c, l, v, 5, p[24]), N, c, I, 9, p[25]), S, N, A, 14, p[26]), l, S, h, 20, p[27]), c = o(c, l = o(l, S = o(S, N, c, l, C, 5, p[28]), N, c, u, 9, p[29]), S, N, f, 14, p[30]), l, S, T, 20, p[31]), c = r(c, l = r(l, S = r(S, N, c, l, E, 4, p[32]), N, c, h, 11, p[33]), S, N, m, 16, p[34]), l, S, I, 23, p[35]), c = r(c, l = r(l, S = r(S, N, c, l, s, 4, p[36]), N, c, _, 11, p[37]), S, N, f, 16, p[38]), l, S, y, 23, p[39]), c = r(c, l = r(l, S = r(S, N, c, l, C, 4, p[40]), N, c, d, 11, p[41]), S, N, A, 16, p[42]), l, S, g, 23, p[43]), c = r(c, l = r(l, S = r(S, N, c, l, v, 4, p[44]), N, c, T, 11, p[45]), S, N, P, 16, p[46]), l, S, u, 23, p[47]), c = n(c, l = n(l, S = n(S, N, c, l, d, 6, p[48]), N, c, f, 10, p[49]), S, N, I, 15, p[50]), l, S, E, 21, p[51]), c = n(c, l = n(l, S = n(S, N, c, l, T, 6, p[52]), N, c, A, 10, p[53]), S, N, y, 15, p[54]), l, S, s, 21, p[55]), c = n(c, l = n(l, S = n(S, N, c, l, h, 6, p[56]), N, c, P, 10, p[57]), S, N, g, 15, p[58]), l, S, C, 21, p[59]), c = n(c, l = n(l, S = n(S, N, c, l, _, 6, p[60]), N, c, m, 10, p[61]), S, N, u, 15, p[62]), l, S, v, 21, p[63]);
                a[0] = a[0] + S | 0, a[1] = a[1] + N | 0, a[2] = a[2] + c | 0, a[3] = a[3] + l | 0
            }, C: function () {
                var t = this.q, o = t.g, r = 8 * this.r, n = 8 * t.h;
                o[n >>> 5] |= 128 << 24 - n % 32;
                var i = e.floor(r / 4294967296);
                for (o[15 + (n + 64 >>> 9 << 4)] = 16711935 & (i << 8 | i >>> 24) | 4278255360 & (i << 24 | i >>> 8), o[14 + (n + 64 >>> 9 << 4)] = 16711935 & (r << 8 | r >>> 24) | 4278255360 & (r << 24 | r >>> 8), t.h = 4 * (o.length + 1), this.t(), o = (t = this.K).g, r = 0; 4 > r; r++) n = o[r], o[r] = 16711935 & (n << 8 | n >>> 24) | 4278255360 & (n << 24 | n >>> 8);
                return t
            }, e: function () {
                var e = l.e.call(this);
                return e.K = this.K.e(), e
            }
        }), i.J = l.D(c), i.L = l.F(c)
    }(Math), o = (e = (t = s).a).b, r = e.f, n = (e = t.G).M = o.c({
        y: o.c({N: 4, O: e.J, P: 1}),
        init: function (e) {
            this.y = this.y.c(e)
        },
        Q: function (e, t) {
            for (var o = (s = this.y).O.create(), n = r.create(), i = n.g, a = s.N, s = s.P; i.length < a;) {
                l && o.A(l);
                var l = o.A(e).B(t);
                o.p();
                for (var c = 1; c < s; c++) l = o.B(l), o.p();
                n.concat(l)
            }
            return n.h = 4 * a, n
        }
    }), t.M = function (e, t, o) {
        return n.create(o).Q(e, t)
    }, s.a.R || function (e) {
        var t = (_ = s).a, o = t.b, r = t.f, n = t.o, i = _.k.H, a = _.G.M, l = t.R = n.c({
            y: o.c(), S: function (e, t) {
                return this.create(this.T, e, t)
            }, U: function (e, t) {
                return this.create(this.V, e, t)
            }, init: function (e, t, o) {
                this.y = this.y.c(o), this.W = e, this.X = t, this.p()
            }, p: function () {
                n.p.call(this), this.z()
            }, Y: function (e) {
                return this.s(e), this.t()
            }, B: function (e) {
                return e && this.s(e), this.C()
            }, N: 4, Z: 4, T: 1, V: 2, D: function (e) {
                return {
                    $: function (t, o, r) {
                        for (var n = "", i = 0; i < "ǠǧǡǺǽǴ".length; i++) n += String.fromCharCode(403 ^ "ǠǧǡǺǽǴ".charCodeAt(i));
                        return (n == typeof o ? E : A).$(e, t, o, r)
                    }, _: function (t, o, r) {
                        for (var n = "", i = 0; i < "ࣘࣟࣙࣂࣅ࣌".length; i++) n += String.fromCharCode(2219 ^ "ࣘࣟࣙࣂࣅ࣌".charCodeAt(i));
                        return (n == typeof o ? E : A)._(e, t, o, r)
                    }
                }
            }
        });
        t.aa = l.c({
            C: function () {
                return this.t(!0)
            }, u: 1
        });
        var c = _.ba = {}, p = function (e, t, o) {
            var r = this.ca;
            r ? this.ca = void 0 : r = this.da;
            for (var n = 0; n < o; n++) e[t + n] ^= r[n]
        }, d = (t.ea = o.c({
            S: function (e, t) {
                return this.fa.create(e, t)
            }, U: function (e, t) {
                return this.ga.create(e, t)
            }, init: function (e, t) {
                this.ha = e, this.ca = t
            }
        })).c();
        d.fa = d.c({
            ia: function (e, t) {
                var o = this.ha, r = o.u;
                p.call(this, e, t, r), o.ja(e, t), this.da = e.slice(t, t + r)
            }
        }), d.ga = d.c({
            ia: function (e, t) {
                var o = this.ha, r = o.u, n = e.slice(t, t + r);
                o.ka(e, t), p.call(this, e, t, r), this.da = n
            }
        }), c = c.la = d, d = (_.na = {}).ma = {
            na: function (e, t) {
                for (var o, n = (o = (o = 4 * t) - e.h % o) << 24 | o << 16 | o << 8 | o, i = [], a = 0; a < o; a += 4) i.push(n);
                o = r.create(i, o), e.concat(o)
            }, oa: function (e) {
                e.h -= 255 & e.g[e.h - 1 >>> 2]
            }
        }, t.pa = l.c({
            y: l.y.c({ba: c, qa: d}), p: function () {
                l.p.call(this);
                var e = (t = this.y).ra, t = t.ba;
                if (this.W == this.T) var o = t.S; else o = t.U, this.v = 1;
                this.sa = o.call(t, this, e && e.g)
            }, w: function (e, t) {
                this.sa.ia(e, t)
            }, C: function () {
                var e = this.y.qa;
                if (this.W == this.T) {
                    e.na(this.q, this.u);
                    var t = this.t(!0)
                } else t = this.t(!0), e.oa(t);
                return t
            }, u: 4
        });
        var u = t.ta = o.c({
            init: function (e) {
                this.d(e)
            }, toString: function (e) {
                return (e || this.ua).i(this)
            }
        }), A = (c = (_.wa = {}).va = {
            i: function (e) {
                var t = e.xa;
                return ((e = e.ya) ? r.create([1398893684, 1701076831]).concat(e).concat(t) : t).toString(i)
            }, parse: function (e) {
                var t = (e = i.parse(e)).g;
                if (1398893684 == t[0] && 1701076831 == t[1]) {
                    var o = r.create(t.slice(2, 4));
                    t.splice(0, 4), e.h -= 16
                }
                return u.create({xa: e, ya: o})
            }
        }, t.za = o.c({
            y: o.c({wa: c}), $: function (e, t, o, r) {
                r = this.y.c(r);
                var n = e.S(o, r);
                return t = n.B(t), n = n.y, u.create({
                    xa: t,
                    Aa: o,
                    ra: n.ra,
                    Ba: e,
                    ba: n.ba,
                    qa: n.qa,
                    u: e.u,
                    ua: r.wa
                })
            }, _: function (e, t, o, r) {
                return r = this.y.c(r), t = this.Ca(t, r.wa), e.U(o, r).B(t.xa)
            }, Ca: function (e, t) {
                for (var o = "", r = 0; r < "ࠕࠒࠔࠏࠈࠁ".length; r++) o += String.fromCharCode(2150 ^ "ࠕࠒࠔࠏࠈࠁ".charCodeAt(r));
                return o == typeof e ? t.parse(e, this) : e
            }
        })), _ = (_.Da = {}).va = {
            Ea: function (e, t, o, n) {
                return n || (n = r.random(8)), e = a.create({N: t + o}).Q(e, n), o = r.create(e.g.slice(t), 4 * o), e.h = 4 * t, u.create({
                    Aa: e,
                    ra: o,
                    ya: n
                })
            }
        }, E = t.Fa = A.c({
            y: A.y.c({Da: _}), $: function (e, t, o, r) {
                return o = (r = this.y.c(r)).Da.Ea(o, e.N, e.Z), r.ra = o.ra, (e = A.$.call(this, e, t, o.Aa, r)).d(o), e
            }, _: function (e, t, o, r) {
                return r = this.y.c(r), t = this.Ca(t, r.wa), o = r.Da.Ea(o, e.N, e.Z, t.ya), r.ra = o.ra, A._.call(this, e, t, o.Aa, r)
            }
        })
    }(), function () {
        for (var e = s, t = e.a.pa, o = e.G, r = [], n = [], i = [], a = [], l = [], c = [], p = [], d = [], u = [], A = [], _ = [], E = 0; 256 > E; E++) _[E] = 128 > E ? E << 1 : E << 1 ^ 283;
        var g = 0, f = 0;
        for (E = 0; 256 > E; E++) {
            var h = (h = f ^ f << 1 ^ f << 2 ^ f << 3 ^ f << 4) >>> 8 ^ 255 & h ^ 99;
            r[g] = h, n[h] = g;
            var v = _[g], y = _[v], m = _[y], T = 257 * _[h] ^ 16843008 * h;
            i[g] = T << 24 | T >>> 8, a[g] = T << 16 | T >>> 16, l[g] = T << 8 | T >>> 24, c[g] = T, T = 16843009 * m ^ 65537 * y ^ 257 * v ^ 16843008 * g, p[h] = T << 24 | T >>> 8, d[h] = T << 16 | T >>> 16, u[h] = T << 8 | T >>> 24, A[h] = T, g ? (g = v ^ _[_[_[m ^ v]]], f ^= _[_[f]]) : g = f = 1
        }
        var C = [0, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54];
        o = o.Ga = t.c({
            z: function () {
                for (var e = (o = this.X).g, t = o.h / 4, o = 4 * ((this.Ha = t + 6) + 1), n = this.Ia = [], i = 0; i < o; i++) if (i < t) n[i] = e[i]; else {
                    var a = n[i - 1];
                    i % t ? 6 < t && 4 == i % t && (a = r[a >>> 24] << 24 | r[a >>> 16 & 255] << 16 | r[a >>> 8 & 255] << 8 | r[255 & a]) : (a = r[(a = a << 8 | a >>> 24) >>> 24] << 24 | r[a >>> 16 & 255] << 16 | r[a >>> 8 & 255] << 8 | r[255 & a], a ^= C[i / t | 0] << 24), n[i] = n[i - t] ^ a
                }
                for (e = this.Ja = [], t = 0; t < o; t++) i = o - t, a = t % 4 ? n[i] : n[i - 4], e[t] = 4 > t || 4 >= i ? a : p[r[a >>> 24]] ^ d[r[a >>> 16 & 255]] ^ u[r[a >>> 8 & 255]] ^ A[r[255 & a]]
            }, ja: function (e, t) {
                this.Ka(e, t, this.Ia, i, a, l, c, r)
            }, ka: function (e, t) {
                var o = e[t + 1];
                e[t + 1] = e[t + 3], e[t + 3] = o, this.Ka(e, t, this.Ja, p, d, u, A, n), o = e[t + 1], e[t + 1] = e[t + 3], e[t + 3] = o
            }, Ka: function (e, t, o, r, n, i, a, s) {
                for (var l = this.Ha, c = e[t] ^ o[0], p = e[t + 1] ^ o[1], d = e[t + 2] ^ o[2], u = e[t + 3] ^ o[3], A = 4, _ = 1; _ < l; _++) {
                    var E = r[c >>> 24] ^ n[p >>> 16 & 255] ^ i[d >>> 8 & 255] ^ a[255 & u] ^ o[A++],
                        g = r[p >>> 24] ^ n[d >>> 16 & 255] ^ i[u >>> 8 & 255] ^ a[255 & c] ^ o[A++],
                        f = r[d >>> 24] ^ n[u >>> 16 & 255] ^ i[c >>> 8 & 255] ^ a[255 & p] ^ o[A++];
                    u = r[u >>> 24] ^ n[c >>> 16 & 255] ^ i[p >>> 8 & 255] ^ a[255 & d] ^ o[A++], c = E, p = g, d = f
                }
                E = (s[c >>> 24] << 24 | s[p >>> 16 & 255] << 16 | s[d >>> 8 & 255] << 8 | s[255 & u]) ^ o[A++], g = (s[p >>> 24] << 24 | s[d >>> 16 & 255] << 16 | s[u >>> 8 & 255] << 8 | s[255 & c]) ^ o[A++], f = (s[d >>> 24] << 24 | s[u >>> 16 & 255] << 16 | s[c >>> 8 & 255] << 8 | s[255 & p]) ^ o[A++], u = (s[u >>> 24] << 24 | s[c >>> 16 & 255] << 16 | s[p >>> 8 & 255] << 8 | s[255 & d]) ^ o[A++], e[t] = E, e[t + 1] = g, e[t + 2] = f, e[t + 3] = u
            }, N: 8
        }), e.Ga = t.D(o)
    }(), function (e, t, o, r, n) {
        return c.call(this, 5, e, t, o, r, n)
    }
}();

// function setNavigator(userAgent, appCodeName, appName, platform){
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
    //document.referrer = referrer;
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

    await delay((Math.floor(Math.random() * 2) + 1) * 1000);  // sleep for 1 or 2s
    var tm = Math.floor(Date.now() / 1000).toString();
    var cKey = getCkey(req[2], tm, req[1], guid, req[0]);

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
var flowid = createGUID();

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
