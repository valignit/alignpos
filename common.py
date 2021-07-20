from alignpos_db import DbConn, DbTable, DbQuery
from common_ui import UiItemLookup


class ItemLookup():
    db_conn = None
    ui_popup = None
       
    db_item_table = None
    sel_item_code = None
    
    def __init__(item_lookup, db_conn, ui_popup):
        item_lookup.db_conn = db_conn
        item_lookup.ui_popup = ui_popup
        
        item_lookup.ui_item_lookup = UiItemLookup(ui_popup)
        item_lookup.db_item_table = DbTable(db_conn, 'tabItem')
        
    
    def populate_item_list(item_lookup, filter):
        item_lookup.ui_item_lookup.item_list = []
        db_item_cursor = item_lookup.db_item_table.list(filter)
        for db_item_row in db_item_cursor:
            item_lookup.ui_item_lookup.item_code = db_item_row.item_code
            item_lookup.ui_item_lookup.item_name = db_item_row.item_name
            item_lookup.ui_item_lookup.add_item_line()
