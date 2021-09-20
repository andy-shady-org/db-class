class DeviceTable(object):
    def __init__(self, record_id=None):
        self.db_id = record_id
        self.name = None
        self.is_enabled = None
        self.mgmt_address = None
        self.username = None
        self.password = None
        if self.db_id:
            self.load_by_id()

    def get_id(self, default=None):
        return self.db_id if self.db_id else default

    @staticmethod
    def load(data):
        if data is None or (isinstance(data, basestring) and len(data) == 0) or (isinstance(data, int) and data <= 0):
            s = DeviceTable()
        elif isinstance(data, int):
            s = DeviceTable(record_id=data)
        elif isinstance(data, dict):
            s = DeviceTable()
            s.from_json(data)
        elif isinstance(data, basestring):
            s = DeviceTable.load_by_name(data)
        else:
            raise DbError('Invalid data type for device load: %s' % type(data))
        return s

    def load_by_id(self, db_rec=None, db_id=None):
        if db_rec is None:
            if db_id is None:
                rec_id = self.get_id()
            else:
                rec_id = db_id
            if not rec_id:
                raise DbError('Record ID not associated with class')
            # there are many ways to make a query and many different frameworks
            
            # web2py
            db_rec = db(db.devices.id == rec_id).select().first()
            
            # django
            # db_rec = Devices.objects.filter(pk=rec_id).first()
        if not db_rec:
            raise DbError('Database record and record id are missing in load request or invalid record id')
        self.db_id = db_rec.id
        self.name = db_rec.name
        self.is_enabled = True if db_rec.is_enabled else False
        self.mgmt_address = db_rec.mgmt_address
        self.username = db_rec.username
        self.password = db_rec.password

    @staticmethod
    def load_by_name(name):
        # many frameworks
        # web2py
        rec = db(db.devices.name == name).select().first()
        
        # django
        # rec = Devices.objects.filter(name=name).first()
        if not rec:
            return None
        s = DeviceTable()
        s.load_by_id(db_rec=rec)
        return s

    def save(self, db_rec=None, db_id=None):
        rec_id = self.get_id(default=db_id)
        if not rec_id and not db_rec:
            query = (db.devices.mgmt_address == self.mgmt_address)
            if db(query).count() > 0:
                raise DuplicateNameError('An device with MGMT Address {0} already exists'.format(self.mgmt_address))
            if db(db.devices.name == self.name).count() > 0:
                raise DuplicateNameError('An device with name {0} already exists'.format(self.name))
            
            # web2py implementation
            rec_id = db.devices.insert(name=self.name, is_enabled=1 if self.is_enabled else 0,
                                                   mgmt_address=self.mgmt_address,
                                                   username=self.username, password=self.password)
            db.commit()
            self.db_id = rec_id
            return True
        else:
            if not db_rec:
                db_rec = db(db.devices.id == rec_id).select().first()
            if db_rec:
                db_rec.update_record(name=self.name, is_enabled=self.is_enabled, mgmt_address=self.mgmt_address,
                                     username=self.username, password=self.password)
                db.commit()
                return True
        return False

    def delete(self, db_rec=None, db_id=None):
        rec_id = self.get_id(default=db_id)
        if not rec_id and not db_rec:
            if not db(db.devices.name == self.name).count() > 0:
                raise DataValidationError(self.__class__.__name__, 'Device with name {0} does not exist'.format(self.name))
            db(db.devices.name == self.name).delete()
            db.commit()
            self.db_id = None
            return True
        else:
            if not db_rec:
                db_rec = db(db.devices.id == rec_id).select().first()
            if db_rec:
                db(db.devices.id == rec_id).delete()
                db.commit()
                self.db_id = None
                return True
        return False

    def from_json(self, json_data):
        if not self.get_id():
            if 'id' in json_data and json_data['id']:
                try:
                    self.db_id = int(json_data.get('id'))
                    if self.db_id <= 0 or db(db.devices.id == self.db_id).count() == 0:
                        self.db_id = None
                except (TypeError, ValueError):
                    self.db_id = None
                if self.db_id is None:
                    raise DataValidationError(self.__class__.__name__,, 'Database ID of device entry is invalid or does not exist')
            if 'name' in json_data and json_data.get('name', '').strip():
                self.name = json_data.get('name', '').strip()
            else:
                if not self.get_id():
                    raise DataValidationError(self.__class__.__name__,, 'Device "name" attribute missing in data structure')
            if 'username' in json_data and json_data.get('username', '').strip():
                self.username = json_data.get('username', '').strip()
            else:
                if not self.get_id():
                    raise DataValidationError(self.__class__.__name__, 'Device "username" attribute missing in data structure')
            if 'password' in json_data and json_data.get('password', '').strip():
                self.password = json_data.get('password', '').strip()
            else:
                if not self.get_id():
                    raise DataValidationError(self.__class__.__name__,, 'Device "password" attribute missing in data structure')
            if 'is_enabled' in json_data and isinstance(json_data.get('is_enabled'), bool):
                self.is_enabled = json_data.get('is_enabled')
            else:
                if not self.get_id():
                    self.is_enabled = True
            if 'mgmt_address' in json_data and json_data.get('mgmt_address', '').strip():
                self.mgmt_address = json_data.get('mgmt_address', '').strip()
                if not validate_ipaddress(self.mgmt_address):
                    raise DataValidationError(self.__class__.__name__,, 'Device "mgmt_address" attribute is not a valid IP Address')
            else:
                if not self.get_id():
                    raise DataValidationError(self.__class__.__name__, 'Device "mgmt_address" attribute missing in data structure')


    def to_json(self):
        return dict(id=self.get_id(), name=self.name, is_enabled=self.is_enabled, mgmt_address=self.mgmt_address,
                    username=self.username, password=self.password)
