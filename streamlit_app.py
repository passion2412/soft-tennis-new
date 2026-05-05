import streamlit as st
import streamlit.components.v1 as components

# 1. ページ設定
st.set_page_config(page_title="Tennis Counter Pro v3", layout="centered")

html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: -apple-system, sans-serif; background: white; padding: 5px; margin: 0; }
        .room-tag { font-size: 10px; color: #ccc; text-align: right; margin-bottom: 5px; }
        
        /* 選手選択（最上部へ） */
        .player-selector { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 10px; }
        .p-btn { border: 2px solid #E67E22; background: white; color: #E67E22; padding: 12px; border-radius: 8px; font-weight: bold; text-align: center; cursor: pointer; font-size: 15px; }
        .p-btn.active { background: #E67E22; color: white; }

        /* スコアボード */
        .score-box { background: #222; color: white; border-radius: 10px; text-align: center; padding: 10px; margin-bottom: 10px; }
        .names-display { font-size: 13px; opacity: 0.9; margin-bottom: 5px; }
        .main-score { font-size: 52px; font-weight: 900; line-height: 1; margin: 5px 0; }
        .game-score { font-size: 20px; color: #4CAF50; font-weight: bold; }

        /* サーブ入力エリア（成功率は消去） */
        .serve-box { background: #f0f8ff; border: 1px solid #007AFF; border-radius: 10px; padding: 8px; margin-bottom: 10px; }
        .serve-btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .s-btn { height: 40px; border-radius: 20px; border: none; color: white; font-weight: bold; cursor: pointer; font-size: 13px; }
        .s-in { background: #28a745; }
        .s-fault { background: #dc3545; }

        /* カウントボタン */
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 10px; }
        .btn { height: 50px; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white !important; font-weight: bold; font-size: 12px; border: none; cursor: pointer; }
        .btn-win { background-color: #007AFF; }
        .btn-loss { background-color: #FF3B30; }

        .undo-btn { background: #666; color: white; border: none; padding: 10px; width: 100%; margin-bottom: 20px; border-radius: 4px; font-weight: bold; cursor: pointer; }

        /* レポートエリア */
        .report-card { border: 2px solid #333; border-radius: 8px; padding: 10px; background: #fff; margin-top: 15px; }
        .report-title { font-size: 14px; font-weight: bold; background: #333; color: white; margin: -10px -10px 10px -10px; padding: 8px; border-radius: 6px 6px 0 0; text-align: center; }
        
        table { width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 10px; }
        th, td { border: 1px solid #ddd; padding: 6px; text-align: center; }
        th { background: #f4f4f4; }
        
        .history-grid { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; margin-top: 10px; }
        .history-item { border: 1px solid #333; border-radius: 4px; padding: 3px 8px; font-size: 12px; font-weight: bold; background: #eee; }

        details { margin-top: 20px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; background: #f9f9f9; color: #666; }
        input { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    </style>
</head>
<body>

    <div class="room-tag">Room: <input type="text" id="room-id" value="Room1" style="width:50px; border:none; background:transparent; color:#ccc; font-size:10px;"></div>

    <!-- 1. 選手選択（最上部に移動） -->
    <div class="player-selector">
        <div id="tag1" class="p-btn active" onclick="setPlayer(1)">自分</div>
        <div id="tag2" class="p-btn" onclick="setPlayer(2)">ペア</div>
    </div>

    <!-- 2. サーブ入力エリア -->
    <div class="serve-box">
        <div class="serve-btn-grid">
            <button class="s-btn s-in" onclick="countServe(true)">1st IN</button>
            <button class="s-btn s-fault" onclick="countServe(false)">1st フォルト</button>
        </div>
    </div>

    <!-- 3. スコアボード -->
    <div class="score-box">
        <div id="disp-names" class="names-display">自分 & ペア vs 相手</div>
        <div id="pts" class="main-score">0 — 0</div>
        <div id="gms" class="game-score">Game: 0 — 0</div>
    </div>

    <!-- 4. メインボタン -->
    <div class="grid" id="button-area"></div>
    <button class="undo-btn" onclick="undo()">↩ 一つ戻る (Undo)</button>

    <!-- 5. レポート -->
    <div class="report-card">
        <div class="report-title">MATCH REPORT</div>
        
        <div style="text-align:center; padding: 10px 0; border-bottom: 1px solid #eee; margin-bottom: 10px;">
            <div id="final-gms" style="font-size:32px; font-weight: 900; color:#d32f2f; letter-spacing: 2px;">0 — 0</div>
            <div id="final-names" style="font-size:13px; font-weight: bold;">自分 & ペア vs 相手</div>
        </div>

        <table>
            <tr style="background:#f0f8ff;">
                <th style="font-size: 10px;">1st成功率</th>
                <th id="rep-srv1" style="color:#007AFF;">自分: 0%</th>
                <th id="rep-srv2" style="color:#007AFF;">ペア: 0%</th>
            </tr>
        </table>
        
        <table>
            <thead id="stats-head"></thead>
            <tbody id="stats-body"></tbody>
        </table>

        <div style="font-size:11px; font-weight:bold; color:#666; margin-top:15px; text-align:center;">GAME HISTORY</div>
        <div id="history-area" class="history-grid"></div>
    </div>

    <details>
        <summary>⚙️ 設定・リセット</summary>
        <input type="text" id="in-p1" placeholder="自分の名前" oninput="updateSettings()">
        <input type="text" id="in-p2" placeholder="ペアの名前" oninput="updateSettings()">
        <input type="text" id="in-opp" placeholder="対戦相手名" oninput="updateSettings()">
        <button onclick="location.reload()" style="background:#f44336; color:white; width:100%; padding:10px; border:none; border-radius:4px; margin-top:10px; font-weight:bold;">データを全消去</button>
    </details>

    <script>
        var state = {
            p1:0, p2:0, g1:0, g2:0, active:1,
            p1_n: "自分", p2_n: "ペア", opp_n: "相手",
            stats: { p1: {}, p2: {} },
            serve: { p1_in: 0, p1_total: 0, p2_in: 0, p2_total: 0 },
            history: []
        };
        var stack = [];
        
        var wins = ['サービスエース', 'レシーブエース', 'スマッシュ', 'エース', 'ボレー', '相手のミス'];
        var loss = ['ダブルフォルト', 'レシーブミス', 'スマッシュミス', 'ストロークミス', 'ボレーミス', '相手のエース'];
        var all_items = ['サービスエース', 'レシーブエース', 'スマッシュ', 'エース', 'ボレー', 'ダブルフォルト', 'レシーブミス', 'スマッシュミス', 'ストロークミス', 'ボレーミス'];

        function init() {
            var area = document.getElementById('button-area');
            area.innerHTML = "";
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
            var pKey = state.active == 1 ? 'p1' : 'p2';
            state.stats[pKey][label] = (state.stats[pKey][label] || 0) + 1;
            if(isWin) state.p1++; else state.p2++;
            if((state.p1 >= 4 || state.p2 >= 4) && Math.abs(state.p1 - state.p2) >= 2) {
                state.history.push(state.p1 + "-" + state.p2);
                if(state.p1 > state.p2) state.g1++; else state.g2++;
                state.p1 = 0; state.p2 = 0;
            }
            render();
        }

        function undo() { if(stack.length > 0) { state = JSON.parse(stack.pop()); render(); } }

        function updateSettings() {
            state.p1_n = document.getElementById('in-p1').value || "自分";
            state.p2_n = document.getElementById('in-p2').value || "ペア";
            state.opp_n = document.getElementById('in-opp').value || "相手";
            render();
        }

        function getSrvRate(p) {
            var total = state.serve[p+'_total'];
            var inc = state.serve[p+'_in'];
            if(total == 0) return "0% (0/0)";
            return Math.round((inc / total) * 100) + "% (" + inc + "/" + total + ")";
        }

        function render() {
            document.getElementById('pts').innerText = state.p1 + " — " + state.p2;
            document.getElementById('gms').innerText = "Game: " + state.g1 + " — " + state.g2;
            document.getElementById('disp-names').innerText = state.p1_n + " & " + state.p2_n + " vs " + state.opp_n;
            document.getElementById('tag1').innerText = state.p1_n;
            document.getElementById('tag2').innerText = state.p2_n;
            document.getElementById('tag1').className = state.active==1 ? 'p-btn active' : 'p-btn';
            document.getElementById('tag2').className = state.active==2 ? 'p-btn active' : 'p-btn';
            
            document.getElementById('final-gms').innerText = state.g1 + " — " + state.g2;
            document.getElementById('final-names').innerText = state.p1_n + " & " + state.p2_n + " vs " + state.opp_n;
            
            document.getElementById('rep-srv1').innerText = state.p1_n + ": " + getSrvRate('p1');
            document.getElementById('rep-srv2').innerText = state.p2_n + ": " + getSrvRate('p2');

            document.getElementById('stats-head').innerHTML = "<tr><th>項目</th><th>"+state.p1_n+"</th><th>"+state.p2_n+"</th></tr>";
            var rows = "";
            all_items.forEach(function(s){
                rows += "<tr><td style='text-align:left;'>"+s+"</td><td>"+(state.stats.p1[s]||0)+"</td><td>"+(state.stats.p2[s]||0)+"</td></tr>";
            });
            document.getElementById('stats-body').innerHTML = rows;
            
            var h = "";
            state.history.forEach(function(x, i){ h += '<div class="history-item">G'+(i+1)+': '+x+'</div>'; });
            document.getElementById('history-area').innerHTML = h || "...";
        }
        init();
    </script>
</body>
</html>
"""

components.html(html_code, height=1600, scrolling=True)
