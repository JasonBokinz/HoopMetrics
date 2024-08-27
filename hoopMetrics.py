# Scoring Distribution:
# Examine how scoring is distributed among players in a team. 
# Identify the top scorers, role players, and their contributions to the team's overall offensive output.

import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import os

class NBAStats:
    def __init__(self, root):
        self.root = root
        self.root.title("NBA Team Scoring Distributions")

        # Load NBA logo image
        nba_logo_image = Image.open("NBA_logo.png")
        nba_logo_image = nba_logo_image.resize((100, 200))
        self.nba_logo = ImageTk.PhotoImage(nba_logo_image)

        # Configure rows and columns to expand the content
        for i in range(16):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(8):
            self.root.grid_columnconfigure(i, weight=1)

        # Title Label
        self.title_label = tk.Label(root, text="NBA Team Statistics", font=("Helvetica", 40, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=8, pady=(60, 30))

        # Welcome Label
        self.welcome_label = tk.Label(root, text="Welcome, please select a team from below:", font=("Helvetica", 35))
        self.welcome_label.grid(row=1, column=0, columnspan=8, pady=20)

        # NBA Logo
        self.logo_label = tk.Label(root, image=self.nba_logo)
        self.logo_label.grid(row=0, column=5, padx=0, pady=0, sticky='e')

        # Dictionary with NBA divisions and corresponding teams
        self.divisions = {
            "Atlantic Division": ["Boston Celtics", "Brooklyn Nets", "New York Knicks", "Philadelphia 76ers", "Toronto Raptors"],
            "Central Division": ["Chicago Bulls", "Cleveland Cavaliers", "Detroit Pistons", "Indiana Pacers", "Milwaukee Bucks"],
            "Southeast Division": ["Atlanta Hawks", "Charlotte Hornets", "Miami Heat", "Orlando Magic", "Washington Wizards"],
            "Northwest Division": ["Denver Nuggets", "Minnesota Timberwolves", "Oklahoma City Thunder", "Portland Trail Blazers", "Utah Jazz"],
            "Pacific Division": ["Golden State Warriors", "LA Clippers", "Los Angeles Lakers", "Phoenix Suns", "Sacramento Kings"],
            "Southwest Division": ["Dallas Mavericks", "Houston Rockets", "Memphis Grizzlies", "New Orleans Pelicans", "San Antonio Spurs"]
        }

        # Create buttons for each division in separate rows
        for row_num, (division, teams) in enumerate(self.divisions.items()):
            self.create_team_buttons(division, teams, row_num * 2 + 2)

    def create_team_buttons(self, division_name, teams, row):
        division_label = tk.Label(self.root, text=division_name + ":", font=("Helvetica", 20, "bold"))
        division_label.grid(row=row, column=0, pady=(20, 10), sticky='e')

        for i, team in enumerate(teams):
            team_button = tk.Button(self.root, text=team, command=lambda t=team: self.team_selected(t), padx=20, pady=10, font=("Helvetica", 16), width=15)
            team_button.grid(row=row, column=i + 2, pady=10, padx=(0, 20), sticky='w')

        # White line to separate divisions
        frame = tk.Frame(self.root, bg='white', height=2, bd=0, relief='ridge')
        frame.grid(row=row + 1, column=1, columnspan=6, sticky='ew')
    
    def team_selected(self, team_name):
        # Remove labels and buttons below
        for widget in self.root.winfo_children():
            widget.destroy()

        # Team Variable
        team = team_name.split(" ")[-1]

        # Create Frames
        back_frame = tk.Frame(root)
        back_frame.place(x = 0, y = 0, relwidth = 1/3, relheight = 0.1)
        back_frame.columnconfigure((0), weight = 1)
        back_frame.rowconfigure((0), weight = 1)
        selected_frame = tk.Frame(root)
        selected_frame.place(relx=1/3, y = 0, relwidth=1/3, relheight=0.1)
        selected_frame.columnconfigure((0), weight = 1)
        selected_frame.rowconfigure((0), weight = 1)
        logo_frame = tk.Frame(root)
        logo_frame.place(relx=2/3, y=0, relwidth=1/3, relheight=0.1)
        logo_frame.columnconfigure((0), weight = 1)
        logo_frame.rowconfigure((0), weight = 1)
        notebook_frame = tk.Frame(root)
        notebook_frame.place(x=0, rely=0.1, relwidth=1, relheight=0.9)
        notebook_frame.columnconfigure((0), weight = 1)
        notebook_frame.rowconfigure((0), weight = 1)

        # Create Back Button
        self.back_button = tk.Button(back_frame, text="Back", command=self.back_to_teams, padx=20, pady=10, font=("Helvetica", 16), width=15)
        self.back_button.grid(row=0, column=0)

        # Create Selected Label
        self.selected_label = tk.Label(selected_frame, text=f"Selected: {team_name}", font=("Helvetica", 30, "bold"))
        self.selected_label.grid(row=0, column=0, sticky='nsew')

        # Create NBA Logo Image
        team_logo_path = os.path.join("NBA_Logos", f"{team}.png")
        nba_team_image = Image.open(team_logo_path)
        nba_team_image = nba_team_image.resize((100, 100))
        self.team_logo = ImageTk.PhotoImage(nba_team_image)
        self.team_logo_label = tk.Label(logo_frame, image=self.team_logo)
        self.team_logo_label.grid(row=0, column=0,  sticky='nsew')

        # Update Widgets
        self.root.update_idletasks()

        # Create a Notebook widget
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.grid(row=0, column=0, sticky='nsew')

        # Add tabs to the Notebook
        about_tab = tk.Frame(self.notebook)
        franchise_tab = tk.Frame(self.notebook)
        player_stats_tab = tk.Frame(self.notebook)
        game_to_game_tab = tk.Frame(self.notebook)

        self.notebook.add(about_tab, text='ABOUT')
        self.notebook.add(franchise_tab, text='FRANCHISE')
        self.notebook.add(player_stats_tab, text='PLAYER STATS')
        self.notebook.add(game_to_game_tab, text='GAME-TO-GAME')

        # Set up Chrome options for headless mode
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless=new")  # Enable headless mode
        # chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (necessary in headless mode)
        # driver = webdriver.Chrome(options=chrome_options)
        driver = webdriver.Chrome()

        team_id_num = self.getTeamPage(team.lower())
        team_roster = self.getRoster(driver, f'https://www.nba.com/team/{team_id_num}/{team.lower()}')
        coaching_array = self.getCoachingStaff(driver, f'https://www.nba.com/team/{team_id_num}/{team.lower()}')
        updates_array = self.getTeamUpdates(driver, f'https://www.nba.com/team/{team_id_num}/{team.lower()}')
        player_specifc_stats = self.getPlayerStats(driver, f'https://www.nba.com/stats/team/{team_id_num}/players-traditional')
        overall_stats = self.getOverallStats(driver, f'https://www.nba.com/stats/team/{team_id_num}/traditional')
        retired_numbers = self.getRetiredNumbers(driver, f'https://www.nba.com/team/{team_id_num}/{team.lower()}')
        hall_of_fame = self.getHallOfFame(driver, f'https://www.nba.com/team/{team_id_num}/{team.lower()}')
        all_time = self.getAllTime(driver, f'https://www.nba.com/team/{team_id_num}/{team.lower()}')
        achievements = self.getAchievements(driver, f'https://www.nba.com/team/{team_id_num}/{team.lower()}')

        # About Tab
        self.About(about_tab, team_roster, coaching_array, updates_array)
        self.Franchise(franchise_tab, retired_numbers, hall_of_fame, all_time, achievements)
        self.Player_Stats(player_stats_tab, team_roster, player_specifc_stats, overall_stats)
        # self.populate_game_to_game_tab(game_to_game_tab, team)
        print("DONE")


    def About(self, tab, team_roster, coaching_array, updates_array):
        # Update the GUI again
        self.root.update_idletasks()

        # Roster Frame
        roster_frame = tk.Frame(tab)
        roster_frame.place(x = 0, y = 0, relwidth = 1, relheight = 0.55)
        roster_frame.columnconfigure((0), weight = 1)
        roster_frame.rowconfigure((0, 1, 2, 3, 4), weight = 1)

        # Roster Label
        roster_label = tk.Label(roster_frame, text="--ROSTER--", fg = 'lightgray', font=("Helvetica", 15, "bold"))
        roster_label.grid(row = 0, column = 0, sticky = 'nsw')

        # Roster Treeview
        roster_table = ttk.Treeview(roster_frame, columns = team_roster[0], show = 'headings', height = len(team_roster))
        roster_table.config(selectmode = "none")
        roster_table.grid(row = 1, column = 0, rowspan = 4, sticky = 'nsew')

        # Add Column Names to Treeview
        for col in team_roster[0]:
            roster_table.heading(col, text=col)
        
        # Add Column Widths
        roster_table.column(team_roster[0][0], width=120)
        roster_table.column(team_roster[0][1], width=10)
        roster_table.column(team_roster[0][2], width=45)
        roster_table.column(team_roster[0][3], width=45)
        roster_table.column(team_roster[0][4], width=45)
        roster_table.column(team_roster[0][5], width=75)
        roster_table.column(team_roster[0][6], width=10)
        roster_table.column(team_roster[0][7], width=10)
        roster_table.column(team_roster[0][8], width=80)

        # Add data to Treeview
        for row in team_roster[1:]:
            roster_table.insert(parent = '', index = tk.END, values = row)

        # Add Coaching Frame
        coaching_frame = tk.Frame(tab, bg = "#404040")
        coaching_frame.place(x = 0, rely = 0.55, relwidth = 0.35, relheight = 0.45)
        coaching_frame.columnconfigure((0, 1, 2), weight = 1)
        coaching_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21), weight = 1)

        # Coaching Staff Label
        # All Time Label
        for i in range(3):
            temp = tk.Label(coaching_frame, fg = 'lightgray', font=("Helvetica", 15, "bold"))
            temp.grid(row = 0, column = i, sticky = 'nsew')
        coaching_label = tk.Label(coaching_frame, text="--COACHING STAFF--", fg = 'lightgray', font=("Helvetica", 15, "bold"))
        coaching_label.grid(row = 0, column = 0,sticky = 'nsw')

        # Coaching Staff
        row_num = 1
        for i in range(len(coaching_array[0])):
            pos = tk.Label(coaching_frame, text=f'{coaching_array[0][i]}:', bg="#404040", fg="white", font=("Helvetica", 14, "bold"))
            pos.grid(row=row_num, column=0, sticky="nsw")
            for j in range(len(coaching_array[1:][i])):
                coach = tk.Label(coaching_frame, text=f'{coaching_array[1:][i][j]}', bg="#404040", fg="white", padx=10, font=("Helvetica", 13))
                coach.grid(row=row_num, column=1, columnspan=2, sticky="nsw")
                row_num += 1

        # Add Updates Frame
        updates_frame = tk.Frame(tab, bg='black')
        updates_frame.place(relx = 0.4, rely = 0.55, relwidth = 0.6, relheight = 0.45)
        updates_frame.columnconfigure((0, 1, 2), weight = 1)
        updates_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight = 1)


        # Team Updates Label
        for i in range(3):
            temp = tk.Label(updates_frame, fg = 'lightgray', font=("Helvetica", 15, "bold"))
            temp.grid(row = 0, column = i, sticky = 'nsew')
        updates_label = tk.Label(updates_frame, text="--TEAM UPDATES--", fg = 'lightgray', font=("Helvetica", 15, "bold"))
        updates_label.grid(row = 0, column = 0, sticky = 'nsw')

        # Updates
        row_num = 1
        for i in range(len(updates_array[0])):
            time = tk.Label(updates_frame, text=f"{updates_array[i].get('date')}", bg="black", fg="darkgray", padx=5, font=("Helvetica", 11))
            time.grid(row=row_num, column=0, columnspan=3, sticky="sw")
            header = tk.Label(updates_frame, text=f"{updates_array[i].get('headline')}", bg="black", fg="white", padx=5, font=("Helvetica", 13, "bold"))
            header.grid(row=row_num+1, column=0, columnspan=3, sticky="nsw")
            content = tk.Label(updates_frame, text=updates_array[i].get('content'), bg='black', fg='white', padx=5, font=("Helvetica", 12), wraplength=800, justify='left')
            content.grid(row=row_num+2, column=0, columnspan=3, sticky='new')
            row_num += 3

    def Player_Stats(self, tab, team_roster, player_stats, overall_stats):
        # Update the GUI again
        self.root.update_idletasks()

        # Player 1 Frame
        player_1_frame = tk.Frame(tab)
        player_1_frame.place(x = 0, y = 0, relwidth = 0.2, relheight = 0.55)
        player_1_frame.columnconfigure((0), weight = 1)
        player_1_frame.rowconfigure((0, 1, 2, 3, 4), weight = 1)

        # Choose Player 1 Label
        player_1_label = tk.Label(player_1_frame, text="--CHOOSE PLAYER 1--", fg = 'lightgray', font=("Helvetica", 15, "bold"))
        player_1_label.grid(row = 0, column = 0, sticky = 'nsw')

        # Roster Treeview
        roster_table_1 = ttk.Treeview(player_1_frame, columns = team_roster[0][:3], show = 'headings', height = len(team_roster))
        roster_table_1.config(selectmode="browse")
        roster_table_1.grid(row = 1, column = 0, rowspan = 4, sticky = 'nsew')

        # Add Column Names to Treeview
        for col in team_roster[0][:3]:
            roster_table_1.heading(col, text=col)
        
        # Add Column Widths
        roster_table_1.column(team_roster[0][0], width=120)
        roster_table_1.column(team_roster[0][1], width=10)
        roster_table_1.column(team_roster[0][2], width=45)
        

        # Add data to Treeview
        for row in team_roster[1:]:
            roster_table_1.insert(parent = '', index = tk.END, values = row[:3])

        # Player 2 Frame
        player_2_frame = tk.Frame(tab)
        player_2_frame.place(relx = 0.8, y = 0, relwidth = 0.2, relheight = 0.55)
        player_2_frame.columnconfigure((0), weight = 1)
        player_2_frame.rowconfigure((0, 1, 2, 3, 4), weight = 1)

        # Choose Player 2 Label
        player_2_label = tk.Label(player_2_frame, text="--CHOOSE PLAYER 2--", fg = 'lightgray', font=("Helvetica", 15, "bold"))
        player_2_label.grid(row = 0, column = 0, sticky = 'nse')

        # Roster Treeview
        roster_table_2 = ttk.Treeview(player_2_frame, columns = team_roster[0][:3], show = 'headings', height = len(team_roster))
        roster_table_2.config(selectmode="browse")
        roster_table_2.grid(row = 1, column = 0, rowspan = 4, sticky = 'nsew')

        # Add Column Names to Treeview
        for col in team_roster[0][:3]:
            roster_table_2.heading(col, text=col)
        
        # Add Column Widths
        roster_table_2.column(team_roster[0][0], width=120)
        roster_table_2.column(team_roster[0][1], width=10)
        roster_table_2.column(team_roster[0][2], width=45)

        # Add data to Treeview
        for row in team_roster[1:]:
            roster_table_2.insert(parent = '', index = tk.END, values = row[:3])

        # Each Treeview Selection
        selection_array = [team_roster[1][0], team_roster[2][0]]
        roster_table_1.bind("<<TreeviewSelect>>", lambda event, table=roster_table_1: player_select(event, tab, table, 0, selection_array))
        roster_table_2.bind("<<TreeviewSelect>>", lambda event, table=roster_table_2: player_select(event, tab, table, 1, selection_array))

        # Team Stats Fram
        team_stats_frame = tk.Frame(tab)
        team_stats_frame.place(x = 0, rely = 0.75, relwidth = 1, relheight = 0.25)
        team_stats_frame.rowconfigure((0, 1, 2, 3, 4), weight = 1)
        team_stats_frame.columnconfigure((0, 1, 2, 3), weight = 1)

        # Team Stats Label
        team_stats_label = tk.Label(team_stats_frame, text="--OVERALL TEAM STATS--", fg = 'lightgray', font=("Helvetica", 15, "bold"))
        team_stats_label.grid(row = 0, column = 0, sticky = 'nsw')

        # Team Stats Treeview
        team_stats = ttk.Treeview(team_stats_frame, columns = overall_stats[0], show = 'headings', height = len(overall_stats))
        team_stats.config(selectmode = 'none')
        team_stats.grid(row = 1, column = 0, rowspan = 4, columnspan = 4, sticky = 'nsew')

        # Set column widths
        for col in overall_stats[0]:
            team_stats.column(col, width=25)

        team_stats.column(overall_stats[0][0], width=35)

        # Add column names to Treeview
        for col in overall_stats[0]:
            team_stats.heading(col, text=col)

        # Add data to Treeview
        for row in overall_stats[1:]:
            team_stats.insert('', tk.END, values=row)

        def player_select(_, tab, table, i, selection_array):
            selected_item = table.selection()[0]  # Get the selected item (assuming single selection)
            index = table.index(selected_item)  # Get the index of the selected item
            player = team_roster[index + 1][0]
            selection_array[i] = player

            player_1_stats = self.getPlayer(selection_array[0], player_stats)
            player_2_stats = self.getPlayer(selection_array[1], player_stats)

            # Add Comparison Frame
            comparison_frame = tk.Frame(tab)
            comparison_frame.place(relx = 0.35, y = 0, relwidth = 0.3, relheight = 0.7)
            comparison_frame.columnconfigure((0), weight = 1)
            comparison_frame.rowconfigure((0, 1, 2, 3, 4), weight = 1)

            # Comparison Label
            comparison_label = tk.Label(comparison_frame, text="--PLAYER COMPARISON--", fg = 'lightgray', font=("Helvetica", 15, "bold"))
            comparison_label.grid(row = 0, column = 0, sticky = 'nsew')

            # Comparison Treeview
            comparison_table = ttk.Treeview(comparison_frame, columns = ["PLAYER 1", "", "PLAYER 2"], show = 'headings', height = len(player_1_stats))
            comparison_table.config(selectmode="none")
            comparison_table.grid(row = 1, column = 0, rowspan = 4, sticky = 'nsew')

            # Add Column Names to Treeview
            comparison_table.heading("PLAYER 1", text='PLAYER 1')
            comparison_table.heading("", text='')
            comparison_table.heading("PLAYER 2", text='PLAYER 2')
            
            # Add Column Widths
            comparison_table.column("PLAYER 1", width=120, anchor='e')
            comparison_table.column("", width=100, anchor='center')
            comparison_table.column("PLAYER 2", width=120, anchor='w')

            # Add Legend Frame
            legend_frame = tk.Frame(tab)
            legend_frame.place(relx = 0.35, rely = 0.7, relwidth = 0.3, relheight = 0.075)
            legend_frame.columnconfigure((0,), weight = 1)
            legend_frame.rowconfigure((0, 1, 2), weight = 1)

            # Add Legend Label
            green_label = tk.Label(legend_frame, text="GREEN:  PLAYER 1  >  PLAYER 2", fg = 'green', font=("Helvetica", 12, "bold"))
            green_label.grid(row = 0, column = 0, sticky = 'nsew', pady=3)
            red_label = tk.Label(legend_frame, text="RED:  PLAYER 1  <  PLAYER 2", fg = 'red', font=("Helvetica", 12))
            red_label.grid(row = 1, column = 0, sticky = 'nsew', pady=3)
            white_label = tk.Label(legend_frame, text="WHITE:  PLAYER 1  =  PLAYER 2", fg = 'white', font=("Helvetica", 12))
            white_label.grid(row = 2, column = 0, sticky = 'nsew', pady=3)

            # Add data to Treeview
            comparison_table.insert(parent = '', index = tk.END, values = [player_1_stats[0], player_stats[0][0], player_2_stats[0]])
            for i in range(len(player_1_stats)-1):
                if float(player_1_stats[i+1]) > float(player_2_stats[i+1]):
                    color_player_1 = 'green'
                    color_player_2 = 'red'
                elif float(player_1_stats[i+1]) < float(player_2_stats[i+1]):
                    color_player_1 = 'red'
                    color_player_2 = 'green'
                else:
                    color_player_1 = 'white'
                    color_player_2 = 'white'

                tag_player_1 = f'col{i+1}_player_1'
                tag_player_2 = f'col{i+1}_player_2'

                comparison_table.tag_configure(tag_player_1, foreground=color_player_1)
                comparison_table.tag_configure(tag_player_2, foreground=color_player_2)

                item_id = comparison_table.insert(parent='', index=tk.END, values=[player_1_stats[i+1], player_stats[0][i+1], player_2_stats[i+1]])

                comparison_table.item(item_id, tags=(tag_player_1, tag_player_2))

    def Franchise(self, tab, retired_numbers, hall_of_fame, all_time, achievements):
        # Update the GUI again
        self.root.update_idletasks()

        # Retired Numbers Frame
        retired_numbers_frame = tk.Frame(tab)
        retired_numbers_frame.place(x = 0, y = 0, relwidth = 0.49, relheight = 0.6)
        retired_numbers_frame.columnconfigure((0), weight = 1)
        retired_numbers_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50), weight = 1)

        # Retired Numbers Label
        retired_numbers_label = tk.Label(retired_numbers_frame, text="--RETIRED NUMBERS--", fg = 'lightgray', font=("Helvetica", 15, "bold"))
        retired_numbers_label.grid(row = 0, column = 0, sticky = 'nsw', pady = 5)

        # Retired Numbers Treeview
        retired_numbers_table= ttk.Treeview(retired_numbers_frame, columns = retired_numbers[0], show = 'headings', height = len(retired_numbers))
        retired_numbers_table.config(selectmode="none")
        retired_numbers_table.grid(row = 1, column = 0, rowspan = 50, sticky = 'nsew')

        # Add Column Names to Treeview
        for col in retired_numbers[0]:
            retired_numbers_table.heading(col, text=col)
        
        # Add Column Widths
        retired_numbers_table.column(retired_numbers[0][0], width=10)
        retired_numbers_table.column(retired_numbers[0][1], width=90)
        retired_numbers_table.column(retired_numbers[0][2], width=80)
        retired_numbers_table.column(retired_numbers[0][3], width=100)
        retired_numbers_table.column(retired_numbers[0][4], width=60)

        # Add data to Treeview
        for row in retired_numbers[1:]:
            retired_numbers_table.insert(parent = '', index = tk.END, values = row)

        # Hall of Fame Frame
        hall_of_fame_frame = tk.Frame(tab)
        hall_of_fame_frame.place(relx = 0.51, y = 0, relwidth = 0.49, relheight = 0.6)
        hall_of_fame_frame.columnconfigure((0), weight = 1)
        hall_of_fame_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50), weight = 1)

        # Hall of Fame Label
        hall_of_fame_label = tk.Label(hall_of_fame_frame, text="--HALL OF FAME--", fg = 'lightgray', font=("Helvetica", 15, "bold"))
        hall_of_fame_label.grid(row = 0, column = 0, sticky = 'nsw', pady = 5)

        # Hall of Fame Treeview
        hall_of_fame_table= ttk.Treeview(hall_of_fame_frame, columns = hall_of_fame[0], show = 'headings', height = len(hall_of_fame))
        hall_of_fame_table.config(selectmode="none")
        hall_of_fame_table.grid(row = 1, column = 0, rowspan = 50, sticky = 'nsew')

        # Add Column Names to Treeview
        for col in hall_of_fame[0]:
            hall_of_fame_table.heading(col, text=col)
        
        # Add Column Widths
        hall_of_fame_table.column(hall_of_fame[0][0], width=90)
        hall_of_fame_table.column(hall_of_fame[0][1], width=45)
        hall_of_fame_table.column(hall_of_fame[0][2], width=100)
        hall_of_fame_table.column(hall_of_fame[0][3], width=60)

        # Add data to Treeview
        for row in hall_of_fame[1:]:
            hall_of_fame_table.insert(parent = '', index = tk.END, values = row)

        # All Time Frame
        all_time_frame = tk.Frame(tab, bg="#404040")
        all_time_frame.place(x = 0, rely = 0.6, relwidth = 0.4, relheight = 0.49)
        all_time_frame.columnconfigure((0, 1, 2), weight = 1)
        all_time_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), weight = 1)

        # All Time Label
        for i in range(3):
            temp = tk.Label(all_time_frame, fg = 'lightgray', font=("Helvetica", 15, "bold"))
            temp.grid(row = 0, column = i, sticky = 'nsew')
        all_time_label = tk.Label(all_time_frame, text="--ALL TIME RECORDS--", fg = 'lightgray', font=("Helvetica", 15, "bold"))
        all_time_label.grid(row = 0, column = 0, sticky = 'nsw')

        # All Time
        row_num = 1
        for i in range(len(all_time)):
            stat = tk.Label(all_time_frame, text=all_time[i][0], bg="#404040", fg="white", font=("Helvetica", 15, "bold"))
            stat.grid(row=row_num, column=0, sticky="nsew")
            name = tk.Label(all_time_frame, text=all_time[i][1], bg="#404040", fg="white", font=("Helvetica", 15))
            name.grid(row=row_num, column=1, sticky="nsew")
            num = tk.Label(all_time_frame, text=all_time[i][2], bg="#404040", fg="white", font=("Helvetica", 15))
            num.grid(row=row_num, column=2, sticky="nsew")
            row_num += 1

        # Achievements Frame
        achievements_frame = tk.Frame(tab, bg='black')
        achievements_frame.place(relx = 0.6, rely = 0.6, relwidth = 0.4, relheight = 0.49)
        achievements_frame.columnconfigure((0, 1), weight = 1)
        achievements_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), weight = 1)

        # Achievements Label
        achievements_label = tk.Label(achievements_frame, text="--ACHIEVEMENTS--", fg = 'lightgray', font=("Helvetica", 15, "bold"))
        achievements_label.grid(row = 0, column = 0, sticky = 'nsew')
        dummy_label = tk.Label(achievements_frame, fg = 'lightgray', font=("Helvetica", 15, "bold"))
        dummy_label.grid(row = 0, column = 1, sticky = 'nsew')

        # Achievements
        row_num = 1
        for i in range(3):
            title = tk.Label(achievements_frame, text=achievements[0][i], background="black", fg="white", font=("Helvetica", 15, "bold"))
            title.grid(row = row_num, column = 0, sticky="nsew")
            years_str = ', '.join(achievements[1:][i])
            years = tk.Label(achievements_frame, text=years_str, background="black", fg="white", font=("Helvetica", 15, "bold"), wraplength=400)
            years.grid(row = row_num, column = 1, rowspan=3, sticky="nsew")
            row_num += 3

    def getPlayer(self, player, player_stats):
        for each in player_stats[1:]:
            if player == each[0]:
                return each
        no_games = [player]
        for _ in range(len(player_stats)-1):
            no_games.append(0)
        return no_games

        
    def back_to_teams(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

    def getTeamPage(self, team_name):
        id_dict = {"hawks": 1610612737, "celtics": 1610612738, "cavaliers": 1610612739, "pelicans": 1610612740, "bulls": 1610612741, "mavericks": 1610612742
                   , "nuggets": 1610612743, "warriors": 1610612744, "rockets": 1610612745, "clippers": 1610612746, "lakers": 1610612747, "heat": 1610612748
                   , "bucks": 1610612749, "timberwolves": 1610612750, "nets": 1610612751, "knicks": 1610612752, "magic": 1610612753, "pacers": 1610612754
                   , "76ers": 1610612755, "suns": 1610612756, "blazers": 1610612757, "kings": 1610612758, "spurs": 1610612759, "thunder": 1610612760
                   , "raptors": 1610612761, "jazz": 1610612762, "grizzlies": 1610612763, "wizards": 1610612764, "pistons": 1610612765, "hornets": 1610612766}
        return id_dict.get(team_name)
    
    def getRecord(self, driver, team_page_str):
        driver.get(team_page_str)
        record_name = driver.find_element(By.CLASS_NAME, "TeamHeader_record__wzofp")
        all_stats_2D = driver.find_elements(By.CLASS_NAME, "TeamHeader_rank__lMnzF")
        
        stat_line = ""
        for stat_element in all_stats_2D:
            stat_text_array = stat_element.text.split("\n")
            stat_line += stat_text_array[2] + " " + stat_text_array[0] + " ~ " + stat_text_array[1]
            
            if stat_element != all_stats_2D[-1]:
                stat_line += "  |  "

        return [record_name.text, stat_line]
    
    def getRoster(self, driver, team_page_str):
        driver.get(team_page_str)
        table = driver.find_element(By.TAG_NAME, 'table')

        header = []
        for row in table.find_elements(By.TAG_NAME, 'th'):
            header.append(row.text)
 
        table_data = []
        for row in table.find_elements(By.TAG_NAME, 'tr'):
            row_data = []
            for col in row.find_elements(By.TAG_NAME, 'td'):
                row_data.append(col.text)
            table_data.append(row_data)

        return [header] + table_data[1:]
    
    def getCoachingStaff(self, driver, team_page_str):
        driver.get(team_page_str)
        container = driver.find_element(By.CLASS_NAME, "TeamProfile_sectionCoaches__e66bL")

        header = []
        for each in container.find_elements(By.TAG_NAME, 'h3'):
            header.append(each.text)

        coaching_data = []
        for row in container.find_elements(By.TAG_NAME, 'ul'):
            row_data = []
            for col in row.find_elements(By.TAG_NAME, 'li'):
                row_data.append(col.text)
            coaching_data.append(row_data)

        return [header] + coaching_data
    
    def getTeamUpdates(self, driver, team_page_str):
        driver.get(team_page_str)

        updates = []

        dates = driver.find_elements(By.CLASS_NAME, 'TeamFantasyNews_articleDate__SrBm7')
        headlines = driver.find_elements(By.CLASS_NAME, 'TeamFantasyNews_articleHeadline__02sbs')
        contents = driver.find_elements(By.CLASS_NAME, 'TeamFantasyNews_articleContent__x7vps')

        for date, headline, content in zip(dates, headlines, contents):
            update = {
                'date': date.text,
                'headline': headline.text,
                'content': content.text
            }
            updates.append(update)

        return updates
    def getPlayerStats(self, driver, team_page_str):
        driver.get(team_page_str)
        table = driver.find_elements(By.CLASS_NAME, 'Crom_table__p1iZz')[-1]

        header = []
        for row in table.find_elements(By.TAG_NAME, 'th'):
            header.append(row.text)

        table_data = []
        for row in table.find_elements(By.TAG_NAME, 'tr'):
            row_data = []
            for col in row.find_elements(By.TAG_NAME, 'td'):
                row_data.append(col.text)
            table_data.append(row_data)

        return [header] + table_data[1:]
    
    def getOverallStats(self, driver, team_page_str):
        driver.get(team_page_str)
        tables = driver.find_elements(By.CLASS_NAME, 'Crom_table__p1iZz')[:3]

        header = []
        for row in tables[0].find_elements(By.TAG_NAME, 'th'):
            header.append(row.text)
        header[0] = ""
        all_data = []
        for table in tables:
            for row in table.find_elements(By.TAG_NAME, 'tr')[1:]:
                row_data = []
                
                for col in row.find_elements(By.TAG_NAME, 'td'):
                    row_data.append(col.text)
                
                all_data.append(row_data)
        
        return [header] + all_data
    
    def getRetiredNumbers(self, driver, team_page_str):
        driver.get(team_page_str)
        table = driver.find_element(By.CLASS_NAME, 'TeamRetired_content__nb7Qt')

        header = []
        for row in table.find_elements(By.TAG_NAME, 'th'):
            header.append(row.text)
        table_data = []
        for row in table.find_elements(By.TAG_NAME, 'tr'):
            row_data = []
            for col in row.find_elements(By.TAG_NAME, 'td'):
                row_data.append(col.text)
            table_data.append(row_data)

        return [header] + table_data[1:]
    
    def getHallOfFame(self, driver, team_page_str):
        driver.get(team_page_str)
        table = driver.find_element(By.CLASS_NAME, 'TeamHallOfFame_content__IZSl2')

        header = []
        for row in table.find_elements(By.TAG_NAME, 'th'):
            header.append(row.text)
        table_data = []
        for row in table.find_elements(By.TAG_NAME, 'tr'):
            row_data = []
            for col in row.find_elements(By.TAG_NAME, 'td'):
                row_data.append(col.text)
            table_data.append(row_data)

        return [header] + table_data[1:]
    
    def getAllTime(self, driver, team_page_str):
        driver.get(team_page_str)
        table = driver.find_element(By.CLASS_NAME, 'TeamRecords_table__0iapO')

        table_data = []
        for row in table.find_elements(By.TAG_NAME, 'tr'):
            row_data = []
            for col in row.find_elements(By.TAG_NAME, 'td'):
                row_data.append(col.text)
            table_data.append(row_data)

        return table_data
    
    def getAchievements(self, driver, team_page_str):
        driver.get(team_page_str)
        rows = driver.find_elements(By.CLASS_NAME, 'TeamAwards_group__XU0o9')

        header = []
        table_data = []
        for row in rows:
            row_data= []
            header.append(row.find_element(By.TAG_NAME, 'h3').text)
            for col in row.find_elements(By.TAG_NAME, 'li'):
                row_data.append(col.text)
            table_data.append(row_data)

        return [header] + table_data

if __name__ == "__main__":
    root = tk.Tk()
    nba_stats = NBAStats(root)
    root.wm_attributes('-fullscreen', True)
    root.mainloop()