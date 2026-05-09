import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="Tennis Counter Pro", layout="centered")

# JavaScriptですべてを制御するHTML/JS
# Pythonのf-stringを完全に排除し、不具合の混入を防ぎます
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: sans-serif; margin: 0; padding: 10px; background: #f0f2f5; color: #333; }
        .card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        
        /* スコア表示 */
        .score-board { background: #1a1a1a; color: white; text-align: center; padding: 15px; border-radius: 8px; }
        .gms { font-size: 18px; color: #4CAF50; font-weight: bold; }
        .pts { font-size: 48px; font-weight: 900; margin: 5px 0; }
        
        /* プレイヤー選択 */
        .selector { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin: 15px 0; }
        .p-btn { padding: 12px; border: 2px solid #E67E22; background: white; color: #E67E22; border-radius: 8px; font-weight: bold; cursor: pointer; text-align: center; }
        .p-btn.active { background: #E67E22; color: white; }

        /* 入力ボタン */
        .btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
        .btn { padding: 15px; border-radius: 6px; border: none; color: white; font-weight: bold; cursor: pointer; font-size: 14px; }
        .win { background: #007AFF; }
        .loss { background: #FF3B30; }
        .undo { background: #666; grid-column: span 2; margin-top: 8px; }

        /* レポート */
        .report-title { background: #333; color: white; padding: 8px; border-radius: 4px; text-align: center; font-weight: bold; margin-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; font-size: 12px; }
        th, td { border: 1px solid #ddd; padding: 8px 4px; text-align: center; }
        th { background: #f8f8f8; }
        .total-row { background: #eee; font-weight: bold; }
    </style>
</head>
<body>

    <div class="card score-board">
        <div id="display-gms">G: 0 - 0</div>
        <div id="display-pts" class="pts">0 - 0</div>
        <div id="display-mode" style="font-size:12px; color:#E67E22;">5G MATCH</div>
    </div>

    <div class="selector">
        <div id="sel1" class="p-btn active" onclick="setPlayer(1)">後衛</div>
        <div id="sel2" class="p-btn" onclick="setPlayer(2)">前衛</div>
        <div id="sel3" class="p-btn" onclick="setPlayer(3)">相手</div>
    </div>

    <div class="card">
        <div class="btn-grid" id="action-buttons">
            <!-- JSでボタンを生成 -->
        </div>
        <button class="btn undo" onclick="undo()">一つ戻る (Undo)</button>
    </div>

    <div class="card">
        <div class="report-title">MATCH REPORT (集計)</div>
        <table>
            <thead>
                <tr>
                    <th>項目</th>
                    <th id="h-p1">後衛</th>
                    <th id="h-p2">前衛</th>
                    <th>相手</th>
                </tr>
            </thead>
            <tbody id="report-body">
                <!-- ここに集計がリアルタイムで入ります -->
            </tbody>
        </table>
    </div>

    <script>
        // --- データ管理 ---
        let state = {
            pts1: 0, pts2: 0, gms1: 0, gms2: 0,
            active: 1, // 1:後衛, 2:前衛, 3:相手
            stats: {
                p1: {}, p2: {}, opp: {}
            }
        };
        let history = [];

        const winLabels = ['サービスエース', 'レシーブエース', 'ストローク', 'ボレー', 'スマッシュ'];
        const lossLabels = ['ダブルフォルト', 'レシーブミス', 'ストロークミス', 'ボレーミス', 'スマッシュミス'];

        // --- 初期化 ---
        function init() {
            const container = document.getElementById('action-buttons');
            const allItems = [...winLabels, ...lossLabels];
            
            // 統計データの初期化
            allItems.forEach(label => {
                state.stats.p1[label] = 0;
                state.stats.p2[label] = 0;
                state.stats.opp[label] = 0;
            });

            // ボタン作成
            for (let i = 0; i < winLabels.length; i++) {
                const wBtn = document.createElement('button');
                wBtn.className = 'btn win';
                wBtn.innerText = winLabels[i];
                wBtn.onclick = () => count(winLabels[i], true);

                const lBtn = document.createElement('button');
                lBtn.className = 'btn loss';
                lBtn.innerText = lossLabels[i];
                lBtn.onclick = () => count(lossLabels[i], false);

                container.appendChild(wBtn);
                container.appendChild(lBtn);
            }
            render();
        }

        function setPlayer(n) {
            state.active = n;
            render();
        }

        function count(label, isWin) {
            // 履歴保存
            history.push(JSON.stringify(state));

            // 統計加算
            const pKey = state.active === 1 ? 'p1' : (state.active === 2 ? 'p2' : 'opp');
            state.stats[pKey][label]++;

            // スコア加算
            // 自分(1 or 2)がWin、または相手(3)がLossなら自分に点数
            if ((state.active < 3 && isWin) || (state.active === 3 && !isWin)) {
                state.pts1++;
            } else {
                state.pts2++;
            }

            checkScore();
            render();
        }

        function checkScore() {
            if (state.pts1 >= 4 && (state.pts1 - state.pts2) >= 2) {
                state.gms1++; state.pts1 = 0; state.pts2 = 0;
            } else if (state.pts2 >= 4 && (state.pts2 - state.pts1) >= 2) {
                state.gms2++; state.pts1 = 0; state.pts2 = 0;
            }
        }

        function undo() {
            if (history.length > 0) {
                state = JSON.parse(history.pop());
                render();
            }
        }

        function render() {
            // スコア更新
            document.getElementById('display-pts').innerText = state.pts1 + " - " + state.pts2;
            document.getElementById('display-gms').innerText = "G: " + state.gms1 + " - " + state.gms2;

            // 選択ボタン更新
            document.getElementById('sel1').className = 'p-btn' + (state.active === 1 ? ' active' : '');
            document.getElementById('sel2').className = 'p-btn' + (state.active === 2 ? ' active' : '');
            document.getElementById('sel3').className = 'p-btn' + (state.active === 3 ? ' active' : '');

            // レポート更新 (ここが重要！)
            let html = "";
            const items = [...winLabels, ...lossLabels];
            
            items.forEach(item => {
                html += `<tr>
                    <td>${item}</td>
                    <td>${state.stats.p1[item]}</td>
                    <td>${state.stats.p2[item]}</td>
                    <td>${state.stats.opp[item]}</td>
                </tr>`;
            });
            document.getElementById('report-body').innerHTML = html;
        }

        init();
    </script>
</body>
</html>
"""

# Streamlitで表示（高さは適宜調整してください）
components.html(html_content, height=1000, scrolling=True)
