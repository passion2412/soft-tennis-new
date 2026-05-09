import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import os

# --- 1. 設定 ---
st.set_page_config(page_title="Tennis Counter Pro", layout="centered")

# --- 2. HTML/JavaScript ---
html_content = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: -apple-system, sans-serif; background: white; padding: 2px; margin: 0; }
        /* スコアボックス（最上部） */
        .score-box { 
            background: #1a1a1a; color: white; border-radius: 8px; 
            display: grid; grid-template-columns: 85px 1fr 85px; 
            padding: 12px 8px; margin-bottom: 6px; align-items: center;
        }
        .srv-stats-area { text-align: left; font-size: 10px; line-height: 1.3; }
        .srv-val { font-size: 11px; color: white; font-weight: bold; }
        .score-center { text-align: center; }
        .main-score { font-size: 42px; font-weight: 900; line-height: 1; margin: 0; }
        .game-score { font-size: 18px; color: #4CAF50; font-weight: 900; }
        
        /* プレイヤー選択 */
        .player-selector { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4px; margin: 8px 0; }
        .p-btn { border: 2px solid #E67E22; background: white; color: #E67E22; padding: 12px 2px; border-radius: 6px; font-weight: bold; text-align: center; cursor: pointer; font-size: 14px; }
        .p-btn.active { background: #E67E22; color: white; }

        /* サーブボタン */
        .serve-btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 6px; }
        .s-btn { height: 38px; border-radius: 19px; border: none; color: white; font-weight: bold; cursor: pointer; font-size: 13px; }
        
        /* メイン入力ボタン */
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 8px; }
        .btn { height: 44px; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px; border: none; cursor: pointer; }
        .btn-win { background-color: #007AFF; }
        .btn-loss { background-color: #FF3B30; }
        
        /* 特殊操作 */
        .bottom-action-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 20px; }
        .netin-btn { background: #5856D6; color: white; border: none; padding: 12px; border-radius: 4px; font-weight: bold; font-size: 14px; }
        .undo-btn { background: #666; color: white; border: none; padding: 12px; border-radius: 4px; font-weight: bold; font-size: 14px; }

        /* マッチレポート（ここが集計の肝） */
        .report-card { border: 2px solid #333; border-radius: 8px; padding: 10px; background: #fff; margin-top: 20px; }
        .report-title { font-size: 14px; font-weight: bold; background: #333; color: white; margin: -10px -10px 10px -10px; padding: 8px; border-radius: 6px 6px 0 0; text-align: center; }
        table { width: 100%; border-collapse: collapse; font-size: 11px; }
        th, td { border: 1px solid #ddd; padding: 6px 2px; text-align: center; }
        th { background: #f8f8f8; }

        /* 設定エリア（折りたたみ） */
        details { margin-top: 20px; padding: 10px; border: 1px solid #eee; background: #fafafa; border-radius: 8px; }
        input { width: 100%; padding: 8px; margin: 4px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        .reset-btn { background: #f44336; color: white; width: 100%; padding: 10px; border: none; border-radius: 4px; margin-top: 10px; font-weight: bold; }
    </style>
</head>
<body>
    <div id="main-ui">
        <!-- スコア表示 -->
        <div class="score-box">
            <div class="srv-stats-area">
                <div><span id="lbl-s1">後衛</span>: <span id="s1-pct" class="srv-val">0%</span></div>
                <div><span id="lbl-s2">前衛</span>: <span id="s2-pct" class="srv-val">0%</span></div>
            </div>
            <div class="score-center">
                <div id="gms" class="game-score">G: 0 — 0</div>
                <div id="pts" class="main-score">0 — 0</div>
            </div>
            <div style="text-align:right; font-size:10px; color:#E67E22; font-weight:bold;">TENNIS PRO</div>
        </div>

        <!-- プレイヤー選択 -->
        <div class="player-selector">
            <div id="tag1" class="p-btn active" onclick="setPlayer(1)">後衛</div>
            <div id="tag2" class="p-btn" onclick="setPlayer(2)">前衛</div>
            <div id="tag3" class="p-btn" onclick="setPlayer(3)">相手</div>
        </div>

        <!-- サーブ -->
        <div class="serve-btn-grid">
            <button class="s-btn" style="background:#28a745;" onclick="countServe(true)">1st イン</button>
            <button class="s-btn" style="background:#dc3545;" onclick="countServe(false)">1st フォルト</button>
        </div>

        <!-- メイン入力 -->
        <div class="grid" id="button-area"></div>
        
        <!-- 下部ボタン -->
        <div class="bottom-action-grid">
            <button class="netin-btn" onclick="count('ネットイン', true)">ネットイン</button>
            <button class="undo-btn" onclick="undo()">↩ 戻る</button>
        </div>
    </div>

    <!-- レポート表示 -->
    <div class="report-card">
        <div class="report-title">MATCH REPORT (集計)</div>
        <div id="rep-match" style="text-align:center; font-size:11px; margin-bottom:5px; color:#666;"></div>
        <table>
            <thead>
                <tr>
                    <th>項目</th>
                    <th id="h-p1">後衛</th>
                    <th id="h-p2">前衛</th>
                    <th id="h-opp">相手</th>
                </tr>
            </thead>
            <tbody id="report-body"></tbody>
        </table>
        <textarea id="memo" style="width:100%; height:50px; margin-top:10px; font-size:11px;" placeholder="メモ..."></textarea>
    </div>

    <!-- 設定 -->
    <details>
        <summary>⚙️ 名前・試合設定 / リセット</summary>
        <input type="text" id="in-match" placeholder="試合名" oninput="updateSettings()">
        <input type="text" id="in-p1" placeholder="後衛の名前" oninput="updateSettings()">
        <input type="text" id="in-p2" placeholder="前衛の名前" oninput="updateSettings()">
        <input type="text" id="in-opp" placeholder="相手の名前" oninput="updateSettings()">
        <button class="reset-btn" onclick="if(confirm('全てのデータを消去しますか？')){location.reload();}">データをリセット</button>
    </details>

    <script>
        var state = {
            p1:0, p2:0, g1:0, g2:0, active:1,
            p1_n: "後衛", p2_n: "前衛", opp_n: "相手", match_n: "未設定の試合",
            stats: { p1: {}, p2: {}, opp: {} },
            serve: { p1_in: 0, p1_tot: 0, p2_in: 0, p2_tot: 0 }
        };
        var stack = [];
        var wins = ['サービスエース', 'レシーブエース', 'ストローク', 'ボレー', 'スマッシュ'];
        var loss = ['ダブルフォルト', 'レシーブミス', 'ストロークミス', 'ボレーミス', 'スマッシュミス'];

        function init() {
            var area = document.getElementById('button-area');
            [...wins, ...loss, 'ネットイン'].forEach(item => {
                state.stats.p1[item] = 0; state.stats.p2[item] = 0; state.stats.opp[item] = 0;
            });
            for(var i=0; i<wins.length; i++) {
                var w = wins[i], l = loss[i];
                area.innerHTML += `<button class="btn btn-win" onclick="count('${w}',true)">${w}</button>`;
                area.innerHTML += `<button class="btn btn-loss" onclick="count('${l}',false)">${l}</button>`;
            }
            render();
        }

        function setPlayer(n) { state.active = n; render(); }
        function countServe(isIn) {
            if(state.active === 3) return;
            stack.push(JSON.stringify(state));
            var p = (state.active === 1) ? 'p1' : 'p2';
            state.serve[p+'_tot']++;
            if(isIn) state.serve[p+'_in']++;
            render();
        }

        function count(label, isWin) {
            stack.push(JSON.stringify(state));
            var pKey = (state.active === 1) ? 'p1' : (state.active === 2 ? 'p2' : 'opp');
            state.stats[pKey][label]++;
            if ((state.active < 3 && isWin) || (state.active === 3 && !isWin)) state.p1++; else state.p2++;
            if (state.p1 >= 4 && (state.p1 - state.p2) >= 2) { state.g1++; state.p1 = 0; state.p2 = 0; }
            else if (state.p2 >= 4 && (state.p2 - state.p1) >= 2) { state.g2++; state.p1 = 0; state.p2 = 0; }
            render();
        }

        function undo() { if(stack.length > 0){ state = JSON.parse(stack.pop()); render(); } }

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
            document.getElementById('tag1').innerText = state.p1_n;
            document.getElementById('tag2').innerText = state.p2_n;
            document.getElementById('tag3').innerText = state.opp_n;
            document.getElementById('lbl-s1').innerText = state.p1_n;
            document.getElementById('lbl-s2').innerText = state.p2_n;
            document.getElementById('h-p1').innerText = state.p1_n;
            document.getElementById('h-p2').innerText = state.p2_n;
            document.getElementById('h-opp').innerText = state.opp_n;
            document.getElementById('rep-match').innerText = state.match_n;
            
            document.getElementById('tag1').className = 'p-btn' + (state.active==1 ? ' active' : '');
            document.getElementById('tag2').className = 'p-btn' + (state.active==2 ? ' active' : '');
            document.getElementById('tag3').className = 'p-btn' + (state.active==3 ? ' active' : '');
            
            document.getElementById('s1-pct').innerText = Math.round((state.serve.p1_in/(state.serve.p1_tot||1))*100) + "%";
            document.getElementById('s2-pct').innerText = Math.round((state.serve.p2_in/(state.serve.p2_tot||1))*100) + "%";

            var rows = "";
            [...wins, ...loss, 'ネットイン'].forEach(item => {
                rows += `<tr><td>${item}</td><td>${state.stats.p1[item]}</td><td>${state.stats.p2[item]}</td><td>${state.stats.opp[item]}</td></tr>`;
            });
            document.getElementById('report-body').innerHTML = rows;
        }
        init();
    </script>
</body>
</html>
"""

components.html(html_content, height=1200, scrolling=True)
