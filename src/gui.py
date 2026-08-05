from src import *
from src.utils.files import files
from src.utils.config import get, configcls
from src.utils.logging import logger

html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Discord Reaper</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;scrollbar-width:none;-ms-overflow-style:none}
*::-webkit-scrollbar{display:none}
:root{
  --bg:#0a0a0c;--sb:#0d0d10;--sf:#131316;--sf2:#18181c;
  --bd:rgba(255,255,255,.06);--bd2:rgba(255,255,255,.10);
  --acc:#ff1f3d;--acc-g:rgba(255,31,61,.18);--acc-d:rgba(255,31,61,.09);
  --tx:#f0e8e8;--tx2:rgba(240,232,232,.40);--tx3:rgba(240,232,232,.18);
  --green:#1fd97a;--red:#ff4455;--yellow:#f5c040;--orange:#ff8844;--cyan:#00d0f0;
}
html,body{width:100%;height:100%;overflow:hidden;background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;-webkit-font-smoothing:antialiased;font-size:13px;user-select:none}

/* ── titlebar ── */
#tb{position:fixed;top:0;left:0;right:0;height:36px;z-index:200;display:flex;align-items:center;padding:0 14px;cursor:default;user-select:none;background:var(--sb);border-bottom:1px solid var(--bd)}
.tb-btns{display:flex;gap:7px;flex-shrink:0}
.tb-btn{width:12px;height:12px;border-radius:50%;border:none;cursor:pointer;transition:filter .12s;flex-shrink:0}
.tb-btn:hover{filter:brightness(.72)}
.tb-c{background:#ff5f57}.tb-m{background:#febc2e}.tb-x{background:#28c840}
.tb-drag{flex:1;height:100%}
.tb-title{position:absolute;left:50%;top:0;transform:translateX(-50%);height:36px;display:flex;align-items:center;font-size:11.5px;font-weight:600;color:var(--tx2);letter-spacing:.4px;user-select:none;white-space:nowrap;pointer-events:none}
.tb-title b{color:var(--tx2);font-weight:600;margin-left:4px}

/* ── layout ── */
#app{display:flex;height:100vh;padding-top:36px}

/* ── sidebar ── */
#sb{width:220px;flex-shrink:0;background:var(--sb);border-right:1px solid var(--bd);display:flex;flex-direction:column;overflow:hidden;transition:width .22s cubic-bezier(.4,0,.2,1)}
#sb.folded{width:48px}

.sb-nav{flex:1;padding:6px 0;overflow-y:auto;overflow-x:hidden}
.sb-sec{font-size:9.5px;font-weight:600;color:var(--tx3);letter-spacing:.7px;text-transform:uppercase;padding:10px 16px 4px;white-space:nowrap;overflow:hidden;transition:opacity .15s ease,max-height .22s cubic-bezier(.4,0,.2,1),padding .22s cubic-bezier(.4,0,.2,1)}
#sb.folded .sb-sec{opacity:0;max-height:0;padding-top:0;padding-bottom:0;pointer-events:none}

.nv{display:flex;align-items:center;height:40px;gap:8px;padding:0 14px;cursor:pointer;color:var(--tx2);border-left:2px solid transparent;font-size:13px;font-weight:450;transition:color .14s,background .14s,border-color .14s,padding .22s cubic-bezier(.4,0,.2,1),gap .22s cubic-bezier(.4,0,.2,1);position:relative}
.nv:hover{background:rgba(255,255,255,.04);color:var(--tx)}
.nv.on{background:var(--acc-d);color:var(--tx);border-left-color:var(--acc)}
#sb.folded .nv{padding:0;justify-content:center;gap:0;border-left-color:transparent}
#sb.folded .nv.on{background:var(--acc-d)}
#sb.folded .nv.on .nv-ico{opacity:1;color:var(--acc)}
.nv-ico{width:16px;height:16px;flex-shrink:0;color:var(--tx2);opacity:.85;transition:opacity .14s,color .14s}
.nv:hover .nv-ico{opacity:1;color:var(--tx)}
.nv.on .nv-ico{opacity:1;color:var(--acc)}
.nv-label{white-space:nowrap;overflow:hidden;transition:opacity .12s ease,max-width .22s cubic-bezier(.4,0,.2,1)}
#sb.folded .nv-label{opacity:0;max-width:0}
.nv-badge{margin-left:auto;background:rgba(255,255,255,.08);color:var(--tx2);font-size:9.5px;font-weight:600;padding:1px 6px;border-radius:8px;min-width:18px;text-align:center;font-variant-numeric:tabular-nums;transition:opacity .12s ease,transform .12s ease;flex-shrink:0}
.nv.on .nv-badge{background:var(--acc-d);color:var(--acc)}
#sb.folded .nv-badge{opacity:0;transform:scale(.6);pointer-events:none;position:absolute}

.nv-tip{display:none;position:fixed;left:54px;background:#1a1a1e;border:1px solid var(--bd2);color:var(--tx);font-size:12px;font-weight:500;padding:5px 10px;border-radius:7px;white-space:nowrap;pointer-events:none;z-index:999;box-shadow:0 4px 16px rgba(0,0,0,.4)}
#sb.folded .nv:hover .nv-tip{display:block}

.sb-settings-row{height:38px;padding:0 12px;display:flex;align-items:center;flex-shrink:0}
.sb-bottom{height:38px;padding:0 12px;display:flex;align-items:center;flex-shrink:0}
.sb-icobtn{width:22px;height:22px;border-radius:5px;background:none;border:none;cursor:pointer;color:var(--tx3);display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:color .14s,background .14s}
.sb-icobtn:hover{color:var(--tx);background:rgba(255,255,255,.06)}
.sb-icobtn.on{color:var(--acc);background:var(--acc-d)}
.sb-icobtn svg{transition:transform .22s cubic-bezier(.4,0,.2,1);flex-shrink:0}
#sb.folded #foldbtn svg{transform:rotate(180deg)}

/* ── main ── */
#main{flex:1;display:flex;flex-direction:column;min-width:0;overflow:hidden}
#ct{flex:1;overflow-y:auto;padding:20px 22px}

/* ── pages ── */
.pg{display:none}
.pg.on{display:flex;flex-direction:column;gap:14px;animation:pgIn .2s cubic-bezier(.16,1,.3,1) both}
#pg-terminal.on{height:100%}
@keyframes pgIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}

.ph{margin-bottom:2px}
.pt{font-size:18px;font-weight:700;letter-spacing:-.3px}
.ps{font-size:12px;color:var(--tx2);margin-top:2px}

/* ── dashboard hero ── */
#pg-dash.on{height:100%}
.dash-hero{text-align:center;padding:10px 0 6px}
.dash-title{font-size:28px;font-weight:800;letter-spacing:-.6px;background:linear-gradient(135deg,var(--tx) 25%,var(--acc) 110%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.dash-sub{font-size:12px;color:var(--tx2);margin-top:5px;font-weight:600;letter-spacing:.2px}
.dash-news{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:10px}

/* ── dashboard stats ── */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px}
.stat{background:var(--sf);border:1px solid var(--bd);border-radius:12px;padding:14px;display:flex;align-items:center;gap:12px;transition:border-color .18s,transform .18s}
.stat:hover{border-color:var(--bd2);transform:translateY(-1px)}
.stat-ico{width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.stat-ico svg{width:18px;height:18px}
.si-load{background:var(--acc-d);color:var(--acc)}
.si-time{background:rgba(245,192,64,.12);color:var(--yellow)}
.si-msg{background:rgba(0,208,240,.12);color:var(--cyan)}
.stat-body{display:flex;flex-direction:column;gap:1px;min-width:0}
.sv{font-size:20px;font-weight:700;line-height:1.15;font-variant-numeric:tabular-nums;letter-spacing:-.3px;color:var(--tx)}
.sl{font-size:9.5px;font-weight:600;color:var(--tx2);letter-spacing:.4px;text-transform:uppercase;white-space:nowrap}

/* ── news carousel ── */
.carousel{position:relative;border-radius:16px;overflow:hidden;box-shadow:0 10px 34px rgba(0,0,0,.35)}
.car-track{display:flex;transition:transform .5s cubic-bezier(.16,1,.3,1)}
.car-slide{min-width:100%;box-sizing:border-box;min-height:190px;padding:34px 86px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:11px;cursor:pointer;position:relative;overflow:hidden;transition:filter .15s}
.car-slide:hover{filter:brightness(1.06)}
.car-glow{position:absolute;width:280px;height:280px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.16),transparent 70%);top:-90px;right:-60px;pointer-events:none}
.car-ico{width:54px;height:54px;border-radius:16px;display:flex;align-items:center;justify-content:center;position:relative;z-index:1;box-shadow:0 6px 18px rgba(0,0,0,.25)}
.car-ico svg{width:26px;height:26px}
.car-title{font-size:19px;font-weight:800;letter-spacing:-.3px;position:relative;z-index:1}
.car-sub{font-size:13px;font-weight:500;position:relative;z-index:1}
.car-tag{font-size:9.5px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;padding:4px 13px;border-radius:20px;position:relative;z-index:1}

.car-slide.ad{background:linear-gradient(135deg,#3d2a0d,#1c1408);border:1.5px dashed rgba(255,191,71,.4);color:#ffcf7d}
.car-slide.ad .car-ico{background:rgba(255,191,71,.16);color:#ffcf7d}
.car-slide.ad .car-sub{color:rgba(255,207,125,.8)}
.car-slide.ad .car-tag{background:rgba(255,191,71,.16);color:#ffcf7d}

.car-slide.tg{background:linear-gradient(135deg,#37b7f5,#1a7fc4);color:#fff}
.car-slide.tg .car-ico{background:rgba(255,255,255,.2);color:#fff}
.car-slide.tg .car-sub{color:rgba(255,255,255,.88)}
.car-slide.tg .car-tag{background:rgba(255,255,255,.2);color:#fff}

.car-slide.tg2{background:linear-gradient(135deg,#1a7fc4,#124d7a);color:#fff}
.car-slide.tg2 .car-ico{background:rgba(255,255,255,.2);color:#fff}
.car-slide.tg2 .car-sub{color:rgba(255,255,255,.88)}
.car-slide.tg2 .car-tag{background:rgba(255,255,255,.2);color:#fff}

.car-slide.gh{background:linear-gradient(135deg,#2b3038,#0d1117);color:#fff}
.car-slide.gh .car-ico{background:rgba(255,255,255,.14);color:#fff}
.car-slide.gh .car-sub{color:rgba(255,255,255,.72)}
.car-slide.gh .car-tag{background:rgba(255,255,255,.14);color:#fff}

.car-arrow{position:absolute;top:50%;transform:translateY(-50%);width:34px;height:34px;border-radius:50%;background:rgba(0,0,0,.4);border:1px solid rgba(255,255,255,.18);color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:2;transition:background .14s,transform .14s}
.car-arrow:hover{background:rgba(0,0,0,.6);transform:translateY(-50%) scale(1.08)}
.car-prev{left:14px}
.car-next{right:14px}
.car-dots{display:flex;justify-content:center;gap:6px;margin-top:4px}
.car-dot{width:6px;height:6px;border-radius:50%;background:var(--bd2);cursor:pointer;transition:background .14s,width .2s}
.car-dot.on{background:var(--acc);width:20px;border-radius:4px}

/* ── card ── */
.card{background:var(--sf);border:1px solid var(--bd);border-radius:12px;padding:18px 20px}
.card-lbl{font-size:10px;font-weight:600;color:var(--tx2);letter-spacing:.5px;text-transform:uppercase;margin-bottom:14px}

/* ── form ── */
.fgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px 18px;margin-bottom:16px}
.fgrid:last-child{margin-bottom:0}
.field{display:flex;flex-direction:column;gap:5px}
.flbl{font-size:10px;font-weight:600;color:var(--tx2);letter-spacing:.5px;text-transform:uppercase;user-select:none}
.inp{width:100%;height:36px;background:var(--sf2);border:1px solid var(--bd2);border-radius:8px;color:var(--tx);font-size:13px;font-family:inherit;padding:0 11px;outline:none;transition:border-color .14s,box-shadow .14s;user-select:text}
.inp:focus{border-color:rgba(255,31,61,.55);box-shadow:0 0 0 3px var(--acc-d)}
.inp::placeholder{color:var(--tx3)}
.inp[type=number]{font-variant-numeric:tabular-nums;padding-right:26px}
.inp[type=number]::-webkit-inner-spin-button,.inp[type=number]::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}

.numwrap{position:relative}
.numspin{position:absolute;right:4px;top:4px;bottom:4px;width:20px;display:flex;flex-direction:column;gap:1px}
.numspin button{flex:1;display:flex;align-items:center;justify-content:center;background:none;border:none;border-radius:4px;color:var(--tx3);cursor:pointer;padding:0;transition:color .12s,background .12s}
.numspin button:hover{color:var(--tx);background:rgba(255,255,255,.08)}
.numspin button:active{background:var(--acc-d);color:var(--acc)}
.numspin svg{width:9px;height:9px;flex-shrink:0}

/* ── start button ── */
.sbtn{width:100%;height:44px;background:var(--acc);border:none;border-radius:10px;color:#fff;font-size:13.5px;font-weight:700;font-family:inherit;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;transition:filter .14s,background .18s,border .18s,color .18s;box-shadow:0 4px 18px var(--acc-g);user-select:none}
.sbtn:hover:not(:disabled){filter:brightness(1.1)}
.sbtn:disabled{cursor:not-allowed;opacity:.45;box-shadow:none}
.sbtn.stop{background:rgba(255,68,85,.08);border:1px solid rgba(255,68,85,.26);color:var(--red);box-shadow:none;filter:none}
.sbtn.stop:hover{background:rgba(255,68,85,.16)}

/* ── log ── */
.logbox{background:var(--sf);border:1px solid var(--bd);border-radius:12px;display:flex;flex-direction:column;min-height:200px;max-height:320px}
.termbox{max-height:none;flex:1}
.logtop{display:flex;align-items:center;justify-content:space-between;padding:9px 14px;border-bottom:1px solid var(--bd);flex-shrink:0}
.loglbl{font-size:10px;font-weight:600;color:var(--tx2);letter-spacing:.5px;text-transform:uppercase}
.logclr{font-size:11px;color:var(--tx3);background:none;border:none;cursor:pointer;font-family:inherit;padding:2px 7px;border-radius:5px;transition:color .12s,background .12s;user-select:none}
.logclr:hover{color:var(--tx);background:rgba(255,255,255,.06)}
#log{flex:1;overflow-y:auto;scroll-behavior:smooth;padding:6px 0;font-family:Consolas,"Courier New",monospace;font-size:11.5px}
.le{display:flex;align-items:flex-start;padding:5px 14px;margin:0 6px;gap:10px;border-radius:6px;transition:background .15s ease;animation:leIn .22s cubic-bezier(.16,1,.3,1) both;user-select:text}
.le:hover{background:rgba(255,255,255,.03)}
@keyframes leIn{from{opacity:0;transform:translateY(3px)}to{opacity:1;transform:none}}
.le-ts{color:var(--tx3);flex-shrink:0;font-size:10px;margin-top:2.5px;min-width:48px;font-variant-numeric:tabular-nums}
.le-lvl{font-weight:700;font-size:9.5px;letter-spacing:.3px;min-width:50px;text-align:center;flex-shrink:0;padding:1.5px 0;border-radius:4px}
.le-ok .le-lvl{color:var(--green);background:rgba(31,217,122,.12)}
.le-err .le-lvl{color:var(--red);background:rgba(255,68,85,.12)}
.le-warn .le-lvl{color:var(--yellow);background:rgba(245,192,64,.12)}
.le-info .le-lvl{color:var(--acc);background:var(--acc-d)}
.le-rl .le-lvl{color:var(--orange);background:rgba(255,136,68,.12)}
.le-cap .le-lvl{color:var(--cyan);background:rgba(0,208,240,.12)}
.le-dbg .le-lvl{color:var(--tx3);background:rgba(255,255,255,.05)}
.le-src{color:var(--tx3);flex-shrink:0;font-size:10px;margin-top:2.5px}
.le-msg{color:rgba(240,232,232,.74);flex:1;word-break:break-word;line-height:1.55;user-select:text}

/* ── drop + paste area ── */
.dzta{border:1.5px dashed var(--bd2);border-radius:12px;transition:border-color .18s,background .18s;position:relative;background:var(--sf2)}
.dzta:hover,.dzta.over{border-color:rgba(255,31,61,.48);background:var(--acc-d)}
.dzta textarea{width:100%;min-height:150px;background:transparent;border:none;color:var(--tx);font-size:12px;font-family:Consolas,monospace;padding:16px;outline:none;resize:vertical;line-height:1.6;user-select:text;position:relative;z-index:1}
.dzta-hint{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;pointer-events:none;transition:opacity .16s ease;z-index:0}
.dzta-hint.hide{opacity:0}
.dzta-hint-ico{width:38px;height:38px;color:var(--acc);opacity:.55}
.dzta-hint-txt{font-size:12.5px;color:var(--tx3);font-weight:500;text-align:center;line-height:1.5}

/* ── lines list ── */
.lbox{background:var(--sf2);border:1px solid var(--bd);border-radius:10px;overflow:hidden;max-height:280px;overflow-y:auto}
.li{display:flex;align-items:center;padding:7px 14px;gap:10px;border-bottom:1px solid rgba(255,255,255,.04);transition:background .1s}
.li:last-child{border-bottom:none}
.li:hover{background:rgba(255,255,255,.02)}
.li-n{font-size:10px;color:var(--tx3);min-width:22px;font-variant-numeric:tabular-nums;font-family:Consolas,monospace;flex-shrink:0}
.li-t{font-size:13px;color:var(--tx2);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.empty{padding:26px 16px;text-align:center;font-size:13px;color:var(--tx3)}

/* ── textarea ── */
.ta{width:100%;min-height:88px;background:var(--sf2);border:1px solid var(--bd2);border-radius:8px;color:var(--tx);font-size:12px;font-family:Consolas,monospace;padding:9px 11px;outline:none;resize:vertical;line-height:1.5;transition:border-color .14s,box-shadow .14s;user-select:text}
.ta:focus{border-color:rgba(255,31,61,.5);box-shadow:0 0 0 3px var(--acc-d)}
.ta::placeholder{color:var(--tx3)}

.row{display:flex;align-items:center;gap:12px}
.f1{flex:1}

/* ── coming soon ── */
.soon{display:inline-flex;align-items:center;gap:5px;padding:2px 8px;border-radius:6px;background:var(--acc-d);color:var(--acc);font-size:10px;font-weight:700;letter-spacing:.4px;text-transform:uppercase}

/* ── spread page ── */
.sp-subnav{max-height:0;overflow:hidden;transition:max-height .22s cubic-bezier(.4,0,.2,1)}
.sp-subnav.on{max-height:130px}
#sb.folded .sp-subnav{max-height:0!important}
.nv-sub{display:flex;align-items:center;height:32px;gap:8px;padding:0 14px 0 32px;cursor:pointer;color:var(--tx2);font-size:12px;font-weight:500;border-left:2px solid transparent;transition:color .14s,background .14s,border-color .14s;white-space:nowrap}
.nv-sub:hover{background:rgba(255,255,255,.04);color:var(--tx)}
.nv-sub.on{color:var(--acc);border-left-color:var(--acc);background:var(--acc-d)}
.nv-sub-dot{width:4px;height:4px;border-radius:50%;background:currentColor;flex-shrink:0;opacity:.4;transition:opacity .14s}
.nv-sub.on .nv-sub-dot{opacity:1}
.sp-segs{position:relative;display:flex;background:var(--sf2);border:1px solid var(--bd);border-radius:10px;padding:3px}
.sp-seg{flex:1;height:30px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:600;letter-spacing:.15px;color:var(--tx2);border-radius:7px;cursor:pointer;transition:color .2s;user-select:none;position:relative;z-index:1}
.sp-seg.on{color:#fff}
.sp-seg-pill{position:absolute;height:calc(100% - 6px);border-radius:7px;background:var(--acc);top:3px;left:3px;z-index:0;transition:transform .22s cubic-bezier(.4,0,.2,1),width .22s cubic-bezier(.4,0,.2,1);box-shadow:0 0 16px rgba(255,31,61,.4)}
.sp-panel{display:none;flex-direction:column;gap:14px}
.sp-panel.on{display:flex}
.sp-note{background:var(--sf2);border:1px solid var(--bd);border-radius:10px;padding:12px 14px;font-size:11.5px;line-height:1.65;color:var(--tx2);margin-top:10px}
.sp-note b{color:var(--tx);font-weight:600}
.tool-panel{display:none;flex-direction:column;gap:6px}
.tool-panel.on{display:flex}
.tool-ta{height:210px;resize:vertical}
.ac-body{background:var(--sf2);border:1px solid var(--bd);border-radius:10px;max-height:300px;overflow-y:auto}
.ac-row{display:flex;align-items:center;gap:10px;padding:8px 13px;border-bottom:1px solid rgba(255,255,255,.04);font-size:12px}
.ac-row:last-child{border-bottom:none}
.ac-row:hover{background:rgba(255,255,255,.03)}
.ac-guild{font-weight:600;color:var(--tx);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ac-tok{color:var(--tx3);font-family:Consolas,monospace;font-size:11px;max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.eval-hdr{display:grid;grid-template-columns:140px 90px 58px 50px 62px 1fr;gap:0;align-items:center;padding:7px 13px;background:var(--sf);border:1px solid var(--bd);border-radius:8px 8px 0 0}
.eval-hdr span{color:var(--tx3);font-size:10px;font-weight:700;letter-spacing:.4px;text-transform:uppercase}
.eval-body{background:var(--sf2);border:1px solid var(--bd);border-top:none;border-radius:0 0 8px 8px;max-height:300px;overflow-y:auto}
.eval-row{display:grid;grid-template-columns:140px 90px 58px 50px 62px 1fr;gap:0;align-items:center;padding:7px 13px;border-bottom:1px solid rgba(255,255,255,.04);font-size:12px}
.eval-row:last-child{border-bottom:none}
.eval-row:hover{background:rgba(255,255,255,.03)}
.ev-uname{font-weight:600;color:var(--tx);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ev-tok{color:var(--tx3);font-family:Consolas,monospace;font-size:11px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
/* filter bar */
.flt-bar{display:flex;align-items:center;gap:14px;flex-wrap:wrap;background:var(--sf);border:1px solid var(--bd);border-radius:10px;padding:10px 14px}
.flt-group{display:flex;align-items:center;gap:6px}
.flt-lbl{font-size:9.5px;font-weight:600;color:var(--tx3);letter-spacing:.5px;text-transform:uppercase;white-space:nowrap;flex-shrink:0}
.flt-tog{height:24px;padding:0 10px;border-radius:20px;font-size:11px;font-weight:600;color:var(--tx2);background:var(--sf2);border:1px solid var(--bd2);cursor:pointer;display:flex;align-items:center;transition:color .14s,background .14s,border-color .14s;white-space:nowrap;user-select:none}
.flt-tog:hover{color:var(--tx);background:rgba(255,255,255,.06)}
.flt-tog.on{color:var(--acc);background:var(--acc-d);border-color:rgba(255,31,61,.3)}
.flt-inp{width:70px;height:28px;font-size:12px;padding:0 8px}
/* rare checker table */
.rc-hdr{display:grid;grid-template-columns:130px 60px 90px 40px 52px 1fr 54px;gap:0;align-items:center;padding:7px 13px;background:var(--sf);border:1px solid var(--bd);border-radius:8px 8px 0 0}
.rc-hdr span{color:var(--tx3);font-size:10px;font-weight:700;letter-spacing:.4px;text-transform:uppercase}
.rc-body{background:var(--sf2);border:1px solid var(--bd);border-top:none;border-radius:0 0 8px 8px;max-height:340px;overflow-y:auto}
.rc-row{display:grid;grid-template-columns:130px 60px 90px 40px 52px 1fr 54px;gap:0;align-items:center;padding:7px 13px;border-bottom:1px solid rgba(255,255,255,.04);font-size:12px}
.rc-row:last-child{border-bottom:none}
.rc-row:hover{background:rgba(255,255,255,.03)}
.rc-uname{font-weight:600;color:var(--tx);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rc-badges{display:flex;gap:3px;flex-wrap:wrap}
.rc-badge{font-size:9.5px;font-weight:600;padding:1px 6px;border-radius:8px;background:rgba(245,192,64,.12);color:var(--yellow);white-space:nowrap}
.rc-score{font-weight:700;font-variant-numeric:tabular-nums}
.rc-rare-y{font-size:9.5px;font-weight:700;padding:2px 7px;border-radius:8px;background:rgba(245,192,64,.15);color:var(--yellow);letter-spacing:.3px}
.rc-rare-n{font-size:9.5px;font-weight:600;padding:2px 7px;border-radius:8px;background:rgba(255,255,255,.05);color:var(--tx3)}
/* token capture table */
.tc-hdr{display:grid;grid-template-columns:125px 62px 82px 108px 1fr 76px 68px;gap:0;align-items:center;padding:7px 13px;background:var(--sf);border:1px solid var(--bd);border-radius:8px 8px 0 0}
.tc-hdr span{color:var(--tx3);font-size:10px;font-weight:700;letter-spacing:.4px;text-transform:uppercase}
.tc-body{background:var(--sf2);border:1px solid var(--bd);border-top:none;border-radius:0 0 8px 8px;max-height:340px;overflow-y:auto}
.tc-row{display:grid;grid-template-columns:125px 62px 82px 108px 1fr 76px 68px;gap:0;align-items:center;padding:7px 13px;border-bottom:1px solid rgba(255,255,255,.04);font-size:12px}
.tc-row:last-child{border-bottom:none}
.tc-row:hover{background:rgba(255,255,255,.03)}
.tc-uname{font-weight:600;color:var(--tx);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tc-tok{color:var(--tx3);font-family:Consolas,monospace;font-size:11px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tc-chips{display:flex;gap:3px;flex-wrap:wrap;align-items:center}
.tc-chip{font-size:9.5px;font-weight:700;padding:2px 7px;border-radius:8px;white-space:nowrap}
.tc-chip.valid{background:rgba(31,217,122,.12);color:var(--green)}
.tc-chip.invalid{background:rgba(255,68,85,.12);color:var(--red)}
.tc-chip.locked{background:rgba(245,192,64,.12);color:var(--yellow)}
.tc-chip.nitro{background:rgba(183,140,255,.12);color:#b78cff}
.tc-chip.pay{background:rgba(0,208,240,.12);color:var(--cyan)}
.tc-chip.badge{background:rgba(245,192,64,.10);color:var(--yellow)}
.tc-chip.mfa{background:rgba(255,136,68,.1);color:var(--orange)}
.tc-chip.eml{background:rgba(31,217,122,.08);color:rgba(31,217,122,.8)}
.sp-pill-tray{background:var(--sf2);border:1px solid var(--bd);border-radius:10px;padding:10px 13px}
.sp-pill-tray-lbl{font-size:9.5px;font-weight:600;color:var(--tx3);letter-spacing:.5px;text-transform:uppercase;margin-bottom:8px}
.sp-pills{display:flex;gap:6px;flex-wrap:wrap}
.sp-pill{display:inline-flex;align-items:center;gap:5px;padding:4px 10px 4px 8px;background:rgba(255,31,61,.07);border:1px solid rgba(255,31,61,.2);border-radius:20px;font-size:11.5px;font-weight:600;color:var(--acc);cursor:grab;transition:background .14s,border-color .14s,transform .12s,box-shadow .12s;user-select:none}
.sp-pill:hover{background:rgba(255,31,61,.15);border-color:rgba(255,31,61,.42);transform:translateY(-1px);box-shadow:0 3px 10px rgba(255,31,61,.18)}
.sp-pill:active{cursor:grabbing;transform:scale(.95)}
.sp-pill svg{width:11px;height:11px;flex-shrink:0}
/* msg editor (contenteditable) */
.msg-editor{width:100%;min-height:110px;background:var(--sf2);border:1px solid var(--bd2);border-radius:8px;color:var(--tx);font-size:12.5px;font-family:Consolas,monospace;padding:9px 11px;outline:none;line-height:1.9;transition:border-color .14s,box-shadow .14s;word-break:break-word;white-space:pre-wrap;overflow-y:auto;cursor:text}
.msg-editor:focus{border-color:rgba(255,31,61,.5);box-shadow:0 0 0 3px var(--acc-d)}
.msg-editor:empty::before{content:attr(data-placeholder);color:var(--tx3);pointer-events:none;font-style:normal}
/* inline token pills */
.mp{display:inline-flex;align-items:center;gap:4px;padding:2px 6px 2px 5px;border-radius:12px;font-size:11px;font-weight:600;cursor:pointer;vertical-align:middle;margin:0 2px;white-space:nowrap;user-select:none;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;line-height:1.4}
.mp svg{width:10px;height:10px;flex-shrink:0}
.mp-x{background:none;border:none;cursor:pointer;color:inherit;opacity:.55;font-size:12px;padding:0 0 0 2px;line-height:1;font-family:inherit}
.mp-x:hover{opacity:1}
.mp-ping{background:rgba(0,208,240,.1);border:1px solid rgba(0,208,240,.22);color:#00d0f0}
.mp-random{background:rgba(245,192,64,.1);border:1px solid rgba(245,192,64,.22);color:#f5c040}
.mp-file{background:rgba(31,217,122,.1);border:1px solid rgba(31,217,122,.22);color:#1fd97a}
.mp-image{background:rgba(255,136,68,.1);border:1px solid rgba(255,136,68,.22);color:#ff8844}
/* pill config popup */
.pill-cfg{position:fixed;background:var(--sf);border:1px solid var(--bd2);border-radius:10px;padding:12px 14px;z-index:400;box-shadow:0 8px 24px rgba(0,0,0,.45);display:none;flex-direction:column;gap:8px;min-width:180px}
.pill-cfg.on{display:flex}
.pill-cfg-title{font-size:10px;font-weight:600;color:var(--tx3);text-transform:uppercase;letter-spacing:.5px}
.pill-cfg-btns{display:flex;gap:6px;margin-top:2px}
.pill-cfg-btn{flex:1;height:28px;border-radius:7px;font-size:11.5px;font-weight:600;font-family:inherit;cursor:pointer;border:none}
.pill-cfg-btn.apply{background:var(--acc);color:#fff}
.pill-cfg-btn.apply:hover{filter:brightness(1.1)}
.pill-cfg-btn.cancel{background:var(--sf2);color:var(--tx2);border:1px solid var(--bd2)}
.pill-cfg-btn.cancel:hover{color:var(--tx)}
/* msg action row */
.msg-actions{display:flex;gap:6px;margin-top:6px}
.msg-act{height:28px;padding:0 11px;background:var(--sf2);border:1px solid var(--bd2);border-radius:7px;font-size:11px;font-weight:600;color:var(--tx2);cursor:pointer;font-family:inherit;display:flex;align-items:center;gap:5px;transition:color .14s,background .14s,border-color .14s}
.msg-act:hover{color:var(--tx);background:rgba(255,255,255,.05)}
.msg-act svg{width:12px;height:12px;flex-shrink:0}
/* ping dropdown */
@keyframes menuIn{from{opacity:0;transform:translateY(-4px) scale(.97)}to{opacity:1;transform:none}}
.ping-menu{position:fixed;background:var(--sf);border:1px solid var(--bd2);border-radius:10px;padding:4px;z-index:450;box-shadow:0 8px 28px rgba(0,0,0,.55);display:none;flex-direction:column;gap:1px;min-width:230px}
.ping-menu.on{display:flex;animation:menuIn .16s cubic-bezier(.16,1,.3,1) both}
.ping-opt{display:flex;align-items:center;gap:9px;padding:6px 8px;border-radius:7px;cursor:pointer;transition:background .1s}
.ping-opt:hover{background:rgba(255,255,255,.06)}
.ping-opt.active{background:rgba(255,31,61,.09)}
.ping-opt-ico{width:30px;height:30px;border-radius:50%;background:var(--sf2);border:1px solid var(--bd);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.ping-opt-ico svg{width:14px;height:14px;color:var(--tx2)}
.ping-opt-name{font-size:12.5px;font-weight:600;color:var(--tx)}
.ping-opt-desc{font-size:11px;color:var(--tx3);margin-top:1px}
.ping-user-inp{width:88px;height:24px;font-size:11px;padding:0 7px;flex-shrink:0}
.ping-sep{height:1px;background:var(--bd);margin:3px 0}
/* file preview popup */
.fp-popup{position:fixed;background:#1e1f22;border:1px solid rgba(0,0,0,.5);border-radius:6px;z-index:450;box-shadow:0 10px 40px rgba(0,0,0,.7);display:none;flex-direction:column;overflow:hidden;max-width:420px}
.fp-popup.on{display:flex;animation:menuIn .16s cubic-bezier(.16,1,.3,1) both}
/* discord message preview */
.dc-preview-shell{background:#313338;border-radius:8px;overflow:hidden;width:820px;max-width:calc(100vw - 40px);box-shadow:0 24px 70px rgba(0,0,0,.75);animation:modalIn .28s cubic-bezier(.16,1,.3,1) both;display:flex;flex-direction:column;max-height:90vh}
.dc-preview-hdr{height:48px;background:#2b2d31;border-bottom:2px solid #1e1f22;display:flex;align-items:center;justify-content:space-between;padding:0 16px;flex-shrink:0}
.dc-preview-hdr span{font-size:15px;font-weight:700;color:#f2f3f5;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif}
.dc-preview-close{background:none;border:none;cursor:pointer;color:#80848e;padding:4px;display:flex;border-radius:4px}
.dc-preview-close:hover{color:#f2f3f5;background:rgba(255,255,255,.07)}
.dc-preview-close svg{width:18px;height:18px}
.dc-preview-chat{padding:16px 16px 20px;background:#313338;overflow-y:auto;flex:1;min-height:0}
.dc-msg-row{display:flex;gap:16px}
.dc-avatar{width:40px;height:40px;border-radius:50%;background:#5865f2;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:900;color:#fff;flex-shrink:0;font-family:-apple-system,sans-serif;letter-spacing:-1px}
.dc-msg-body{flex:1;min-width:0}
.dc-msg-hdr{display:flex;align-items:baseline;gap:8px;margin-bottom:2px}
.dc-uname{font-size:15px;font-weight:500;color:#f2f3f5;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif}
.dc-ts{font-size:11.5px;color:#80848e;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif}
.dc-text{font-size:15px;color:#dbdee1;line-height:1.375;word-break:break-word;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;white-space:pre-wrap}
.dc-text:empty::after{content:'(empty)';color:#4e5058;font-style:italic}
.dc-men{background:rgba(88,101,242,.3);color:#c9cdfb;border-radius:3px;padding:0 2px;font-weight:500}
.dc-men:hover{background:#5865f2;color:#fff}
.dc-attaches{display:flex;flex-direction:column;gap:4px;margin-top:8px}
/* discord image embed — fills the message column, caps tall images */
.dc-img-embed{display:block;line-height:0;border-radius:4px;overflow:hidden;background:#1e1f22;max-width:520px;width:fit-content}
.dc-att-img{display:block;max-width:100%;max-height:400px;width:auto;height:auto}
.dc-att-file{display:inline-flex;align-items:center;gap:10px;background:#2b2d31;border:1px solid #1e1f22;border-radius:3px;padding:10px 12px;max-width:432px}
.dc-att-file-ico{width:30px;height:30px;background:#5865f2;border-radius:6px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.dc-att-file-ico svg{width:16px;height:16px}
.dc-att-fname{font-size:14px;font-weight:600;color:#00aff4}
.dc-att-fsize{font-size:12px;color:#80848e;margin-top:1px}
.dc-file-card{display:flex;align-items:center;gap:12px;padding:12px 14px;background:#2b2d31}
.dc-file-ico{width:40px;height:40px;flex-shrink:0;display:flex;align-items:center;justify-content:center;background:#36393f;border-radius:6px}
.dc-file-ico svg{width:22px;height:22px}
.dc-file-name{font-size:13.5px;font-weight:600;color:#dbdee1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:260px}
.dc-file-meta{font-size:12px;color:#80848e;margin-top:2px}
.dc-img-wrap{background:#111214;display:flex;align-items:center;justify-content:center;padding:6px 6px 0}
.dc-img-wrap img{max-width:400px;max-height:280px;border-radius:3px;display:block;object-fit:contain}
.dc-img-meta{display:flex;align-items:center;gap:6px;padding:6px 10px;background:#2b2d31}
.dc-img-name{font-size:12px;font-weight:600;color:#dbdee1;flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dc-img-size{font-size:11.5px;color:#80848e;flex-shrink:0}
.fp-footer{display:flex;align-items:center;gap:6px;padding:8px 10px;background:#2b2d31;border-top:1px solid rgba(0,0,0,.3)}
.fp-drop-zone{flex:1;height:28px;border:1px dashed rgba(255,255,255,.18);border-radius:5px;display:flex;align-items:center;justify-content:center;gap:5px;font-size:11px;color:#80848e;cursor:pointer;transition:border-color .14s,color .14s;user-select:none}
.fp-drop-zone:hover,.fp-drop-zone.drag{border-color:rgba(255,255,255,.4);color:#dbdee1}
.fp-btn-remove{height:28px;padding:0 11px;border-radius:5px;font-size:11.5px;font-weight:600;font-family:inherit;cursor:pointer;border:none;background:rgba(255,31,61,.18);color:#ff4757;flex-shrink:0}
.fp-btn-remove:hover{background:rgba(255,31,61,.3)}
.sp-opts{display:flex;flex-direction:column;gap:6px}
.sp-opt{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;background:var(--sf2);border-radius:10px;cursor:pointer;border:1px solid var(--bd);transition:border-color .14s,background .14s;user-select:none}
.sp-opt:hover{border-color:var(--bd2);background:rgba(255,255,255,.03)}
.sp-opt-info{display:flex;flex-direction:column;gap:2px}
.sp-opt-name{font-size:12.5px;font-weight:600;color:var(--tx)}
.sp-opt-desc{font-size:10.5px;color:var(--tx2)}
.tog{width:34px;height:18px;border-radius:9px;background:rgba(255,255,255,.10);flex-shrink:0;position:relative;transition:background .18s;pointer-events:none}
.tog::after{content:'';position:absolute;width:12px;height:12px;border-radius:50%;background:#fff;top:3px;left:3px;transition:transform .18s,box-shadow .18s;box-shadow:0 1px 3px rgba(0,0,0,.3)}
.tog.on{background:var(--acc)}
.tog.on::after{transform:translateX(16px)}
.sp-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(100px,1fr));gap:8px}
.sp-stat{background:var(--sf);border:1px solid var(--bd);border-radius:10px;padding:10px 14px;display:flex;flex-direction:column;gap:2px}
.sp-stat-val{font-size:18px;font-weight:700;font-variant-numeric:tabular-nums;letter-spacing:-.3px;color:var(--tx)}
.sp-stat-lbl{font-size:9.5px;font-weight:600;color:var(--tx2);letter-spacing:.4px;text-transform:uppercase}

/* ── update modal ── */
.modal-backdrop{position:fixed;inset:0;background:rgba(0,0,0,.6);display:none;align-items:center;justify-content:center;z-index:500}
.modal-backdrop.on{display:flex}
.modal-card{width:340px;background:var(--sf);border:1px solid var(--bd2);border-radius:14px;padding:24px 22px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.5);animation:modalIn .2s cubic-bezier(.16,1,.3,1) both}
@keyframes modalIn{from{opacity:0;transform:translateY(10px) scale(.97)}to{opacity:1;transform:none}}
@keyframes modalOut{to{opacity:0;transform:translateY(12px) scale(.97)}}
/* launch modal – always display:flex so transitions can run */
#launch-modal{display:flex;opacity:0;pointer-events:none;transition:opacity .22s cubic-bezier(.4,0,.2,1),backdrop-filter .22s}
#launch-modal.on{opacity:1;pointer-events:auto}
#launch-modal.on .modal-card{animation:modalIn .28s cubic-bezier(.16,1,.3,1) both}
#launch-modal.closing .modal-card{animation:modalOut .2s cubic-bezier(.4,0,1,1) forwards}
.modal-ico{width:44px;height:44px;margin:0 auto 14px;border-radius:12px;background:var(--acc-d);color:var(--acc);display:flex;align-items:center;justify-content:center}
.modal-ico svg{width:22px;height:22px}
.modal-title{font-size:15px;font-weight:700;margin-bottom:6px}
.modal-msg{font-size:12.5px;color:var(--tx2);line-height:1.6;margin-bottom:20px}
.modal-actions{display:flex;gap:8px}
.modal-btn{flex:1;height:38px;border-radius:9px;font-size:12.5px;font-weight:700;font-family:inherit;cursor:pointer;transition:filter .14s,background .14s,border-color .14s;border:none}
.modal-btn.ghost{background:var(--sf2);border:1px solid var(--bd2);color:var(--tx2)}
.modal-btn.ghost:hover{color:var(--tx);background:rgba(255,255,255,.06)}
.modal-btn.primary{background:var(--acc);color:#fff;box-shadow:0 4px 18px var(--acc-g)}
.modal-btn.primary:hover{filter:brightness(1.1)}
/* ── notifications ── */
#notif-stack{position:fixed;top:46px;left:50%;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:6px;z-index:9999;pointer-events:none}
.notif{display:flex;align-items:center;gap:10px;padding:10px 16px 10px 13px;border-radius:10px;background:var(--sf2);border:1px solid var(--bd2);box-shadow:0 6px 24px rgba(0,0,0,.55);color:var(--tx);font-size:13px;min-width:280px;max-width:420px;pointer-events:auto;cursor:pointer;animation:notifIn .22s cubic-bezier(.16,1,.3,1) both;white-space:nowrap}
.notif.out{animation:notifOut .18s ease forwards}
.notif-error{border-color:rgba(255,68,85,.35);background:rgba(255,68,85,.06)}
.notif-warn{border-color:rgba(245,192,64,.35);background:rgba(245,192,64,.06)}
.notif-ok{border-color:rgba(31,217,122,.35);background:rgba(31,217,122,.06)}
.notif-info{border-color:var(--bd2)}
.notif-ico{flex-shrink:0;width:15px;height:15px}
.notif-error .notif-ico{color:var(--red)}
.notif-warn .notif-ico{color:var(--yellow)}
.notif-ok .notif-ico{color:var(--green)}
.notif-info .notif-ico{color:var(--tx2)}
.notif-msg{flex:1;line-height:1.4}
@keyframes notifIn{from{opacity:0;transform:translateY(-8px) scale(.97)}to{opacity:1;transform:none}}
@keyframes notifOut{to{opacity:0;transform:translateY(-8px) scale(.97)}}
</style>
</head>
<body>

<div id="tb">
  <div class="tb-btns">
    <button class="tb-btn tb-c" onclick="call('close')"></button>
    <button class="tb-btn tb-m" onclick="call('minimize')"></button>
    <button class="tb-btn tb-x" onclick="call('maximize')"></button>
  </div>
  <div class="tb-drag"></div>
  <div class="tb-title">Discord Reaper <b>made by r3ci</b></div>
</div>

<div id="app">
  <div id="sb">
    <div class="sb-nav">
      <div class="sb-sec">Main</div>
      <div class="nv on" data-pg="dash" onclick="nav(this)">
        <svg class="nv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
        <span class="nv-label">Dashboard</span>
        <span class="nv-tip">Dashboard</span>
      </div>
      <div class="nv" data-pg="terminal" onclick="nav(this)">
        <svg class="nv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/></svg>
        <span class="nv-label">Terminal</span>
        <span class="nv-tip">Terminal</span>
      </div>
      <div class="sb-sec">Data</div>
      <div class="nv" data-pg="tokens" onclick="nav(this)">
        <svg class="nv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"/><path d="m21.2 2.8-6.4 6.4"/><circle cx="8.5" cy="15.5" r="5.5"/></svg>
        <span class="nv-label">Tokens</span>
        <span class="nv-badge" id="badge-tokens">0</span>
        <span class="nv-tip">Tokens</span>
      </div>
      <div class="nv" data-pg="proxies" onclick="nav(this)">
        <svg class="nv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>
        <span class="nv-label">Proxies</span>
        <span class="nv-badge" id="badge-proxies">0</span>
        <span class="nv-tip">Proxies</span>
      </div>
      <div class="sb-sec">Tools</div>
      <div class="nv" data-pg="spread" onclick="nav(this)">
        <svg class="nv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/></svg>
        <span class="nv-label">Spread</span>
        <span class="nv-tip">Spread</span>
      </div>
      <div class="sp-subnav" id="spread-subnav">
        <div class="nv-sub on" data-spread="main" onclick="spSubNav(this)"><span class="nv-sub-dot"></span>Main</div>
        <div class="nv-sub" data-spread="settings" onclick="spSubNav(this)"><span class="nv-sub-dot"></span>Settings</div>
        <div class="nv-sub" data-spread="messages" onclick="spSubNav(this)"><span class="nv-sub-dot"></span>Messages</div>
      </div>
      <div class="nv" data-pg="checker" onclick="nav(this)">
        <svg class="nv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.801 10A10 10 0 1 1 17 3.335"/><path d="m9 11 3 3L22 4"/></svg>
        <span class="nv-label">Checker</span>
        <span class="nv-tip">Checker</span>
      </div>
      <div class="nv" data-pg="admincap" onclick="nav(this)">
        <svg class="nv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 3 6v6c0 5 4 8.5 9 10 5-1.5 9-5 9-10V6z"/></svg>
        <span class="nv-label">Nukable Capture</span>
        <span class="nv-tip">Nukable Capture</span>
      </div>
      <div class="nv" data-pg="evaluator" onclick="nav(this)">
        <svg class="nv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M8 12h8M12 8v8"/></svg>
        <span class="nv-label">Evaluator</span>
        <span class="nv-tip">Evaluator</span>
      </div>
      <div class="nv" data-pg="rarechecker" onclick="nav(this)">
        <svg class="nv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
        <span class="nv-label">Rare Checker</span>
        <span class="nv-tip">Rare Checker</span>
      </div>
      <div class="nv" data-pg="tokencapture" onclick="nav(this)">
        <svg class="nv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
        <span class="nv-label">Token Capture</span>
        <span class="nv-tip">Token Capture</span>
      </div>
    </div>
    <div class="sb-settings-row">
      <button class="sb-icobtn" id="settingsbtn" onclick="openSettings()" title="Settings">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
      </button>
    </div>
    <div class="sb-bottom">
      <button class="sb-icobtn" id="foldbtn" onclick="toggleSb()" title="Toggle sidebar">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M9 2L4 7l5 5"/></svg>
      </button>
    </div>
  </div>

  <div id="main">
    <div id="ct">

      <div class="pg on" id="pg-dash">
        <div class="dash-hero">
          <div class="dash-title">Discord Reaper</div>
          <div class="dash-sub">Made by r3ci</div>
        </div>

        <div class="stats">
          <div class="stat">
            <div class="stat-ico si-load"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"/><path d="m21.2 2.8-6.4 6.4"/><circle cx="8.5" cy="15.5" r="5.5"/></svg></div>
            <div class="stat-body"><div class="sv" id="stat-loaded">0</div><div class="sl">Tokens Loaded</div></div>
          </div>
          <div class="stat">
            <div class="stat-ico si-time"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>
            <div class="stat-body"><div class="sv" id="stat-runtime">00:00:00</div><div class="sl">Runtime</div></div>
          </div>
          <div class="stat">
            <div class="stat-ico si-msg"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg></div>
            <div class="stat-body"><div class="sv" id="stat-messages">0</div><div class="sl">Total Sent</div></div>
          </div>
        </div>

        <div class="dash-news">
        <div class="carousel">
          <button class="car-arrow car-prev" onclick="carouselNav(-1)">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
          </button>
          <div class="car-track" id="car-track">
            <div class="car-slide tg" onclick="call('openurl','https://t.me/DiscordReaperChat')">
              <div class="car-glow"></div>
              <div class="car-ico"><svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.831-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg></div>
              <div class="car-title">Join our Telegram Chat</div>
              <div class="car-sub">t.me/DiscordReaperChat</div>
            </div>
            <div class="car-slide tg2" onclick="call('openurl','https://t.me/DiscordReaper')">
              <div class="car-glow"></div>
              <div class="car-ico"><svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.831-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg></div>
              <div class="car-title">Telegram Channel</div>
              <div class="car-sub">t.me/DiscordReaper</div>
            </div>
            <div class="car-slide ad" onclick="call('openurl','https://t.me/ther3ci')">
              <div class="car-glow"></div>
              <div class="car-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/></svg></div>
              <div class="car-title">Your AD Here</div>
              <div class="car-sub">t.me/ther3ci</div>
            </div>
            <div class="car-slide gh" onclick="call('openurl','https://github.com/R3CI/DiscordReaper')">
              <div class="car-glow"></div>
              <div class="car-ico"><svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.385-1.333-1.754-1.333-1.754-1.089-.744.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.108-.775.418-1.305.762-1.605-2.665-.3-5.467-1.332-5.467-5.93 0-1.31.469-2.381 1.236-3.221-.124-.303-.535-1.523.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.29-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.873.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.61-2.807 5.625-5.479 5.921.43.372.823 1.102.823 2.222 0 1.606-.015 2.898-.015 3.293 0 .322.216.696.825.578C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg></div>
              <div class="car-title">GitHub Repository</div>
              <div class="car-sub">github.com/R3CI/DiscordReaper</div>
            </div>
          </div>
          <button class="car-arrow car-next" onclick="carouselNav(1)">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
          </button>
        </div>
        <div class="car-dots">
          <div class="car-dot on" onclick="carouselGoto(0)"></div>
          <div class="car-dot" onclick="carouselGoto(1)"></div>
          <div class="car-dot" onclick="carouselGoto(2)"></div>
          <div class="car-dot" onclick="carouselGoto(3)"></div>
        </div>
        </div>
      </div>

      <div class="pg" id="pg-terminal">
        <div class="ph">
          <div class="pt">Terminal</div>
          <div class="ps">Live output from the app</div>
        </div>
        <div class="logbox termbox">
          <div class="logtop">
            <span class="loglbl">Output</span>
            <div class="row" style="gap:4px">
              <button class="logclr" onclick="copyLog()">Copy</button>
              <button class="logclr" onclick="document.getElementById('log').innerHTML=''">Clear</button>
            </div>
          </div>
          <div id="log"></div>
        </div>
      </div>

      <div class="pg" id="pg-settings">
        <div class="ph">
          <div class="pt">Settings</div>
          <div class="ps">Proxy and general behaviour configuration</div>
        </div>
        <div class="card">
          <div class="card-lbl">Proxies</div>
          <div class="fgrid">
            <div class="field">
              <label class="flbl">Timeout (s)</label>
              <input class="inp" type="number" id="cfg-proxytimeout" value="15" min="1" oninput="syncCfg()">
            </div>
          </div>
        </div>
      </div>

      <div class="pg" id="pg-tokens">
        <div class="row">
          <div class="f1">
            <div class="pt">Tokens</div>
            <div class="ps">Discord account tokens loaded for this session</div>
          </div>
          <div class="avcnt"><b id="tokens-count">0</b> loaded</div>
        </div>
        <div class="dzta" id="tokens-dzta" ondragover="dzOver(event,this)" ondragleave="dzLeave(this)" ondrop="dzDropText(event,this,'tokens')">
          <div class="dzta-hint" id="tokens-hint">
            <svg class="dzta-hint-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 12v9"/><path d="m16 16-4-4-4 4"/><path d="M16 16.74a4 4 0 0 0-1-7.86 5.5 5.5 0 0 0-10.63.5A4.5 4.5 0 0 0 5.5 18H6"/></svg>
            <div class="dzta-hint-txt">Drag &amp; drop a file<br>or paste it here</div>
          </div>
          <textarea id="tokens-manual" oninput="manualUpdate('tokens');toggleHint('tokens')"></textarea>
        </div>
        <div class="lbox" id="tokens-lines-box"><div class="empty">No tokens loaded</div></div>
      </div>

      <div class="pg" id="pg-proxies">
        <div class="row">
          <div class="f1">
            <div class="pt">Proxies</div>
            <div class="ps">Proxy pool used to spread outgoing requests</div>
          </div>
          <div class="avcnt"><b id="proxies-count">0</b> loaded</div>
        </div>
        <div class="dzta" id="proxies-dzta" ondragover="dzOver(event,this)" ondragleave="dzLeave(this)" ondrop="dzDropText(event,this,'proxies')">
          <div class="dzta-hint" id="proxies-hint">
            <svg class="dzta-hint-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 12v9"/><path d="m16 16-4-4-4 4"/><path d="M16 16.74a4 4 0 0 0-1-7.86 5.5 5.5 0 0 0-10.63.5A4.5 4.5 0 0 0 5.5 18H6"/></svg>
            <div class="dzta-hint-txt">Drag &amp; drop a file<br>or paste it here</div>
          </div>
          <textarea id="proxies-manual" oninput="manualUpdate('proxies');toggleHint('proxies')"></textarea>
        </div>
        <div class="lbox" id="proxies-lines-box"><div class="empty">No proxies loaded</div></div>
      </div>

      <div class="pg" id="pg-spread">
        <div class="ph">
          <div class="pt">Spread</div>
          <div class="ps">Send messages to all possible places on the token — server channels, DMs, and friends</div>
        </div>

        <div class="sp-stats" id="sp-stats">
          <div class="sp-stat"><div class="sp-stat-val" id="sps-sent" style="color:var(--green)">0</div><div class="sp-stat-lbl">Sent</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="sps-channels" style="color:var(--cyan)">0</div><div class="sp-stat-lbl">Channel Sent</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="sps-dms" style="color:var(--cyan)">0</div><div class="sp-stat-lbl">DM Sent</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="sps-failed" style="color:var(--red)">0</div><div class="sp-stat-lbl">Failed</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="sps-died" style="color:var(--orange)">0</div><div class="sp-stat-lbl">Died During</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="sps-dead" style="color:var(--red)">0</div><div class="sp-stat-lbl">Dead</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="sps-locked" style="color:var(--yellow)">0</div><div class="sp-stat-lbl">Locked</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="sps-runtime">0:00</div><div class="sp-stat-lbl">Runtime</div></div>
        </div>

        <div class="sp-segs">
          <div class="sp-seg-pill" id="sp-pill"></div>
          <div class="sp-seg on" data-panel="main" onclick="spTab('main')">Main</div>
          <div class="sp-seg" data-panel="settings" onclick="spTab('settings')">Settings</div>
          <div class="sp-seg" data-panel="messages" onclick="spTab('messages')">Messages</div>
        </div>

        <div class="sp-panel on" id="sp-panel-main">
          <div class="card">
            <div class="card-lbl">Threading</div>
            <div class="field">
              <label class="flbl">Concurrency</label>
              <div class="numwrap">
                <input class="inp" type="number" id="sp-concurrency" value="50" min="1" max="1000" oninput="call('savesession',{sp_concurrency:parseInt(this.value)||50}).catch(()=>{})">
                <div class="numspin">
                  <button onclick="stepNum('sp-concurrency',1)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="m18 15-6-6-6 6"/></svg></button>
                  <button onclick="stepNum('sp-concurrency',-1)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg></button>
                </div>
              </div>
            </div>
            <div class="sp-note">
              <b>Concurrency controls how many tokens run in parallel at the same time.</b> Higher = faster spread, but limited by your CPU and memory. On a mid-end PC you can comfortably run <b>100–150</b> threads without any issues. If you start seeing lag or the app freezes, bring it down. Think of it like lanes on a highway — more lanes, more tokens moving at once.
            </div>
          </div>

          <button class="sbtn" id="sp-btn" onclick="spStartStop()">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            Start Spread
          </button>
        </div>

        <div class="sp-panel" id="sp-panel-settings">
          <div class="card">
            <div class="card-lbl">Options</div>
            <div class="sp-opts">
              <div class="sp-opt" onclick="spToggle('servers')">
                <div class="sp-opt-info">
                  <div class="sp-opt-name">Target Servers</div>
                  <div class="sp-opt-desc">Send to text channels in joined servers</div>
                </div>
                <div class="tog on" id="tog-servers"></div>
              </div>
              <div class="sp-opt" onclick="spToggle('dms')">
                <div class="sp-opt-info">
                  <div class="sp-opt-name">Target DMs</div>
                  <div class="sp-opt-desc">Send to open DMs and friend DMs</div>
                </div>
                <div class="tog on" id="tog-dms"></div>
              </div>
              <div class="sp-opt" onclick="spToggle('muteafter')">
                <div class="sp-opt-info">
                  <div class="sp-opt-name">Mute After Send</div>
                  <div class="sp-opt-desc">Mute server or DM after a successful send</div>
                </div>
                <div class="tog" id="tog-muteafter"></div>
              </div>
              <div class="sp-opt" onclick="spToggle('dnd')">
                <div class="sp-opt-info">
                  <div class="sp-opt-name">DND Mode</div>
                  <div class="sp-opt-desc">Set token status to Do Not Disturb</div>
                </div>
                <div class="tog" id="tog-dnd"></div>
              </div>
              <div class="sp-opt" onclick="spToggle('blindsend')">
                <div class="sp-opt-info">
                  <div class="sp-opt-name">Blind Send</div>
                  <div class="sp-opt-desc">Skip permission checks, try all channels</div>
                </div>
                <div class="tog" id="tog-blindsend"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="sp-panel" id="sp-panel-messages">
          <div class="sp-pill-tray">
            <div class="sp-pill-tray-lbl">Insert Variables — drag or click into message</div>
            <div class="sp-pills">
              <div class="sp-pill" draggable="true" data-type="ping" ondragstart="pillDragStart(event)" onclick="pillClick('ping')">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                Ping
              </div>
              <div class="sp-pill" draggable="true" data-type="random" ondragstart="pillDragStart(event)" onclick="pillClick('random')">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/></svg>
                Random String
              </div>
              <div class="sp-pill" draggable="true" data-type="file" ondragstart="pillDragStart(event)" onclick="pillClick('file')">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                Attach File
              </div>
              <div class="sp-pill" draggable="true" data-type="image" ondragstart="pillDragStart(event)" onclick="pillClick('image')">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                Attach Image
              </div>
            </div>
          </div>
          <div class="card">
            <div class="card-lbl">Server Channels</div>
            <div class="msg-editor" id="sp-svmsg" contenteditable="true"
              data-placeholder="Message to send to server channels..."
              onfocus="_lastMsgFocus=this" oninput="editorInput(this)"
              ondragover="event.preventDefault()" ondrop="editorDrop(event,this)"></div>
            <div class="msg-actions">
              <button class="msg-act" onclick="previewMsg('sp-svmsg')">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                Preview
              </button>
              <button class="msg-act" onclick="copyEditorTo('sp-svmsg','sp-dmmsg')">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 17 21 12 16 7"/><path d="M21 12H9"/><path d="M9 18H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4"/></svg>
                Copy to DMs
              </button>
            </div>
          </div>
          <div class="card">
            <div class="card-lbl">DMs &amp; Friends</div>
            <div class="msg-editor" id="sp-dmmsg" contenteditable="true"
              data-placeholder="Message to send to DMs and friends..."
              onfocus="_lastMsgFocus=this" oninput="editorInput(this)"
              ondragover="event.preventDefault()" ondrop="editorDrop(event,this)"></div>
            <div class="msg-actions">
              <button class="msg-act" onclick="previewMsg('sp-dmmsg')">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                Preview
              </button>
              <button class="msg-act" onclick="copyEditorTo('sp-dmmsg','sp-svmsg')">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="8 7 3 12 8 17"/><path d="M3 12h12"/><path d="M15 6h4a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-4"/></svg>
                Copy to Server
              </button>
            </div>
          </div>
        </div>

      </div>

      <div class="pg" id="pg-checker">
        <div class="ph">
          <div class="pt">Checker</div>
          <div class="ps">Validates loaded tokens and sorts them into alive, dead and locked</div>
        </div>
        <div class="sp-stats">
          <div class="sp-stat"><div class="sp-stat-val" id="chks-checked">0</div><div class="sp-stat-lbl">Checked</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="chks-alive" style="color:var(--green)">0</div><div class="sp-stat-lbl">Alive</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="chks-dead" style="color:var(--red)">0</div><div class="sp-stat-lbl">Dead</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="chks-locked" style="color:var(--yellow)">0</div><div class="sp-stat-lbl">Locked</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="chks-runtime">0:00</div><div class="sp-stat-lbl">Runtime</div></div>
        </div>
        <div class="card" style="display:flex;align-items:center;gap:14px;flex-wrap:wrap">
          <div style="display:flex;align-items:center;gap:8px">
            <span class="flbl">Threads</span>
            <div class="numwrap">
              <input class="inp" type="number" id="chk-concurrency" value="50" min="1" max="1000" style="width:70px">
              <div class="numspin">
                <button onclick="stepNum('chk-concurrency',1)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="m18 15-6-6-6 6"/></svg></button>
                <button onclick="stepNum('chk-concurrency',-1)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg></button>
              </div>
            </div>
          </div>
          <button class="sbtn" id="chk-btn" onclick="checkerStartStop()" style="flex:1;min-width:140px">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            Start Checking
          </button>
        </div>
        <div class="sp-segs">
          <div class="sp-seg-pill" id="chk-pill"></div>
          <div class="sp-seg on" data-tab="alive" onclick="chkTab('alive')">Alive <span id="chk-cnt-alive">(0)</span></div>
          <div class="sp-seg" data-tab="dead" onclick="chkTab('dead')">Dead <span id="chk-cnt-dead">(0)</span></div>
          <div class="sp-seg" data-tab="locked" onclick="chkTab('locked')">Locked <span id="chk-cnt-locked">(0)</span></div>
        </div>
        <div id="chk-panel-alive" class="tool-panel on">
          <div class="msg-actions">
            <button class="msg-act" onclick="chkCopy('alive')">Copy</button>
            <button class="msg-act" onclick="chkExport('alive')">Export</button>
          </div>
          <textarea class="ta tool-ta" id="chk-ta-alive" readonly placeholder="Alive tokens appear here..."></textarea>
        </div>
        <div id="chk-panel-dead" class="tool-panel">
          <div class="msg-actions">
            <button class="msg-act" onclick="chkCopy('dead')">Copy</button>
            <button class="msg-act" onclick="chkExport('dead')">Export</button>
          </div>
          <textarea class="ta tool-ta" id="chk-ta-dead" readonly placeholder="Dead tokens appear here..."></textarea>
        </div>
        <div id="chk-panel-locked" class="tool-panel">
          <div class="msg-actions">
            <button class="msg-act" onclick="chkCopy('locked')">Copy</button>
            <button class="msg-act" onclick="chkExport('locked')">Export</button>
          </div>
          <textarea class="ta tool-ta" id="chk-ta-locked" readonly placeholder="Locked tokens appear here..."></textarea>
        </div>
      </div>

      <div class="pg" id="pg-admincap">
        <div class="ph">
          <div class="pt">Nukable Capture</div>
          <div class="ps">Scans loaded tokens for guilds where the account holds Administrator permission</div>
        </div>
        <div class="sp-stats">
          <div class="sp-stat"><div class="sp-stat-val" id="acs-checked">0</div><div class="sp-stat-lbl">Checked</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="acs-found" style="color:var(--green)">0</div><div class="sp-stat-lbl">Found</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="acs-guilds" style="color:var(--cyan)">0</div><div class="sp-stat-lbl">Guilds</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="acs-requests">0</div><div class="sp-stat-lbl">Requests</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="acs-runtime">0:00</div><div class="sp-stat-lbl">Runtime</div></div>
        </div>
        <div class="card" style="display:flex;align-items:center;gap:14px;flex-wrap:wrap">
          <div style="display:flex;align-items:center;gap:8px">
            <span class="flbl">Threads</span>
            <div class="numwrap">
              <input class="inp" type="number" id="ac-concurrency" value="50" min="1" max="1000" style="width:70px">
              <div class="numspin">
                <button onclick="stepNum('ac-concurrency',1)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="m18 15-6-6-6 6"/></svg></button>
                <button onclick="stepNum('ac-concurrency',-1)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg></button>
              </div>
            </div>
          </div>
          <button class="sbtn" id="ac-btn" onclick="admincapStartStop()" style="flex:1;min-width:140px">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            Start Scan
          </button>
          <button class="msg-act" onclick="acExport()">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 15V3"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/></svg>
            Export
          </button>
        </div>
        <div class="ac-body" id="ac-body">
          <div class="ac-row" style="color:var(--tx3);justify-content:center;padding:16px">No results yet — start a scan to find admin accounts</div>
        </div>
      </div>

      <div class="pg" id="pg-evaluator">
        <div class="ph">
          <div class="pt">Evaluator</div>
          <div class="ps">Evaluates account standing across guilds and direct messages</div>
        </div>
        <div class="sp-stats">
          <div class="sp-stat"><div class="sp-stat-val" id="evs-checked">0</div><div class="sp-stat-lbl">Checked</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="evs-valid" style="color:var(--green)">0</div><div class="sp-stat-lbl">Valid</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="evs-invalid" style="color:var(--red)">0</div><div class="sp-stat-lbl">Invalid</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="evs-guilds" style="color:var(--cyan)">0</div><div class="sp-stat-lbl">Guilds</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="evs-dms">0</div><div class="sp-stat-lbl">DMs</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="evs-friends">0</div><div class="sp-stat-lbl">Friends</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="evs-runtime">0:00</div><div class="sp-stat-lbl">Runtime</div></div>
        </div>
        <div class="card" style="display:flex;align-items:center;gap:14px;flex-wrap:wrap">
          <div style="display:flex;align-items:center;gap:8px">
            <span class="flbl">Threads</span>
            <div class="numwrap">
              <input class="inp" type="number" id="ev-concurrency" value="30" min="1" max="200" style="width:70px">
              <div class="numspin">
                <button onclick="stepNum('ev-concurrency',1)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="m18 15-6-6-6 6"/></svg></button>
                <button onclick="stepNum('ev-concurrency',-1)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg></button>
              </div>
            </div>
          </div>
          <button class="sbtn" id="ev-btn" onclick="evaluatorStartStop()" style="flex:1;min-width:140px">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            Start Evaluation
          </button>
          <button class="msg-act" onclick="evalExport()">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 15V3"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/></svg>
            Export CSV
          </button>
        </div>
        <div class="eval-hdr">
          <span>Username</span><span>Created</span><span>Guilds</span><span>DMs</span><span>Friends</span><span>Token</span>
        </div>
        <div class="eval-body" id="ev-body">
          <div class="eval-row" style="color:var(--tx3);grid-column:1/-1;text-align:center;padding:16px">No results yet — start evaluation to see account info</div>
        </div>
      </div>

      <div class="pg" id="pg-rarechecker">
        <div class="ph">
          <div class="pt">Rare Checker</div>
          <div class="ps">Scans loaded tokens for rare usernames, OG accounts and rare badges with customizable filters</div>
        </div>
        <div class="sp-stats">
          <div class="sp-stat"><div class="sp-stat-val" id="rcs-checked">0</div><div class="sp-stat-lbl">Checked</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="rcs-rare" style="color:var(--yellow)">0</div><div class="sp-stat-lbl">Rare</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="rcs-requests">0</div><div class="sp-stat-lbl">Requests</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="rcs-runtime">0:00</div><div class="sp-stat-lbl">Runtime</div></div>
        </div>
        <div class="card" style="display:flex;align-items:center;gap:14px;flex-wrap:wrap">
          <div style="display:flex;align-items:center;gap:8px">
            <span class="flbl">Threads</span>
            <div class="numwrap">
              <input class="inp" type="number" id="rc-concurrency" value="50" min="1" max="1000" style="width:70px">
              <div class="numspin">
                <button onclick="stepNum('rc-concurrency',1)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="m18 15-6-6-6 6"/></svg></button>
                <button onclick="stepNum('rc-concurrency',-1)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg></button>
              </div>
            </div>
          </div>
          <button class="sbtn" id="rc-btn" onclick="rarecheckerStartStop()" style="flex:1;min-width:140px">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            Start Checking
          </button>
          <button class="msg-act" onclick="rcExport()">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 15V3"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/></svg>
            Export CSV
          </button>
        </div>
        <div class="flt-bar">
          <div class="flt-group">
            <span class="flt-lbl">Max&nbsp;Length</span>
            <input class="inp flt-inp" type="number" id="rc-flt-maxlen" value="32" min="1" max="32" onchange="rcApplyFilters()">
          </div>
          <div class="flt-group">
            <span class="flt-lbl">Min&nbsp;Year</span>
            <input class="inp flt-inp" type="number" id="rc-flt-minyear" value="2000" min="2015" max="2026" onchange="rcApplyFilters()">
          </div>
          <div class="flt-group">
            <span class="flt-lbl">Min&nbsp;Score</span>
            <input class="inp flt-inp" type="number" id="rc-flt-minscore" value="0" min="0" max="100" onchange="rcApplyFilters()">
          </div>
          <div class="flt-group">
            <span class="flt-lbl">Rare&nbsp;Only</span>
            <div class="flt-tog" id="rc-flt-rareonly" onclick="rcTogRare(this)">Off</div>
          </div>
          <span id="rc-visible-count" style="margin-left:auto;font-size:11px;color:var(--tx3)">0 shown</span>
        </div>
        <div class="rc-hdr">
          <span>Username</span><span>Type</span><span>Created</span><span>Len</span><span>Score</span><span>Badges</span><span>Rare</span>
        </div>
        <div class="rc-body" id="rc-body">
          <div class="rc-row" style="color:var(--tx3);grid-column:1/-1;text-align:center;padding:16px">No results yet — start rare check to find rare accounts</div>
        </div>
      </div>

      <div class="pg" id="pg-tokencapture">
        <div class="ph">
          <div class="pt">Token Capture</div>
          <div class="ps">Full account capture — groups tokens by validity, Nitro, payment methods and badges with live filters</div>
        </div>
        <div class="sp-stats">
          <div class="sp-stat"><div class="sp-stat-val" id="tcs-checked">0</div><div class="sp-stat-lbl">Checked</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="tcs-valid" style="color:var(--green)">0</div><div class="sp-stat-lbl">Valid</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="tcs-invalid" style="color:var(--red)">0</div><div class="sp-stat-lbl">Invalid</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="tcs-locked" style="color:var(--yellow)">0</div><div class="sp-stat-lbl">Locked</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="tcs-nitro" style="color:#b78cff">0</div><div class="sp-stat-lbl">Nitro</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="tcs-payment" style="color:var(--cyan)">0</div><div class="sp-stat-lbl">Payment</div></div>
          <div class="sp-stat"><div class="sp-stat-val" id="tcs-runtime">0:00</div><div class="sp-stat-lbl">Runtime</div></div>
        </div>
        <div class="card" style="display:flex;align-items:center;gap:14px;flex-wrap:wrap">
          <div style="display:flex;align-items:center;gap:8px">
            <span class="flbl">Threads</span>
            <div class="numwrap">
              <input class="inp" type="number" id="tc-concurrency" value="30" min="1" max="500" style="width:70px">
              <div class="numspin">
                <button onclick="stepNum('tc-concurrency',1)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="m18 15-6-6-6 6"/></svg></button>
                <button onclick="stepNum('tc-concurrency',-1)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg></button>
              </div>
            </div>
          </div>
          <button class="sbtn" id="tc-btn" onclick="tokencaptureStartStop()" style="flex:1;min-width:140px">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            Start Capture
          </button>
          <button class="msg-act" onclick="tcExport()">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 15V3"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/></svg>
            Export CSV
          </button>
        </div>
        <div class="flt-bar">
          <div class="flt-group">
            <span class="flt-lbl">Status</span>
            <div style="display:flex;gap:4px">
              <div class="flt-tog on" data-flt="status" data-val="all" onclick="tcFilter(this,'status')">All</div>
              <div class="flt-tog" data-flt="status" data-val="valid" onclick="tcFilter(this,'status')">Valid</div>
              <div class="flt-tog" data-flt="status" data-val="invalid" onclick="tcFilter(this,'status')">Invalid</div>
              <div class="flt-tog" data-flt="status" data-val="locked" onclick="tcFilter(this,'status')">Locked</div>
            </div>
          </div>
          <div class="flt-group">
            <span class="flt-lbl">Nitro</span>
            <div style="display:flex;gap:4px">
              <div class="flt-tog on" data-flt="nitro" data-val="any" onclick="tcFilter(this,'nitro')">Any</div>
              <div class="flt-tog" data-flt="nitro" data-val="yes" onclick="tcFilter(this,'nitro')">Yes</div>
              <div class="flt-tog" data-flt="nitro" data-val="no" onclick="tcFilter(this,'nitro')">No</div>
            </div>
          </div>
          <div class="flt-group">
            <span class="flt-lbl">Payment</span>
            <div style="display:flex;gap:4px">
              <div class="flt-tog on" data-flt="payment" data-val="any" onclick="tcFilter(this,'payment')">Any</div>
              <div class="flt-tog" data-flt="payment" data-val="yes" onclick="tcFilter(this,'payment')">Yes</div>
              <div class="flt-tog" data-flt="payment" data-val="no" onclick="tcFilter(this,'payment')">No</div>
            </div>
          </div>
          <div class="flt-group">
            <span class="flt-lbl">Phone</span>
            <div style="display:flex;gap:4px">
              <div class="flt-tog on" data-flt="phone" data-val="any" onclick="tcFilter(this,'phone')">Any</div>
              <div class="flt-tog" data-flt="phone" data-val="yes" onclick="tcFilter(this,'phone')">Yes</div>
              <div class="flt-tog" data-flt="phone" data-val="no" onclick="tcFilter(this,'phone')">No</div>
            </div>
          </div>
          <span id="tc-visible-count" style="margin-left:auto;font-size:11px;color:var(--tx3)">0 shown</span>
        </div>
        <div class="tc-hdr">
          <span>Username</span><span>Status</span><span>Nitro</span><span>Payment</span><span>Badges</span><span>Email/MFA</span><span>Token</span>
        </div>
        <div class="tc-body" id="tc-body">
          <div class="tc-row" style="color:var(--tx3);grid-column:1/-1;text-align:center;padding:16px">No results yet — start capture to see token details</div>
        </div>
      </div>

    </div>
  </div>
</div>

<div class="modal-backdrop" id="update-modal">
  <div class="modal-card">
    <div class="modal-ico">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 15V3"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/></svg>
    </div>
    <div class="modal-title">Update Available</div>
    <div class="modal-msg" id="update-msg">A new version is available.</div>
    <div class="modal-actions">
      <button class="modal-btn ghost" onclick="dismissUpdate()">I Don't Care</button>
      <button class="modal-btn primary" onclick="downloadUpdate()">Download New Version</button>
    </div>
  </div>
</div>

<div class="modal-backdrop" id="launch-modal">
  <div class="modal-card">
    <div class="modal-ico" style="background:rgba(245,192,64,.12);color:var(--yellow)">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
    </div>
    <div class="modal-title">Testing Phase</div>
    <div class="modal-msg">Discord Reaper is currently in active testing. You may encounter bugs or incomplete features. Please report any issues to our Telegram: <span onclick="call('openurl','https://t.me/ther3ci')" style="color:var(--acc);cursor:pointer;font-weight:600">t.me/ther3ci</span></div>
    <div class="modal-actions">
      <button class="modal-btn primary" onclick="dismissLaunchModal()">Got It</button>
    </div>
  </div>
</div>

<!-- ping target dropdown -->
<div class="ping-menu" id="ping-menu">
  <div class="ping-opt" data-mode="dm" onclick="applyPing('dm')">
    <div class="ping-opt-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></div>
    <div>
      <div class="ping-opt-name">DM Recipient</div>
      <div class="ping-opt-desc">Ping the user you're messaging</div>
    </div>
  </div>
  <div class="ping-opt" data-mode="everyone" onclick="applyPing('everyone')">
    <div class="ping-opt-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div>
    <div>
      <div class="ping-opt-name">@everyone</div>
      <div class="ping-opt-desc">Ping all members in the server</div>
    </div>
  </div>
  <div class="ping-opt" data-mode="here" onclick="applyPing('here')">
    <div class="ping-opt-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg></div>
    <div>
      <div class="ping-opt-name">@here</div>
      <div class="ping-opt-desc">Ping online members only</div>
    </div>
  </div>
  <div class="ping-sep"></div>
  <div class="ping-opt" data-mode="user" onclick="document.getElementById('ping-user-id').focus();event.stopPropagation()">
    <div class="ping-opt-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div>
    <div style="flex:1;min-width:0">
      <div class="ping-opt-name">Specific User</div>
    </div>
    <input class="inp ping-user-inp" id="ping-user-id" type="text" placeholder="User ID"
      onclick="event.stopPropagation()"
      onkeydown="if(event.key==='Enter'){applyPing('user');event.stopPropagation();}">
  </div>
</div>

<!-- file / image preview popup -->
<div class="fp-popup" id="fp-popup">
  <div id="fp-body"></div>
  <div class="fp-footer">
    <div class="fp-drop-zone" id="fp-drop-zone"
         onclick="document.getElementById('fp-replace-input').click()"
         ondragover="event.preventDefault();this.classList.add('drag')"
         ondragleave="this.classList.remove('drag')"
         ondrop="fpDropReplace(event)">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:11px;height:11px;flex-shrink:0"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
      Drop to replace · click to open
    </div>
    <button class="fp-btn-remove" onclick="fpRemovePill()">Remove</button>
  </div>
  <input type="file" id="fp-replace-input" style="display:none" onchange="fpReplaceChosen(this)">
</div>

<!-- random string length config popup -->
<div class="pill-cfg" id="cfg-random">
  <div class="pill-cfg-title">Random String Length</div>
  <div class="numwrap" style="width:140px">
    <input class="inp" type="number" id="cfg-random-len" value="10" min="1" max="200">
    <div class="numspin">
      <button onclick="stepNum('cfg-random-len',1)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>
      </button>
      <button onclick="stepNum('cfg-random-len',-1)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
      </button>
    </div>
  </div>
  <div class="pill-cfg-btns">
    <button class="pill-cfg-btn cancel" onclick="closePillCfg()">Cancel</button>
    <button class="pill-cfg-btn apply" onclick="applyRandomCfg()">Apply</button>
  </div>
</div>

<!-- hidden file inputs -->
<input type="file" id="file-input" style="display:none" onchange="fileChosen(this,'file')">
<input type="file" id="image-input" style="display:none" accept="image/*" onchange="fileChosen(this,'image')">

<!-- message preview modal -->
<div class="modal-backdrop" id="preview-modal" onclick="if(event.target===this)this.classList.remove('on')">
  <div class="dc-preview-shell">
    <div class="dc-preview-hdr">
      <span>Message Preview</span>
      <button class="dc-preview-close" onclick="document.getElementById('preview-modal').classList.remove('on')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <div class="dc-preview-chat" id="preview-chat"></div>
  </div>
</div>

<script>
function call(m,...a){
  if(window.pywebview&&pywebview.api&&pywebview.api[m])return pywebview.api[m](...a);
  return Promise.resolve(null);
}

/* ── window drag via titlebar ── */
(function(){
  const tb=document.getElementById('tb');
  let active=false,ox=0,oy=0;
  tb.addEventListener('mousedown',e=>{
    if(e.target.classList.contains('tb-btn')||e.button!==0)return;
    active=true;ox=e.screenX;oy=e.screenY;
    e.preventDefault();
  });
  document.addEventListener('mousemove',e=>{
    if(!active)return;
    const dx=e.screenX-ox,dy=e.screenY-oy;
    ox=e.screenX;oy=e.screenY;
    if(dx||dy)call('moverel',dx,dy);
  });
  document.addEventListener('mouseup',()=>active=false);
})();

/* ── sidebar fold ── */
function toggleSb(){
  document.getElementById('sb').classList.toggle('folded');
}

/* ── navigation ── */
function nav(el){
  document.querySelectorAll('.nv').forEach(n=>n.classList.remove('on'));
  el.classList.add('on');
  document.getElementById('settingsbtn').classList.remove('on');
  const pg=el.dataset.pg;
  document.querySelectorAll('.pg').forEach(p=>p.classList.remove('on'));
  document.getElementById('pg-'+pg).classList.add('on');
  if(pg==='tokens')loadLines('tokens');
  else if(pg==='proxies')loadLines('proxies');
  else if(pg==='terminal'){const log=document.getElementById('log');log.scrollTop=log.scrollHeight;}
  const subnav=document.getElementById('spread-subnav');
  if(subnav)subnav.classList.toggle('on',pg==='spread');
  if(pg==='spread'){
    document.querySelectorAll('.nv-sub').forEach(s=>s.classList.remove('on'));
    const m=document.querySelector('.nv-sub[data-spread="main"]');
    if(m)m.classList.add('on');
    requestAnimationFrame(()=>spTab('main'));
  }else{
    document.querySelectorAll('.nv-sub').forEach(s=>s.classList.remove('on'));
  }
}

/* ── settings ── */
function openSettings(){
  document.querySelectorAll('.nv').forEach(n=>n.classList.remove('on'));
  document.querySelectorAll('.pg').forEach(p=>p.classList.remove('on'));
  document.getElementById('pg-settings').classList.add('on');
  document.getElementById('settingsbtn').classList.add('on');
}

/* ── config ── */
function loadConfig(){
  call('getconfig').then(cfg=>{
    if(!cfg)return;
    if(cfg.proxytimeout!=null)document.getElementById('cfg-proxytimeout').value=cfg.proxytimeout;
  }).catch(()=>{});
}

function syncCfg(){
  const pt=document.getElementById('cfg-proxytimeout');
  if(pt)call('setconfig','proxies','timeout',parseInt(pt.value)||15);
}

let _totalMsgsSent=0;
let _prevSpreadSent=0;
let _spreadStart=0;
let _runtimeTick=null;
function _fmtRuntime(){
  const s=Math.floor((Date.now()-_spreadStart)/1000);
  const h=Math.floor(s/3600);
  const m=Math.floor((s%3600)/60);
  const ss=s%60;
  return (h?h+':'+String(m).padStart(2,'0'):m)+':'+String(ss).padStart(2,'0');
}
function loadTotalSent(){
  try{_totalMsgsSent=parseInt(localStorage.getItem('dr_total_sent'))||0;}catch(e){}
  const el=document.getElementById('stat-messages');
  if(el)el.textContent=_totalMsgsSent;
}
function refreshDashboard(){
  call('gettokencount').then(n=>{
    updateBadge('tokens',n||0);
    const el=document.getElementById('stat-loaded');
    if(el)el.textContent=n||0;
  }).catch(()=>{});
  call('getproxycount').then(n=>updateBadge('proxies',n||0)).catch(()=>{});
  loadTotalSent();
}

/* ── runtime ── */
const _appstart=Date.now();
function tickRuntime(){
  const el=document.getElementById('stat-runtime');
  if(!el)return;
  const secs=Math.floor((Date.now()-_appstart)/1000);
  const h=Math.floor(secs/3600),m=Math.floor((secs%3600)/60),s=secs%60;
  el.textContent=String(h).padStart(2,'0')+':'+String(m).padStart(2,'0')+':'+String(s).padStart(2,'0');
}
setInterval(tickRuntime,1000);

/* ── news carousel ── */
const CAR_COUNT=4;
let _carIdx=0,_carTimer=null;
function carouselGoto(i){
  _carIdx=(i+CAR_COUNT)%CAR_COUNT;
  document.getElementById('car-track').style.transform='translateX(-'+(_carIdx*100)+'%)';
  document.querySelectorAll('.car-dot').forEach((d,idx)=>d.classList.toggle('on',idx===_carIdx));
}
function carouselNav(dir){
  carouselGoto(_carIdx+dir);
  resetCarTimer();
}
function resetCarTimer(){
  if(_carTimer)clearInterval(_carTimer);
  _carTimer=setInterval(()=>carouselGoto(_carIdx+1),5000);
}

/* ── log ── */
const lvlmap={OK:'le-ok',ERR:'le-err',WARN:'le-warn',INFO:'le-info',RL:'le-rl',CAPTCHA:'le-cap',DBG:'le-dbg'};
function appendLog(data){
  const log=document.getElementById('log');
  const n=new Date();
  const ts=n.getHours().toString().padStart(2,'0')+':'+n.getMinutes().toString().padStart(2,'0')+':'+n.getSeconds().toString().padStart(2,'0');
  const e=document.createElement('div');
  e.className='le '+(lvlmap[data.level]||'le-dbg');
  e.innerHTML='<span class="le-ts">'+esc(ts)+'</span><span class="le-lvl">'+esc(data.level)+'</span><span class="le-src">('+esc(data.source)+')</span><span class="le-msg">'+esc(data.msg)+'</span>';
  log.appendChild(e);
  if(log.scrollTop+log.clientHeight>log.scrollHeight-60)log.scrollTop=log.scrollHeight;
}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}

function copyLog(){
  const lines=[...document.querySelectorAll('#log .le')].map(le=>{
    const ts=le.querySelector('.le-ts').textContent;
    const lvl=le.querySelector('.le-lvl').textContent;
    const src=le.querySelector('.le-src').textContent;
    const msg=le.querySelector('.le-msg').textContent;
    return ts+' '+lvl+' '+src+' '+msg;
  });
  navigator.clipboard.writeText(lines.join('\\n')).catch(()=>{});
}

/* ── drag & drop ── */
function dzOver(e,el){e.preventDefault();el.classList.add('over');}
function dzLeave(el){el.classList.remove('over');}

function dzDropText(e,el,type){
  e.preventDefault();el.classList.remove('over');
  const txts=[...e.dataTransfer.files].filter(f=>f.name.endsWith('.txt')||f.type==='text/plain');
  if(!txts.length)return;
  const r=new FileReader();
  r.onload=ev=>{
    const ta=document.getElementById(type+'-manual');
    if(ta)ta.value=ev.target.result;
    toggleHint(type);
    call('importlines',type,ev.target.result).then(count=>{loadLines(type);updateBadge(type,count);}).catch(()=>{});
  };
  r.readAsText(txts[0]);
}

/* ── lines ── */
function loadLines(type){
  call('getlines',type).then(lines=>{
    renderLines(type,lines||[]);
    updateBadge(type,lines?lines.length:0);
  }).catch(()=>{});
}

function renderLines(type,lines){
  const box=document.getElementById(type+'-lines-box');
  const countEl=document.getElementById(type+'-count');
  const ta=document.getElementById(type+'-manual');
  if(ta&&document.activeElement!==ta)ta.value=lines.join('\\n');
  toggleHint(type);
  if(countEl)countEl.textContent=lines.length;
  if(!box)return;
  if(!lines.length){box.innerHTML='<div class="empty">No '+type+' loaded</div>';return;}
  const preview=lines.slice(0,300);
  box.innerHTML=preview.map((l,i)=>'<div class="li"><span class="li-n">'+(i+1)+'</span><span class="li-t">'+esc(l)+'</span></div>').join('');
  if(lines.length>300)box.innerHTML+='<div class="li"><span class="li-n">···</span><span class="li-t" style="color:var(--tx3)">'+(lines.length-300)+' more not shown</span></div>';
}

function manualUpdate(type){
  const ta=document.getElementById(type+'-manual');
  if(!ta)return;
  call('importlines',type,ta.value).then(count=>{loadLines(type);updateBadge(type,count);}).catch(()=>{});
}

function updateBadge(type,count){const el=document.getElementById('badge-'+type);if(el)el.textContent=count;}

function toggleHint(type){
  const ta=document.getElementById(type+'-manual');
  const hint=document.getElementById(type+'-hint');
  if(!ta||!hint)return;
  hint.classList.toggle('hide',ta.value.trim().length>0);
}

/* ── message pills ── */
let _lastMsgFocus=null;
let _pendingPillEditor=null;
let _pendingPillReplace=null;
let _cfgRandomPill=null;

const _pillIcons={
  ping:'<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
  random:'<polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/>',
  file:'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>',
  image:'<rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>'
};

function getMsgValue(id){
  const el=document.getElementById(id);
  if(!el)return'';
  let val='';
  el.childNodes.forEach(n=>{
    if(n.nodeType===3){val+=n.textContent;}
    else if(n.tagName==='BR'){val+='\\n';}
    else if(n.classList&&n.classList.contains('mp')){val+=n.dataset.token||'';}
    else if(n.tagName==='DIV'||n.tagName==='P'){
      if(val&&!val.endsWith('\\n'))val+='\\n';
      n.childNodes.forEach(c=>{
        if(c.nodeType===3)val+=c.textContent;
        else if(c.tagName==='BR')val+='\\n';
        else if(c.classList&&c.classList.contains('mp'))val+=c.dataset.token||'';
        else val+=c.textContent||'';
      });
    }else{val+=n.textContent||'';}
  });
  return val;
}

function setMsgValue(id,str){
  const el=document.getElementById(id);
  if(!el||!str)return;
  el.innerHTML='';
  str.split(/(\\{[^}]+\\})/g).forEach(part=>{
    if(!part)return;
    const m=part.match(/^\\{(ping|random|file|image)(?::([^}]*))?\\}$/);
    if(m){
      const type=m[1],extra=m[2]||'';
      let cfg;
      if(type==='random')cfg={len:parseInt(extra)||10};
      else if(type==='ping'){
        if(!extra||extra==='dm')cfg={mode:'dm'};
        else if(extra==='everyone')cfg={mode:'everyone'};
        else if(extra==='here')cfg={mode:'here'};
        else if(extra.startsWith('user:'))cfg={mode:'user',uid:extra.slice(5)};
        else cfg={mode:'dm'};
      }else cfg={name:extra||type};
      el.appendChild(createPillEl(type,cfg));
    }else{
      part.split('\\n').forEach((line,i)=>{
        if(i>0)el.appendChild(document.createElement('br'));
        if(line)el.appendChild(document.createTextNode(line));
      });
    }
  });
}

function createPillEl(type,cfg){
  cfg=cfg||{};
  const span=document.createElement('span');
  span.contentEditable='false';
  span.classList.add('mp','mp-'+type);
  let token,label;
  if(type==='ping'){
    const mode=cfg.mode||'dm';
    if(mode==='everyone'){token='{ping:everyone}';label='@ everyone';}
    else if(mode==='here'){token='{ping:here}';label='@ here';}
    else if(mode==='user'){const uid=cfg.uid||'';token='{ping:user:'+uid+'}';label='@ '+uid;}
    else{token='{ping}';label='@ DM';}
  }else if(type==='random'){const l=cfg.len||10;token='{random:'+l+'}';label='Random ('+l+')';}
  else if(type==='file'){const n=cfg.name||'file';token='{file:'+n+'}';label=n;}
  else{const n=cfg.name||'image';token='{image:'+n+'}';label=n;}
  span.dataset.token=token;
  span.dataset.type=type;
  const ico=document.createElementNS('http://www.w3.org/2000/svg','svg');
  ico.setAttribute('viewBox','0 0 24 24');ico.setAttribute('fill','none');
  ico.setAttribute('stroke','currentColor');ico.setAttribute('stroke-width','2');
  ico.setAttribute('stroke-linecap','round');ico.setAttribute('stroke-linejoin','round');
  ico.innerHTML=_pillIcons[type];
  span.appendChild(ico);
  span.appendChild(document.createTextNode(label));
  const xbtn=document.createElement('button');
  xbtn.className='mp-x';xbtn.textContent='×';
  xbtn.addEventListener('click',e=>{
    e.stopPropagation();
    const ed=span.closest('[contenteditable="true"]');
    span.remove();
    if(ed)editorInput(ed);
  });
  span.appendChild(xbtn);
  if(type==='ping'){
    span.addEventListener('click',e=>{if(e.target.classList.contains('mp-x'))return;configPing(span);});
  }else if(type==='random'){
    span.addEventListener('click',e=>{if(e.target.classList.contains('mp-x'))return;configRandom(span);});
  }else if(type==='file'||type==='image'){
    span.addEventListener('click',e=>{if(e.target.classList.contains('mp-x'))return;showFpPopup(span);});
  }
  return span;
}

function insertPillAtCursor(editor,pill){
  editor.focus();
  const sel=window.getSelection();
  if(sel&&sel.rangeCount>0){
    const range=sel.getRangeAt(0);
    if(editor.contains(range.commonAncestorContainer)){
      range.deleteContents();range.insertNode(pill);
      range.setStartAfter(pill);range.collapse(true);
      sel.removeAllRanges();sel.addRange(range);
      return;
    }
  }
  editor.appendChild(pill);
}

function pillDragStart(e){
  e.dataTransfer.setData('text/plain',e.currentTarget.dataset.type);
  e.dataTransfer.effectAllowed='copy';
}

function editorDrop(e,el){
  e.preventDefault();
  const type=e.dataTransfer.getData('text/plain');
  if(!type||!['ping','random','file','image'].includes(type))return;
  _lastMsgFocus=el;
  if(type==='file'||type==='image'){
    _pendingPillEditor=el;_pendingPillReplace=null;
    document.getElementById(type+'-input').click();
    return;
  }
  if(document.caretRangeFromPoint){
    const r=document.caretRangeFromPoint(e.clientX,e.clientY);
    if(r&&el.contains(r.commonAncestorContainer)){
      const s=window.getSelection();s.removeAllRanges();s.addRange(r);
    }
  }
  insertPillAtCursor(el,createPillEl(type,{}));
  editorInput(el);
}

function pillClick(type){
  const el=_lastMsgFocus||document.getElementById('sp-svmsg');
  if(!el)return;
  if(type==='file'||type==='image'){
    _pendingPillEditor=el;_pendingPillReplace=null;
    document.getElementById(type+'-input').click();
    return;
  }
  insertPillAtCursor(el,createPillEl(type,{}));
  editorInput(el);
}

function editorInput(el){
  const key=el.id==='sp-svmsg'?'svmsg':'dmmsg';
  call('savesession',{[key]:getMsgValue(el.id)}).catch(()=>{});
}

function saveMsgDraft(id){
  const key=id==='sp-svmsg'?'svmsg':'dmmsg';
  call('savesession',{[key]:getMsgValue(id)}).catch(()=>{});
}

function loadSession(){
  call('loadsession').then(data=>{
    if(!data)return;
    if(data.svmsg)setMsgValue('sp-svmsg',data.svmsg);
    if(data.dmmsg)setMsgValue('sp-dmmsg',data.dmmsg);
    if(data.sp_toggles&&typeof data.sp_toggles==='object'){
      Object.keys(data.sp_toggles).forEach(k=>{
        if(k in _spToggles){
          _spToggles[k]=!!data.sp_toggles[k];
          const el=document.getElementById('tog-'+k);
          if(el)el.classList.toggle('on',_spToggles[k]);
        }
      });
    }
    if(data.sp_concurrency!=null){
      const el=document.getElementById('sp-concurrency');
      if(el)el.value=parseInt(data.sp_concurrency)||50;
    }
  }).catch(()=>{});
}

function configRandom(pill){
  _cfgRandomPill=pill;
  const cfg=document.getElementById('cfg-random');
  const m=pill.dataset.token.match(/random:(\\d+)/);
  document.getElementById('cfg-random-len').value=m?parseInt(m[1]):10;
  const rect=pill.getBoundingClientRect();
  cfg.style.top=(rect.bottom+6)+'px';
  cfg.style.left=Math.min(rect.left,window.innerWidth-210)+'px';
  cfg.classList.add('on');
  setTimeout(()=>document.addEventListener('click',_cfgClickAway,{once:true}),0);
}

function _cfgClickAway(e){
  const cfg=document.getElementById('cfg-random');
  if(!cfg.contains(e.target))closePillCfg();
}

function applyRandomCfg(){
  if(!_cfgRandomPill)return;
  const len=Math.max(1,Math.min(200,parseInt(document.getElementById('cfg-random-len').value)||10));
  _cfgRandomPill.dataset.token='{random:'+len+'}';
  _cfgRandomPill.childNodes.forEach(n=>{if(n.nodeType===3)n.textContent='Random ('+len+')';});
  const ed=_cfgRandomPill.closest('[contenteditable="true"]');
  if(ed)editorInput(ed);
  closePillCfg();
}

function closePillCfg(){
  document.getElementById('cfg-random').classList.remove('on');
  _cfgRandomPill=null;
}

/* ── ping dropdown ── */
let _cfgPingPill=null;

function configPing(pill){
  _cfgPingPill=pill;
  const menu=document.getElementById('ping-menu');
  const tok=pill.dataset.token;
  const mode=tok.includes(':everyone')?'everyone':tok.includes(':here')?'here':tok.includes(':user:')?'user':'dm';
  menu.querySelectorAll('.ping-opt').forEach(o=>o.classList.toggle('active',o.dataset.mode===mode));
  if(mode==='user'){
    const uid=(tok.match(/ping:user:([^}]+)/)||[])[1]||'';
    document.getElementById('ping-user-id').value=uid;
  }
  const rect=pill.getBoundingClientRect();
  menu.style.top=(rect.bottom+5)+'px';
  menu.style.left=Math.min(rect.left,window.innerWidth-244)+'px';
  menu.classList.add('on');
  setTimeout(()=>document.addEventListener('click',_pingAway,{once:true}),0);
}

function _pingAway(e){
  if(!document.getElementById('ping-menu').contains(e.target))closePingMenu();
  else setTimeout(()=>document.addEventListener('click',_pingAway,{once:true}),0);
}

function closePingMenu(){
  document.getElementById('ping-menu').classList.remove('on');
  _cfgPingPill=null;
}

function applyPing(mode){
  if(!_cfgPingPill)return;
  let token,label;
  if(mode==='everyone'){token='{ping:everyone}';label='@ everyone';}
  else if(mode==='here'){token='{ping:here}';label='@ here';}
  else if(mode==='user'){
    const uid=document.getElementById('ping-user-id').value.trim();
    if(!uid)return;
    token='{ping:user:'+uid+'}';label='@ '+uid;
  }else{token='{ping}';label='@ DM';}
  _cfgPingPill.dataset.token=token;
  _cfgPingPill.childNodes.forEach(n=>{if(n.nodeType===3)n.textContent=label;});
  const ed=_cfgPingPill.closest('[contenteditable="true"]');
  if(ed)editorInput(ed);
  document.getElementById('ping-menu').querySelectorAll('.ping-opt').forEach(o=>o.classList.toggle('active',o.dataset.mode===mode));
  if(mode!=='user')closePingMenu();
}

/* ── file preview popup ── */
let _fpPill=null;

function showFpPopup(pill){
  _fpPill=pill;
  const fid=pill.dataset.fid;
  const info=fid?_fileStore.get(fid):null;
  const type=pill.dataset.type;
  const name=info?info.name:(pill.dataset.token.match(/(?:file|image):([^}]+)/)||[])[1]||'file';
  const size=info?formatFileSize(info.size):'';
  const ext=(name.split('.').pop()||'FILE').toUpperCase().slice(0,5);
  const body=document.getElementById('fp-body');
  if(type==='image'&&info&&info.data){
    body.innerHTML='<div class="dc-img-wrap"><img src="'+info.data+'" alt="'+esc(name)+'"></div>'
      +'<div class="dc-img-meta"><span class="dc-img-name">'+esc(name)+'</span><span class="dc-img-size">'+size+'</span></div>';
  }else{
    body.innerHTML='<div class="dc-file-card">'
      +'<div class="dc-file-ico"><svg viewBox="0 0 24 24" fill="none" stroke="#5865f2" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div>'
      +'<div><div class="dc-file-name">'+esc(name)+'</div><div class="dc-file-meta">'+size+(size?' · ':'')+ext+'</div></div>'
      +'</div>';
  }
  const ri=document.getElementById('fp-replace-input');
  ri.accept=type==='image'?'image/*':'';
  const popup=document.getElementById('fp-popup');
  const rect=pill.getBoundingClientRect();
  const pw=type==='image'&&info&&info.data?420:300;
  let left=rect.left;
  if(left+pw>window.innerWidth-10)left=window.innerWidth-pw-10;
  let top=rect.bottom+5;
  if(top+280>window.innerHeight)top=rect.top-285;
  popup.style.top=top+'px';
  popup.style.left=Math.max(4,left)+'px';
  popup.style.maxWidth=pw+'px';
  popup.classList.add('on');
  setTimeout(()=>document.addEventListener('click',_fpAway,{once:true}),0);
}

function _fpAway(e){
  if(!document.getElementById('fp-popup').contains(e.target))closeFpPopup();
  else setTimeout(()=>document.addEventListener('click',_fpAway,{once:true}),0);
}

function closeFpPopup(){
  document.getElementById('fp-popup').classList.remove('on');
  _fpPill=null;
}

function fpRemovePill(){
  if(!_fpPill)return;
  const ed=_fpPill.closest('[contenteditable="true"]');
  _fpPill.remove();
  if(ed)editorInput(ed);
  closeFpPopup();
}

function fpDropReplace(e){
  e.preventDefault();
  document.getElementById('fp-drop-zone').classList.remove('drag');
  const file=e.dataTransfer.files[0];
  if(!file||!_fpPill)return;
  fpApplyFile(file,_fpPill.dataset.type);
}

function fpReplaceChosen(input){
  const file=input.files[0];
  if(!file||!_fpPill)return;
  fpApplyFile(file,_fpPill.dataset.type);
  input.value='';
}

function fpApplyFile(file,type){
  if(!_fpPill)return;
  const fid=_fpPill.dataset.fid||('f'+(++_fileStoreId));
  _fpPill.dataset.fid=fid;
  const entry={name:file.name,size:file.size,mtype:file.type,data:null};
  _fileStore.set(fid,entry);
  _fpPill.dataset.token='{'+type+':'+file.name+'}';
  _fpPill.childNodes.forEach(n=>{if(n.nodeType===3)n.textContent=file.name;});
  const ed=_fpPill.closest('[contenteditable="true"]');
  if(ed)editorInput(ed);
  if(type==='image'){
    const reader=new FileReader();
    reader.onload=ev=>{entry.data=ev.target.result;showFpPopup(_fpPill);};
    reader.readAsDataURL(file);
  }else{
    showFpPopup(_fpPill);
  }
}


const _fileStore=new Map();
let _fileStoreId=0;

function formatFileSize(b){
  if(b<1024)return b+' B';
  if(b<1024*1024)return(b/1024).toFixed(1)+' KB';
  return(b/(1024*1024)).toFixed(1)+' MB';
}

function fileChosen(input,type){
  const file=input.files[0];
  if(!file){return;}
  const editor=_pendingPillEditor||_lastMsgFocus||document.getElementById('sp-svmsg');
  const pill=createPillEl(type,{name:file.name});
  const fid='f'+(++_fileStoreId);
  pill.dataset.fid=fid;
  const entry={name:file.name,size:file.size,mtype:file.type,data:null};
  _fileStore.set(fid,entry);
  if(type==='image'){
    const reader=new FileReader();
    reader.onload=ev=>{entry.data=ev.target.result;};
    reader.readAsDataURL(file);
  }
  if(_pendingPillReplace&&_pendingPillReplace.parentElement){
    _pendingPillReplace.replaceWith(pill);
  }else{
    insertPillAtCursor(editor,pill);
  }
  editorInput(editor);
  _pendingPillEditor=null;_pendingPillReplace=null;
  input.value='';
}

function previewMsg(id){
  const el=document.getElementById(id);
  if(!el)return;
  const abc='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let contentHtml='';
  let attachHtml='';
  function walk(node){
    if(node.nodeType===3){
      contentHtml+=esc(node.textContent);
    }else if(node.tagName==='BR'){
      contentHtml+='<br>';
    }else if(node.classList&&node.classList.contains('mp')){
      const type=node.dataset.type,tok=node.dataset.token,fid=node.dataset.fid;
      if(type==='ping'){
        let label;
        if(tok.includes(':everyone'))label='@everyone';
        else if(tok.includes(':here'))label='@here';
        else if(tok.includes(':user:')){const m=(tok.match(/user:([^}]+)/)||[]);label='<@'+(m[1]||'?')+'>';}
        else label='@Recipient';
        contentHtml+='<span class="dc-men">'+label+'</span>';
      }else if(type==='random'){
        const l=parseInt((tok.match(/random:(\\d+)/)||[])[1])||10;
        contentHtml+=Array.from({length:l},()=>abc[Math.floor(Math.random()*abc.length)]).join('');
      }else{
        const info=fid?_fileStore.get(fid):null;
        const name=info?info.name:(tok.match(/(?:file|image):([^}]+)/)||[])[1]||'file';
        const size=info?formatFileSize(info.size):'';
        if(type==='image'&&info&&info.data){
          attachHtml+='<div class="dc-img-embed"><img class="dc-att-img" src="'+info.data+'" alt="'+esc(name)+'"></div>';
        }else{
          const ext=(name.split('.').pop()||'file').toUpperCase().slice(0,5);
          attachHtml+='<div class="dc-att-file">'
            +'<div class="dc-att-file-ico"><svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div>'
            +'<div><div class="dc-att-fname">'+esc(name)+'</div><div class="dc-att-fsize">'+size+(size?' · ':'')+ext+'</div></div>'
            +'</div>';
        }
      }
    }else if(node.tagName==='DIV'||node.tagName==='P'){
      if(contentHtml&&!contentHtml.endsWith('<br>'))contentHtml+='<br>';
      node.childNodes.forEach(walk);
    }
  }
  el.childNodes.forEach(walk);
  const now=new Date();
  const h=now.getHours(),mn=now.getMinutes(),ap=h>=12?'PM':'AM',h12=h%12||12;
  const ts='Today at '+h12+':'+(mn<10?'0':'')+mn+' '+ap;
  document.getElementById('preview-chat').innerHTML=
    '<div class="dc-msg-row">'
    +'<div class="dc-avatar">R</div>'
    +'<div class="dc-msg-body">'
    +'<div class="dc-msg-hdr"><span class="dc-uname">Reaper</span><span class="dc-ts">'+ts+'</span></div>'
    +'<div class="dc-text">'+contentHtml+'</div>'
    +(attachHtml?'<div class="dc-attaches">'+attachHtml+'</div>':'')
    +'</div></div>';
  document.getElementById('preview-modal').classList.add('on');
}

function copyEditorTo(fromId,toId){
  const v=getMsgValue(fromId);
  setMsgValue(toId,v);
  saveMsgDraft(toId);
}

function dismissLaunchModal(){
  const el=document.getElementById('launch-modal');
  el.classList.add('closing');
  setTimeout(()=>el.classList.remove('on','closing'),220);
}

/* ── notifications ── */
const _notifIcos={
  error:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
  warn:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
  ok:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
  info:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
};
function notify(msg,type,duration){
  type=type||'info';
  duration=duration===undefined?4000:duration;
  const el=document.createElement('div');
  el.className='notif notif-'+type;
  el.innerHTML='<span class="notif-ico">'+(_notifIcos[type]||_notifIcos.info)+'</span><span class="notif-msg">'+msg+'</span>';
  const stack=document.getElementById('notif-stack');
  stack.appendChild(el);
  const dismiss=()=>{
    if(el.classList.contains('out'))return;
    el.classList.add('out');
    setTimeout(()=>{if(el.parentNode)el.remove();},200);
  };
  el.addEventListener('click',dismiss);
  setTimeout(dismiss,duration);
}

/* ── spread ── */
const _spToggles={servers:true,dms:true,muteafter:false,dnd:false,blindsend:false};
let _spRunning=false;

function spToggle(key){
  _spToggles[key]=!_spToggles[key];
  document.getElementById('tog-'+key).classList.toggle('on',_spToggles[key]);
  call('savesession',{sp_toggles:_spToggles}).catch(()=>{});
}

function spTab(panel){
  const segs=document.querySelectorAll('#pg-spread .sp-seg');
  const pill=document.getElementById('sp-pill');
  segs.forEach(s=>{
    const on=s.dataset.panel===panel;
    s.classList.toggle('on',on);
    if(on&&pill){pill.style.width=s.offsetWidth+'px';pill.style.transform='translateX('+(s.offsetLeft-3)+'px)';}
  });
  document.querySelectorAll('#pg-spread .sp-panel').forEach(p=>{
    p.classList.toggle('on',p.id==='sp-panel-'+panel);
  });
  document.querySelectorAll('.nv-sub[data-spread]').forEach(s=>{
    s.classList.toggle('on',s.dataset.spread===panel);
  });
}

function spSubNav(el){
  document.querySelectorAll('.nv').forEach(n=>n.classList.remove('on'));
  document.querySelector('.nv[data-pg="spread"]').classList.add('on');
  document.getElementById('settingsbtn').classList.remove('on');
  document.querySelectorAll('.pg').forEach(p=>p.classList.remove('on'));
  document.getElementById('pg-spread').classList.add('on');
  document.getElementById('spread-subnav').classList.add('on');
  requestAnimationFrame(()=>spTab(el.dataset.spread));
}

function spStartStop(){
  if(_spRunning){call('stopspread');return;}
  const serversOn=_spToggles.servers;
  const dmsOn=_spToggles.dms;
  if(!serversOn&&!dmsOn){
    notify('Enable at least one target — Servers or DMs','error');
    return;
  }
  const svmsg=getMsgValue('sp-svmsg').trim();
  const dmmsg=getMsgValue('sp-dmmsg').trim();
  if(serversOn&&!svmsg){
    notify('Add a message for Server Channels','error');
    return;
  }
  if(dmsOn&&!dmmsg){
    notify('Add a message for DMs & Friends','error');
    return;
  }
  call('gettokencount').then(n=>{
    if(!n){
      notify('No tokens loaded — add tokens in the Tokens tab','warn');
      return;
    }
    const settings={..._spToggles,svmsg,dmmsg,concurrency:parseInt(document.getElementById('sp-concurrency').value)||50};
    call('startspread',settings).then(ok=>{
      if(ok)setSpreadRunning(true);
      else notify('Failed to start — check your settings','error');
    }).catch(()=>notify('Failed to start — check your settings','error'));
  }).catch(()=>{
    const settings={..._spToggles,svmsg,dmmsg,concurrency:parseInt(document.getElementById('sp-concurrency').value)||50};
    call('startspread',settings).then(ok=>{if(ok)setSpreadRunning(true);}).catch(()=>{});
  });
}

function setSpreadRunning(running){
  _spRunning=running;
  const btn=document.getElementById('sp-btn');
  if(running){
    btn.innerHTML='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg> Stop Spread';
    btn.classList.add('stop');
    _spreadStart=Date.now();
    _runtimeTick=setInterval(()=>{
      const el=document.getElementById('sps-runtime');
      if(el)el.textContent=_fmtRuntime();
    },1000);
  }else{
    btn.innerHTML='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg> Start Spread';
    btn.classList.remove('stop');
    clearInterval(_runtimeTick);
    _runtimeTick=null;
    _prevSpreadSent=0;
  }
}

function updateSpreadStats(state){
  const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v;};
  set('sps-sent',state.sent||0);
  set('sps-channels',state.channels||0);
  set('sps-dms',state.dms||0);
  set('sps-failed',state.failed||0);
  set('sps-died',state.died||0);
  set('sps-dead',state.dead||0);
  set('sps-locked',state.locked||0);
  const delta=(state.sent||0)-_prevSpreadSent;
  if(delta>0){
    _totalMsgsSent+=delta;
    try{localStorage.setItem('dr_total_sent',_totalMsgsSent);}catch(e){}
  }
  _prevSpreadSent=state.sent||0;
  const msg=document.getElementById('stat-messages');
  if(msg)msg.textContent=_totalMsgsSent;
}

function stepNum(id,delta){
  const el=document.getElementById(id);
  if(!el)return;
  const mn=parseInt(el.min)||1,mx=parseInt(el.max)||999;
  el.value=Math.max(mn,Math.min(mx,(parseInt(el.value)||1)+delta));
  if(id==='sp-concurrency')call('savesession',{sp_concurrency:parseInt(el.value)||50}).catch(()=>{});
}

/* ── runtime helper ── */
function _fmtRt(start){
  const s=Math.floor((Date.now()-start)/1000);
  const h=Math.floor(s/3600);
  const m=Math.floor((s%3600)/60);
  const ss=s%60;
  return (h?h+':'+String(m).padStart(2,'0'):m)+':'+String(ss).padStart(2,'0');
}

/* ── checker ── */
let _chkRunning=false;
let _chkStart=0;
let _chkTick=null;
let _chkData={alive:[],dead:[],locked:[]};

function chkTab(tab){
  const pill=document.getElementById('chk-pill');
  document.querySelectorAll('#pg-checker .sp-seg').forEach(s=>{
    const on=s.dataset.tab===tab;
    s.classList.toggle('on',on);
    if(on&&pill){pill.style.width=s.offsetWidth+'px';pill.style.transform='translateX('+(s.offsetLeft-3)+'px)';}
  });
  document.querySelectorAll('#pg-checker .tool-panel').forEach(p=>{
    p.classList.toggle('on',p.id==='chk-panel-'+tab);
  });
}

function checkerStartStop(){
  if(_chkRunning){call('stopchecker');return;}
  call('gettokencount').then(n=>{
    if(!n){notify('No tokens loaded — add tokens in the Tokens tab','warn');return;}
    const settings={concurrency:parseInt(document.getElementById('chk-concurrency').value)||50};
    call('startchecker',settings).then(ok=>{
      if(ok)setCheckerRunning(true);
      else notify('Failed to start checker','error');
    }).catch(()=>notify('Failed to start checker','error'));
  }).catch(()=>{});
}

function setCheckerRunning(running){
  _chkRunning=running;
  const btn=document.getElementById('chk-btn');
  if(!btn)return;
  if(running){
    _chkData={alive:[],dead:[],locked:[]};
    ['alive','dead','locked'].forEach(t=>{const ta=document.getElementById('chk-ta-'+t);if(ta)ta.value='';});
    btn.innerHTML='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg> Stop';
    btn.classList.add('stop');
    _chkStart=Date.now();
    _chkTick=setInterval(()=>{const e=document.getElementById('chks-runtime');if(e)e.textContent=_fmtRt(_chkStart);},1000);
  }else{
    btn.innerHTML='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg> Start Checking';
    btn.classList.remove('stop');
    clearInterval(_chkTick);_chkTick=null;
  }
}

function updateCheckerStats(s){
  const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v;};
  set('chks-checked',s.checked||0);
  set('chks-alive',s.alive||0);
  set('chks-dead',s.dead||0);
  set('chks-locked',s.locked||0);
  set('chk-cnt-alive','('+(s.alive||0)+')');
  set('chk-cnt-dead','('+(s.dead||0)+')');
  set('chk-cnt-locked','('+(s.locked||0)+')');
  if(s.running===false)setCheckerRunning(false);
}

function pushCheckerResult(token,status){
  if(!_chkData[status])return;
  _chkData[status].push(token);
  const ta=document.getElementById('chk-ta-'+status);
  if(ta){ta.value=ta.value?ta.value+'\\n'+token:token;ta.scrollTop=ta.scrollHeight;}
}

function chkCopy(cat){
  const ta=document.getElementById('chk-ta-'+cat);
  if(ta&&ta.value){navigator.clipboard.writeText(ta.value).then(()=>notify('Copied','ok')).catch(()=>{});}
  else notify('No '+cat+' tokens to copy','warn');
}

function chkExport(cat){
  const data=(_chkData[cat]||[]).join('\\n');
  if(!data){notify('No '+cat+' tokens to export','warn');return;}
  call('exportresults','checker_'+cat,data).then(f=>{
    if(f)notify('Saved: '+f,'ok');
    else notify('Export failed','error');
  }).catch(()=>notify('Export failed','error'));
}

/* ── admincap ── */
let _acRunning=false;
let _acStart=0;
let _acTick=null;
let _acResults=[];

function admincapStartStop(){
  if(_acRunning){call('stopadmincap');return;}
  call('gettokencount').then(n=>{
    if(!n){notify('No tokens loaded — add tokens in the Tokens tab','warn');return;}
    const settings={concurrency:parseInt(document.getElementById('ac-concurrency').value)||50};
    call('startadmincap',settings).then(ok=>{
      if(ok)setAdmincapRunning(true);
      else notify('Failed to start scan','error');
    }).catch(()=>notify('Failed to start scan','error'));
  }).catch(()=>{});
}

function setAdmincapRunning(running){
  _acRunning=running;
  const btn=document.getElementById('ac-btn');
  if(!btn)return;
  if(running){
    _acResults=[];
    const body=document.getElementById('ac-body');
    if(body)body.innerHTML='';
    btn.innerHTML='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg> Stop';
    btn.classList.add('stop');
    _acStart=Date.now();
    _acTick=setInterval(()=>{const e=document.getElementById('acs-runtime');if(e)e.textContent=_fmtRt(_acStart);},1000);
  }else{
    btn.innerHTML='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg> Start Scan';
    btn.classList.remove('stop');
    clearInterval(_acTick);_acTick=null;
  }
}

function updateAdmincapStats(s){
  const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v;};
  set('acs-checked',s.checked||0);
  set('acs-found',s.found||0);
  set('acs-guilds',s.guilds||0);
  set('acs-requests',s.requests||0);
  if(s.running===false)setAdmincapRunning(false);
}

function pushAdmincapResult(d){
  _acResults.push(d);
  const body=document.getElementById('ac-body');
  if(!body)return;
  const tok=d.token||'';
  const gname=d.guild_name||'Unknown';
  const gid=d.guild_id||'';
  const row=document.createElement('div');
  row.className='ac-row';
  row.innerHTML='<span class="ac-guild" title="'+gname+' (ID: '+gid+')">'+gname+'</span><span class="ac-tok" title="'+tok+'">'+tok.substring(0,32)+'...</span>';
  body.appendChild(row);
  body.scrollTop=body.scrollHeight;
}

function acExport(){
  if(!_acResults.length){notify('No results to export','warn');return;}
  const lines=_acResults.map(r=>r.token+'|'+r.guild_name+'|'+r.guild_id);
  call('exportresults','admincap',lines.join('\\n')).then(f=>{
    if(f)notify('Saved: '+f,'ok');
    else notify('Export failed','error');
  }).catch(()=>notify('Export failed','error'));
}

/* ── evaluator ── */
let _evRunning=false;
let _evStart=0;
let _evTick=null;
let _evResults=[];

function evaluatorStartStop(){
  if(_evRunning){call('stopevaluator');return;}
  call('gettokencount').then(n=>{
    if(!n){notify('No tokens loaded — add tokens in the Tokens tab','warn');return;}
    const settings={concurrency:parseInt(document.getElementById('ev-concurrency').value)||30};
    call('startevaluator',settings).then(ok=>{
      if(ok)setEvaluatorRunning(true);
      else notify('Failed to start evaluator','error');
    }).catch(()=>notify('Failed to start evaluator','error'));
  }).catch(()=>{});
}

function setEvaluatorRunning(running){
  _evRunning=running;
  const btn=document.getElementById('ev-btn');
  if(!btn)return;
  if(running){
    _evResults=[];
    const body=document.getElementById('ev-body');
    if(body)body.innerHTML='';
    btn.innerHTML='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg> Stop';
    btn.classList.add('stop');
    _evStart=Date.now();
    _evTick=setInterval(()=>{const e=document.getElementById('evs-runtime');if(e)e.textContent=_fmtRt(_evStart);},1000);
  }else{
    btn.innerHTML='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg> Start Evaluation';
    btn.classList.remove('stop');
    clearInterval(_evTick);_evTick=null;
  }
}

function updateEvaluatorStats(s){
  const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v;};
  set('evs-checked',s.checked||0);
  set('evs-valid',s.valid||0);
  set('evs-invalid',s.invalid||0);
  set('evs-guilds',s.guilds||0);
  set('evs-dms',s.dms||0);
  set('evs-friends',s.friends||0);
  if(s.running===false)setEvaluatorRunning(false);
}

function pushEvaluatorResult(e){
  _evResults.push(e);
  const body=document.getElementById('ev-body');
  if(!body)return;
  const tok=e.token||'';
  const row=document.createElement('div');
  row.className='eval-row';
  row.innerHTML=
    '<span class="ev-uname" title="'+e.uid+'">'+e.username+'</span>'+
    '<span style="color:var(--tx2)">'+e.created+'</span>'+
    '<span style="color:var(--green);text-align:center">'+e.guilds+'</span>'+
    '<span style="text-align:center">'+e.dms+'</span>'+
    '<span style="text-align:center">'+e.friends+'</span>'+
    '<span class="ev-tok" title="'+tok+'">'+tok.substring(0,28)+'...</span>';
  body.appendChild(row);
  body.scrollTop=body.scrollHeight;
}

function evalExport(){
  if(!_evResults.length){notify('No results to export','warn');return;}
  const header='username,uid,created,guilds,dms,friends,token';
  const rows=_evResults.map(e=>[e.username,e.uid,e.created,e.guilds,e.dms,e.friends,e.token].join(','));
  const csv=header+'\\n'+rows.join('\\n');
  call('exportresults','evaluator_csv',csv).then(f=>{
    if(f)notify('Saved: '+f,'ok');
    else notify('Export failed','error');
  }).catch(()=>notify('Export failed','error'));
}

/* ── rare checker ── */
let _rcRunning=false;
let _rcStart=0;
let _rcTick=null;
let _rcResults=[];

function rcApplyFilters(){
  const maxlen  =parseInt(document.getElementById('rc-flt-maxlen').value)||32;
  const minyear =parseInt(document.getElementById('rc-flt-minyear').value)||2000;
  const minscore=parseInt(document.getElementById('rc-flt-minscore').value)||0;
  const rareonly=document.getElementById('rc-flt-rareonly').classList.contains('on');
  const filtered=_rcResults.filter(r=>r.length<=maxlen&&r.year>=minyear&&r.score>=minscore&&(!rareonly||r.rare));
  const body=document.getElementById('rc-body');
  if(!body)return;
  body.innerHTML='';
  if(!filtered.length){
    body.innerHTML='<div class="rc-row" style="color:var(--tx3);grid-column:1/-1;text-align:center;padding:16px">No results match current filters</div>';
    const c=document.getElementById('rc-visible-count');if(c)c.textContent='0 shown';
    return;
  }
  filtered.forEach(r=>{
    const row=document.createElement('div');
    row.className='rc-row';
    const badges=r.badges.map(b=>'<span class="rc-badge">'+b+'</span>').join('');
    const rareTag=r.rare?'<span class="rc-rare-y">RARE</span>':'<span class="rc-rare-n">—</span>';
    const sc=r.score>=60?'var(--yellow)':r.score>=30?'var(--orange)':'var(--tx2)';
    row.innerHTML=
      '<span class="rc-uname" title="'+r.uid+'">'+r.username+'</span>'+
      '<span style="color:var(--tx2)">'+r.type+'</span>'+
      '<span style="color:var(--tx2)">'+r.created+'</span>'+
      '<span style="text-align:center;color:var(--tx2)">'+r.length+'</span>'+
      '<span class="rc-score" style="color:'+sc+'">'+r.score+'</span>'+
      '<div class="rc-badges">'+badges+'</div>'+
      rareTag;
    body.appendChild(row);
  });
  const c=document.getElementById('rc-visible-count');if(c)c.textContent=filtered.length+' shown';
}

function rcTogRare(el){
  el.classList.toggle('on');
  el.textContent=el.classList.contains('on')?'On':'Off';
  rcApplyFilters();
}

function rarecheckerStartStop(){
  if(_rcRunning){call('stoprarechecker');return;}
  call('gettokencount').then(n=>{
    if(!n){notify('No tokens loaded — add tokens in the Tokens tab','warn');return;}
    const settings={concurrency:parseInt(document.getElementById('rc-concurrency').value)||50};
    call('startrarechecker',settings).then(ok=>{
      if(ok)setRarecheckerRunning(true);
      else notify('Failed to start rare checker','error');
    }).catch(()=>notify('Failed to start rare checker','error'));
  }).catch(()=>{});
}

function setRarecheckerRunning(running){
  _rcRunning=running;
  const btn=document.getElementById('rc-btn');
  if(!btn)return;
  if(running){
    _rcResults=[];
    const body=document.getElementById('rc-body');if(body)body.innerHTML='';
    const c=document.getElementById('rc-visible-count');if(c)c.textContent='0 shown';
    btn.innerHTML='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg> Stop';
    btn.classList.add('stop');
    _rcStart=Date.now();
    _rcTick=setInterval(()=>{const e=document.getElementById('rcs-runtime');if(e)e.textContent=_fmtRt(_rcStart);},1000);
  }else{
    btn.innerHTML='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg> Start Checking';
    btn.classList.remove('stop');
    clearInterval(_rcTick);_rcTick=null;
  }
}

function updateRarecheckerStats(s){
  const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v;};
  set('rcs-checked',s.checked||0);
  set('rcs-rare',s.rare||0);
  set('rcs-requests',s.requests||0);
  if(s.running===false)setRarecheckerRunning(false);
}

function pushRarecheckerResult(e){
  _rcResults.push(e);
  rcApplyFilters();
}

function rcExport(){
  if(!_rcResults.length){notify('No results to export','warn');return;}
  const hdr='username,uid,created,length,type,score,rare,badges,token';
  const rows=_rcResults.map(r=>[r.username,r.uid,r.created,r.length,r.type,r.score,r.rare,'"'+r.badges.join(';')+'"',r.token].join(','));
  const csv=hdr+'\\n'+rows.join('\\n');
  call('exportresults','rarechecker_csv',csv).then(f=>{
    if(f)notify('Saved: '+f,'ok');
    else notify('Export failed','error');
  }).catch(()=>notify('Export failed','error'));
}

/* ── token capture ── */
let _tcRunning=false;
let _tcStart=0;
let _tcTick=null;
let _tcResults=[];
let _tcFlt={status:'all',nitro:'any',payment:'any',phone:'any'};

function tcFilter(el,key){
  document.querySelectorAll('.flt-tog[data-flt="'+key+'"]').forEach(t=>t.classList.remove('on'));
  el.classList.add('on');
  _tcFlt[key]=el.dataset.val;
  tcApplyFilters();
}

function tcApplyFilters(){
  const filtered=_tcResults.filter(r=>{
    if(_tcFlt.status!=='all'&&r.status!==_tcFlt.status)return false;
    if(_tcFlt.nitro==='yes'&&!r.nitro)return false;
    if(_tcFlt.nitro==='no'&&r.nitro)return false;
    if(_tcFlt.payment==='yes'&&!r.payment.length)return false;
    if(_tcFlt.payment==='no'&&r.payment.length)return false;
    if(_tcFlt.phone==='yes'&&!r.phone)return false;
    if(_tcFlt.phone==='no'&&r.phone)return false;
    return true;
  });
  const body=document.getElementById('tc-body');
  if(!body)return;
  body.innerHTML='';
  if(!filtered.length){
    body.innerHTML='<div class="tc-row" style="color:var(--tx3);grid-column:1/-1;text-align:center;padding:16px">No results match current filters</div>';
    const c=document.getElementById('tc-visible-count');if(c)c.textContent='0 shown';
    return;
  }
  filtered.forEach(r=>{
    const row=document.createElement('div');
    row.className='tc-row';
    const tok=r.token||'';
    const stChip='<span class="tc-chip '+r.status+'">'+r.status.toUpperCase()+'</span>';
    const nitChip=r.nitro?'<span class="tc-chip nitro">'+r.nitrotype+'</span>':'<span style="color:var(--tx3)">—</span>';
    const payChips=r.payment&&r.payment.length?r.payment.map(p=>'<span class="tc-chip pay">'+p+'</span>').join(''):'<span style="color:var(--tx3)">—</span>';
    const bdgChips=r.badges&&r.badges.length?r.badges.map(b=>'<span class="tc-chip badge">'+b+'</span>').join(''):'<span style="color:var(--tx3)">—</span>';
    const extChips=(r.mfa?'<span class="tc-chip mfa">MFA</span>':'')+(r.email?'<span class="tc-chip eml">Email</span>':'');
    row.innerHTML=
      '<span class="tc-uname" title="'+r.uid+'  created:'+r.created+'">'+r.username+'</span>'+
      stChip+
      '<span>'+nitChip+'</span>'+
      '<div class="tc-chips">'+payChips+'</div>'+
      '<div class="tc-chips">'+bdgChips+'</div>'+
      '<div class="tc-chips">'+extChips+'</div>'+
      '<span class="tc-tok" title="'+tok+'">'+tok.substring(0,20)+'...</span>';
    body.appendChild(row);
  });
  const c=document.getElementById('tc-visible-count');if(c)c.textContent=filtered.length+' shown';
}

function tokencaptureStartStop(){
  if(_tcRunning){call('stoptokencapture');return;}
  call('gettokencount').then(n=>{
    if(!n){notify('No tokens loaded — add tokens in the Tokens tab','warn');return;}
    const settings={concurrency:parseInt(document.getElementById('tc-concurrency').value)||30};
    call('starttokencapture',settings).then(ok=>{
      if(ok)setTokencaptureRunning(true);
      else notify('Failed to start capture','error');
    }).catch(()=>notify('Failed to start capture','error'));
  }).catch(()=>{});
}

function setTokencaptureRunning(running){
  _tcRunning=running;
  const btn=document.getElementById('tc-btn');
  if(!btn)return;
  if(running){
    _tcResults=[];_tcFlt={status:'all',nitro:'any',payment:'any',phone:'any'};
    document.querySelectorAll('#pg-tokencapture .flt-tog').forEach(t=>{
      t.classList.toggle('on',t.dataset.val==='all'||t.dataset.val==='any');
    });
    const body=document.getElementById('tc-body');if(body)body.innerHTML='';
    const c=document.getElementById('tc-visible-count');if(c)c.textContent='0 shown';
    btn.innerHTML='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg> Stop';
    btn.classList.add('stop');
    _tcStart=Date.now();
    _tcTick=setInterval(()=>{const e=document.getElementById('tcs-runtime');if(e)e.textContent=_fmtRt(_tcStart);},1000);
  }else{
    btn.innerHTML='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg> Start Capture';
    btn.classList.remove('stop');
    clearInterval(_tcTick);_tcTick=null;
  }
}

function updateTokencaptureStats(s){
  const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v;};
  set('tcs-checked',s.checked||0);
  set('tcs-valid',s.valid||0);
  set('tcs-invalid',s.invalid||0);
  set('tcs-locked',s.locked||0);
  set('tcs-nitro',s.withnitro||0);
  set('tcs-payment',s.withpayment||0);
  if(s.running===false)setTokencaptureRunning(false);
}

function pushTokencaptureResult(e){
  _tcResults.push(e);
  tcApplyFilters();
}

function tcExport(){
  if(!_tcResults.length){notify('No results to export','warn');return;}
  const hdr='username,uid,status,nitro,nitrotype,payment,badges,email,phone,mfa,created,token';
  const rows=_tcResults.map(r=>[
    r.username,r.uid,r.status,r.nitro,r.nitrotype,
    '"'+(r.payment||[]).join(';')+'"','"'+(r.badges||[]).join(';')+'"',
    r.email,r.phone,r.mfa,r.created,r.token
  ].join(','));
  const csv=hdr+'\\n'+rows.join('\\n');
  call('exportresults','tokencapture_csv',csv).then(f=>{
    if(f)notify('Saved: '+f,'ok');
    else notify('Export failed','error');
  }).catch(()=>notify('Export failed','error'));
}

/* ── update check ── */
let _updateurl=null;
function checkForUpdate(){
  call('checkupdate').then(res=>{
    if(!res||!res.available)return;
    _updateurl=res.url;
    document.getElementById('update-msg').textContent='Version '+res.latest+' is available on GitHub. You are currently running an older version.';
    document.getElementById('update-modal').classList.add('on');
  }).catch(()=>{});
}
function dismissUpdate(){
  document.getElementById('update-modal').classList.remove('on');
}
function downloadUpdate(){
  if(_updateurl)call('openurl',_updateurl);
  dismissUpdate();
}

window.addEventListener('load',()=>{
  document.getElementById('launch-modal').classList.add('on');
  setTimeout(()=>{loadConfig();loadSession();refreshDashboard();checkForUpdate();},200);
  tickRuntime();
  resetCarTimer();
});
</script>
<div id="notif-stack"></div>
</body>
</html>'''


class guiapi:
    def __init__(self):
        self.window    = None
        self._spread        = None
        self._checker       = None
        self._admincap      = None
        self._evaluator     = None
        self._rarechecker   = None
        self._tokencapture  = None


    def setwindow(self, w):
        self.window = w
        self.window._serializable = False
        logger.guihandler = self.pushlog


    def pushlog(self, level, source, msg):
        if self.window:
            try:
                data = json.dumps({'level': level, 'source': source, 'msg': msg})
                self.window.evaluate_js(f'appendLog({data})')

            except Exception:
                pass


    def isnewer(self, latest, current):
        try:
            lparts = [int(p) for p in latest.split('.')]
            cparts = [int(p) for p in current.split('.')]
            length = max(len(lparts), len(cparts))
            lparts += [0] * (length - len(lparts))
            cparts += [0] * (length - len(cparts))
            return lparts > cparts

        except Exception:
            return bool(latest) and latest != current


    def checkupdate(self):
        try:
            r = requests.get(f'https://api.github.com/repos/{repo}/releases/latest', timeout=8)

            if r.status_code != 200:
                return {'available': False}

            data = r.json()
            latest = data.get('tag_name', '').lstrip('vV')
            url = data.get('html_url', f'https://github.com/{repo}/releases/latest')

            if latest and self.isnewer(latest, version):
                return {'available': True, 'latest': latest, 'url': url}

            return {'available': False}

        except Exception as e:
            logger.debug(f'update check failed » {e}')
            return {'available': False}


    def openurl(self, url):
        try:
            webbrowser.open(url)

        except Exception:
            pass

        return True


    def close(self):
        if self.window:
            self.window.destroy()


    def minimize(self):
        if self.window:
            self.window.minimize()


    def maximize(self):
        if self.window:
            try:
                if self.window.maximized:
                    self.window.restore()

                else:
                    self.window.maximize()

            except Exception:
                self.window.maximize()


    def moverel(self, dx, dy):
        try:
            if sys.platform == 'win32':
                import ctypes
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                rect = ctypes.wintypes.RECT()
                ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                ctypes.windll.user32.SetWindowPos(
                    hwnd, 0,
                    rect.left + int(dx), rect.top + int(dy),
                    0, 0, 0x0001 | 0x0004,
                )
            else:
                gtk_win = self.window._window
                x, y = gtk_win.get_position()
                gtk_win.move(x + int(dx), y + int(dy))

        except Exception:
            pass


    def getconfig(self):
        return {
            'concurrency':  get.general.concurrency(),
            'delaymin':     get.general.delaymin(),
            'delaymax':     get.general.delaymax(),
            'proxytimeout': get.proxies.timeout(),
        }


    def setconfig(self, section, key, value):
        configcls().set(section, key, value)
        return True


    def gettokencount(self):
        return len(files.loadtokens())


    def getproxycount(self):
        return len(files.loadproxies())


    def getlines(self, filetype):
        if filetype == 'tokens':
            return files.loadtokens()

        if filetype == 'proxies':
            return files.loadproxies()

        return []


    def importlines(self, filetype, content):
        lines = [l.strip() for l in content.splitlines() if l.strip()]

        if filetype == 'tokens':
            files.writelines(files.tokensfile, lines)

        elif filetype == 'proxies':
            files.writelines(files.proxiesfile, lines)

        return len(lines)


    def startspread(self, settings):
        from src.spread import spreadhandler
        if hasattr(self, '_spread') and self._spread and self._spread.isrunning():
            return False
        tokens = files.loadtokens()
        if not tokens:
            logger.warning('No tokens loaded', 'Spread')
            return False
        svmsg = ''
        dmmsg = ''
        if isinstance(settings, dict):
            svmsg = settings.get('svmsg', '').strip()
            dmmsg = settings.get('dmmsg', '').strip()
        if not svmsg and not dmmsg:
            logger.warning('No message configured', 'Spread')
            return False
        logger.info(f'Starting spread Tokens={len(tokens)}', 'Spread')

        def onupdate(state):
            if self.window:
                try:
                    self.window.evaluate_js(f'updateSpreadStats({json.dumps(state)})')

                except Exception:
                    pass

        def ondone():
            state = self._spread.getstats() if self._spread else {}
            if self.window:
                try:
                    self.window.evaluate_js('setSpreadRunning(false)')
                    self.window.evaluate_js(f'updateSpreadStats({json.dumps(state)})')

                except Exception:
                    pass
            logger.success(
                f'Spread done Sent={state.get("sent", 0)} Dead={state.get("dead", 0)} Failed={state.get("failed", 0)}',
                'Spread',
            )

        self._spread = spreadhandler()
        self._spread.setonupdate(onupdate)
        self._spread.setondone(ondone)
        self._spread.start(tokens, svmsg, dmmsg, settings)
        return True


    _session_file = os.path.join(APPDATA, 'session.json')

    def loadsession(self):
        try:
            with open(self._session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def savesession(self, data):
        try:
            os.makedirs(APPDATA, exist_ok=True)
            try:
                with open(self._session_file, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            except Exception:
                existing = {}
            if isinstance(data, dict):
                existing.update(data)
            with open(self._session_file, 'w', encoding='utf-8') as f:
                json.dump(existing, f)
            return True
        except Exception:
            return False

    def startchecker(self, settings):
        from src.checker import checker as checkercls
        if self._checker and self._checker.running:
            return False
        tokens = files.loadtokens()
        if not tokens:
            logger.warning('No tokens loaded', 'Checker')
            return False

        def onupdate(state):
            if self.window:
                try:
                    self.window.evaluate_js(f'updateCheckerStats({json.dumps(state)})')
                except Exception:
                    pass

        def ondone():
            state = self._checker.getstats() if self._checker else {}
            if self.window:
                try:
                    self.window.evaluate_js('setCheckerRunning(false)')
                    self.window.evaluate_js(f'updateCheckerStats({json.dumps(state)})')
                except Exception:
                    pass
            logger.success(
                f'Checker done  Alive={state.get("alive",0)}  Dead={state.get("dead",0)}  Locked={state.get("locked",0)}',
                'Checker',
            )

        def onresult(token, status):
            if self.window:
                try:
                    self.window.evaluate_js(f'pushCheckerResult({json.dumps(token)},{json.dumps(status)})')
                except Exception:
                    pass

        self._checker = checkercls()
        self._checker.setonupdate(onupdate)
        self._checker.setondone(ondone)
        self._checker.setonresult(onresult)
        return self._checker.start(tokens, settings if isinstance(settings, dict) else {})


    def stopchecker(self):
        if self._checker:
            self._checker.stop()
        return True


    def startadmincap(self, settings):
        from src.nukeablecapture import admincap as admincapcls
        if self._admincap and self._admincap.running:
            return False
        tokens = files.loadtokens()
        if not tokens:
            logger.warning('No tokens loaded', 'NukableCap')
            return False

        def onupdate(state):
            if self.window:
                try:
                    self.window.evaluate_js(f'updateAdmincapStats({json.dumps(state)})')
                except Exception:
                    pass

        def ondone():
            state = self._admincap.getstats() if self._admincap else {}
            if self.window:
                try:
                    self.window.evaluate_js('setAdmincapRunning(false)')
                    self.window.evaluate_js(f'updateAdmincapStats({json.dumps(state)})')
                except Exception:
                    pass
            logger.success(
                f'NukableCap done  Found={state.get("found",0)}  Guilds={state.get("guilds",0)}',
                'NukableCap',
            )

        def onresult(token, guild_name, guild_id):
            if self.window:
                try:
                    data = json.dumps({'token': token, 'guild_name': guild_name, 'guild_id': guild_id})
                    self.window.evaluate_js(f'pushAdmincapResult({data})')
                except Exception:
                    pass

        self._admincap = admincapcls()
        self._admincap.setonupdate(onupdate)
        self._admincap.setondone(ondone)
        self._admincap.setonresult(onresult)
        return self._admincap.start(tokens, settings if isinstance(settings, dict) else {})


    def stopadmincap(self):
        if self._admincap:
            self._admincap.stop()
        return True


    def startevaluator(self, settings):
        from src.evaluator import evaluator as evaluatorcls
        if self._evaluator and self._evaluator.running:
            return False
        tokens = files.loadtokens()
        if not tokens:
            logger.warning('No tokens loaded', 'Evaluator')
            return False

        def onupdate(state):
            if self.window:
                try:
                    self.window.evaluate_js(f'updateEvaluatorStats({json.dumps(state)})')
                except Exception:
                    pass

        def ondone():
            state = self._evaluator.getstats() if self._evaluator else {}
            if self.window:
                try:
                    self.window.evaluate_js('setEvaluatorRunning(false)')
                    self.window.evaluate_js(f'updateEvaluatorStats({json.dumps(state)})')
                except Exception:
                    pass
            logger.success(
                f'Evaluator done  Valid={state.get("valid",0)}  Invalid={state.get("invalid",0)}',
                'Evaluator',
            )

        def onresult(entry):
            if self.window:
                try:
                    self.window.evaluate_js(f'pushEvaluatorResult({json.dumps(entry)})')
                except Exception:
                    pass

        self._evaluator = evaluatorcls()
        self._evaluator.setonupdate(onupdate)
        self._evaluator.setondone(ondone)
        self._evaluator.setonresult(onresult)
        return self._evaluator.start(tokens, settings if isinstance(settings, dict) else {})


    def stopevaluator(self):
        if self._evaluator:
            self._evaluator.stop()
        return True


    def startrarechecker(self, settings):
        from src.rarechecker import rarechecker as rarecheckcls
        if self._rarechecker and self._rarechecker.running:
            return False
        tokens = files.loadtokens()
        if not tokens:
            logger.warning('No tokens loaded', 'RareChecker')
            return False

        def onupdate(state):
            if self.window:
                try:
                    self.window.evaluate_js(f'updateRarecheckerStats({json.dumps(state)})')
                except Exception:
                    pass

        def ondone():
            state = self._rarechecker.getstats() if self._rarechecker else {}
            if self.window:
                try:
                    self.window.evaluate_js('setRarecheckerRunning(false)')
                    self.window.evaluate_js(f'updateRarecheckerStats({json.dumps(state)})')
                except Exception:
                    pass
            logger.success(
                f'RareChecker done  Rare={state.get("rare",0)}  Checked={state.get("checked",0)}',
                'RareChecker',
            )

        def onresult(entry):
            if self.window:
                try:
                    self.window.evaluate_js(f'pushRarecheckerResult({json.dumps(entry)})')
                except Exception:
                    pass

        self._rarechecker = rarecheckcls()
        self._rarechecker.setonupdate(onupdate)
        self._rarechecker.setondone(ondone)
        self._rarechecker.setonresult(onresult)
        return self._rarechecker.start(tokens, settings if isinstance(settings, dict) else {})


    def stoprarechecker(self):
        if self._rarechecker:
            self._rarechecker.stop()
        return True


    def starttokencapture(self, settings):
        from src.tokencapture import tokencapture as tokencapturecls
        if self._tokencapture and self._tokencapture.running:
            return False
        tokens = files.loadtokens()
        if not tokens:
            logger.warning('No tokens loaded', 'TokenCapture')
            return False

        def onupdate(state):
            if self.window:
                try:
                    self.window.evaluate_js(f'updateTokencaptureStats({json.dumps(state)})')
                except Exception:
                    pass

        def ondone():
            state = self._tokencapture.getstats() if self._tokencapture else {}
            if self.window:
                try:
                    self.window.evaluate_js('setTokencaptureRunning(false)')
                    self.window.evaluate_js(f'updateTokencaptureStats({json.dumps(state)})')
                except Exception:
                    pass
            logger.success(
                f'TokenCapture done  Valid={state.get("valid",0)}  Nitro={state.get("withnitro",0)}  Payment={state.get("withpayment",0)}',
                'TokenCapture',
            )

        def onresult(entry):
            if self.window:
                try:
                    self.window.evaluate_js(f'pushTokencaptureResult({json.dumps(entry)})')
                except Exception:
                    pass

        self._tokencapture = tokencapturecls()
        self._tokencapture.setonupdate(onupdate)
        self._tokencapture.setondone(ondone)
        self._tokencapture.setonresult(onresult)
        return self._tokencapture.start(tokens, settings if isinstance(settings, dict) else {})


    def stoptokencapture(self):
        if self._tokencapture:
            self._tokencapture.stop()
        return True


    def exportresults(self, tool, content):
        try:
            os.makedirs(APPDATA, exist_ok=True)
            ts = time.strftime('%Y%m%d_%H%M%S')
            fname = os.path.join(APPDATA, f'{tool}_{ts}.txt')
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(content)
            webbrowser.open(os.path.dirname(fname))
            return fname
        except Exception as e:
            logger.error(f'Export failed: {e}', 'Export')
            return None


    def stopspread(self):
        if hasattr(self, '_spread') and self._spread:
            self._spread.stop()
        return True


    def getspreadstats(self):
        if hasattr(self, '_spread') and self._spread:
            return self._spread.getstats()
        return {}


def startgui():
    api = guiapi()
    window = webview.create_window(
        'Discord Reaper',
        html=html,
        js_api=api,
        width=1260,
        height=760,
        min_size=(980, 600),
        frameless=True,
        easy_drag=False,
        background_color='#0a0a0c',
        on_top=True,
    )
    api.setwindow(window)

    def disableontop():
        time.sleep(2)
        try:
            window.on_top = False

        except Exception:
            pass

    webview.start(debug=False, func=disableontop)
