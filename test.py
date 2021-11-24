import pickledb
db = pickledb.load('data/alignpos_settings.db', False)
db.set('key', 'value')
db.get('key')
db.dump()
