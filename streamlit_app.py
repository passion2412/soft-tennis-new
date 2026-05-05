import streamlit as st
import streamlit.components.v1 as components

# 1. ページ設定
st.set_page_config(page_title="Tennis Counter Pro v9", layout="centered")

# --- PWA対応のHTMLコード ---
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
    <link rel="manifest" href="static/manifest.json">
    <script>
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
          navigator.serviceWorker.register('static/sw.js').then(function(reg) {
            console.log('PWA ServiceWorker registered');
          }).catch(function(err) {
            console.log('PWA ServiceWorker failed', err);
          });
        });
      }
    </script>

    <style>
        body { font-family: -apple-system, sans-serif; background: white; padding: 2px; margin: 0; }
        
        /* スコアボード */
        .score-box { background: #1a1a1a; color: white; border-radius: 8px; text-align: center; padding: 12px 8px; margin-bottom: 6px; position: relative; }
        .main-score { font-size: 48px; font-weight: 900; line-height: 1; margin: 5px 0; }
        .game-score { font-size: 18px; color: #4CAF50; font-weight: bold; }
        .names-display { font-size: 12px; opacity: 0.8; margin-top: 4px; }
        
        /* サーブ確率表示 (白文字・大) */
        .srv-mini { position: absolute; font-size: 14px; color: white; font-weight: bold; top: 12px; line-height: 1.2; }
        #srv-p1-mini { left: 12px; text-align: left; }
        #srv-p2-mini { right: 12px; text-align: right; }

        .player-selector { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 6px; }
        .p-btn { border: 2px solid #E67E22; background: white; color: #E67E22; padding: 10px; border-radius: 6px; font-weight: bold; text-align: center; cursor: pointer; font-size: 14px; }
        .p-btn.active { background: #E67E22; color: white; }

        .serve-btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 6px; }
        .s-btn { height: 38px; border-radius: 19px; border: none; color: white; font-weight: bold; cursor: pointer; font-size: 13px; }
        .s-in { background: #28a745; }
        .s-fault { background: #dc3545; }

        .label-grid { display: grid; grid-template-columns: 1fr 1fr; text-align: center; font-size: 12px; font-weight: bold; margin-bottom: 2px; }
        .label-win { color: #007AFF; }
        .label-loss { color: #FF3B30; }

        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 8px; }
        .btn { height: 44px; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: white !important; font-weight: bold; font-size: 12px; border: none; cursor: pointer; }
        .btn-win { background-color: #007AFF; }
        .btn-loss { background-color: #FF3B30; }

        .undo-btn { background: #666; color: white; border: none; padding: 12px; width: 100%; margin-bottom: 20px; border-radius: 4px; font-weight: bold; font-size: 14px; cursor: pointer; }

        /* Match Report */
        .report-card { border: 2px solid #333; border-radius: 8px; padding: 10px; background: #fff; width: 100%; box-sizing: border-box; }
        .report-title { font-size: 14px; font-weight: bold; background: #333; color: white; margin: -10px -10px 10px -10px; padding: 8px; border-radius: 6px 6px 0 0; text-align: center; }
        .rep-match-name { font-size: 13px; font-weight: bold; text-align: center; color: #444; margin-bottom: 5px; }
        .final-score-rep { text-align:center; padding-bottom: 8px; border-bottom: 1px solid #eee; margin-bottom: 8px; }
        
        table { width: 100%; border-collapse: collapse; font-size: 11px; }
        th, td { border: 1px solid #ddd; padding: 5px 2px; text-align: center; }
        th { background: #f4f4f4; }
        .total-row { background: #f9f9f9; font-weight: bold; }
        .srv-row { background: #f0f8ff; font-weight: bold; }
        
        .memo-box { font-size: 11px; background: #f9f9f9; padding: 8px; border-radius: 4px; margin-top: 8px; border-left: 3px solid #ccc; white-space: pre-wrap; }
        .history-grid { display: flex; flex-wrap: wrap; gap: 4px; justify-content: center; margin-top: 8px; }
        .history-item { border: 1px solid #333; border-radius: 3px; padding: 3px 8px; font-size: 11px; font-weight: bold; background: #eee; }

        details { margin-top: 25px; padding: 10px; font-size: 13px; color: #666; border: 1px solid #eee; }
        input, textarea { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-size: 14px; }
    </style>
</head>
<body>
    <div id="main-ui">
        <div class="score-box">
            <div id="srv-p1-mini" class="srv-mini">1st: 0%<br>(0/0)</div>
            <div id="srv-p2-mini" class="srv-mini">1st: 0%<br>(0/0)</div>
            <div id="gms" class="game-score">G: 0 — 0</div>
            <div id="pts" class="main-score">0 — 0</div>
            <div id="disp-names" class="names-display">自分 & ペア vs 相手</div>
        </div>
        <div class="player-selector">
            <div id="tag1" class="p-btn active" onclick="setPlayer(1)">自分</div>
            <div id="tag2" class="p-btn" onclick="setPlayer(2)">ペア</div>
        </div>
        <div class="serve-btn-grid">
            <button class="s-btn s-in" onclick="countServe(true)">1st IN</button>
            <button class="s-btn s-fault" onclick="countServe(false)">1st フォルト</button>
        </div>
        <div class="label-grid">
            <div class="label-win">得点</div>
            <div class="label-loss">失点</div>
        </div>
        <div class="grid" id="button-area"></div>
        <button class="undo-btn" onclick="undo()">↩ 戻る (修正)</button>
    </div>

    <div class="report-card" id="screenshot-area">
        <div class="report-title">MATCH REPORT</div>
        <div id="rep-match-name" class="rep-match-name">未設定の試合</div>
        <div class="final-score-rep">
            <div id="final-gms" style="font-size:32px; font-weight: 900; color:#d32f2f;">0 — 0</div>
            <div id="final-names" style="font-size:12px; font-weight: bold;">自分 & ペア vs 相手</div>
        </div>
        <table>
            <thead id="stats-head"></thead>
            <tbody id="stats-body"></tbody>
        </table>
        <div id="history-area" class="history-grid"></div>
        <div id="rep-memo" class="memo-box">メモなし</div>
    </div>

    <details>
        <summary>⚙️ 試合設定・リセット</summary>
        <input type="text" id="in-match" placeholder="試合名" oninput="updateSettings()">
        <input type="text" id="in-p1" placeholder="自分" oninput="updateSettings()">
        <input type="text" id="in-p2" placeholder="ペア" oninput="updateSettings()">
        <input type="text" id="in-opp" placeholder="相手" oninput="updateSettings()">
        <textarea id="in-memo" rows="3" placeholder="メモ" oninput="updateSettings()"></textarea>
        <button onclick="location.reload()" style="background:#f44336; color:white; width:100%; padding:12px; border:none; border-radius:4px; margin-top:10px; font-weight:bold;">全消去</button>
    </details>

    <script>
        // --- 内部ロジックは前回通り ---
        var state = {
            p1:0, p2:0, g1:0, g2:0, active:1,
            match_n: "未設定の試合", p1_n: "自分", p2_n: "ペア", opp_n: "相手", memo: "メモなし",
            stats: { p1: {}, p2: {}, other: { '相手のミス': 0, '相手のエース': 0 } },
            serve: { p1_in: 0, p1_total: 0, p2_in: 0, p2_total: 0 },
            history: []
        };
        var stack = [];
        var wins = ['サービスエース', 'レシーブエース', 'スマッシュ', 'エース', 'ボレー', '相手のミス'];
        var loss = ['ダブルフォルト', 'レシーブミス', 'スマッシュミス', 'ストロークミス', 'ボレーミス', '相手のエース'];

        function init() {
            var area = document.getElementById('button-area');
            wins.forEach(function(w, i) {
                var l = loss[i];
                var bW = document.createElement('button'); bW.className='btn btn-win'; bW.innerText=w; bW.onclick=function(){count(w,true)};
                var bL = document.createElement('button'); bL.className='btn btn-loss'; bL.innerText=l; bL.onclick=function(){count(l,false)};
                area.appendChild(bW); area.appendChild(bL);
                state.stats.p1[w]=0; state.stats.p1[l]=0; state.stats.p2[w]=0; state.stats.p2[l]=0;
            });
            render();
        }

        function setPlayer(n) { state.active = n; render(); }

        function countServe(isIn) {
            stack.push(JSON.stringify(state));
            var p = state.active == 1 ? 'p1' : 'p2';
            state.serve[p+'_total']++;
            if(isIn) state.serve[p+'_in']++;
            render();
        }

        function count(label, isWin) {
            stack.push(JSON.stringify(state));
            if (label === '相手のミス') {
                state.stats.other['相手のミス']++;
                state.p1++;
            } else if (label === '相手のエース') {
                state.stats.other['相手のエース']++;
                state.p2++;
            } else {
                var pKey = state.active == 1 ? 'p1' : 'p2';
                state.stats[pKey][label] = (state.stats[pKey][label] || 0) + 1;
                if(isWin) state.p1++; else state.p2++;
            }
            if((state.p1 >= 4 || state.p2 >= 4) && Math.abs(state.p1 - state.p2) >= 2) {
                state.history.push(state.p1 + "-" + state.p2);
                if(state.p1 > state.p2) state.g1++; else state.g2++;
                state.p1 = 0; state.p2 = 0;
            }
            render();
        }

        function undo() { if(stack.length > 0) { state = JSON.parse(stack.pop()); render(); } }

        function updateSettings() {
            state.match_n = document.getElementById('in-match').value || "未設定の試合";
            state.p1_n = document.getElementById('in-p1').value || "自分";
            state.p2_n = document.getElementById('in-p2').value || "ペア";
            state.opp_n = document.getElementById('in-opp').value || "相手";
            state.memo = document.getElementById('in-memo').value || "メモなし";
            render();
        }

        function getSrvText(p) {
            var total = state.serve[p+'_total'];
            var inc = state.serve[p+'_in'];
            if(total == 0) return "0% (0/0)";
            return Math.round((inc / total) * 100) + "% (" + inc + "/" + total + ")";
        }

        function render() {
            document.getElementById('pts').innerText = state.p1 + " — " + state.p2;
            document.getElementById('gms').innerText = "G: " + state.g1 + " — " + state.g2;
            document.getElementById('disp-names').innerText = state.p1_n + " & " + state.p2_n + " vs " + state.opp_n;
            document.getElementById('tag1').innerText = state.p1_n;
            document.getElementById('tag2').innerText = state.p2_n;
            document.getElementById('tag1').className = state.active==1 ? 'p-btn active' : 'p-btn';
            document.getElementById('tag2').className = state.active==2 ? 'p-btn active' : 'p-btn';
            document.getElementById('srv-p1-mini').innerHTML = "1st: " + getSrvText('p1').split(' ')[0] + "<br>" + getSrvText('p1').split(' ')[1];
            document.getElementById('srv-p2-mini').innerHTML = "1st: " + getSrvText('p2').split(' ')[0] + "<br>" + getSrvText('p2').split(' ')[1];
            document.getElementById('rep-match-name').innerText = state.match_n;
            document.getElementById('final-gms').innerText = state.g1 + " — " + state.g2;
            document.getElementById('final-names').innerText = state.p1_n + " & " + state.p2_n + " vs " + state.opp_n;
            document.getElementById('rep-memo').innerText = state.memo;
            document.getElementById('stats-head').innerHTML = "<tr><th style='width:40%'>項目</th><th>"+state.p1_n+"</th><th>"+state.p2_n+"</th></tr>";
            var rows = "<tr class='srv-row'><td style='text-align:left;'>1st成功率</td><td>"+getSrvText('p1')+"</td><td>"+getSrvText('p2')+"</td></tr>";
            var items = ['サービスエース', 'レシーブエース', 'スマッシュ', 'エース', 'ボレー', 'ダブルフォルト', 'レシーブミス', 'スマッシュミス', 'ストロークミス', 'ボレーミス'];
            items.forEach(function(s){
                rows += "<tr><td style='text-align:left;'>"+s+"</td><td>"+(state.stats.p1[s]||0)+"</td><td>"+(state.stats.p2[s]||0)+"</td></tr>";
            });
            rows += "<tr class='total-row'><td style='text-align:left;'>相手のミス (計)</td><td colspan='2' style='font-size:14px;'>"+state.stats.other['相手のミス']+"</td></tr>";
            rows += "<tr class='total-row'><td style='text-align:left;'>相手のエース (計)</td><td colspan='2' style='font-size:14px;'>"+state.stats.other['相手のエース']+"</td></tr>";
            document.getElementById('stats-body').innerHTML = rows;
            var h = "";
            state.history.forEach(function(x, i){ h += '<div class="history-item">G'+(i+1)+': '+x+'</div>'; });
            document.getElementById('history-area').innerHTML = h;
        }
        init();
    </script>
</body>
</html>
"""

components.html(html_code, height=1500, scrolling=True)
