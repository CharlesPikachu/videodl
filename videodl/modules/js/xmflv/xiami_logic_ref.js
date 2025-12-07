let XMlayEr = {
  initWasm: async function (i1lII1I1) {
    const lllllIIl = i1lII1I1 || "https://nim.nosdn.127.net/MTY4NDA1NTk=/bmltYV8yNjk4MzIxNjQyMTNfMTc2MzM3NjM2MDk2Ml9iMTdiZDNiZC1hZTRjLTQ0M2QtYmZjNi00ODQ3M2NkZTk5ZTg=";
    if (this.isWasmLoaded) {
      return true;
    }
    try {
      {
        const Iii1Ill1 = await fetch(lllllIIl, {
          mode: "cors"
        });
        if (!Iii1Ill1.ok) {
          console.error("WASM加载失败：HTTP " + Iii1Ill1.status);
          return false;
        }
        const IIII11I1 = await Iii1Ill1.arrayBuffer();
        const Ii11II1 = {
          env: {
            memory: new WebAssembly.Memory({
              initial: 10,
              maximum: 100
            }),
            abort: () => console.error("WASM执行异常"),
            emscripten_notify_memory_growth: lii11ilI => {}
          }
        };
        const Ii1IlI1 = await WebAssembly.instantiate(IIII11I1, Ii11II1);
        this.wasmExports = Ii1IlI1.instance.exports;
        this.isWasmLoaded = true;
        console.log("WASM初始化成功");
        return true;
      }
    } catch (liiIl1l) {
      console.error("WASM初始化失败：", liiIl1l.message);
      this.isWasmLoaded = false;
      return false;
    }
  },
  encryptWithWasm: async function (ll1Il1li) {
    if (!this.isWasmLoaded) {
      console.error("WASM未初始化，请先调用initWasm()");
      return null;
    }
    if (typeof ll1Il1li !== "string" || ll1Il1li.trim() === "") {
      console.error("加密文本无效");
      return null;
    }
    const ll1iI1 = this.wasmExports._wasm_malloc || this.wasmExports.wasm_malloc;
    const lliiI11l = this.wasmExports._wasm_free || this.wasmExports.wasm_free;
    const I1IIlli1 = this.wasmExports._encrypt_data || this.wasmExports.encrypt_data;
    const il1ilil = new TextEncoder();
    const llIiIiIi = il1ilil.encode(ll1Il1li);
    const li1liIi1 = llIiIiIi.length;
    const lIII1Iii = (li1liIi1 + 15) / 16 * 16;
    const li1lill = ll1iI1(lIII1Iii);
    const Il1Iliil = ll1iI1(lIII1Iii);
    if (!li1lill || !Il1Iliil) {
      return null;
    }
    try {
      {
        const IlIIl1lI = new Uint8Array(this.wasmExports.memory.buffer);
        IlIIl1lI.set(llIiIiIi, li1lill);
        const lIi1Il1 = I1IIlli1(li1lill, li1liIi1, Il1Iliil, lIII1Iii);
        if (lIi1Il1 < 0) {
          console.error("加密失败：内存不足");
          return null;
        }
        const l1III1 = IlIIl1lI.subarray(Il1Iliil, Il1Iliil + lIi1Il1);
        return btoa(String.fromCharCode(...l1III1));
      }
    } finally {
      lliiI11l(li1lill);
      lliiI11l(Il1Iliil);
    }
  },
  decrypt: function (llIiiili) {
    const lilIIl1i = "4zYgSAsEAUS6YAud";
    const Il1liIii = "ppa7qtR4McCIMCX4";
    let li1iil1l = CryptoJS.AES.decrypt(llIiiili, CryptoJS.enc.Utf8.parse(lilIIl1i), {
      iv: CryptoJS.enc.Utf8.parse(Il1liIii),
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    });
    return li1iil1l.toString(CryptoJS.enc.Utf8);
  },
  error: function (I11Ill1) {
    $("#player").hide();
    $("#loading").hide();
    $("body").append("<div id=\"error\"><h1>" + I11Ill1 + "</h1></div>");
  },
  AjaxData: function (i1IIIii, llill1I1) {
    $.ajaxSettings.timeout = "10000";
    $.ajaxSettings.async = true;
    $.post("https://202.189.8.170/Api.js", i1IIIii, function (i1iIli1l) {
      if (i1iIli1l.code == 200) {
        {
          const iI1iiIi = i1iIli1l.data;
          llill1I1(XMlayEr.decrypt(iI1iiIi));
        }
      } else {
        XMlayEr.error(i1iIli1l.msg);
      }
    }, "json").error(function (lll1ill, iiiIiIi, IIliiii) {
      {
        $.post("https://cache.hls.one/Api.js", i1IIIii, function (lI111lil) {
          if (lI111lil.code == 200) {
            {
              const llil11l = lI111lil.data;
              llill1I1(XMlayEr.decrypt(llil11l));
            }
          } else {
            XMlayEr.error(lI111lil.msg);
          }
        }, "json").error(function (iII1ilIl, II1IIlIl, iIiliIi1) {
          XMlayEr.error("接口请求失败,请尝试刷新重试！");
        });
      }
    });
  },
  XMlayEr: function (I1liii) {
    const li11il1I = this;
    $.ajax({
      type: "get",
      url: "https://data.video.iqiyi.com/v.f4v",
      success: function (iIIIi11i) {
        {
          const liIII1 = navigator.userAgent.match(/iPad|iPhone|Android|Linux|iPod/i) ? 1 : 0;
          const iiIl1lii = new URLSearchParams(location.search);
          const illlIiil = iiIl1lii.get("ua") ?? liIII1;
          li11il1I.next0 = iiIl1lii.get("next");
          const Il11Ill = iIIIi11i.t;
          const llli1lIi = iIIIi11i.time;
          const IiillI = sign(hex_md5(llli1lIi + I1liii));
          li11il1I.initWasm().then(() => li11il1I.encryptWithWasm(IiillI)).then(IilIi1l => {
            li11il1I.AjaxData({
              ua: illlIiil,
              url: I1liii,
              time: llli1lIi,
              key: IiillI,
              token: IilIi1l,
              area: Il11Ill
            }, function (i11i1ii) {
              parsedData = JSON.parse(i11i1ii);
              li11il1I.name = parsedData.name || "";
              this.pic = parsedData.pic || "";
              li11il1I.type = parsedData.type || "";
              li11il1I.vurl = parsedData.url || "";
              li11il1I.next = parsedData.next || "";
              li11il1I.listapi = parsedData.listapi || "";
              li11il1I.dmid = parsedData.dmid || "";
              li11il1I.ggdmapi = parsedData.ggdmapi || "";
              li11il1I.load();
            });
          }).catch(lI1iIII1 => {
            {
              console.error("额呵出现错误：", lI1iIII1.message);
              li11il1I.error("验证失败，请重试！");
            }
          });
        }
      },
      error: function (ll1Ii1il, lIl1I1i1, IilIIli) {
        li11il1I.error("请检查你的网络是否正常!");
      }
    });
  },
  empty: function (IIilliIl) {
    return IIilliIl == null || IIilliIl === "";
  },
  cookie: {
    Set: function (lI1li1l1, ii1lIiII, i1iiillI = 7, lI1Illi = "1") {
      if (lI1Illi === "1") {
        localStorage.setItem(lI1li1l1, ii1lIiII);
      } else {
        let iIi11il = new Date();
        iIi11il.setTime(iIi11il.getTime() + i1iiillI * 24 * 60 * 60 * 1000);
        document.cookie = lI1li1l1 + "=" + encodeURIComponent(ii1lIiII) + ";path=/;expires=" + iIi11il.toUTCString();
      }
    },
    Get: function (ili1lii1, Il11l1l = "1") {
      if (Il11l1l === "1") {
        return localStorage.getItem(ili1lii1);
      } else {
        let illIiliI = document.cookie.match(new RegExp("(^| )" + ili1lii1 + "=([^;]*)(;|$)"));
        if (illIiliI != null) {
          return decodeURIComponent(illIiliI[2]);
        }
      }
    },
    Del: function (I11ilil1, l11ii1 = "1") {
      if (l11ii1 === "1") {
        localStorage.removeItem(I11ilil1);
      } else {
        {
          let il1ilIll = new Date();
          il1ilIll.setTime(il1ilIll.getTime() - 1);
          let l1ii1i1 = this.Get(I11ilil1, 2);
          l1ii1i1 != null && (document.cookie = I11ilil1 + "=" + encodeURIComponent(l1ii1i1) + ";path=/;expires=" + il1ilIll.toUTCString());
        }
      }
    }
  },
  play: function () {
    let I1ll1iii = {
      container: "#player",
      contextmenu: [],
      autoplay: true,
      poster: XMlayEr.pic || "https://nim.nosdn.127.net/MTY4NDA1NTk=/bmltYV8yNjk4MzIxNjQyMTNfMTc2MzIzODkzMDM5OF80ZjM1MGM0YS02NzJiLTQ4YWMtOWJlOS04NjA5NDMwMjE2MzU=",
      icons: {
        loading: "<div id=\"qloading\"></div>",
        indicator: "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 18 18\" width=\"18\" height=\"18\" preserveAspectRatio=\"xMidYMid meet\" style=\"width: 100%; height: 100%; transform: translate3d(0px, 0px, 0px);\"><defs><clipPath id=\"__lottie_element_602\"><rect width=\"18\" height=\"18\" x=\"0\" y=\"0\"></rect></clipPath></defs><g clip-path=\"url(#__lottie_element_602)\"><g transform=\"matrix(0.9883429408073425,-0.7275781631469727,0.6775955557823181,0.920446515083313,7.3224687576293945,-0.7606706619262695)\" opacity=\"1\" style=\"display: block;\"><g opacity=\"1\" transform=\"matrix(0.9937776327133179,-0.11138220876455307,0.11138220876455307,0.9937776327133179,-2.5239999294281006,1.3849999904632568)\"><path fill=\"rgb(51,51,51)\" fill-opacity=\"1\" d=\" M0.75,-1.25 C0.75,-1.25 0.75,1.25 0.75,1.25 C0.75,1.663925051689148 0.4139249920845032,2 0,2 C0,2 0,2 0,2 C-0.4139249920845032,2 -0.75,1.663925051689148 -0.75,1.25 C-0.75,1.25 -0.75,-1.25 -0.75,-1.25 C-0.75,-1.663925051689148 -0.4139249920845032,-2 0,-2 C0,-2 0,-2 0,-2 C0.4139249920845032,-2 0.75,-1.663925051689148 0.75,-1.25z\"></path></g></g><g transform=\"matrix(1.1436611413955688,0.7535901665687561,-0.6317168474197388,0.9587040543556213,16.0070743560791,2.902894973754883)\" opacity=\"1\" style=\"display: block;\"><g opacity=\"1\" transform=\"matrix(0.992861807346344,0.1192704513669014,-0.1192704513669014,0.992861807346344,-2.5239999294281006,1.3849999904632568)\"><path fill=\"rgb(51,51,51)\" fill-opacity=\"1\" d=\" M0.75,-1.25 C0.75,-1.25 0.75,1.25 0.75,1.25 C0.75,1.663925051689148 0.4139249920845032,2 0,2 C0,2 0,2 0,2 C-0.4139249920845032,2 -0.75,1.663925051689148 -0.75,1.25 C-0.75,1.25 -0.75,-1.25 -0.75,-1.25 C-0.75,-1.663925051689148 -0.4139249920845032,-2 0,-2 C0,-2 0,-2 0,-2 C0.4139249920845032,-2 0.75,-1.663925051689148 0.75,-1.25z\"></path></g></g><g transform=\"matrix(1,0,0,1,8.890999794006348,8.406000137329102)\" opacity=\"1\" style=\"display: block;\"><g opacity=\"1\" transform=\"matrix(1,0,0,1,0.09099999815225601,1.1009999513626099)\"><path fill=\"rgb(255,255,255)\" fill-opacity=\"1\" d=\" M7,-3 C7,-3 7,3 7,3 C7,4.379749774932861 5.879749774932861,5.5 4.5,5.5 C4.5,5.5 -4.5,5.5 -4.5,5.5 C-5.879749774932861,5.5 -7,4.379749774932861 -7,3 C-7,3 -7,-3 -7,-3 C-7,-4.379749774932861 -5.879749774932861,-5.5 -4.5,-5.5 C-4.5,-5.5 4.5,-5.5 4.5,-5.5 C5.879749774932861,-5.5 7,-4.379749774932861 7,-3z\"></path><path stroke-linecap=\"butt\" stroke-linejoin=\"miter\" fill-opacity=\"0\" stroke-miterlimit=\"4\" stroke=\"rgb(51,51,51)\" stroke-opacity=\"1\" stroke-width=\"1.5\" d=\" M7,-3 C7,-3 7,3 7,3 C7,4.379749774932861 5.879749774932861,5.5 4.5,5.5 C4.5,5.5 -4.5,5.5 -4.5,5.5 C-5.879749774932861,5.5 -7,4.379749774932861 -7,3 C-7,3 -7,-3 -7,-3 C-7,-4.379749774932861 -5.879749774932861,-5.5 -4.5,-5.5 C-4.5,-5.5 4.5,-5.5 4.5,-5.5 C5.879749774932861,-5.5 7,-4.379749774932861 7,-3z\"></path></g></g><g transform=\"matrix(1,0,0,1,8.89900016784668,8.083999633789062)\" opacity=\"1\" style=\"display: block;\"><g opacity=\"1\" transform=\"matrix(1,0,0,1,-2.5239999294281006,1.3849999904632568)\"><path fill=\"rgb(51,51,51)\" fill-opacity=\"1\" d=\" M0.875,-1.125 C0.875,-1.125 0.875,1.125 0.875,1.125 C0.875,1.607912540435791 0.48291251063346863,2 0,2 C0,2 0,2 0,2 C-0.48291251063346863,2 -0.875,1.607912540435791 -0.875,1.125 C-0.875,1.125 -0.875,-1.125 -0.875,-1.125 C-0.875,-1.607912540435791 -0.48291251063346863,-2 0,-2 C0,-2 0,-2 0,-2 C0.48291251063346863,-2 0.875,-1.607912540435791 0.875,-1.125z\"></path></g></g><g transform=\"matrix(1,0,0,1,14.008999824523926,8.083999633789062)\" opacity=\"1\" style=\"display: block;\"><g opacity=\"1\" transform=\"matrix(1,0,0,1,-2.5239999294281006,1.3849999904632568)\"><path fill=\"rgb(51,51,51)\" fill-opacity=\"1\" d=\" M0.8999999761581421,-1.100000023841858 C0.8999999761581421,-1.100000023841858 0.8999999761581421,1.100000023841858 0.8999999761581421,1.100000023841858 C0.8999999761581421,1.596709966659546 0.4967099726200104,2 0,2 C0,2 0,2 0,2 C-0.4967099726200104,2 -0.8999999761581421,1.596709966659546 -0.8999999761581421,1.100000023841858 C-0.8999999761581421,1.100000023841858 -0.8999999761581421,-1.100000023841858 -0.8999999761581421,-1.100000023841858 C-0.8999999761581421,-1.596709966659546 -0.4967099726200104,-2 0,-2 C0,-2 0,-2 0,-2 C0.4967099726200104,-2 0.8999999761581421,-1.596709966659546 0.8999999761581421,-1.100000023841858z\"></path></g></g></g></svg>",
        state: "<svg t=\"1735985723837\" class=\"icon\" viewBox=\"0 0 1024 1024\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" p-id=\"18247\" width=\"80\" height=\"80\"><path d=\"M830.577778 227.555556H657.066667l74.903703-70.162963c11.377778-11.377778 11.377778-29.392593 0-39.822223-5.688889-5.688889-13.274074-8.533333-21.807407-8.533333-7.585185 0-15.17037 2.844444-21.807407 8.533333L570.785185 227.555556H456.059259L338.488889 117.57037c-5.688889-5.688889-13.274074-8.533333-21.807408-8.533333-7.585185 0-15.17037 2.844444-21.807407 8.533333-11.377778 11.377778-11.377778 29.392593 0 39.822223L369.777778 227.555556H193.422222C117.57037 227.555556 56.888889 295.822222 56.888889 381.155556v332.8c0 85.333333 60.681481 153.6 136.533333 153.6h42.666667c0 25.6 22.755556 47.407407 50.251852 47.407407s50.251852-20.859259 50.251852-47.407407h353.659259c0 25.6 22.755556 47.407407 50.251852 47.407407s50.251852-20.859259 50.251852-47.407407h38.874074c75.851852 0 136.533333-69.214815 136.533333-153.6V381.155556c0.948148-85.333333-59.733333-153.6-135.585185-153.6zM698.785185 574.577778L425.718519 733.866667c-22.755556 13.274074-41.718519 2.844444-41.718519-24.651852V389.688889c0-26.548148 18.962963-37.925926 41.718519-24.651852l273.066666 160.237037c22.755556 14.222222 22.755556 35.081481 0 49.303704z\" p-id=\"18248\" fill=\"#ffffff\"></path></svg>",
        play: "<svg t=\"1735986127554\" class=\"icon\" viewBox=\"0 0 1024 1024\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" p-id=\"35346\" width=\"24\" height=\"24\"><path d=\"M829.696 584.405333c-3.626667 3.712-17.28 19.584-29.994667 32.597334-74.538667 82.133333-311.765333 216.533333-413.568 257.536-15.445333 6.613333-54.528 20.565333-75.434666 21.461333a123.733333 123.733333 0 0 1-57.301334-13.952 119.893333 119.893333 0 0 1-50.858666-57.856c-6.4-16.853333-16.426667-67.2-16.426667-68.096C176.213333 701.013333 170.666667 611.456 170.666667 512.512c0-94.293333 5.504-180.181333 13.653333-236.117333 0.938667-0.853333 10.922667-63.445333 21.802667-84.906667C226.176 152.32 265.258667 128 307.072 128h3.626667c27.264 0.938667 84.565333 25.258667 84.565333 26.197333 96.298667 41.088 329.002667 168.874667 405.376 253.824 0 0 21.504 21.802667 30.890667 35.413334 14.549333 19.626667 21.802667 43.861333 21.802666 68.096 0 27.093333-8.149333 52.309333-23.637333 72.832z\" fill=\"#ffffff\" p-id=\"35347\"></path></svg>",
        volume: "<svg class=\"icon\" xmlns=\"http://www.w3.org/2000/svg\" fill=\"none\" data-pointer=\"none\" viewBox=\"0 0 24 24\" width=\"20\" height=\"20\"><path fill=\"#fff\" fill-rule=\"evenodd\" stroke=\"#fff\" stroke-width=\"0.3\" d=\"M12.781 4.285A.75.75 0 0 1 14 4.871V19.13a.75.75 0 0 1-1.219.586l-4.24-3.393a3.75 3.75 0 0 0-2.343-.822H4.38c-.343 0-.583-.219-.628-.482A18.013 18.013 0 0 1 3.5 12c0-1.246.13-2.297.253-3.018.045-.263.285-.482.628-.482h1.817a3.75 3.75 0 0 0 2.342-.822l4.242-3.393Zm2.719.586c0-1.886-2.182-2.936-3.656-1.757l-4.24 3.393A2.25 2.25 0 0 1 6.197 7H4.38c-.996 0-1.925.671-2.106 1.728A19.516 19.516 0 0 0 2 12c0 1.347.14 2.485.275 3.272C2.456 16.328 3.385 17 4.38 17h1.817c.51 0 1.006.174 1.405.493l4.241 3.393c1.474 1.179 3.656.129 3.656-1.757V4.87Zm4.56.565a.75.75 0 0 1 1.057.084 10.002 10.002 0 0 1 0 12.96.75.75 0 0 1-1.141-.974 8.502 8.502 0 0 0 0-11.012.75.75 0 0 1 .084-1.058Zm-2.815 2.808a.75.75 0 0 1 1.05.147 6.003 6.003 0 0 1 0 7.216.75.75 0 1 1-1.198-.903 4.504 4.504 0 0 0 0-5.41.75.75 0 0 1 .148-1.05Z\" clip-rule=\"evenodd\"></path></svg>",
        volumeClose: "<svg xmlns=\"http://www.w3.org/2000/svg\" fill=\"none\" data-pointer=\"none\" viewBox=\"0 0 24 24\" width=\"20\" height=\"20\"><path fill=\"#fff\" fill-rule=\"evenodd\" stroke=\"#fff\" stroke-width=\"0.3\" d=\"M12.781 4.285A.75.75 0 0 1 14 4.871V19.13a.75.75 0 0 1-1.219.586l-4.24-3.393a3.75 3.75 0 0 0-2.343-.822H4.38c-.343 0-.583-.219-.628-.482A18.013 18.013 0 0 1 3.5 12c0-1.246.13-2.297.253-3.018.045-.263.285-.482.628-.482h1.817a3.75 3.75 0 0 0 2.342-.822l4.242-3.393Zm2.719.586c0-1.886-2.182-2.936-3.656-1.757l-4.24 3.393A2.25 2.25 0 0 1 6.197 7H4.38c-.996 0-1.925.671-2.106 1.728A19.516 19.516 0 0 0 2 12c0 1.347.14 2.485.275 3.272C2.456 16.328 3.385 17 4.38 17h1.817c.51 0 1.006.174 1.405.493l4.241 3.393c1.474 1.179 3.656.129 3.656-1.757V4.87Zm7.78 5.16a.75.75 0 1 0-1.06-1.061l-1.97 1.97-1.97-1.97a.75.75 0 1 0-1.06 1.06L19.19 12l-1.97 1.97a.75.75 0 1 0 1.06 1.06l1.97-1.97 1.97 1.97a.75.75 0 1 0 1.06-1.06L21.31 12l1.97-1.97Z\" clip-rule=\"evenodd\"></path></svg>",
        setting: "<svg class=\"icon\" viewBox=\"0 0 28 28\" xmlns=\"http://www.w3.org/2000/svg\" width=\"26\" height=\"26\"><path d=\"M17.404 4.557a3.5 3.5 0 0 1 3.031 1.75l3.516 6.09a3.5 3.5 0 0 1 0 3.5l-3.49 6.044a3.5 3.5 0 0 1-3.133  1.748l-6.88-.202a3.5 3.5 0 0 1-2.87-1.65l-3.664-5.892a3.5 3.5 0 0 1-.059-3.599l3.487-6.039a3.5 3.5 0 0 1 3.031-1.75Zm0 1.75h-7.031a1.75 1.75 0 0 0-1.516.875l-3.486 6.04a1.75 1.75 0 0 0 .03 1.799l3.664 5.892c.31.498.848.808 1.434.825l6.88.202a1.75 1.75 0 0 0 1.567-.874l3.49-6.045a1.75 1.75 0 0 0 0-1.75L18.92 7.182a1.75 1.75 0 0 0-1.516-.875Zm-6.437 5.962a3.5 3.5 0 1 1 6.063 3.5 3.5 3.5 0 0 1-6.063-3.5Zm3.907.234a1.75 1.75 0 1 0-1.75 3.031 1.75 1.75 0 0 0 1.75-3.03Z\" stroke-width=\".5\" fill-rule=\"evenodd\"></path></svg>",
        fullscreenOn: "<svg xmlns=\"http://www.w3.org/2000/svg\" fill=\"none\" data-pointer=\"none\" viewBox=\"0 0 24 24\" width=\"24\" height=\"24\"><path fill=\"#fff\" stroke=\"#fff\" stroke-width=\"0.3\" fill-rule=\"evenodd\" d=\"M6 4a2 2 0 0 0-2 2v6.5a1 1 0 0 0 2 0V6h6.5a1 1 0 1 0 0-2H6Zm14 7.5a1 1 0 1 0-2 0V18h-6.5a1 1 0 1 0 0 2H18a2 2 0 0 0 2-2v-6.5Z\" clip-rule=\"evenodd\"></path></svg>"
      },
      flip: true,
      hotkey: true,
      playbackRate: true,
      aspectRatio: true,
      screenshot: false,
      pip: true,
      fullscreen: true,
      miniProgressBar: true,
      fastForward: true,
      airplay: true,
      autoOrientation: true,
      lang: "zh-cn",
      theme: "#CC6633",
      volume: Number(0.5),
      setting: true,
      url: iiiiliil
    };
    let iiiiliil = XMlayEr.vurl;
    let IIl1II1I = XMlayEr.type;
    if (IIl1II1I === "flv") {
      I1ll1iii.type = "flv";
      I1ll1iii.customType = {
        flv: function iiIllIii(i1lI1ill, iil11lIi, IlII1ll) {
          if (flvjs.isSupported()) {
            {
              const iI1III = flvjs.createPlayer({
                type: "flv",
                url: iil11lIi
              });
              iI1III.attachMediaElement(i1lI1ill);
              iI1III.load();
              IlII1ll.flv = iI1III;
              IlII1ll.once("url", () => iI1III.destroy());
              IlII1ll.once("destroy", () => iI1III.destroy());
            }
          } else {
            IlII1ll.notice.show = "Unsupported playback format: flv";
          }
        }
      };
    } else {
      (IIl1II1I === "m3u8" || IIl1II1I === "hls") && (I1ll1iii.type = "m3u8", I1ll1iii.customType = {
        m3u8: function iII1ii1l(ilIilI, IIiI1il1, i11Illl1) {
          {
            if (Hls.isSupported()) {
              const lIlIlIl1 = new Hls();
              lIlIlIl1.loadSource(IIiI1il1);
              lIlIlIl1.attachMedia(ilIilI);
              i11Illl1.hls = lIlIlIl1;
              i11Illl1.once("url", () => lIlIlIl1.destroy());
              i11Illl1.once("destroy", () => lIlIlIl1.destroy());
            } else {
              ilIilI.canPlayType("application/vnd.apple.mpegurl") ? ilIilI.src = IIiI1il1 : i11Illl1.notice.show = "Unsupported playback format: m3u8";
            }
          }
        }
      });
    }
    XMlayEr.void = new Artplayer(I1ll1iii);
    XMlayEr.void.on("ready", () => {
      XMlayEr.void.play().catch(iilill1l => {
        console.log("自动播放可能被浏览器阻止，可手动点击播放", iilill1l);
      });
    });
    $(document).on("click", ".yxq-vod-list", function () {
      var Ii1ii1l = $(".yxq-listbox");
      Ii1ii1l.length > 0 ? ($(".vodlist-of,.r-button").toggle(), $(".yxq-stting").length > 0 ? Ii1ii1l.removeClass("yxq-stting") : Ii1ii1l.addClass("yxq-stting")) : Ii1ii1l.addClass("yxq-stting");
    });
  },
  load: function () {
    XMlayEr.play();
    let l1llIiI1 = "#CC6633";
    let I11lIIIi = ".s-on svg circle,.s-on svg path{fill:" + l1llIiI1 + "!important}.t-color{color:" + l1llIiI1 + "}.t-bj{background-color:" + l1llIiI1 + "}.ec-subtitle p{color: #fff; font-size: 1.6vw;background:#000c;}" + XMlayEr.header.logoCss() + "@media (max-width: 767px){.player-logo{width:100px}}";
    $("head").append("<style>" + I11lIIIi + "</style>");
    box.children().append("<div class=\"lock-box\"></div><div class=\"ec-danMa text\"><div class=\"ec-danMa-item ec-danMa-item--demo\"></div></div><div class=\"ec-subtitle\"></div><div class=\"header ease flex between\"><div class=\"player-title\"></div><div class=\"flex qoe-normal\" style=\"display:none\"><div class=\"kui-time\"></div><div class=\"batteryShape\"><div class=\"level\"><div class=\"percentage\"></div></div></div></div></div><div class=\"dm-box flex dm-wap\"><div class=\"dm-box-left flex\"><div class=\"dm-box-cc\" data-id=\"0\"></div><div class=\"dm-box-set\"></div><div class=\"dm-set-box ec-box\"><div id=\"dm_n1\" class=\"dm-set-list ds-set-show\">\n<div class=\"flex between\" data-id=\"1\"><div class=\"dm-set-label\">弹幕速度</div><div class=\"set-toggle flex\"><span>适中</span></div></div>\n<div class=\"flex between\" data-id=\"2\"><div class=\"dm-set-label\">字体大小</div><div class=\"set-toggle flex\"><span>默认</span></div></div>\n<div class=\"flex between\" data-id=\"3\"><div class=\"dm-set-label\">不透明度</div><div class=\"set-toggle flex\"><span>100%</span></div></div>\n<div class=\"flex between\"  data-id=\"4\"><div class=\"dm-set-label\">弹幕范围</div><div class=\"set-toggle flex\"><span>3/4</span></div></div></div></div></div>\n<div class=\"dm-input-box flex-auto\"><div class=\"dm-box-t\"><div class=\"dm-style-box ec-box\"><div class=\"dm-style-title\">弹幕方向</div><div class=\"content_dmP-1 flex\">\n<div class=\"item on-1\" data-type=\"right\">滚动<i></i></div><div class=\"item\" data-type=\"top\">顶部<i></i></div><div class=\"item\" data-type=\"bottom\">底部<i></i></div></div>\n<div class=\"dm-style-title\">弹幕颜色</div><div class=\"content_dmP-2 flex\"><div class=\"item on-1\">默认<i></i></div><div class=\"item\" data-color=\"#02CC92\" style=\"color:#02CC92;border-color:#02CC92;\">青草绿<i></i></div>\n<div class=\"item\" data-color=\"#03A5FF\"  style=\"color:#03A5FF;border-color:#03A5FF;\">香菇蓝<i></i></div><div class=\"item\" data-color=\"#FF893B\"  style=\"color:#FF893B;border-color:#FF893B;\">暖阳橙<i></i></div>\n<div class=\"item\" data-color=\"#FC265E\"  style=\"color:#FC265E;border-color:#FC265E;\">喜庆红<i></i></div><div class=\"item\" data-color=\"#BE8DF7\"  style=\"color:#BE8DF7;border-color:#BE8DF7;\">销魂紫<i></i></div>\n</div></div><img alt=\"弹幕颜色\" class=\"dm-box-t-img\" src=\"https://img.alicdn.com/imgextra/i2/O1CN01KdGeoZ25bCijuGQzn_!!6000000007544-2-tps-69-66.png\"></div><input class=\"dm-input\" type=\"text\" data-time=\"10\" autocomplete=\"off\" placeholder=\"来发个弹幕吧~\" maxlength=\"22\">\n<button class=\"dm-send t-bj\" data-balloon=\"发送\" data-balloon-pos=\"up\">发送</button></div></div><div class=\"player-list-off off\"></div><div class=\"ec-box player-list\"><div class=\"new-check\"><div class=\"new-body\"></div></div></div><div class=\"ec-remember\"></div><div class=\"broadside seat1\"></div>");
    $(".art-controls-right").prepend("<div class=\"art-control dm-bnt hint--rounded hint--top\" data-index=\"20\" aria-label=\"发弹幕\"><i class=\"art-icon\"><svg viewBox=\"0 0 1024 1024\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M833.94335938 148.30859375H190.05664062c-39.28710938 0-71.19140625 31.90429688-71.19140624 71.19140625V689.5390625c0 39.28710938 31.90429688 71.19140625 71.19140625 71.19140625h169.45312499l131.13281251 107.05078125c6.50390625 5.2734375 14.32617188 7.91015625 22.23632812 7.91015625 7.82226563 0 15.73242188-2.63671875 22.1484375-7.91015625l131.8359375-107.05078125h166.9921875c39.28710938 0 71.19140625-31.90429688 71.19140625-71.19140625V219.5c0.08789063-39.28710938-31.90429688-71.19140625-71.10351563-71.19140625z m0.87890624 541.23046875c0 0.43945313-0.43945313 0.87890625-0.87890625 0.87890625H654.47070313c-8.0859375 0-15.90820313 2.8125-22.14843751 7.91015625L512.96679688 795.18359375 394.31445312 698.328125c-6.24023438-5.09765625-14.15039063-7.91015625-22.23632812-7.91015625H190.05664062c-0.43945313 0-0.87890625-0.43945313-0.87890624-0.87890625V219.5c0-0.43945313 0.43945313-0.87890625 0.87890625-0.87890625h643.79882812c0.43945313 0 0.87890625 0.43945313 0.87890625 0.87890625V689.5390625z\"></path><path d=\"M345.09570312 455.3984375m-43.94531249 0a43.9453125 43.9453125 0 1 0 87.89062499 0 43.9453125 43.9453125 0 1 0-87.890625 0Z\"></path><path d=\"M512.96679688 455.3984375m-43.9453125 0a43.9453125 43.9453125 0 1 0 87.89062499 0 43.9453125 43.9453125 0 1 0-87.890625 0Z\"></path><path d=\"M681.01367188 455.3984375m-43.94531251 0a43.9453125 43.9453125 0 1 0 87.89062501 0 43.9453125 43.9453125 0 1 0-87.890625 0Z\"></path></svg></i></div><div class=\"art-control content-bnt hint--rounded hint--top\" data-index=\"20\" aria-label=\"字幕开关\"><i class=\"art-icon\"><svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 32 32\"><path d=\"M26.667 5.333h-21.333c-0 0-0.001 0-0.001 0-1.472 0-2.666 1.194-2.666 2.666 0 0 0 0.001 0 0.001v-0 16c0 0 0 0.001 0 0.001 0 1.472 1.194 2.666 2.666 2.666 0 0 0.001 0 0.001 0h21.333c0 0 0.001 0 0.001 0 1.472 0 2.666-1.194 2.666-2.666 0-0 0-0.001 0-0.001v0-16c0-0 0-0.001 0-0.001 0-1.472-1.194-2.666-2.666-2.666-0 0-0.001 0-0.001 0h0zM5.333 16h5.333v2.667h-5.333v-2.667zM18.667 24h-13.333v-2.667h13.333v2.667zM26.667 24h-5.333v-2.667h5.333v2.667zM26.667 18.667h-13.333v-2.667h13.333v2.667z\"></path></svg></i></div>");
    XMlayEr.LoadAnimation();
    XMlayEr.header.Init();
    $(".content-bnt").remove();
    XMlayEr.danMu.Init();
    XMlayEr.list.html();
    XMlayEr.list.next();
    XMlayEr.list.autoNext();
    XMlayEr.broadside();
    XMlayEr.void.on("video:timeupdate", function () {
      {
        let liiIiIil = XMlayEr.void.currentTime;
        XMlayEr.cookie.Set(url, liiIiIil, 7, 2);
      }
    });
    XMlayEr.void.on("video:ended", function () {
      XMlayEr.cookie.Del(url, 2);
    });
  },
  tips: {
    removeMsg: function () {
      $(".pop-msg").remove();
    },
    msg: function (I1I1ilil, Illl11l) {
      let llIIll1l = Illl11l || 5000;
      let Il1lliI = $("body");
      $(".pop-msg").length > 0 && XMlayEr.tips.removeMsg();
      Il1lliI.children().append("<div class=\"pop-msg vague4\" style=\"background: rgba(0, 0, 0, 0.7); color: #FFFFFF; border-radius: 6px; padding: 10px 20px; font-weight: bold;\"><div class=\"pop-content\"></div></div>");
      $(".pop-msg .pop-content").html(I1I1ilil);
      setTimeout(XMlayEr.tips.removeMsg, llIIll1l);
    }
  },
  header: {
    Init: function () {
      this.marquee();
      this.title(XMlayEr.name);
      this.time();
      this.qfe();
    },
    logoCss: function () {
      switch (1) {
        case "1":
          return ".player-logo{left: 20px;top: 20px;width: 15%;}";
        case "2":
          return ".player-logo{right: 20px;top: 20px;width: 15%;}";
        case "3":
          return ".player-logo{left: 20px;bottom: 80px;width: 15%;}";
        default:
          return ".player-logo{right: 20px;bottom: 80px;width: 15%;}";
      }
    },
    marquee: function () {
      box.children().append("<div class=\"bullet-screen\" style=\"animation: bullet 10s linear infinite;color:#E50916</div>");
      setTimeout(function () {
        $(".bullet-screen").remove();
      }, 60000);
      XMlayEr.void.on("pause", function () {
        {
          $(".bullet-screen").css("animation-play-state", "paused");
        }
      });
      XMlayEr.void.on("play", function () {
        $(".bullet-screen").css("animation-play-state", "running");
      });
    },
    time: function () {
      let iliIill1 = new Date();
      let IilliiII = iliIill1.getHours() < 10 ? "0" + iliIill1.getHours() : iliIill1.getHours();
      let I11Iiill = iliIill1.getMinutes() < 10 ? "0" + iliIill1.getMinutes() : iliIill1.getMinutes();
      $(".kui-time").text(IilliiII + ":" + I11Iiill);
      setTimeout(function () {
        XMlayEr.header.time();
      }, 1000);
      $(".header .qoe-normal").show();
    },
    qfe: function () {
      try {
        navigator.getBattery().then(function (l1iliIil) {
          let ililII1i = l1iliIil.level * 100 + "%";
          let IIlI1IIl = $(".percentage");
          ililII1i === "10%" ? IIlI1IIl.css({
            "background-color": "red",
            width: ililII1i
          }) : IIlI1IIl.css("width", ililII1i);
          $(".batteryShape").show();
          l1iliIil.addEventListener("levelchange", function () {
            this.qfe();
          });
        });
      } catch (lIli11ll) {
        console.log("该浏览器不支持电量显示");
      }
    },
    title: function (Il11Il1i) {
      $(".player-title").text(Il11Il1i);
      XMlayEr.header.onShowNameTipsMouseenter();
    },
    onShowNameTipsMouseenter: function () {
      let liil1ll = document.querySelector(".player-title");
      if (liil1ll.scrollWidth > liil1ll.offsetWidth) {
        function II1i1i1I() {
          liil1ll.innerHTML = liil1ll.innerHTML.slice(1) + liil1ll.innerHTML[0];
        }
        setInterval(II1i1i1I, 200);
      }
    }
  },
  subtitle: {
    hide: false,
    Init: function (lI1iilIi) {
      const lllIi1I1 = document.getElementsByTagName("video");
      const I1liliI = document.createElement("track");
      $(".content-bnt").click(function () {
        {
          $(".ec-subtitle").toggle();
          XMlayEr.subtitle.hide === false ? ($(this).css("opacity", "0.6"), XMlayEr.subtitle.hide = true) : ($(this).css("opacity", ""), XMlayEr.subtitle.hide = false);
        }
      });
      I1liliI.default = true;
      I1liliI.kind = "metadata";
      lllIi1I1[0].appendChild(I1liliI);
      fetch(lI1iilIi.url).then(iIliiIIl => iIliiIIl.arrayBuffer()).then(l1I1I11i => {
        const l1IillII = new TextDecoder(lI1iilIi.encoding).decode(l1I1I11i);
        switch (lI1iilIi.type || this.getExt(lI1iilIi.url)) {
          case "srt":
            return this.text.vttToBlob(this.text.srtToVtt(l1IillII));
          case "ass":
            return this.text.vttToBlob(this.text.assToVtt(l1IillII));
          case "vtt":
            return this.text.vttToBlob(l1IillII);
          default:
            return lI1iilIi.url;
        }
      }).then(llI111i1 => {
        {
          I1liliI.default = true;
          I1liliI.kind = "metadata";
          I1liliI.src = llI111i1.toString();
          I1liliI.track.mode = "hidden";
          I1liliI.addEventListener("cuechange", this.text.update);
        }
      }).catch(iIII1ilI => {
        {
          XMlayEr.tips.msg("字幕加载失败!!!");
          throw iIII1ilI;
        }
      });
    },
    text: {
      fixSrt: function (lIiIl) {
        return lIiIl.replace(/(\d\d:\d\d:\d\d)[,.](\d+)/g, (I1lIlii1, IiIli11, i1I1i1l) => {
          let lI1iIIIl = i1I1i1l.slice(0, 3);
          i1I1i1l.length === 1 && (lI1iIIIl = i1I1i1l + "00");
          i1I1i1l.length === 2 && (lI1iIIIl = i1I1i1l + "0");
          return IiIli11 + "," + lI1iIIIl;
        });
      },
      srtToVtt: function (illlIill) {
        return "WEBVTT \r\n\r\n".concat(this.fixSrt(illlIill).replace(/\{\\([ibu])\}/g, "</$1>").replace(/\{\\([ibu])1\}/g, "<$1>").replace(/\{([ibu])\}/g, "<$1>").replace(/\{\/([ibu])\}/g, "</$1>").replace(/(\d\d:\d\d:\d\d),(\d\d\d)/g, "$1.$2").replace(/{[\s\S]*?}/g, "").concat("\r\n\r\n"));
      },
      vttToBlob: function (l1l11lii) {
        return URL.createObjectURL(new Blob([l1l11lii], {
          type: "text/vtt"
        }));
      },
      assToVtt: function (lIl1i1i) {
        const i1ll111 = new RegExp("Dialogue:\\s\\d,(\\d+:\\d\\d:\\d\\d.\\d\\d),(\\d+:\\d\\d:\\d\\d.\\d\\d),([^,]*),([^,]*),(?:[^,]*,){4}([\\s\\S]*)$", "i");
        function ll1iiIi1(ll1I1I1i = "") {
          return ll1I1I1i.split(/[:.]/).map((llillili, I1IIi11, lliIi1iI) => {
            if (I1IIi11 === lliIi1iI.length - 1) {
              if (llillili.length === 1) {
                return "." + llillili + "00";
              }
              if (llillili.length === 2) {
                return "." + llillili + "0";
              }
            } else {
              if (llillili.length === 1) {
                return (I1IIi11 === 0 ? "0" : ":0") + llillili;
              }
            }
            return I1IIi11 === 0 ? llillili : I1IIi11 === lliIi1iI.length - 1 ? "." + llillili : ":" + llillili;
          }).join("");
        }
        return "WEBVTT\n\n" + lIl1i1i.split(/\r?\n/).map(Ili1I1il => {
          const il1IIilI = Ili1I1il.match(i1ll111);
          if (!il1IIilI) {
            return null;
          }
          return {
            start: ll1iiIi1(il1IIilI[1].trim()),
            end: ll1iiIi1(il1IIilI[2].trim()),
            text: il1IIilI[5].replace(/{[\s\S]*?}/g, "").replace(/(\\N)/g, "\n").trim().split(/\r?\n/).map(liilllll => liilllll.trim()).join("\n")
          };
        }).filter(lI1111i1 => lI1111i1).map((l11Ii1Il, liIlI11i) => {
          if (l11Ii1Il) {
            return liIlI11i + 1 + "\n" + l11Ii1Il.start + " --> " + l11Ii1Il.end + "\n" + l11Ii1Il.text;
          }
          return "";
        }).filter(iiIiI1Il => iiIiI1Il.trim()).join("\n\n");
      },
      update: function () {
        const I11l1iI = document.getElementsByTagName("video");
        const Iiiii1l = I11l1iI[0].textTracks[0].activeCues[0];
        const l1lIIiIi = document.querySelector(".ec-subtitle");
        l1lIIiIi.innerHTML = "";
        Iiiii1l && (l1lIIiIi.innerHTML = Iiiii1l.text.split(/\r?\n/).map(Il111III => "<p>" + function (lII1Ilil) {
          return lII1Ilil.replace(/[&<>'"]/g, l1I1lill => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            "'": "&#39;",
            "\"": "&quot;"
          })[l1I1lill] || l1I1lill);
        }(Il111III) + "</p>").join(""));
      }
    },
    getExt: function (IllIi1il) {
      return IllIi1il.includes("?") ? n(IllIi1il.split("?")[0]) : IllIi1il.includes("#") ? n(IllIi1il.split("#")[0]) : IllIi1il.trim().toLowerCase().split(".").pop();
    }
  },
  danMu: {
    dm_api: [],
    dan: [],
    time: "",
    danTunnel: {
      right: {},
      top: {},
      bottom: {}
    },
    container: null,
    paused: true,
    off: false,
    showing: true,
    speedRate: 0.2,
    unlimited: false,
    height: 15,
    opacity: 1,
    danIndex: 0,
    Init: function () {
      let llIil = $(".dm-box");
      this.off = true;
      this.api();
      this.container = document.querySelector(".ec-danMa");
      let IiIiilI = getComputedStyle(document.getElementsByClassName("ec-danMa")[0], null)["font-size"];
      let llIIlIII = IiIiilI.slice(0, -2);
      this.height = Number(llIIlIII) + 6;
      for (let l1il1Ii1 = [], lliliii = 0; lliliii < this.dm_api.length; ++lliliii) {
        this.apiBackend.read(this.dm_api[lliliii][2], function (IIiilili) {
          return function (l1lIiI, iillllI) {
            l1lIiI ? (l1lIiI.response, l1il1Ii1[IIiilili] = []) : (l1il1Ii1[IIiilili] = iillllI ? iillllI.map(function (i1IIIiIi) {
              {
                return {
                  time: i1IIIiIi[0],
                  type: i1IIIiIi[1],
                  color: i1IIIiIi[2],
                  author: i1IIIiIi[3],
                  text: i1IIIiIi[4].indexOf("777ys") != -1 ? "68yy.com 全网影视在线看🎬" : i1IIIiIi[4],
                  size: i1IIIiIi[7]
                };
              }
            }) : [], l1il1Ii1[IIiilili] = l1il1Ii1[IIiilili], XMlayEr.danMu.readAllEndpoints(l1il1Ii1));
          };
        }(lliliii));
      }
      this.content();
      false && $(".dm-input").attr({
        disabled: true,
        placeholder: "请先登录~"
      });
      XMlayEr.void.on("play", function () {
        XMlayEr.danMu.paused = false;
        $(".ec-danMa").addClass("dm-show");
      });
      XMlayEr.void.on("pause", function () {
        {
          XMlayEr.danMu.paused = true;
          $(".ec-danMa").removeClass("dm-show");
        }
      });
      switch ("1") {
        case "0":
          llIil.hide();
          break;
        case "2":
          llIil.hide();
          XMlayEr.void.on("fullscreen", function (IiiIii1) {
            IiiIii1 ? llIil.show() : llIil.hide();
          });
          break;
      }
      XMlayEr.void.on("seek", function () {
        XMlayEr.danMu.seek();
      });
    },
    api: function () {
      let iIi1IIi1 = XMlayEr.dmid;
      let lI11Ii1 = XMlayEr.ggdmapi ? "#1$" + XMlayEr.ggdmapi : "";
      let lli1l1il = "0$https://dmku.hls.one/?ac=dm" + lI11Ii1;
      let lIIlIII = lli1l1il.split("#");
      let I1I1lIlI = [];
      for (let Ii1li1i = 0; Ii1li1i < lIIlIII.length; Ii1li1i++) {
        let Il1IIill = lIIlIII[Ii1li1i].split("$");
        let l1lIl1ii = "";
        let l111l111 = "";
        switch (Il1IIill["0"]) {
          case "1":
            l111l111 = iIi1IIi1;
            break;
          default:
            l111l111 = iIi1IIi1;
            l1lIl1ii = "&id=" + l111l111;
            break;
        }
        I1I1lIlI[Ii1li1i] = [Il1IIill["0"], Il1IIill["1"], Il1IIill["1"] + l1lIl1ii, l111l111];
      }
      this.dm_api = I1I1lIlI;
    },
    apiBackend: {
      read: function (I11iiiII, lil1Ii1i) {
        this.api(I11iiiII, null, function (I1IllIiI, Ill1Il1I) {
          {
            lil1Ii1i(null, Ill1Il1I.danmuku);
          }
        }, function (iI1Iiii1, il111Iil) {
          lil1Ii1i({
            status: iI1Iiii1.status,
            response: il111Iil
          });
        }, function (ll1iliIi) {
          {
            lil1Ii1i({
              status: ll1iliIi.status,
              response: null
            });
          }
        });
      },
      send: function (l1IIIIiI, iIl1iliI) {
        this.api(XMlayEr.danMu.dm_api[0][1], l1IIIIiI, function () {
          {
            console.log("发送弹幕成功");
            XMlayEr.tips.msg("您的弹幕已送达");
            iIl1iliI(l1IIIIiI);
          }
        }, function (lii1IIII, l11i111I) {
          XMlayEr.tips.msg(l11i111I.msg);
        }, function (l1lllI) {
          console.log("Request was unsuccessful: " + l1lllI.status);
        });
      },
      api: function (IlI1lll, IIl1i11l, llIIl11, l1Ii1ll, l11lIiIi) {
        let li1IIIil = new XMLHttpRequest();
        li1IIIil.onreadystatechange = function () {
          if (4 === li1IIIil.readyState) {
            if (li1IIIil.status >= 200 && li1IIIil.status < 300 || 304 === li1IIIil.status) {
              let iliiIi11 = JSON.parse(li1IIIil.responseText);
              return 23 !== iliiIi11.code ? l1Ii1ll(li1IIIil, iliiIi11) : llIIl11(li1IIIil, iliiIi11);
            }
            l11lIiIi(li1IIIil);
          }
        };
        li1IIIil.open(null !== IIl1i11l ? "POST" : "GET", IlI1lll, true);
        li1IIIil.send(null !== IIl1i11l ? JSON.stringify(IIl1i11l) : null);
      }
    },
    readAllEndpoints: function (iII111Ii) {
      let l1lI1i1I = this;
      l1lI1i1I.dan = [].concat.apply([], iII111Ii).sort(function (Il1I111i, Ii1ii1II) {
        return Il1I111i.time - Ii1ii1II.time;
      });
      window.requestAnimationFrame(function () {
        l1lI1i1I.frame();
      });
    },
    frame: function () {
      if (this.dan.length && !XMlayEr.danMu.paused && this.showing) {
        {
          let lIii1ili = this.dan[this.danIndex];
          const lIiIIIlI = [];
          while (lIii1ili && XMlayEr.void.video.currentTime > parseFloat(lIii1ili.time)) {
            lIiIIIlI.push(lIii1ili);
            lIii1ili = this.dan[++this.danIndex];
          }
          this.draw(lIiIIIlI);
        }
      }
      window.requestAnimationFrame(() => {
        this.frame();
      });
    },
    number2Color: function (l1l1lIlI) {
      return "#" + ("00000" + l1l1lIlI.toString()).slice(-6);
    },
    number2Type: function (II1ii1l) {
      switch (II1ii1l) {
        case 0:
        case "right":
          return "right";
        case 1:
        case "top":
          return "top";
        case 2:
        case "bottom":
          return "bottom";
        default:
          return "right";
      }
    },
    _measure: function (l11IlIl) {
      if (!this.context) {
        const l1I1l1ii = getComputedStyle(this.container.getElementsByClassName("ec-danMa-item")[0], null);
        this.context = document.createElement("canvas").getContext("2d");
        this.context.font = l1I1l1ii.getPropertyValue("font");
      }
      return this.context.measureText(l11IlIl).width;
    },
    _danAnimation: function (iIIllI11) {
      const iIIll11l = this.speedRate || 1;
      const IliIl11I = !!XMlayEr.void.fullscreen;
      const IlI11il = {
        top: (IliIl11I ? 6 : 4) / iIIll11l + "s",
        right: (IliIl11I ? 8 : 5) / iIIll11l + "s",
        bottom: (IliIl11I ? 6 : 4) / iIIll11l + "s"
      };
      return IlI11il[iIIllI11];
    },
    seek: function () {
      if (!this.off) {
        return;
      }
      this.clear();
      for (let lIIli11l = 0; lIIli11l < this.dan.length; lIIli11l++) {
        {
          if (this.dan[lIIli11l].time >= XMlayEr.void.video.currentTime) {
            this.danIndex = lIIli11l;
            break;
          }
          this.danIndex = this.dan.length;
        }
      }
    },
    clear: function () {
      this.danTunnel = {
        right: {},
        top: {},
        bottom: {}
      };
      this.danIndex = 0;
      this.container.innerHTML = "<div class=\"ec-danMa-item ec-danMa-item--demo\"></div>";
    },
    draw: function (I1I1iIii) {
      if (this.showing) {
        const i1IlI1ii = this.height;
        const iIilii1l = this.container.offsetWidth;
        const IiliIiii = this.container.offsetHeight;
        const llliii1l = parseInt(IiliIiii) / parseInt(i1IlI1ii);
        const i1iii1Il = liIIil1i => {
          const lIIl1Il1 = liIIil1i.offsetWidth || parseInt(liIIil1i.style.width);
          const lllilli = liIIil1i.getBoundingClientRect().right || this.container.getBoundingClientRect().right + lIIl1Il1;
          return this.container.getBoundingClientRect().right - lllilli;
        };
        const Ii1i1Iil = II1il1I1 => (iIilii1l + II1il1I1) / 5;
        const iillI1Il = (i11lIIll, lll11l11, IiI1I11l) => {
          const lllI1111 = iIilii1l / Ii1i1Iil(IiI1I11l);
          for (let il1III1 = 0; this.unlimited || il1III1 < llliii1l; il1III1++) {
            const iIIiIi1l = this.danTunnel[lll11l11][il1III1 + ""];
            if (iIIiIi1l && iIIiIi1l.length) {
              {
                if (lll11l11 !== "right") {
                  continue;
                }
                for (let l1il = 0; l1il < iIIiIi1l.length; l1il++) {
                  {
                    const I11lIII = i1iii1Il(iIIiIi1l[l1il]) - 10;
                    if (I11lIII <= iIilii1l - lllI1111 * Ii1i1Iil(parseInt(iIIiIi1l[l1il].style.width)) || I11lIII <= 0) {
                      break;
                    }
                    if (l1il === iIIiIi1l.length - 1) {
                      this.danTunnel[lll11l11][il1III1 + ""].push(i11lIIll);
                      i11lIIll.addEventListener("animationend", () => {
                        this.danTunnel[lll11l11][il1III1 + ""].splice(0, 1);
                      });
                      return il1III1 % llliii1l;
                    }
                  }
                }
              }
            } else {
              this.danTunnel[lll11l11][il1III1 + ""] = [i11lIIll];
              i11lIIll.addEventListener("animationend", () => {
                this.danTunnel[lll11l11][il1III1 + ""].splice(0, 1);
              });
              return il1III1 % llliii1l;
            }
          }
          return -1;
        };
        Object.prototype.toString.call(I1I1iIii) !== "[object Array]" && (I1I1iIii = [I1I1iIii]);
        const llllI1li = document.createDocumentFragment();
        for (let IIII1il = 0; IIII1il < I1I1iIii.length; IIII1il++) {
          I1I1iIii[IIII1il].type = this.number2Type(I1I1iIii[IIII1il].type);
          !I1I1iIii[IIII1il].color && (I1I1iIii[IIII1il].color = 16777215);
          const IlIIli1I = document.createElement("div");
          IlIIli1I.classList.add("ec-danMa-item");
          IlIIli1I.classList.add("ec-danMa-" + I1I1iIii[IIII1il].type);
          I1I1iIii[IIII1il].border ? IlIIli1I.innerHTML = "<span style=\"border:" + I1I1iIii[IIII1il].border + "\">" + I1I1iIii[IIII1il].text + "</span>" : IlIIli1I.innerHTML = I1I1iIii[IIII1il].text;
          IlIIli1I.style.opacity = this.opacity;
          IlIIli1I.style.color = this.number2Color(I1I1iIii[IIII1il].color);
          IlIIli1I.addEventListener("animationend", () => {
            this.container.removeChild(IlIIli1I);
          });
          const I1I1Il1l = this._measure(I1I1iIii[IIII1il].text);
          let l1IlI1li;
          switch (I1I1iIii[IIII1il].type) {
            case "right":
              l1IlI1li = iillI1Il(IlIIli1I, I1I1iIii[IIII1il].type, I1I1Il1l);
              l1IlI1li >= 0 && (IlIIli1I.style.width = I1I1Il1l + 1 + "px", IlIIli1I.style.top = i1IlI1ii * l1IlI1li + "px");
              break;
            case "top":
              l1IlI1li = iillI1Il(IlIIli1I, I1I1iIii[IIII1il].type);
              l1IlI1li >= 0 && (IlIIli1I.style.top = i1IlI1ii * l1IlI1li + "px");
              break;
            case "bottom":
              l1IlI1li = iillI1Il(IlIIli1I, I1I1iIii[IIII1il].type);
              l1IlI1li >= 0 && (IlIIli1I.style.bottom = i1IlI1ii * l1IlI1li + "px");
              break;
            default:
              XMlayEr.tips.msg("Can't handled danMa type: " + I1I1iIii[IIII1il].type);
          }
          l1IlI1li >= 0 && (IlIIli1I.classList.add("ec-danMa-move"), IlIIli1I.style.animationDuration = this._danAnimation(I1I1iIii[IIII1il].type), llllI1li.appendChild(IlIIli1I));
        }
        this.container.appendChild(llllI1li);
        return llllI1li;
      }
    },
    htmlEncode: function (iiiIII11) {
      return iiiIII11.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#x27;").replace(/\//g, "&#x2f;");
    },
    hide: function () {
      this.showing = false;
      this.clear();
    },
    show: function () {
      this.seek();
      this.showing = true;
    },
    send: function (II1II1lI) {
      var I1liIliI = document.referrer;
      I1liIliI == "" && (I1liIliI = document.URL);
      const IIiIilIl = {
        text: II1II1lI.text,
        color: II1II1lI.color,
        type: II1II1lI.type,
        time: XMlayEr.void.video.currentTime,
        player: XMlayEr.danMu.dm_api[0][3],
        size: "32px",
        referer: I1liIliI
      };
      this.apiBackend.send(IIiIilIl, function (lI111lI1) {
        XMlayEr.danMu.dan.splice(this.danIndex, 0, lI111lI1);
        XMlayEr.danMu.danIndex++;
        const iiI1ilII = {
          text: XMlayEr.danMu.htmlEncode(lI111lI1.text),
          color: lI111lI1.color,
          type: lI111lI1.type,
          border: "2px solid #24a5ff"
        };
        XMlayEr.danMu.draw(iiI1ilII);
        let I1l1liii = $(".dm-input");
        I1l1liii.val("");
        let iI1l1Iii = setInterval(function () {
          {
            let i1lliiIi = Number(I1l1liii.data("time")) - 1;
            I1l1liii.data("time", i1lliiIi).attr("placeholder", i1lliiIi + "s后解除冻结").attr("disabled", true);
            i1lliiIi <= 0 && (I1l1liii.data("time", 10).attr("placeholder", "来发个弹幕吧~").attr("disabled", false), clearInterval(iI1l1Iii));
          }
        }, 1000);
      });
    },
    getFontSize: function (lIiiilii) {
      const i1IIl1i1 = function (iliIIIl, I1iI1iiI, ll11lIl) {
        {
          return Math.max(Math.min(iliIIIl, Math.max(I1iI1iiI, ll11lIl)), Math.min(I1iI1iiI, ll11lIl));
        }
      };
      const lII111i = document.getElementById("player").clientWidth;
      if (typeof lIiiilii === "number") {
        return i1IIl1i1(lIiiilii, 12, lII111i);
      }
      if (typeof lIiiilii === "string" && lIiiilii.endsWith("%")) {
        const iiIiIlI1 = parseFloat(lIiiilii) / 100;
        return i1IIl1i1(lII111i * iiIiIlI1, 12, lII111i);
      }
      return lIiiilii;
    },
    set: function (I11lii1l, il1i1iI1, I1IIIi1) {
      I1IIIi1 && XMlayEr.cookie.Set("d_set" + I11lii1l, [I11lii1l, il1i1iI1, I1IIIi1], 7);
      switch (I11lii1l) {
        case 1:
          {
            {
              this.speedRate = il1i1iI1;
              break;
            }
          }
        case 2:
          {
            {
              let ii1I11Ii = this.getFontSize(il1i1iI1);
              $(".ec-danMa").css("font-size", ii1I11Ii);
              this.height = ii1I11Ii + 5;
              break;
            }
          }
        case 3:
          {
            this.opacity = il1i1iI1;
            break;
          }
        case 4:
          {
            $(".ec-danMa").css("bottom", il1i1iI1);
            break;
          }
        default:
          break;
      }
    },
    content: function () {
      $(".dm-bnt").click(function () {
        $(".art-bottom").hide();
        $(".dm-box").removeClass("dm-wap");
        $(".player-list-off").addClass("dm-off").removeClass("off");
        $(".dm-off").click(function () {
          $(".art-bottom").show();
          $(".dm-box").addClass("dm-wap");
          $(".player-list-off").removeClass("dm-off").addClass("off");
        });
      });
      $(".art-bottom,.dm-box-cc").click(function () {
        $(".dm-set-box,.dm-style-box").removeClass("ec-show");
      });
      let ll1illIi = $(".dm-box-cc");
      let iIlIiil1 = XMlayEr.cookie.Get("dm-box-cc");
      let iI1II1i = XMlayEr.cookie.Get("content_dmP-1");
      let i1I1I = XMlayEr.cookie.Get("content_dmP-2");
      let iI1iIlii = $(".content_dmP-1 .item");
      let Ii11I11l = $(".content_dmP-2 .item");
      let liIlIIIi = function (lI1ll1iI, ii1iII1, i1liiiii) {
        (lI1ll1iI !== undefined || lI1ll1iI !== "") && ii1iII1.eq(lI1ll1iI).addClass("on-1").siblings().removeClass("on-1");
        ii1iII1.click(function () {
          {
            $(this).addClass("on-1").siblings().removeClass("on-1");
            XMlayEr.cookie.Set(i1liiiii, $("." + i1liiiii + " .item").index(this), 7);
          }
        });
      };
      liIlIIIi(iI1II1i, iI1iIlii, "content_dmP-1");
      liIlIIIi(i1I1I, Ii11I11l, "content_dmP-2");
      $(".dm-box-t-img").click(function () {
        {
          $(".dm-set-box").removeClass("ec-show");
          $(".dm-style-box").toggleClass("ec-show");
        }
      });
      let i1Ii1l1l = function () {
        let liIIIlII = $(".content_dmP-2 .on-1").data("color");
        let IlIi1iII = $(".content_dmP-1 .on-1").data("type");
        let li11llli = $(".dm-input").val();
        if (XMlayEr.empty(li11llli)) {
          XMlayEr.tips.msg("要输入弹幕内容啊喂");
        } else {
          li11llli.length > 22 ? XMlayEr.tips.msg("弹幕内容长度最大30位!!!") : XMlayEr.danMu.send({
            text: li11llli,
            color: liIIIlII,
            type: IlIi1iII
          });
        }
      };
      $(".dm-input").keydown(function (l1Ii1lI1) {
        l1Ii1lI1.keyCode === 13 && i1Ii1l1l();
      });
      $(".dm-send").click(function () {
        i1Ii1l1l();
      });
      iIlIiil1 === "1" && (XMlayEr.danMu.hide(), ll1illIi.addClass("dm-box-cc2").data("id", "1"));
      ll1illIi.click(function () {
        $(this).data("id") === "1" ? (XMlayEr.danMu.show(), XMlayEr.cookie.Del("dm-box-cc"), $(this).removeClass("dm-box-cc2").data("id", "0")) : (XMlayEr.danMu.hide(), XMlayEr.cookie.Set("dm-box-cc", "1", 7), $(this).addClass("dm-box-cc2").data("id", "1"));
      });
      let IIlIllil = [["弹幕速度", "极慢", "较慢", "适中", "极快", "较快"], ["字体大小", "默认", "极小", "较小", "适中", "较大", "极大"], ["不透明度", "100%", "75%", "50%", "25%", "0%"], ["弹幕范围", "1/4", "半屏", "3/4"]];
      let li1l1li1 = [["", "0.5", "0.8", "1", "1.5", "2"], ["", XMlayEr.danMu.height, "1%", "2%", "3%", "4%", "5%"], ["", "1", "0.75", "0.5", "0.25", "0"], ["", "60%", "45%", "10%"]];
      $(".set-toggle").append("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 32 32\"><path d=\"M22 16l-10.105-10.6-1.895 1.987 8.211 8.613-8.211 8.612 1.895 1.988 8.211-8.613z\"></path></svg>");
      let l1l1lIIl = "";
      let iIiiiIl1 = null;
      for (let Iiiii1li = 0; Iiiii1li < IIlIllil.length; Iiiii1li++) {
        let I1Ii1il1 = "";
        for (let iIl11ii1 = 0; iIl11ii1 < IIlIllil[Iiiii1li].length; iIl11ii1++) {
          iIl11ii1 === 0 ? I1Ii1il1 = I1Ii1il1 + "<div class=\"flex between br\"><span class=\"dm-set-label flex\"><i><svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 32 32\"><path d=\"M22 16l-10.105-10.6-1.895 1.987 8.211 8.613-8.211 8.612 1.895 1.988 8.211-8.613z\"></path></svg></i>" + IIlIllil[Iiiii1li][iIl11ii1] + "</span></div>" : I1Ii1il1 = I1Ii1il1 + "<div class=\"flex between dm-n2\" data-time=\"" + li1l1li1[Iiiii1li][iIl11ii1] + "\"><span class=\"dm-set-label flex\"><i></i>" + IIlIllil[Iiiii1li][iIl11ii1] + "</span></div>";
        }
        l1l1lIIl = l1l1lIIl + "<div class=\"dm-set-list\">" + I1Ii1il1 + "</div>";
        let l1lIIli1 = XMlayEr.cookie.Get("d_set" + (Iiiii1li + 1));
        if (l1lIIli1) {
          {
            let lI1li11 = l1lIIli1.split(",");
            XMlayEr.danMu.set(Number(lI1li11[0]), lI1li11[1]);
            $(".dm-set-box .dm-set-list").eq(0).children().eq(Iiiii1li).find("span").text(lI1li11[2]);
          }
        }
      }
      $(".dm-set-box").append(l1l1lIIl);
      $(".dm-box-set").click(function () {
        $(".dm-style-box").removeClass("ec-show");
        $(".dm-set-box").toggleClass("ec-show");
      });
      $("#dm_n1 .between").click(function () {
        let il1lllii = $(this).data("id");
        $(".dm-set-box .dm-set-list").eq(il1lllii).addClass("ds-set-show").siblings().removeClass("ds-set-show");
        iIiiiIl1 = il1lllii;
      });
      $(".dm-set-box .br").click(function () {
        {
          $(".dm-set-box .dm-set-list").eq(0).addClass("ds-set-show").siblings().removeClass("ds-set-show");
        }
      });
      $(".dm-n2").click(function () {
        let I1Iillli = $(this).text();
        let ll1i1IIl = $(".dm-set-box .dm-set-list");
        ll1i1IIl.eq(0).children().eq(iIiiiIl1 - 1).find("span").text(I1Iillli);
        ll1i1IIl.eq(0).addClass("ds-set-show").siblings().removeClass("ds-set-show");
        let Ii1il11I = $(this).data("time");
        I1Iillli !== "默认" ? XMlayEr.danMu.set(iIiiiIl1, Ii1il11I, I1Iillli) : XMlayEr.cookie.Del("d_set2");
      });
    }
  },
  list: {
    html: function () {
      if (XMlayEr.listapi) {
        let lliIiii1 = "<div class=\"art-control yxq-vod-list\" data-index=\"50\"><i class=\"art-icon hint--rounded hint--top\" aria-label=\"选集\"><svg t=\"1697209271632\" class=\"icon\" viewBox=\"0 0 1024 1024\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" p-id=\"12264\" width=\"18\" height=\"18\"><path d=\"M62 152h105.356v105.356h-105.356v-105.356zM263.937 152h698.063v105.356h-698.063v-105.356zM62 459.237h105.356v105.356h-105.356v-105.356zM263.937 459.237h698.063v105.356h-698.063v-105.356zM62 766.644h105.356v105.356h-105.356v-105.356zM263.937 766.644h698.063v105.356h-698.063v-105.356z\" p-id=\"12265\" fill=\"#ffffff\"></path></svg></i></div>";
        $(".art-control-playAndPause").after(lliIiii1);
        $(".yxq-vod-list").click(function () {
          XMlayEr.VodList.initial();
        });
      }
    },
    next: function () {
      if (XMlayEr.next0 || XMlayEr.next) {
        {
          let l1liI11I = "<div class=\"art-control ec-next\" data-index=\"40\"><i class=\"art-icon hint--rounded hint--top\" aria-label=\"下一集\"><svg t=\"1697202769049\" class=\"icon\" viewBox=\"0 0 1024 1024\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" p-id=\"4237\" width=\"41\" height=\"41\"><path d=\"M853.333333 204.8h-68.266666c-20.48 0-34.133333 13.653333-34.133334 34.133333v546.133334c0 17.066667 17.066667 34.133333 34.133334 34.133333h68.266666c20.48 0 34.133333-13.653333 34.133334-34.133333V238.933333c0-20.48-17.066667-34.133333-34.133334-34.133333zM614.4 467.626667L256 235.52C208.213333 204.8 170.666667 228.693333 170.666667 283.306667v484.693333c0 58.026667 37.546667 78.506667 85.333333 47.786667l358.4-238.933334c47.786667-30.72 47.786667-78.506667 0-109.226666z\" fill=\"#ffffff\" p-id=\"4238\"></path></svg></i></div>";
          $(".art-control-playAndPause").after(l1liI11I);
          $(".ec-next").click(function () {
            {
              XMlayEr.next0 ? top.location.href = "/?url=" + XMlayEr.next0 : self.location.href = "/?url=" + XMlayEr.next;
            }
          });
        }
      }
    },
    autoNext: function () {
      XMlayEr.void.on("video:ended", function () {
        if (!!XMlayEr.next0 || !!XMlayEr.next) {
          {
            box.children().append("<div class=\"pop-msg vague2 again\"><div class=\"again-icon\"><svg viewBox=\"0 0 1024 1024\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M1007.4674 42.036669c-12.751909-12.751909-38.255728-12.751909-51.007638 0l-95.63932 95.63932c-57.383592-57.383592-133.895048-95.63932-210.406505-121.143139C376.247886-53.602651 95.70588 105.796216 19.194424 373.586313c-76.511456 274.166051 82.887411 554.708057 350.677507 631.219513 274.166051 76.511456 554.708057-82.887411 631.219514-350.677507 12.751909-38.255728-12.751909-76.511456-51.007638-89.263366s-76.511456 12.751909-89.263365 51.007637c-25.503819 89.263366-89.263366 165.774822-165.774822 216.78246-172.150776 102.015275-395.30919 38.255728-497.324465-133.895049-82.887411-140.271003-63.759547-312.421779 44.631683-433.564918 133.895048-146.646958 369.805371-159.398867 516.452329-19.127864l-114.767184 114.767184c-6.375955 6.375955-6.375955 12.751909-6.375955 19.127864 0 19.127864 19.127864 38.255728 38.255728 38.255728h312.42178c12.751909 0 31.879773-12.751909 31.879773-31.879773V67.540488c0-6.375955-6.375955-12.751909-12.751909-25.503819z\"></path></svg></div><div class=\"pop-content\"><span id=\"count2\">3</span>s后自动播放下一集</div></div>");
            $(".pause-ad").remove();
            let iilllII1 = setTimeout(function () {
              XMlayEr.next0 ? top.location.href = XMlayEr.next0 : self.location.href = "/?url=" + XMlayEr.next;
            }, 3000);
            $(".again").click(function () {
              {
                clearTimeout(iilllII1);
                $(".again").remove();
                XMlayEr.void.play();
              }
            });
            XMlayEr.void.on("play", function () {
              clearTimeout(iilllII1);
              $(".again").remove();
            });
          }
        }
      });
    }
  },
  broadside: function () {
    let li1I11ll = $(".broadside");
    li1I11ll.append("<div class=\"ec-lock\" data-id=\"1\"><svg viewBox=\"0 0 1024 1024\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M800 448H704V320c0-106.4-85.6-192-192-192S320 213.6 320 320h64c0-70.4 57.6-128 128-128s128 57.6 128 128v128H224c-17.6 0-32 14.4-32 32v384c0 17.6 14.4 32 32 32h576c17.6 0 32-14.4 32-32V480c0-17.6-14.4-32-32-32zM512 736c-35.2 0-64-28.8-64-64s28.8-64 64-64 64 28.8 64 64-28.8 64-64 64z\"></path></svg></div>");
    let i11Iii1I = $(".ec-lock");
    i11Iii1I.click(function () {
      Number(i11Iii1I.data("id")) === 1 ? (i11Iii1I.html("<svg viewBox=\"0 0 1024 1024\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M800 448H704V320c0-106.4-85.6-192-192-192S320 213.6 320 320v128H224c-17.6 0-32 14.4-32 32v384c0 17.6 14.4 32 32 32h576c17.6 0 32-14.4 32-32V480c0-17.6-14.4-32-32-32zM512 736c-35.2 0-64-28.8-64-64s28.8-64 64-64 64 28.8 64 64-28.8 64-64 64z m128-288H384V320c0-70.4 57.6-128 128-128s128 57.6 128 128v128z\"></path></svg>").data("id", "2"), box.addClass("lock-hide")) : (i11Iii1I.html("<svg viewBox=\"0 0 1024 1024\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M800 448H704V320c0-106.4-85.6-192-192-192S320 213.6 320 320h64c0-70.4 57.6-128 128-128s128 57.6 128 128v128H224c-17.6 0-32 14.4-32 32v384c0 17.6 14.4 32 32 32h576c17.6 0 32-14.4 32-32V480c0-17.6-14.4-32-32-32zM512 736c-35.2 0-64-28.8-64-64s28.8-64 64-64 64 28.8 64 64-28.8 64-64 64z\"></path></svg>").data("id", "1"), box.removeClass("lock-hide"));
    });
    li1I11ll.append("<div class=\"ec-change\"><svg viewBox=\"0 0 1024 1024\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M480.5 251.2c13-1.6 25.9-2.4 38.8-2.5v63.9c0 6.5 7.5 10.1 12.6 6.1L660 217.6c4-3.2 4-9.2 0-12.3l-128-101c-5.1-4-12.6-0.4-12.6 6.1l-0.2 64c-118.6 0.5-235.8 53.4-314.6 154.2-69.6 89.2-95.7 198.6-81.1 302.4h74.9c-0.9-5.3-1.7-10.7-2.4-16.1-5.1-42.1-2.1-84.1 8.9-124.8 11.4-42.2 31-81.1 58.1-115.8 27.2-34.7 60.3-63.2 98.4-84.3 37-20.6 76.9-33.6 119.1-38.8zM880 418H352c-17.7 0-32 14.3-32 32v414c0 17.7 14.3 32 32 32h528c17.7 0 32-14.3 32-32V450c0-17.7-14.3-32-32-32z m-44 402H396V494h440v326z\"></path></svg></div>");
    let i111iIli = 0;
    let lIi1l1II = $("video");
    $(".ec-change").click(function () {
      switch (i111iIli) {
        case 0:
          lIi1l1II.addClass("along1");
          ++i111iIli;
          break;
        case 1:
          lIi1l1II.removeClass("along1");
          ++i111iIli;
          lIi1l1II.addClass("along2");
          break;
        case 2:
          lIi1l1II.removeClass("along2");
          ++i111iIli;
          lIi1l1II.addClass("along3");
          break;
        case 3:
          lIi1l1II.removeClass("along3");
          i111iIli = 0;
          break;
      }
    });
    li1I11ll.append("<div class=\"ec-pip\" data-id=\"1\"><svg viewBox=\"0 0 1024 1024\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M849.5 174.5a37.50000029 37.50000029 0 0 1 37.50000029 37.50000029v262.49999942h-75.00000058V249.49999971H212.00000029v525.00000058h225v74.99999971H174.5a37.50000029 37.50000029 0 0 1-37.50000029-37.50000029V212.00000029a37.50000029 37.50000029 0 0 1 37.50000029-37.50000029h675z m0 375.00000029a37.50000029 37.50000029 0 0 1 37.50000029 37.49999942v225a37.50000029 37.50000029 0 0 1-37.50000029 37.50000029h-299.99999971a37.50000029 37.50000029 0 0 1-37.50000029-37.50000029v-225a37.50000029 37.50000029 0 0 1 37.50000029-37.49999942h299.99999971z\"></path></svg></div>");
    let iiiiilIi = $("video")[0];
    $(".ec-pip").click(async () => {
      {
        try {
          {
            if (document.pictureInPictureEnabled && !iiiiilIi.disablePictureInPicture) {
              document.pictureInPictureElement ? await document.exitPictureInPicture() : await iiiiilIi.requestPictureInPicture();
            } else {
              iiiiilIi.webkitSupportsPresentationMode && typeof iiiiilIi.webkitSetPresentationMode === "function" ? iiiiilIi.webkitSetPresentationMode(iiiiilIi.webkitPresentationMode === "picture-in-picture" ? "inline" : "picture-in-picture") : $(".ec-pip").hide();
            }
          }
        } catch (iiII1l1I) {
          $(".ec-pip").hide();
          throw iiII1l1I;
        }
      }
    });
  },
  secondToTime: function (l1iiilI) {
    const ii1llii1 = II1i111i => II1i111i < 10 ? "0" + II1i111i : String(II1i111i);
    const iill1Ii1 = Math.floor(l1iiilI / 3600);
    const lllIlIiI = Math.floor((l1iiilI - iill1Ii1 * 3600) / 60);
    const illiIil1 = Math.floor(l1iiilI - iill1Ii1 * 3600 - lllIlIiI * 60);
    return (iill1Ii1 > 0 ? [iill1Ii1, lllIlIiI, illiIil1] : [lllIlIiI, illiIil1]).map(ii1llii1).join(":");
  },
  VodList: {
    initial: iIli1Iii => {
      if ($(".yxq-listbox").length < 1) {
        {
          let Ili1lI1 = $(".art-video-player");
          Ili1lI1.prepend("<div class=\"vodlist-of danmu-hide\" style=\"display: none;\"></div><div class=\"yxq-listbox\"><div class=\"anthology-wrap\"></div></div></div>");
        }
      }
      $(document).on("click", ".vodlist-of", function () {
        XMlayEr.VodList.Off();
      });
      if ($(".normal-title-wrap").length < 1) {
        {
          let lil1I1l1 = $(".anthology-wrap");
          const lI1lI11 = Date.now();
          const i1lIili = url || "";
          const lI1I11Il = sign(hex_md5(lI1lI11 + url));
          $.ajaxSettings.timeout = "10000";
          $.ajaxSettings.async = true;
          $.post(XMlayEr.listapi, {
            time: lI1lI11,
            url: i1lIili,
            token: lI1I11Il
          }, function (llliI1) {
            if (llliI1.code == 200) {
              const IllliliI = XMlayEr.decrypt(llliI1.html);
              lil1I1l1.html(IllliliI);
            } else {
              XMlayEr.VodList.Off();
              XMlayEr.tips.msg("未获取到选集数据！");
            }
          }, "json").error(function (iIiI1IIl, lIIliiiI, II1iiIIi) {
            {
              XMlayEr.VodList.Off();
              XMlayEr.tips.msg("选集接口出现异常！");
            }
          });
        }
      }
    },
    Off: () => {
      $(".vodlist-of,.r-button").hide();
      $(".yxq-listbox").removeClass("yxq-stting");
    },
    Tab: () => {
      $(".yxq-list").toggle();
      XMlayEr.VodList.TabList();
    },
    TabList: () => {
      $(".yxq-list a").click(function () {
        $(this).addClass("yxq-this").siblings().removeClass("yxq-this");
        let i1IiilII = $(".yxq-list a").index(this);
        let III1IIii = $(".scroll-area .yxq-selset-list").eq(i1IiilII);
        III1IIii.addClass("yxq-show").siblings().removeClass("yxq-show");
        $(".yxq-list").hide();
      });
    },
    Next: llI1IIl1 => {
      console.log(llI1IIl1);
      self.location.href = llI1IIl1;
    }
  },
  LoadAnimation: function () {
    $("#loading").hide();
    let IIlIlIi = Number(XMlayEr.cookie.Get(url, 2));
    let ilIii1Il = XMlayEr.secondToTime(IIlIlIi);
    if (ilIii1Il !== "00:00" && ilIii1Il !== "NaN:NaN") {
      {
        $(".ec-remember").html("<i class=\"art-icon art-icon-close s-on\"><svg viewBox=\"0 0 1024 1024\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"m571.733 512 268.8-268.8c17.067-17.067 17.067-42.667 0-59.733-17.066-17.067-42.666-17.067-59.733 0L512 452.267l-268.8-268.8c-17.067-17.067-42.667-17.067-59.733 0-17.067 17.066-17.067 42.666 0 59.733l268.8 268.8-268.8 268.8c-17.067 17.067-17.067 42.667 0 59.733 8.533 8.534 19.2 12.8 29.866 12.8s21.334-4.266 29.867-12.8l268.8-268.8 268.8 268.8c8.533 8.534 19.2 12.8 29.867 12.8s21.333-4.266 29.866-12.8c17.067-17.066 17.067-42.666 0-59.733L571.733 512z\"></path></svg></i>上次看到<em>" + ilIii1Il + "</em><span class=\"t-color\">继续上次播放</span>").show();
        $(".ec-remember span").click(function () {
          $(".ec-remember").html("<p></p>").hide();
          setTimeout(() => {
            XMlayEr.void.currentTime = IIlIlIi;
          }, 500);
        });
        $(".ec-remember svg").click(function () {
          {
            $(".ec-remember").html("<p></p>").hide();
          }
        });
        let llIiilIi = setTimeout(function () {
          $(".ec-remember").html("<p></p>").hide();
          clearTimeout(llIiilIi);
        }, 6000);
      }
    }
  }
};
function getCurrentDate() {
  const I1iii1iI = new Date();
  const i1iiliii = I1iii1iI.getFullYear();
  const ll11lIii = String(I1iii1iI.getMonth() + 1).padStart(2, "0");
  const iII11I11 = String(I1iii1iI.getDate()).padStart(2, "0");
  return i1iiliii + "-" + ll11lIii + "-" + iII11I11;
}
document.addEventListener("DOMContentLoaded", function () {
  const lIliiiIi = "XMFLV";
  const II1lliI = getCurrentDate();
  const lIillI1i = localStorage.getItem(lIliiiIi);
  url === "" || url === "undefined" || url === "null" ? XMlayEr.error("请填入视频URL地址！<br><br>本接口仅供学习与交流、请勿用于非法用途") : lIillI1i === II1lliI ? (textElement.classList.remove("center-container"), textElement.classList.add("mov"), playVideo(), textElement.addEventListener("click", playVideo)) : textElement.addEventListener("click", function () {
    playVideo();
    localStorage.setItem(lIliiiIi, II1lliI);
  });
});
var OriginTitile = document.title;
var titleTime;
document.addEventListener("visibilitychange", function () {
  document.hidden ? (document.title = "o(╥﹏╥)o你去哪了？快回来！- " + OriginTitile, clearTimeout(titleTime)) : (document.title = "๑乛◡乛๑亲爱的，欢迎回来~• - " + OriginTitile, titleTime = setTimeout(function () {
    document.title = OriginTitile;
  }, 1500));
});