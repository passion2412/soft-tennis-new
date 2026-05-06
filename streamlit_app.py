import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import os

# --- 設定: アイコンの読み込み ---
icon_path = "icon.png"
if os.path.exists(icon_path):
    icon_image = Image.open(icon_path)
else:
    icon_image = "🎾"

st.set_page_config(
    page_title="Tennis Counter Pro",
    page_icon=icon_image,
    layout="centered"
)

html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: -apple-system, sans-serif; background: white; padding: 2px; margin: 0; }
        .score-box { 
            background: #1a1a1a; color: white; border-radius: 8px; 
            display: grid; grid-template-columns: 80px 1fr 80px; 
            padding: 12px 8px; margin-bottom: 6px; align-items: center;
        }
        .srv-stats-area { text-align: left; font-size: 10px; line-height: 1.3; }
        .srv-item { margin-bottom: 4px; color: #bbb; }
        .srv-item.active { color: #FFD700; font-weight: bold; }
        .srv-val { font-size: 11px; color: white; }
        .score-center { text-align: center; width: 100%; }
        .main-score { font-size: 42px; font-weight: 900; line-height: 1; margin: 0; }
        .game-score { font-size: 20px; color: #4CAF50; font-weight: 900; margin-bottom: 2px; display: block; width: 100%; text-align: center; }
        .info-right { text-align: right; font-size: 10px; color: #E67E22; font-weight: bold; }
        
        .player-selector { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4px; margin: 8px 0; }
        .p-btn { border: 2px solid #E67E22; background: white; color: #E67E22; padding: 12px 2px; border-radius: 6px; font-weight: bold; text-align: center; cursor: pointer; font-size: 14px; }
        .p-btn.active { background: #E67E22; color: white; }

        .serve-btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 6px; min-height: 38px; }
        .s-btn { height: 38px; border-radius: 19px; border: none; color: white; font-weight: bold; cursor: pointer; font-size: 13px; }
        .s-in { background: #28a745; }
        .s-fault { background: #dc3545; }
        
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 8px; }
        .btn { height: 44px; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: white !important; font-weight: bold; font-size: 12px; border: none; }
        .btn-win { background-color: #007AFF; }
        .btn-loss { background-color: #FF3B30; }
        
        .bottom-action-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 20px; }
        .netin-btn { background: #007AFF; color: white; border: none; padding: 12px; border-radius: 4px; font-weight: bold; font-size: 14px; cursor: pointer; }
        .undo-btn { background: #666; color: white; border: none; padding: 12px; border-radius: 4px; font-weight: bold; font-size: 14px; cursor: pointer; }
        
        textarea { width: 100%; height: 60px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-size: 12px; margin-bottom: 20px; }

        .report-card { border: 2px solid #333; border-radius: 8px; padding: 10px; background: #fff; width: 100%; box-sizing: border-box; }
        .report-title { font-size: 14px; font-weight: bold; background: #333; color: white; margin: -10px -10px 10px -10px; padding: 8px; border-radius: 6px 6px 0 0; text-align: center; }
        
        .report-header-area { text-align: center; padding: 10px 0; border-bottom: 1px solid #eee; margin-bottom: 10px; }
        .rep-names { font-size: 13px; font-weight: bold; color: #333; margin-bottom: 4px; }
        .rep-match { font-size: 11px; color: #666; margin-bottom: 8px; }
        .final-gms { font-size: 40px; font-weight: 900; color: #d32f2f; line-height: 1; margin-bottom: 5px; }
        
        table { width: 100%; border-collapse: collapse; font-size: 10px; margin-bottom: 10px; }
        th, td { border: 1px solid #ddd; padding: 4px 2px; text-align: center; }
        .total-row { background: #f9f9f9; font-weight: bold; font-size: 11px; }
        
        .history-section { border-top: 1px dashed #ccc; padding: 10px 0; margin-bottom: 10px; }
        .history-label { font-size: 11px; font-weight: bold; color: #666; margin-bottom: 5px; text-align: center; }
        .history-list { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; }
        .history-item { border: 1px solid #333; padding: 3px 6px; font-size: 10px; background: #f8f8f8; border-radius: 4px; font-weight: bold; }
        .srv-mark { color: #E67E22; margin-right: 2px; }

        .report-memo { background: #fff9c4; padding: 8px; border-radius: 4px; font-size: 11px; border-left: 4px solid #fbc02d; margin-top: 10px; white-space: pre-wrap; }
        
        details { margin-top: 25px; padding: 10px; border: 1px solid #eee; }
        .settings-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 10px; }
        .m-btn { padding: 10px; border: 1px solid #ccc; background: white; border-radius: 4px; cursor: pointer; font-weight: bold; }
        .m-btn.active { background: #333; color: white; border-color: #333; }
        input { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        .reset-btn { background: #f44336; color: white; width: 100%; padding: 12px; border: none; border-radius: 4px; margin-top: 15px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div id="main-ui">
        <div class="score-box">
            <div class="srv-stats-area">
                <div id="srv-p1-box" class="srv-item"><span id="lbl-s1">後衛</span><br><span id="s1-pct" class="srv-val">0%</span> <span id="s1-cnt">(0/0)</span></div>
                <div id="srv-p2-box" class="srv-item"><span id="lbl-s2">前衛</span><br><span id="s2-pct" class="srv-val">0%</span> <span id="s2-cnt">(0/0)</span></div>
            </div>
            <div class="score-center">
                <div id="gms" class="game-score">G: 0 — 0</div>
                <div id="pts" class="main-score">0 — 0</div>
            </div>
            <div class="info-right">
                <div id="game-mode"></div>
            </div>
        </div>

        <div class="player-selector">
            <div id="tag1" class="p-btn" onclick="setPlayer(1)">後衛</div>
            <div id="tag2" class="p-btn" onclick="setPlayer(2)">前衛</div>
            <div id="tag3" class="p-btn" onclick="setPlayer(3)">相手</div>
        </div>

        <div class="serve-btn-grid" id="serve-input-area">
            <button id="s-in-btn" class="s-btn s-in" onclick="countServe(true)">1st イン</button>
            <button id="s-fault-btn" class="s-btn s-fault" onclick="countServe(false)">1st フォルト</button>
        </div>

        <div class="grid" id="button-area"></div>
        
        <div class="bottom-action-grid">
            <button class="netin-btn" onclick="count('ネットイン', true)">ネットイン</button>
            <button class="undo-btn" onclick="undo()">↩ 戻る</button>
        </div>

        <textarea id="match-memo" placeholder="試合のメモ（ここに入力するとレポートに反映されます）" oninput="render()"></textarea>
    </div>

    <div class="report-card">
        <div class="report-title">MATCH REPORT</div>
        <div class="report-header-area">
            <div id="rep-match-name" class="rep-match"></div>
            <div id="final-names" class="rep-names"></div>
            <div id="final-gms" class="final-gms">0 — 0</div>
        </div>
        <div class="history-section">
            <div class="history-label">GAME SCORE HISTORY</div>
            <div id="history-area" class="history-list"></div>
        </div>
        <table>
            <thead id="stats-head"></thead>
            <tbody id="stats-body"></tbody>
        </table>
        <div id="report-memo-display" class="report-memo" style="display:none;"></div>
    </div>

    <details>
        <summary>⚙️ 試合設定</summary>
        <div style="font-size:12px; margin: 10px 0 5px 0; font-weight:bold;">マッチ形式:</div>
        <div class="settings-grid">
            <button id="m5" class="m-btn active" onclick="setMatchType(5)">5ゲーム</button>
            <button id="m7" class="m-btn" onclick="setMatchType(7)">7ゲーム</button>
        </div>
        <input type="text" id="in-match" placeholder="試合名" oninput="updateSettings()">
        <input type="text" id="in-p1" placeholder="後衛の名前" oninput="updateSettings()">
        <input type="text" id="in-p2" placeholder="前衛の名前" oninput="updateSettings()">
        <input type="text" id="in-opp" placeholder="相手" oninput="updateSettings()">
        <button class="reset-btn" onclick="if(confirm('全てのデータを消去しますか？')){location.reload();}">データを全消去</button>
    </details>

    <script>
        var state = {
            p1:0, p2:0, g1:0, g2:0, active:1, match_type: 5, is_final: false,
            p1_n: "後衛", p2_n: "前衛", opp_n: "相手", match_n: "未設定の試合",
            stats: { p1: {}, p2: {}, opp: {} },
            serve: { p1_in: 0, p1_total: 0, p2_in: 0, p2_total: 0 },
            history: [],
            current_game_serves: 0 
        };
        var stack = [];
        var wins = ['サービスエース', 'レシーブエース', 'ストローク', 'ボレー', 'スマッシュ'];
        var loss = ['ダブルフォルト', 'レシーブミス', 'ストロークミス', 'ボレーミス', 'スマッシュミス'];

        function init() {
            var area = document.getElementById('button-area');
            wins.forEach(function(w, i) {
                var l = loss[i];
                var bW = document.createElement('button'); bW.className='btn btn-win'; bW.innerText=w; bW.onclick=function(){count(w,true)};
                var bL = document.createElement('button'); bL.className='btn btn-loss'; bL.innerText=l; bL.onclick=function(){count(l,false)};
                area.appendChild(bW); area.appendChild(bL);
                state.stats.p1[w]=0; state.stats.p1[l]=0; 
                state.stats.p2[w]=0; state.stats.p2[l]=0;
                state.stats.opp[w]=0; state.stats.opp[l]=0;
            });
            state.stats.p1['ネットイン']=0; state.stats.p2['ネットイン']=0; state.stats.opp['ネットイン']=0;
            render();
        }

        function setMatchType(n) {
            state.match_type = n;
            render();
        }

        function setPlayer(n) { state.active = n; render(); }

        function countServe(isIn) {
            if(state.active === 3) return;
            stack.push(JSON.stringify(state));
            var p = state.active == 1 ? 'p1' : 'p2';
            state.serve[p+'_total']++;
            if(isIn) state.serve[p+'_in']++;
            state.current_game_serves++; 
            render();
        }

        function count(label, isWin) {
            stack.push(JSON.stringify(state));
            var pKey = (state.active == 1) ? 'p1' : (state.active == 2 ? 'p2' : 'opp');
            state.stats[pKey][label] = (state.stats[pKey][label] || 0) + 1;
            if (state.active == 3) { if(isWin) state.p2++; else state.p1++; }
            else { if(isWin) state.p1++; else state.p2++; }
            checkScore(); render();
        }

        function checkScore() {
            var target = Math.floor(state.match_type / 2); // 5→2, 7→3
            if (!state.is_final && state.g1 === target && state.g2 === target) state.is_final = true;
            var limit = state.is_final ? 7 : 4;
            if ((state.p1 >= limit || state.p2 >= limit) && Math.abs(state.p1 - state.p2) >= 2) finishGame();
        }

        function finishGame() {
            var side = (state.current_game_serves > 0) ? "S" : "R";
            state.history.push({
                score: state.p1 + "-" + state.p2 + (state.is_final ? "(F)" : ""),
                side: side
            });
            if(state.p1 > state.p2) state.g1++; else state.g2++;
            state.p1 = 0; state.p2 = 0;
            state.current_game_serves = 0;
            
            var win_limit = Math.ceil(state.match_type / 2);
            if(state.g1 >= win_limit || state.g2 >= win_limit) state.is_final = false;
        }

        function undo() { if(stack.length > 0) { state = JSON.parse(stack.pop()); render(); } }

        function updateSettings() {
            state.match_n = document.getElementById('in-match').value || "未設定の試合";
            state.p1_n = document.getElementById('in-p1').value || "後衛";
            state.p2_n = document.getElementById('in-p2').value || "前衛";
            state.opp_n = document.getElementById('in-opp').value || "相手";
            render();
        }

        function render() {
            document.getElementById('pts').innerText = state.p1 + " — " + state.p2;
            document.getElementById('gms').innerText = "G: " + state.g1 + " — " + state.g2;
            document.getElementById('game-mode').innerText = (state.is_final ? "FINAL" : state.match_type + "G");
            
            document.getElementById('m5').className = 'm-btn' + (state.match_type==5 ? ' active' : '');
            document.getElementById('m7').className = 'm-btn' + (state.match_type==7 ? ' active' : '');

            document.getElementById('serve-input-area').style.visibility = (state.active === 3) ? "hidden" : "visible";

            document.getElementById('lbl-s1').innerText = state.p1_n;
            document.getElementById('lbl-s2').innerText = state.p2_n;
            document.getElementById('tag1').innerText = state.p1_n;
            document.getElementById('tag2').innerText = state.p2_n;
            
            document.getElementById('tag1').className = 'p-btn' + (state.active==1 ? ' active' : '');
            document.getElementById('tag2').className = 'p-btn' + (state.active==2 ? ' active' : '');
            document.getElementById('tag3').className = 'p-btn' + (state.active==3 ? ' active' : '');
            
            var s1_v = state.serve.p1_in + "/" + state.serve.p1_total;
            var s2_v = state.serve.p2_in + "/" + state.serve.p2_total;
            var s1_pct = Math.round((state.serve.p1_in/(state.serve.p1_total||1))*100) + "%";
            var s2_pct = Math.round((state.serve.p2_in/(state.serve.p2_total||1))*100) + "%";
            document.getElementById('s1-pct').innerText = s1_pct;
            document.getElementById('s1-cnt').innerText = "(" + s1_v + ")";
            document.getElementById('s2-pct').innerText = s2_pct;
            document.getElementById('s2-cnt').innerText = "(" + s2_v + ")";

            document.getElementById('rep-match-name').innerText = state.match_n;
            document.getElementById('final-gms').innerText = state.g1 + " — " + state.g2;
            document.getElementById('final-names').innerText = state.p1_n + " ・ " + state.p2_n + " vs " + state.opp_n;
            document.getElementById('stats-head').innerHTML = "<tr><th>項目</th><th>"+state.p1_n+"</th><th>"+state.p2_n+"</th><th>相手</th></tr>";
            
            var rows = "<tr><td>1st成功率</td><td>"+s1_pct+" ("+s1_v+")</td><td>"+s2_pct+" ("+s2_v+")</td><td>-</td></tr>";
            var items = ['サービスエース', 'レシーブエース', 'ストローク', 'ボレー', 'スマッシュ', 'ネットイン', 'ダブルフォルト', 'レシーブミス', 'ストロークミス', 'ボレーミス', 'スマッシュミス'];
            items.forEach(item => {
                rows += "<tr><td>"+item+"</td><td>"+(state.stats.p1[item]||0)+"</td><td>"+(state.stats.p2[item]||0)+"</td><td>"+(state.stats.opp[item]||0)+"</td></tr>";
            });

            var p12_aces = 0, p12_miss = 0, opp_aces = 0, opp_miss = 0;
            ['サービスエース','レシーブエース','ストローク','ボレー','スマッシュ'].forEach(k => { 
                p12_aces += (state.stats.p1[k]||0) + (state.stats.p2[k]||0); 
                opp_aces += (state.stats.opp[k]||0);
            });
            ['ダブルフォルト','レシーブミス','ストロークミス','ボレーミス','スマッシュミス'].forEach(k => { 
                p12_miss += (state.stats.p1[k]||0) + (state.stats.p2[k]||0); 
                opp_miss += (state.stats.opp[k]||0);
            });
            rows += "<tr class='total-row'><td>エース計</td><td colspan='2' style='color:#007AFF;'>" + p12_aces + "</td><td style='color:#007AFF;'>" + opp_aces + "</td></tr>";
            rows += "<tr class='total-row'><td>ミス計</td><td colspan='2' style='color:#FF3B30;'>" + p12_miss + "</td><td style='color:#FF3B30;'>" + opp_miss + "</td></tr>";
            document.getElementById('stats-body').innerHTML = rows;

            var h = "";
            state.history.forEach((obj, i) => { 
                var label = obj.side === "S" ? '<span class="srv-mark">S</span>' : '<span class="srv-mark" style="color:#666;">R</span>';
                h += '<div class="history-item">G'+(i+1)+': '+label+obj.score+'</div>'; 
            });
            document.getElementById('history-area').innerHTML = h || '<div style="font-size:10px; color:#999;">データなし</div>';

            var memoVal = document.getElementById('match-memo').value;
            var memoDisp = document.getElementById('report-memo-display');
            if(memoVal.trim() !== "") {
                memoDisp.innerText = "【Match Memo】\\n" + memoVal;
                memoDisp.style.display = "block";
            } else {
                memoDisp.style.display = "none";
            }
        }
        init();
    </script>
</body>
</html>
"""

components.html(html_code, height=1500, scrolling=True)
