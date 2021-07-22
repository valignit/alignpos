from alignpos_db import DbConn, DbTable, DbQuery
from main_menu_ui import UiDetailPane, UiFooterPane, UiSummaryPane


class MainMenu():
    db_conn = None
    ui_window = None
    
    ui_detail_pane = None
    ui_footer_pane = None
    ui_summary_pane = None
    
    
    def __init__(main_menu, db_conn, ui_window):
        main_menu.db_conn = db_conn
        main_menu.ui_window = ui_window
        
        main_menu.ui_detail_pane = UiDetailPane(ui_window)
        main_menu.ui_footer_pane = UiFooterPane(ui_window)
        main_menu.ui_summary_pane = UiSummaryPane(ui_window)
        
    
    def initialize_ui_detail_pane(main_menu):
        None


    def initialize_ui_footer_pane(main_menu):
        main_menu.ui_footer_pane.user_id = 'XXX'
        main_menu.ui_footer_pane.terminal_id = '101'
        main_menu.ui_footer_pane.current_date = '2021/06/13'


    def initialize_ui_summary_pane(main_menu):
        main_menu.ui_summary_pane.welcome_text = 'Welcome to AlignPos, a Point Of Sale application.'


    def initialize_ui(main_menu):
        main_menu.initialize_ui_detail_pane()
        main_menu.initialize_ui_footer_pane()
        main_menu.initialize_ui_summary_pane()
  