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
        body { font-family: -apple-system, sans-serif; background: #f5f5f5; padding: 10px; margin: 0; color: #333; }
        .card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        
        /* スコアボード */
        .score-box { background: #1a1a1a; color: white; border-radius: 10px; padding: 15px; text-align: center; }
        .gms { font-size: 18px; color: #4CAF50; font-weight: bold; }
        .pts { font-size: 50px; font-weight: 900; margin: 5px 0; line-height: 1; }
        .srv-info { font-size: 12px; color: #aaa; margin-top: 10px; display: flex; justify-content: space-around; }

        /* 入力エリア */
        .input-group { margin-bottom: 10px; }
        label { font-size: 11px; color: #666; font-weight: bold; margin-bottom: 3px; display: block; }
        input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; font-size: 14px; }
        
        /* プレイヤー選択 */
        .selector { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin: 15px 0; }
        .p-btn { padding: 12px 5px; border: 2px solid #E67E22; background: white; color: #E67E22; border-radius: 8px; font-weight: bold; text-align: center; cursor: pointer; }
        .p-btn.active { background: #E67E22; color: white; }

        /* ボタン類 */
        .btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
        .btn { padding: 15px 5px; border-radius: 6px; border: none; color: white; font-weight: bold; font-size: 13px; cursor: pointer; }
        .win { background: #007AFF; }
        .loss { background: #FF3B30; }
        .netin { background: #5856D6; grid-column: span 2; margin-top: 4px; }
        .undo { background: #8e8e93; grid-column: span 2; margin-top: 10px; }

        /* レポート */
        .report-title { background: #333; color: white; padding: 8px; border-radius: 6px 6px 0 0; text-align: center; font-weight: bold; margin: -15px -15px 15px -15px; }
        table { width: 100%; border-collapse: collapse; font-size: 11px; }
        th, td { border: 1px solid #eee; padding: 8px 4px; text-align: center; }
        th { background: #f9f9f9; }
        .memo-area { width: 100%; height: 60px; margin-top: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 12px; padding: 5px; box-sizing: border-box; }
    </style>
</head>
<body>

    <!-- 1. 試合設定入力 -->
    <div class="card">
        <div class="input-group"><label>試合名</label><input type="text" id="in-match" placeholder="大会名・対戦カード" oninput="updateNames()"></div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px;">
            <div class="input-group"><label>自分(後衛)</label><input type="text" id="in-p1" placeholder="名前" oninput="updateNames()"></div>
            <div class="input-group"><label>自分(前衛)</label><input type="text" id="in-p2" placeholder="名前" oninput="updateNames()"></div>
            <div class="input-group"><label>相手</label><input type="text" id="in-opp" placeholder="名前" oninput="updateNames()"></div>
        </div>
    </div>

    <!-- 2. スコア表示 -->
    <div class="card score-box">
        <div id="disp-match" style="font-size:12px; margin-bottom:5px; color:#aaa;">未設定の試合</div>
        <div id="disp-gms" class="gms">G: 0 - 0</div>
        <div id="disp-pts" class="pts">0 - 0</div>
        <div class="srv-info">
            <div id="srv-p1">1st: 0%</div>
            <div id="srv-p2">1st: 0%</div>
        </div>
    </div>

    <!-- 3. 入力操作 -->
    <div class="card">
        <div class="selector">
            <div id="sel1" class="p-btn active" onclick="setPlayer(1)">後衛</div>
            <div id="sel2" class="p-btn" onclick="setPlayer(2)">前衛</div>
            <div id="sel3" class="p-btn" onclick="setPlayer(3)">相手</div>
        </div>

        <div class="btn-grid" style="margin-bottom:10px;">
            <button class="btn" style="background:#28a745;" onclick="countServe(true)">1st イン</button>
            <button class="btn" style="background:#dc3545;" onclick="countServe(false)">1st フォルト</button>
        </div>

        <div id="action-btns" class="btn-grid">
            <!-- JSで生成 -->
        </div>
        
        <div class="btn-grid">
            <button class="btn netin" onclick="count('ネットイン', true)">ネットイン</button>
            <button class="btn undo" onclick="undo()">↩ 一つ戻る</button>
        </div>
    </div>

    <!-- 4. マッチレポート（集計） -->
    <div class="card">
        <div class="report-title">MATCH REPORT</div>
        <table id="report-table">
            <thead>
                <tr>
                    <th>項目</th>
                    <th id="h-p1">後衛</th>
                    <th id="h-p2">前衛</th>
                    <th id="h-opp">相手</th>
                </tr>
            </thead>
            <tbody id="report-body">
                <!-- リアルタイム集計 -->
            </tbody>
        </table>
        <textarea class="memo-area" id="memo" placeholder="試合のメモ..."></textarea>
    </div>

    <script>
        let state = {
            p1:0, p2:0, g1:0, g2:0, active:1,
            names: { match: "未設定の試合", p1: "後衛", p2: "前衛", opp: "相手" },
            stats: { p1: {}, p2: {}, opp: {} },
            serve: { p1_in: 0, p1_tot: 0, p2_in: 0, p2_tot: 0 }
        };
        let stack = [];

        const wins = ['サービスエース', 'レシーブエース', 'ストローク', 'ボレー', 'スマッシュ'];
        const loss = ['ダブルフォルト', 'レシーブミス', 'ストロークミス', 'ボレーミス', 'スマッシュミス'];

        function init() {
            const container = document.getElementById('action-btns');
            [...wins, ...loss, 'ネットイン'].forEach(item => {
                state.stats.p1[item] = 0; state.stats.p2[item] = 0; state.stats.opp[item] = 0;
            });

            for (let i = 0; i < wins.length; i++) {
                container.innerHTML += `<button class="btn win" onclick="count('${wins[i]}', true)">${wins[i]}</button>`;
                container.innerHTML += `<button class="btn loss" onclick="count('${loss[i]}', false)">${loss[i]}</button>`;
            }
            render();
        }

        function updateNames() {
            state.names.match = document.getElementById('in-match').value || "未設定の試合";
            state.names.p1 = document.getElementById('in-p1').value || "後衛";
            state.names.p2 = document.getElementById('in-p2').value || "前衛";
            state.names.opp = document.getElementById('in-opp').value || "相手";
            render();
        }

        function setPlayer(n) { state.active = n; render(); }

        function countServe(isIn) {
            if (state.active === 3) return;
            stack.push(JSON.stringify(state));
            let p = state.active === 1 ? 'p1' : 'p2';
            state.serve[p+'_tot']++;
            if (isIn) state.serve[p+'_in']++;
            render();
        }

        function count(label, isWin) {
            stack.push(JSON.stringify(state));
            let pKey = state.active === 1 ? 'p1' : (state.active === 2 ? 'p2' : 'opp');
            state.stats[pKey][label]++;

            if ((state.active < 3 && isWin) || (state.active === 3 && !isWin)) state.p1++;
            else state.p2++;

            if (state.p1 >= 4 && (state.p1 - state.p2) >= 2) { state.g1++; state.p1 = 0; state.p2 = 0; }
            else if (state.p2 >= 4 && (state.p2 - state.p1) >= 2) { state.g2++; state.p1 = 0; state.p2 = 0; }
            render();
        }

        function undo() { if (stack.length > 0) { state = JSON.parse(stack.pop()); render(); } }

        function render() {
            document.getElementById('disp-match').innerText = state.names.match;
            document.getElementById('disp-pts').innerText = state.p1 + " - " + state.p2;
            document.getElementById('disp-gms').innerText = "G: " + state.g1 + " - " + state.g2;
            document.getElementById('h-p1').innerText = state.names.p1;
            document.getElementById('h-p2').innerText = state.names.p2;
            document.getElementById('h-opp').innerText = state.names.opp;
            document.getElementById('sel1').innerText = state.names.p1;
            document.getElementById('sel2').innerText = state.names.p2;
            document.getElementById('sel3').innerText = state.names.opp;

            document.getElementById('sel1').className = 'p-btn' + (state.active === 1 ? ' active' : '');
            document.getElementById('sel2').className = 'p-btn' + (state.active === 2 ? ' active' : '');
            document.getElementById('sel3').className = 'p-btn' + (state.active === 3 ? ' active' : '');

            let s1 = Math.round((state.serve.p1_in/(state.serve.p1_tot||1))*100);
            let s2 = Math.round((state.serve.p2_in/(state.serve.p2_tot||1))*100);
            document.getElementById('srv-p1').innerText = state.names.p1 + " 1st: " + s1 + "%";
            document.getElementById('srv-p2').innerText = state.names.p2 + " 1st: " + s2 + "%";

            let rows = "";
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
