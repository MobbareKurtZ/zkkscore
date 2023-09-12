import gspread
from oauth2client.service_account import ServiceAccountCredentials

class DataHandler:
    def __init__(self) -> None:
        self.setup_connection();

    def setup_connection(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name('cred.json')
        self.client = gspread.authorize(credentials)
        self.db = self.client.open("database").sheet1

    def update_user(self, uid, data):
        if self.exists(uid):
            data = self.decode_data(uid, data)
            user = self.get_user(uid);
            for i, v in enumerate(data):
                if v == None:
                    data[i] = user[i]
            row = self.get_cell(uid).row
            print(row)
            self.db.update(values=[data], range_name=f'A{row}:D{row}')
        return None

    def get_cell(self, query):
        return self.db.find(query, in_column=1)

    def get_user(self, uid):
        user = None
        if self.exists(uid):
            user_cell = self.get_cell(uid)
            user = self.db.row_values(user_cell.row)
        return self.encode_data(user)

    def add_user(self, uid, data):
        data = self.decode_data(uid, data)
        self.db.append_row(data)
        return None

    def exists(self, uid):
        user_cell = self.db.find(uid)
        return user_cell is not None

    def decode_data(self, uid, data):
        list = [uid, data.get("score",None), data.get("date",None), data.get("paid",None)]
        return list

    def encode_data(self, data):
        return {"uid": data[0], "score": data[1], "date": data[2], "paid": data[3]}

d = DataHandler()

data = [12, "nu", True]

d.exists("testuid")
d.add_user("ralf", {'score': 14, 'date': 'sdsds', 'paid': False})
