import src.crud as crud


class CompanyManager:
    def __init__(self, company_database):
        self.__db = company_database

    def get_root_company_unit(self):
        return crud.get_root_node(self.__db)
