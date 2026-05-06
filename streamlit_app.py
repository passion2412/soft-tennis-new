import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Tennis Counter Pro v14", layout="centered")

html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: -apple-system, sans-serif; background: white; padding: 2px; margin: 0; }
        .score-box { background: #1a1a1a; color: white; border-radius: 8px; text-align: center; padding: 12px 8px; margin-bottom: 6px; position: relative; }
        .main-score { font-size: 48px; font-weight: 900; line-height: 1; margin: 5px 0; }
        .game-score { font-size: 24px; color: #4CAF50; font-weight: 900; margin-top: 5px; }
        .mode-display { font-size: 12px; color: #E67E22; font-weight: bold; min-height: 14px; }
        .names-display { font-size: 12px; opacity: 0.8; margin-top: 4px; }
        
        .srv-mini { position: absolute; font-size: 14px; color: white; font-weight: bold; top: 12px; line-height: 1.2; }
        #srv-p1-mini { left: 12px; text-align: left; }
        #srv-p2-mini { right: 12px; text-align: right; }

        /* サービス権表示のスタイル */
        .player-selector { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4px; margin-bottom: 6px; }
        .p-btn { border: 2px solid #E67E22; background: white; color: #E67E22; padding: 10px 2px; border-radius: 6px; font-weight: bold; text-align: center; cursor: pointer; font-size: 13px; transition: 0.2s; }
        .p-btn.active { background: #E67E22; color: white; box-shadow: 0 0 10px rgba(230,126,34,0.5); }
        .ball-icon { margin-left: 4px; }

        .serve-btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 6px; }
        .s-btn { height: 38px; border-radius: 19px; border: none; color: white; font-weight: bold; cursor: pointer; font-size: 13px; }
        .s-in { background: #28a745; }
        .s-fault { background: #dc3545; }

        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 8px; }
        .btn { height: 44px; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: white !important; font-weight: bold; font-size: 12px; border: none; cursor: pointer; }
        .btn-win { background-color: #007AFF; }
        .btn-loss { background-color: #FF3B30; }

        .undo-btn { background: #666; color: white; border: none; padding: 12px; width: 100%; margin-bottom: 20px; border-radius: 4px; font-weight: bold; font-size: 14px; cursor: pointer; }
        .report-card { border: 2px solid #333; border-radius: 8px; padding: 10px; background: #fff; width: 100%; box-sizing: border-box; }
        .report-title { font-size: 14px; font-weight: bold; background: #333; color: white; margin: -10px -10px 10px -10px; padding: 8px; border-radius: 6px 6px 0 0; text-align: center; }
        table { width: 100%; border-collapse: collapse; font-size: 11px; }
        th, td { border: 1px solid #ddd; padding: 5px 2px; text-align: center; }
        .total-row { background: #f9f9f9; font-weight: bold; font-size: 13px; }
        details { margin-top: 25px; padding: 10px; border: 1px solid #eee; }
        input, textarea, select { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    </style>
</head>
<body>
    <div id="main-ui">
        <div class="score-box">
            <div id="srv-p1-mini" class="srv-mini"></div>
            <div id="srv-p2-mini" class="srv-mini"></div>
            <div id="game-mode" class="mode-display"></div>
            <div id="gms" class="game-score">G: 0 — 0</div>
            <div id="pts" class="main-score">0 — 0</div>
            <div id="disp-names" class="names-display"></div>
        </div>

        <!-- サーブ権選択ボタン -->
        <div class="player-selector">
            <div id="tag1" class="p-btn" onclick="setPlayer(1)">自分</div>
            <div id="tag2" class="p-btn" onclick="setPlayer(2)">ペア</div>
            <div id="tag3" class="p-btn" onclick="setPlayer(3)">相手サーブ</div>
        </div>

        <div class="serve-btn-grid" id="serve-input-area">
            <button class="s-btn s-in" onclick="countServe(true)">1st IN</button>
            <button class="s-btn s-fault" onclick="countServe(false)">1st フォルト</button>
        </div>

        <div class="grid" id="button-area"></div>
        <button class="undo-btn" onclick="undo()">↩ 戻る (修正)</button>
    </div>

    <div class="report-card">
        <div class="report-title">MATCH REPORT</div>
        <div id="rep-match-name" style="text-align:center; font-weight:bold; margin-bottom:5px;"></div>
        <div style="text-align:center; padding-bottom: 8px;">
            <div id="final-gms" style="font-size:32px; font-weight: 900; color:#d32f2f;">0 — 0</div>
            <div id="final-names" style="font-size:12px; font-weight: bold;"></div>
        </div>
        <table>
            <thead id="stats-head"></thead>
            <tbody id="stats-body"></tbody>
        </table>
        <div id="history-area" class="history-grid" style="display: flex; flex-wrap: wrap; gap: 4px; justify-content: center; margin-top: 8px;"></div>
    </div>

    <details>
        <summary>⚙️ 試合設定</summary>
        <label>試合形式:</label>
        <select id="match-type" onchange="updateSettings()">
            <option value="5">5ゲームマッチ</option>
            <option value="7">7ゲームマッチ</option>
        </select>
        <input type="text" id="in-match" placeholder="試合名" oninput="updateSettings()">
        <input type="text" id="in-p1" placeholder="自分" oninput="updateSettings()">
        <input type="text" id="in-p2" placeholder="ペア" oninput="updateSettings()">
        <input type="text" id="in-opp" placeholder="相手" oninput="updateSettings()">
        <button onclick="location.reload()" style="background:#f44336; color:white; width:100%; padding:12px; border:none; border-radius:4px; margin-top:10px;">全消去</button>
    </details>

    <script>
        var state = {
            p1:0, p2:0, g1:0, g2:0, active:1, match_type: 5, is_final: false,
            p1_n: "自分", p2_n: "ペア", opp_n: "相手", match_n: "未設定の試合",
            stats: { p1: {}, p2: {}, other: { '相手のミス': 0, '相手のエース': 0 } },
            serve: { p1_in: 0, p1_total: 0, p2_in: 0, p2_total: 0 },
            history: []
        };
        var stack = [];
        var wins = ['サービスエース', 'レシーブエース', 'エース', 'ボレー', 'スマッシュ', '相手のミス'];
        var loss = ['ダブルフォルト', 'レシーブミス', 'ストロークミス', 'ボレーミス', 'スマッシュミス', '相手のエース'];

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
            if(state.active === 3) return; // 相手サーブ時は自分たちの確率はカウントしない
            stack.push(JSON.stringify(state));
            var p = state.active == 1 ? 'p1' : 'p2';
            state.serve[p+'_total']++;
            if(isIn) state.serve[p+'_in']++;
            render();
        }

        function count(label, isWin) {
            stack.push(JSON.stringify(state));
            if (label === '相手のミス') { state.stats.other['相手のミス']++; state.p1++; }
            else if (label === '相手のエース') { state.stats.other['相手のエース']++; state.p2++; }
            else {
                // 得点/失点した時に選択されているのが「自分」か「ペア」か、それとも「相手(3)」かで統計の付け先を決める
                // 相手サーブ中でも、自分たちのミスやエースは記録したいので、直前に選択していた方を優先するロジックなどもありますが、
                // ここではシンプルに active が 1or2 の時はその人に、3の時は最後に選択していた自分側の人に付けるか、
                // もしくは入力を促す形になります。今回は「自分」をデフォルトにします。
                var pKey = (state.active == 2) ? 'p2' : 'p1';
                state.stats[pKey][label] = (state.stats[pKey][label] || 0) + 1;
                if(isWin) state.p1++; else state.p2++;
            }
            checkScore();
            render();
        }

        function checkScore() {
            var target = Math.floor(state.match_type / 2);
            if (!state.is_final && state.g1 === target && state.g2 === target) state.is_final = true;
            var limit = state.is_final ? 7 : 4;
            if ((state.p1 >= limit || state.p2 >= limit) && Math.abs(state.p1 - state.p2) >= 2) finishGame();
        }

        function finishGame() {
            state.history.push(state.p1 + "-" + state.p2 + (state.is_final ? "(F)" : ""));
            if(state.p1 > state.p2) state.g1++; else state.g2++;
            state.p1 = 0; state.p2 = 0;
            var win_limit = Math.ceil(state.match_type / 2);
            if(state.g1 >= win_limit || state.g2 >= win_limit) state.is_final = false;
        }

        function undo() { if(stack.length > 0) { state = JSON.parse(stack.pop()); render(); } }

        function updateSettings() {
            state.match_type = parseInt(document.getElementById('match-type').value);
            state.match_n = document.getElementById('in-match').value || "未設定の試合";
            state.p1_n = document.getElementById('in-p1').value || "自分";
            state.p2_n = document.getElementById('in-p2').value || "ペア";
            state.opp_n = document.getElementById('in-opp').value || "相手";
            render();
        }

        function render() {
            document.getElementById('pts').innerText = state.p1 + " — " + state.p2;
            document.getElementById('gms').innerText = "G: " + state.g1 + " — " + state.g2;
            document.getElementById('game-mode').innerText = state.is_final ? "★ファイナルゲーム (7点先取)" : "";
            
            // 名前表示の更新（🎾マーク付き）
            var p1_disp = state.p1_n + (state.active==1 ? "🎾" : "");
            var p2_disp = state.p2_n + (state.active==2 ? "🎾" : "");
            var opp_disp = state.opp_n + (state.active==3 ? "🎾" : "");
            document.getElementById('disp-names').innerText = p1_disp + " & " + p2_disp + " vs " + opp_disp;

            // ボタンの更新
            document.getElementById('tag1').innerHTML = state.p1_n + (state.active==1 ? '<span class="ball-icon">🎾</span>' : '');
            document.getElementById('tag2').innerHTML = state.p2_n + (state.active==2 ? '<span class="ball-icon">🎾</span>' : '');
            document.getElementById('tag3').innerHTML = "相手サーブ" + (state.active==3 ? '<span class="ball-icon">🎾</span>' : '');
            
            document.getElementById('tag1').className = state.active==1 ? 'p-btn active' : 'p-btn';
            document.getElementById('tag2').className = state.active==2 ? 'p-btn active' : 'p-btn';
            document.getElementById('tag3').className = state.active==3 ? 'p-btn active' : 'p-btn';

            // 相手サーブ時はサーブ確率入力エリアを薄くする（または非表示）
            document.getElementById('serve-input-area').style.opacity = (state.active === 3) ? "0.3" : "1";

            // サーブ確率表示
            var s1 = Math.round((state.serve.p1_in/(state.serve.p1_total||1))*100) + "%";
            var s2 = Math.round((state.serve.p2_in/(state.serve.p2_total||1))*100) + "%";
            document.getElementById('srv-p1-mini').innerHTML = "1st:" + s1 + (state.active==1?"🎾":"");
            document.getElementById('srv-p2-mini').innerHTML = "1st:" + s2 + (state.active==2?"🎾":"");

            // レポート更新
            document.getElementById('rep-match-name').innerText = state.match_n + " (" + state.match_type + "Gマッチ)";
            document.getElementById('final-gms').innerText = state.g1 + " — " + state.g2;
            document.getElementById('final-names').innerText = state.p1_n + " & " + state.p2_n + " vs " + state.opp_n;
            
            var p1_aces = (state.stats.p1['サービスエース']||0) + (state.stats.p1['レシーブエース']||0) + (state.stats.p1['エース']||0) + (state.stats.p1['ボレー']||0) + (state.stats.p1['スマッシュ']||0);
            var p2_aces = (state.stats.p2['サービスエース']||0) + (state.stats.p2['レシーブエース']||0) + (state.stats.p2['エース']||0) + (state.stats.p2['ボレー']||0) + (state.stats.p2['スマッシュ']||0);
            var p1_miss = (state.stats.p1['ダブルフォルト']||0) + (state.stats.p1['レシーブミス']||0) + (state.stats.p1['ストロークミス']||0) + (state.stats.p1['ボレーミス']||0) + (state.stats.p1['スマッシュミス']||0);
            var p2_miss = (state.stats.p2['ダブルフォルト']||0) + (state.stats.p2['レシーブミス']||0) + (state.stats.p2['ストロークミス']||0) + (state.stats.p2['ボレーミス']||0) + (state.stats.p2['スマッシュミス']||0);

            var tableRows = "<tr><th style='width:40%'>項目</th><th>"+state.p1_n+"</th><th>"+state.p2_n+"</th></tr>";
            tableRows += "<tr class='srv-row'><td>1st成功率</td><td>"+s1+"</td><td>"+s2+"</td></tr>";
            
            ['サービスエース', 'レシーブエース', 'エース', 'ボレー', 'スマッシュ', 'ダブルフォルト', 'レシーブミス', 'ストロークミス', 'ボレーミス', 'スマッシュミス'].forEach(item => {
                tableRows += "<tr><td>"+item+"</td><td>"+(state.stats.p1[item]||0)+"</td><td>"+(state.stats.p2[item]||0)+"</td></tr>";
            });
            tableRows += "<tr class='total-row'><td>自分たちのエース (計)</td><td colspan='2' style='color:#007AFF; font-size:16px;'>" + (p1_aces+p2_aces) + "</td></tr>";
            tableRows += "<tr class='total-row'><td>自分たちのミス (計)</td><td colspan='2' style='color:#FF3B30; font-size:16px;'>" + (p1_miss+p2_miss) + "</td></tr>";
            tableRows += "<tr class='total-row'><td>相手のエース (計)</td><td colspan='2'>"+state.stats.other['相手のエース']+"</td></tr>";
            tableRows += "<tr class='total-row'><td>相手のミス (計)</td><td colspan='2'>"+state.stats.other['相手のミス']+"</td></tr>";
            document.getElementById('stats-body').innerHTML = tableRows;
        }
        init();
    </script>
</body>
</html>
"""

components.html(html_code, height=1500, scrolling=True)
