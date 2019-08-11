import MySQLdb

class PibbleDatabase:
    def __init__(self, brain, paramMysql=None):
        self.brain = brain
        
        if paramMysql:
            self.params = paramMysql
        else:
            self.params = {
                'db_host'   : 'localhost',
                'db_user'   : 'root',
                'db_password' : 'test',
                'db_name'     : 'pibble_catalog'
            }

        self.conn_error = False
            
        try:
            self.conn = MySQLdb.connect(host=self.params["db_host"], user=self.params["db_user"], passwd=self.params["db_password"], db=self.params["db_name"])
            self.cursor = self.conn.cursor()
        except(Exception) as err:
            self.conn_error = True
            print(err, flush=True)

    """def getNames(self):
        if not self.conn_error:
            try:
                self.cursor.execute("SELECT * FROM objects")
                names = self.cursor.fetchall()
                return names
            except(Exception) as err:
                print(err, flush=True)
                return None
        else:
            return None"""

    def getTypes(self):
        if not self.conn_error:
            try:
                self.cursor.execute("SELECT DISTINCT type FROM objects")
                types = self.cursor.fetchall()
                return types
            except(Exception) as err:
                print(err, flush=True)
                return None
        else:
            return None
        
    def getConstellations(self, table):
        if not self.conn_error:
            try:
                self.cursor.execute("SELECT DISTINCT constellation FROM {}".format(table))
                constellations = self.cursor.fetchall()
                return constellations
            except(Exception) as err:
                print(err, flush=True)
                return None
        else:
            return None

    def getAllFromTable(self, table=None, args=None):
        if not self.conn_error:
            try:
                visibility = args.pop("visible")
                liste = []
                
                self.cursor.execute("SELECT * FROM {}".format(table))
                sql_request = "SELECT * FROM {}".format(table)
                first = True
                for key in args:
                    if not args[key] == None:
                        if first == False:
                            sql_request += " AND "
                        else:
                            sql_request += " WHERE "

                        if type(args[key]) == str:
                            sql_request +=  "{} = '{}'".format(key, args[key])
                        else:
                            sql_request +=  "{} = {}".format(key, args[key])
                            
                        first = False

                self.cursor.execute(sql_request)
                        
                row = self.cursor.fetchall()
                collNames = self.getAllCollumns(table)
                index = 0
                for obj in row:
                    liste.append({})
                    for x in range(0,len(collNames)):
                        liste[index].update({collNames[x] : obj[x]})
                    index += 1
                return liste
            except(Exception) as err:
                print(err, flush=True)
                return None
        else:
            return None

    def getAllCollumns(self, table):
        if not self.conn_error:
            try:
                collNames = []
                self.cursor.execute("SHOW COLUMNS FROM {}".format(table))
                coll = self.cursor.fetchall()
                for collumn in coll:
                    collNames.append(collumn[0])
                return collNames
            except(Exception) as err:
                print(err, flush=True)
                return None
        else:
            return None

    def getObjectByName(self, table=None, name=None):
        if not self.conn_error:
            try:
                objs_dict = {}
                self.cursor.execute("SELECT * FROM objects WHERE NAME = '{}'".format(name))
                row = self.cursor.fetchall()
                collNames = self.getAllCollumns(table)
                for obj in row:
                    for x in range(0,len(collNames)):
                        objs_dict.update({collNames[x] : obj[x]})
                return objs_dict
            except(Exception) as err:
                print(err, flush=True)
                return None
        else:
            return None


    def getAlignInit(self):
        if not self.conn_error:
            try:
                objs_dict = {}
                self.cursor.execute("SELECT * FROM stars WHERE PROPER NOT NULL")
                row = self.cursor.fetchall()
            
            except(Exception) as err:
                print(err, flush=True)
                return None
        else:
            return None
