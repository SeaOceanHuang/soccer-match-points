import tkinter as tk
import re

class FootballPoints:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("积分计算器")
        
        tk.Label(self.window, text="输入或粘贴比分信息:").pack()
        self.input_text = tk.Text(self.window, height=8, width=50)
        self.input_text.pack()
        
        tk.Label(self.window, text="输入或粘贴历史积分信息:").pack()
        self.history_text = tk.Text(self.window, height=8, width=50)
        self.history_text.pack()
        
        tk.Button(self.window, text="计算积分", command=self.calculate_points).pack()
        tk.Button(self.window, text="清除输入", command=self.clear_input).pack()
        
        tk.Label(self.window, text="结果:").pack()
        self.results_table = tk.Text(self.window, height=12, width=50)
        self.results_table.pack()
        
        self.window.mainloop()
        
    def calculate_points(self):
        raw_text = self.input_text.get("1.0", "end-1c")
        matches = re.findall(r'([\u4e00-\u9fff ]+) (\d+)-(\d+) ([\u4e00-\u9fff ]+)', raw_text)
        teams = {}
        round_points = {}  # 保存每个队伍的本轮积分
        for home_team, home_score, away_score, away_team in matches:
            home_score, away_score = int(home_score), int(away_score)
            teams.setdefault(home_team, 0)
            teams.setdefault(away_team, 0)
            if home_score > away_score:
                teams[home_team] += 3
                round_points[home_team] = round_points.get(home_team, 0) + 3
            elif home_score < away_score:
                teams[away_team] += 3
                round_points[away_team] = round_points.get(away_team, 0) + 3
            else:
                teams[home_team] += 1
                teams[away_team] += 1
                round_points[home_team] = round_points.get(home_team, 0) + 1
                round_points[away_team] = round_points.get(away_team, 0) + 1
        
        history_text = self.history_text.get("1.0", "end-1c")
        history_matches = re.findall(r'([\u4e00-\u9fff ]+)(\d+)分', history_text)
        for team, points in history_matches:
            teams.setdefault(team, 0)
            teams[team] += int(points)
        
        sorted_teams = sorted(teams.items(), key=lambda x: x[1], reverse=True)
        result_text = "排名\t球队\t本轮积分\t总积分\n"
        for rank, (team, points) in enumerate(sorted_teams, start=1):
            result_text += f"{rank}\t{team}\t{round_points.get(team, 0)}\t{points}\n"
        self.results_table.delete('1.0', tk.END)
        self.results_table.insert('1.0', result_text)
        
    def clear_input(self):
        self.input_text.delete("1.0", "end")
        self.self.results_table.delete("1.0", "end")

if __name__ == '__main__':
    FootballPoints()