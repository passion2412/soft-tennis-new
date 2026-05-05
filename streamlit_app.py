import streamlit as st
import streamlit.components.v1 as components

# 1. ページ設定
st.set_page_config(page_title="Tennis Compact Counter", layout="centered")

html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: -apple-system, sans-serif; background: white; padding: 2px; margin: 0; overflow-x: hidden; }
        
        /* コンパクトスコアボード */
        .score-box { background: #1a1a1a; color: white; border-radius: 8px; text-align: center; padding: 8px; margin-bottom: 6px; position: relative; }
        .main-score { font-size: 42px; font-weight: 900; line-height: 1; margin: 2px 0; }
        .game-score { font-size: 16px; color: #4CAF50; font-weight: bold; }
        .names-display { font-size: 12px; opacity: 0.8; margin-top: 2px; }
        
        /* スコア内のサーブ確率（絶対配置で四隅へ） */
        .srv-mini { position: absolute; font-size: 10px; color: #007AFF; font-weight: bold; top: 8px; }
        #srv-p1-mini { left: 10px; }
        #srv-p2-mini { right: 10px; }

        /* 選手選択 */
        .player-selector { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 6px; }
        .p-btn { border: 1.5px solid #E67E22; background: white; color: #E67E22; padding: 8px; border-radius: 6px; font-weight: bold; text-align: center; cursor: pointer; font-size: 13px; }
        .p-btn.active { background: #E67E22; color: white; }

        /* サーブ入力 */
        .serve-btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 6px; }
        .s-btn { height: 34px; border-radius: 17px; border: none; color: white; font-weight: bold; cursor: pointer; font-size: 12px; }
        .s-in { background: #28a745; }
        .s-fault { background: #dc3545; }

        /* メインボタン */
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 6px; }
        .btn { height: 42px; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: white !important; font-weight: bold; font-size: 11px; border: none; cursor: pointer; }
        .btn-win { background-color: #007AFF; }
        .btn-loss { background-color: #FF3B30; }

        .undo-btn { background: #666; color: white; border: none; padding: 8px; width: 100%; margin-bottom: 20px; border-radius: 4px; font-weight: bold; font-size: 12px; }

        /* 1画面用スクショレポート */
        .report-card { border: 2px solid #333; border-radius: 8px; padding: 8px; background: #fff; max-width: 100%; box-sizing: border-box; }
        .report-title { font-size: 13px; font-weight: bold; background: #333; color: white; margin: -8px -8px 8px -8px; padding: 6px; border-radius: 6px 6px 0 0; text-align: center; }
        .final-score-rep { text-align:center; padding-bottom: 8px; border-bottom: 1px solid #eee; margin-bottom: 8px; }
        
        table { width: 100%; border-collapse: collapse; font-size: 10.5px; line-height: 1.1; }
        th, td { border: 1px solid #ddd; padding: 4px 2px; text-align: center; }
        th { background: #f4f4f4; }
        
        .history-grid { display: flex; flex-wrap: wrap; gap: 4px; justify-content: center; margin-top: 6px; }
        .history-item { border: 1px solid #333; border-radius: 3px; padding: 2px 6px; font-size: 10px; font-weight: bold; background: #eee; }

        details { margin-top: 20px; padding: 10px; font-size: 12px; color: #666; }
        input { width: 100%; padding: 8px; margin: 4px 0; border: 1px solid #ccc; border-radius: 4px; }
    </style>
</head>
<body>

    <!-- 1. 操作エリア（一画面に収まるよう設計） -->
    <div id="main-ui">
        <div class="score-box">
            <div id="srv-p1-mini" class="srv-mini">1st: 0%</div>
            <div id="srv-p2-mini" class="srv-mini">1st: 0%</div>
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

        <div class="grid" id="button-area"></div>
        <button class="undo-btn" onclick="undo()">↩ Undo</button>
    </div>

    <hr style="border: 1px dashed #ccc; margin: 20px 0;">

    <!-- 2. レポートエリア（スクショ用一画面） -->
    <div class="report-card" id="screenshot-area">
        <div class="report-title">MATCH REPORT</div>
        <div class="final-score-rep">
            <div id="final-gms" style="font-size:28px; font-weight: 900; color:#d32f2f;">0 — 0</div>
            <div id="final-names" style="font-size:11px; font-weight: bold;">自分 & ペア vs 相手</div>
        </div>

        <table>
            <thead id="stats-head"></thead>
            <tbody id="stats-body"></tbody>
            <tr style="background:#f0f8ff; font-weight:bold;">
                <td>1st成功率</td>
                <td id="rep-srv1">0%</td>
                <td id="rep-srv2">0%</td>
            </tr>
        </table>

        <div id="history-area" class="history-grid"></div>
    </div>

    <details>
        <summary>⚙️ 設定</summary>
        <input type="text" id="in-p1" placeholder="自分" oninput="updateSettings()">
        <input type="text" id="in-p2" placeholder="ペア" oninput="updateSettings()">
        <input type="text" id="in-opp" placeholder="相手" oninput="updateSettings()">
        <button onclick="location.reload()" style="background:#f44336; color:white; width:100%; padding:10px; border:none; border-radius:4px; margin-top:10px; font-weight:bold;">全消去</button>
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
            if(total == 0) return "0%";
            return Math.round((state.serve[p+'_in'] / total) * 100) + "%";
        }

        function render() {
            document.getElementById('pts').innerText = state.p1 + " — " + state.p2;
            document.getElementById('gms').innerText = "G: " + state.g1 + " — " + state.g2;
            document.getElementById('disp-names').innerText = state.p1_n + " & " + state.p2_n + " vs " + state.opp_n;
            document.getElementById('tag1').innerText = state.p1_n;
            document.getElementById('tag2').innerText = state.p2_n;
            document.getElementById('tag1').className = state.active==1 ? 'p-btn active' : 'p-btn';
            document.getElementById('tag2').className = state.active==2 ? 'p-btn active' : 'p-btn';
            
            // スコア内のミニ確率
            document.getElementById('srv-p1-mini').innerText = "1st: " + getSrvRate('p1');
            document.getElementById('srv-p2-mini').innerText = "1st: " + getSrvRate('p2');

            // レポート表示
            document.getElementById('final-gms').innerText = state.g1 + " — " + state.g2;
            document.getElementById('final-names').innerText = state.p1_n + " & " + state.p2_n + " vs " + state.opp_n;
            document.getElementById('rep-srv1').innerText = getSrvRate('p1');
            document.getElementById('rep-srv2').innerText = getSrvRate('p2');

            document.getElementById('stats-head').innerHTML = "<tr><th style='width:40%'>項目</th><th>"+state.p1_n+"</th><th>"+state.p2_n+"</th></tr>";
            var rows = "";
            [...wins, ...loss].forEach(function(s){
                if(s === '相手のエース' || s === '相手のミス') return; // 重複を避けるか、特定ルールで出す
                rows += "<tr><td style='text-align:left;'>"+s+"</td><td>"+(state.stats.p1[s]||0)+"</td><td>"+(state.stats.p2[s]||0)+"</td></tr>";
            });
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

components.html(html_code, height=1200, scrolling=True)
